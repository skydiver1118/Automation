from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
sys.path.insert(0, str(ROOT / "scripts"))

from soxl_tqqq_cash_signal_scanner import (  # noqa: E402
    StrategyConfig as CashScannerConfig,
    build_base_rotation,
    cash_filtered_targets,
)
from src.strategy_lab.exit_profiles import (  # noqa: E402
    ExitProfile,
    ScaleOutRule,
    TrailingRule,
    all_exit_profiles,
    calculate_atr,
    top_loss_taking_profiles,
    top_profit_taking_profiles,
)


DATA_START = "2010-03-11"
DATA_END = "2026-05-25"
IS_START = pd.Timestamp("2010-03-11")
IS_END = pd.Timestamp("2019-12-31")
OOS_START = pd.Timestamp("2020-01-01")
SYMBOLS = ["SOXL", "TQQQ"]
CONTEXT_SYMBOLS = ["SOXL", "TQQQ", "QQQ"]


@dataclass(frozen=True)
class ManagedPosition:
    symbol: str
    entry_price: float
    initial_risk: float
    active_stop: float
    remaining_fraction: float
    highest_close: float
    bars_held: int
    scaleouts_done: frozenset[float]


def fetch_adjusted_ohlc() -> dict[str, pd.DataFrame]:
    raw = yf.download(
        CONTEXT_SYMBOLS,
        start=DATA_START,
        end=DATA_END,
        interval="1d",
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    if raw.empty:
        raise RuntimeError("No price data returned by yfinance.")
    raw.index = pd.to_datetime(raw.index).tz_localize(None)
    out: dict[str, pd.DataFrame] = {}
    for symbol in CONTEXT_SYMBOLS:
        if isinstance(raw.columns, pd.MultiIndex):
            out[symbol] = raw.loc[:, (["Open", "High", "Low", "Close"], symbol)].copy()
            out[symbol].columns = ["Open", "High", "Low", "Close"]
        else:
            raise RuntimeError("Expected multi-symbol yfinance result.")
    common = out["SOXL"].dropna().index
    for symbol in CONTEXT_SYMBOLS[1:]:
        common = common.intersection(out[symbol].dropna().index)
    return {symbol: frame.loc[common].astype(float) for symbol, frame in out.items()}


def build_close(ohlc: dict[str, pd.DataFrame]) -> pd.DataFrame:
    close = pd.DataFrame({symbol: frame["Close"] for symbol, frame in ohlc.items()})
    return close[CONTEXT_SYMBOLS].dropna()


def scanner_targets(close: pd.DataFrame) -> pd.Series:
    config = CashScannerConfig()
    base = build_base_rotation(close, config)
    targets = cash_filtered_targets(close, base, config)
    return targets.reindex(close.index).ffill().fillna("CASH")


def max_drawdown(equity: pd.Series) -> float:
    return float((equity / equity.cummax() - 1).min() * 100)


def sharpe_ratio(equity: pd.Series) -> float:
    returns = equity.pct_change().fillna(0)
    std = float(returns.std(ddof=0))
    if std == 0 or not np.isfinite(std):
        return 0.0
    return float(returns.mean() / std * math.sqrt(252))


def cagr_pct(equity: pd.Series) -> float:
    years = max((equity.index[-1] - equity.index[0]).days / 365.25, 1 / 365.25)
    return (float(equity.iloc[-1] / equity.iloc[0]) ** (1 / years) - 1) * 100


def summarize_curve(name: str, equity: pd.Series, *, period_name: str, profit_key: str = "", loss_key: str = "") -> dict[str, object]:
    normalized = equity / float(equity.iloc[0])
    returns = normalized.pct_change().fillna(0)
    return {
        "period": period_name,
        "strategy": name,
        "profit_profile": profit_key,
        "loss_profile": loss_key,
        "start": normalized.index[0].date().isoformat(),
        "end": normalized.index[-1].date().isoformat(),
        "cumulative_return_pct": round((float(normalized.iloc[-1]) - 1) * 100, 2),
        "cagr_pct": round(cagr_pct(normalized), 2),
        "max_drawdown_pct": round(max_drawdown(normalized), 2),
        "sharpe": round(sharpe_ratio(normalized), 3),
        "daily_vol_pct": round(float(returns.std(ddof=0) * math.sqrt(252) * 100), 2),
    }


def run_baseline(close: pd.DataFrame, targets: pd.Series) -> pd.Series:
    equity = np.ones(len(close), dtype=float)
    held = str(targets.iloc[0])
    for i in range(1, len(close)):
        if held in SYMBOLS:
            equity[i] = equity[i - 1] * (float(close[held].iloc[i]) / float(close[held].iloc[i - 1]))
        else:
            equity[i] = equity[i - 1]
        held = str(targets.iloc[i])
    return pd.Series(equity, index=close.index, name="baseline")


def run_with_exit_profiles(
    ohlc: dict[str, pd.DataFrame],
    targets: pd.Series,
    profit_profile: ExitProfile,
    loss_profile: ExitProfile,
) -> tuple[pd.Series, pd.DataFrame]:
    close = build_close(ohlc)
    atr = {symbol: calculate_atr(ohlc[symbol], period=14).reindex(close.index) for symbol in SYMBOLS}
    ema20 = {symbol: close[symbol].ewm(span=20, adjust=False).mean() for symbol in SYMBOLS}
    equity = np.ones(len(close), dtype=float)
    position: ManagedPosition | None = None
    events: list[dict[str, object]] = []

    for i in range(1, len(close)):
        ts = close.index[i]
        prev_ts = close.index[i - 1]

        if position is not None:
            day_return = float(close.loc[ts, position.symbol] / close.loc[prev_ts, position.symbol] - 1)
            equity[i] = equity[i - 1] * (1 + position.remaining_fraction * day_return)
        else:
            equity[i] = equity[i - 1]

        desired = str(targets.loc[ts])

        if position is not None:
            low = float(ohlc[position.symbol].loc[ts, "Low"])
            close_price = float(close.loc[ts, position.symbol])
            if low <= position.active_stop:
                pnl = position.remaining_fraction * (position.active_stop / float(close.loc[prev_ts, position.symbol]) - 1)
                equity[i] = equity[i - 1] * (1 + pnl)
                events.append(_event(ts, "stop_exit", position, position.remaining_fraction, position.active_stop, "active stop breached"))
                position = None
            elif _loss_exit_trigger(loss_profile, position, close_price, float(ema20[position.symbol].loc[ts])):
                events.append(_event(ts, "loss_exit", position, position.remaining_fraction, close_price, loss_profile.name))
                position = None
            elif _time_failure_trigger(loss_profile, position, close_price):
                events.append(_event(ts, "time_exit", position, position.remaining_fraction, close_price, loss_profile.name))
                position = None

        if position is not None and (desired == "CASH" or desired != position.symbol):
            close_price = float(close.loc[ts, position.symbol])
            events.append(_event(ts, "scanner_exit", position, position.remaining_fraction, close_price, f"target changed to {desired}"))
            position = None

        if position is not None:
            position, scale_events = _apply_profit_profile(
                ts,
                position,
                float(close.loc[ts, position.symbol]),
                float(ohlc[position.symbol].loc[ts, "Low"]),
                float(atr[position.symbol].loc[ts]),
                profit_profile,
            )
            events.extend(scale_events)
            if position.remaining_fraction <= 0:
                position = None

        if position is None and desired in SYMBOLS:
            entry = float(close.loc[ts, desired])
            risk = _initial_risk(entry, float(atr[desired].loc[ts]), loss_profile)
            position = ManagedPosition(
                symbol=desired,
                entry_price=entry,
                initial_risk=risk,
                active_stop=entry - risk,
                remaining_fraction=1.0,
                highest_close=entry,
                bars_held=0,
                scaleouts_done=frozenset(),
            )
            events.append(_event(ts, "entry", position, 1.0, entry, f"scanner target {desired}"))
        elif position is not None:
            position = ManagedPosition(
                symbol=position.symbol,
                entry_price=position.entry_price,
                initial_risk=position.initial_risk,
                active_stop=position.active_stop,
                remaining_fraction=position.remaining_fraction,
                highest_close=position.highest_close,
                bars_held=position.bars_held + 1,
                scaleouts_done=position.scaleouts_done,
            )

    return pd.Series(equity, index=close.index, name=f"{profit_profile.key}+{loss_profile.key}"), pd.DataFrame(events)


def _initial_risk(entry: float, atr: float, loss_profile: ExitProfile) -> float:
    if loss_profile.key == "trend_structure_break":
        return max(entry * 0.15, atr * 3.0)
    return max(entry * 0.10, atr * 2.0)


def _loss_exit_trigger(loss_profile: ExitProfile, position: ManagedPosition, close_price: float, ema20: float) -> bool:
    if loss_profile.key != "trend_structure_break":
        return False
    return position.bars_held >= 2 and close_price < ema20 and close_price < position.entry_price


def _time_failure_trigger(loss_profile: ExitProfile, position: ManagedPosition, close_price: float) -> bool:
    if loss_profile.key != "time_and_volatility_failure":
        return False
    current_r = (close_price - position.entry_price) / position.initial_risk
    return position.bars_held >= 20 and current_r < 0.5


def _apply_profit_profile(
    ts: pd.Timestamp,
    position: ManagedPosition,
    close_price: float,
    low: float,
    atr: float,
    profit_profile: ExitProfile,
) -> tuple[ManagedPosition, list[dict[str, object]]]:
    events: list[dict[str, object]] = []
    remaining = position.remaining_fraction
    active_stop = position.active_stop
    done = set(position.scaleouts_done)
    current_r = (close_price - position.entry_price) / position.initial_risk
    for rule in profit_profile.scale_outs:
        if rule.trigger_r in done or current_r < rule.trigger_r:
            continue
        fraction = min(rule.fraction, remaining)
        remaining -= fraction
        done.add(rule.trigger_r)
        events.append(_event(ts, "scale_out", position, fraction, close_price, rule.label or f"+{rule.trigger_r:g}R"))
        if rule.stop_r is not None:
            active_stop = max(active_stop, position.entry_price + rule.stop_r * position.initial_risk)

    highest_close = max(position.highest_close, close_price)
    active_stop = max(active_stop, _profile_trailing_stop(profit_profile.trailing_rule, position, highest_close, low, atr, current_r))
    updated = ManagedPosition(
        symbol=position.symbol,
        entry_price=position.entry_price,
        initial_risk=position.initial_risk,
        active_stop=active_stop,
        remaining_fraction=remaining,
        highest_close=highest_close,
        bars_held=position.bars_held,
        scaleouts_done=frozenset(done),
    )
    return updated, events


def _profile_trailing_stop(
    rule: TrailingRule | None,
    position: ManagedPosition,
    highest_close: float,
    low: float,
    atr: float,
    current_r: float,
) -> float:
    if rule is None or current_r < rule.activation_r:
        return float("-inf")
    if rule.method == "chandelier" and rule.atr_multiple is not None:
        return highest_close - rule.atr_multiple * atr
    if rule.method == "structure":
        return low - atr
    return float("-inf")


def _event(ts: pd.Timestamp, action: str, position: ManagedPosition, fraction: float, price: float, reason: str) -> dict[str, object]:
    return {
        "date": ts.date().isoformat(),
        "action": action,
        "symbol": position.symbol,
        "fraction": round(float(fraction), 6),
        "price": round(float(price), 6),
        "remaining_before": round(float(position.remaining_fraction), 6),
        "r_multiple": round((float(price) - position.entry_price) / position.initial_risk, 4),
        "reason": reason,
    }


def slice_curve(equity: pd.Series, start: pd.Timestamp, end: pd.Timestamp | None = None) -> pd.Series:
    mask = equity.index >= start
    if end is not None:
        mask &= equity.index <= end
    out = equity.loc[mask]
    return out / float(out.iloc[0])


def markdown_table(df: pd.DataFrame) -> str:
    headers = [str(col) for col in df.columns]
    rows = [[str(value).replace("|", "\\|") for value in row] for row in df.to_numpy().tolist()]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def main() -> None:
    REPORTS.mkdir(exist_ok=True)
    ohlc = fetch_adjusted_ohlc()
    close = build_close(ohlc)
    targets = scanner_targets(close)
    baseline = run_baseline(close, targets)

    profit_profiles = top_profit_taking_profiles()
    loss_profiles = top_loss_taking_profiles()
    curves: dict[str, pd.Series] = {"baseline": baseline}
    event_logs: dict[str, pd.DataFrame] = {}
    rows: list[dict[str, object]] = []

    for profit in profit_profiles:
        for loss in loss_profiles:
            curve, events = run_with_exit_profiles(ohlc, targets, profit, loss)
            key = f"{profit.key}__{loss.key}"
            curves[key] = curve
            event_logs[key] = events
            rows.append(
                {
                    **summarize_curve(
                        "with_exit_profiles",
                        slice_curve(curve, IS_START, IS_END),
                        period_name="IS",
                        profit_key=profit.key,
                        loss_key=loss.key,
                    ),
                    "event_count": len(events[events["date"].between(IS_START.date().isoformat(), IS_END.date().isoformat())]) if not events.empty else 0,
                }
            )

    is_grid = pd.DataFrame(rows).sort_values(["sharpe", "max_drawdown_pct", "cumulative_return_pct"], ascending=[False, False, False]).reset_index(drop=True)
    is_grid.insert(0, "is_rank", is_grid.index + 1)
    selected = is_grid.head(3).copy()
    selected_keys = [
        f"{row.profit_profile}__{row.loss_profile}"
        for row in selected.itertuples(index=False)
    ]

    comparison_rows = [
        summarize_curve("baseline_no_exit_submodule", slice_curve(baseline, IS_START, IS_END), period_name="IS"),
        summarize_curve("baseline_no_exit_submodule", slice_curve(baseline, OOS_START), period_name="OOS"),
    ]
    for rank, row in enumerate(selected.itertuples(index=False), start=1):
        key = f"{row.profit_profile}__{row.loss_profile}"
        comparison_rows.append(
            summarize_curve(
                f"is_rank_{rank}_with_exit_submodule",
                slice_curve(curves[key], IS_START, IS_END),
                period_name="IS",
                profit_key=str(row.profit_profile),
                loss_key=str(row.loss_profile),
            )
        )
        comparison_rows.append(
            summarize_curve(
                f"is_rank_{rank}_with_exit_submodule",
                slice_curve(curves[key], OOS_START),
                period_name="OOS",
                profit_key=str(row.profit_profile),
                loss_key=str(row.loss_profile),
            )
        )
    comparison = pd.DataFrame(comparison_rows)

    curve_frame = pd.DataFrame({"date": close.index, "baseline": baseline.values})
    for rank, key in enumerate(selected_keys, start=1):
        curve_frame[f"is_rank_{rank}_with_exit_profiles"] = curves[key].values
    for key, curve in curves.items():
        if key != "baseline":
            curve_frame[key] = curve.values

    is_grid_path = REPORTS / "soxl_tqqq_cash_exit_profile_is_grid.csv"
    comparison_path = REPORTS / "soxl_tqqq_cash_exit_profile_is_oos_comparison.csv"
    curves_path = REPORTS / "soxl_tqqq_cash_exit_profile_curves.csv"
    events_path = REPORTS / "soxl_tqqq_cash_exit_profile_top3_events.csv"
    report_path = REPORTS / "soxl_tqqq_cash_exit_profile_is_oos.md"
    is_grid.to_csv(is_grid_path, index=False)
    comparison.to_csv(comparison_path, index=False)
    curve_frame.to_csv(curves_path, index=False)
    top3_events = []
    for rank, key in enumerate(selected_keys, start=1):
        events = event_logs[key].copy()
        events.insert(0, "is_rank", rank)
        events.insert(1, "profile_pair", key)
        top3_events.append(events)
    pd.concat(top3_events, ignore_index=True).to_csv(events_path, index=False)

    source_profiles = {profile.key: profile for profile in all_exit_profiles()}
    oos_base = comparison[(comparison["period"] == "OOS") & (comparison["strategy"] == "baseline_no_exit_submodule")].iloc[0]
    oos_top3 = comparison[(comparison["period"] == "OOS") & (comparison["strategy"] != "baseline_no_exit_submodule")].copy()
    best_oos = oos_top3.sort_values(["sharpe", "max_drawdown_pct", "cumulative_return_pct"], ascending=[False, False, False]).iloc[0]
    report = [
        "# SOXL/TQQQ Rotation With Cash Exit-Profile IS/OOS Test",
        "",
        f"Scanner: `scripts/soxl_tqqq_cash_signal_scanner.py` using the existing daily scanner config.",
        f"IS: {IS_START.date().isoformat()} to {IS_END.date().isoformat()}. OOS: {OOS_START.date().isoformat()} to {close.index[-1].date().isoformat()}.",
        "",
        "Execution model: scanner target changes are applied after the signal close, matching the existing local scanner comparison. The exit sub-module adds partial scale-outs, R-based stops, and optional loss exits while unallocated capital stays in cash.",
        "",
        "## Selected IS Sub-Models",
        "",
        "Top 3 profile pairs selected by IS Sharpe, then lower drawdown, then higher cumulative return:",
        "",
        markdown_table(
            selected[["is_rank", "profit_profile", "loss_profile", "cumulative_return_pct", "cagr_pct", "max_drawdown_pct", "sharpe"]]
        ),
        "",
        "## IS/OOS Comparison",
        "",
        markdown_table(comparison),
        "",
        "## Top IS Exit-Profile Grid",
        "",
        markdown_table(is_grid.head(9)[["is_rank", "profit_profile", "loss_profile", "cumulative_return_pct", "cagr_pct", "max_drawdown_pct", "sharpe", "event_count"]]),
        "",
        "## OOS Takeaway",
        "",
        f"Baseline OOS return was {oos_base['cumulative_return_pct']}% with {oos_base['max_drawdown_pct']}% max drawdown and Sharpe {oos_base['sharpe']}.",
        f"Best top-3 exit sub-module by OOS Sharpe was `{best_oos['strategy']}` using `{best_oos['profit_profile']}` + `{best_oos['loss_profile']}`: return {best_oos['cumulative_return_pct']}%, max drawdown {best_oos['max_drawdown_pct']}%, Sharpe {best_oos['sharpe']}.",
        "",
        "## Files",
        "",
        f"- IS grid: `{is_grid_path}`",
        f"- IS/OOS comparison: `{comparison_path}`",
        f"- Daily curves: `{curves_path}`",
        f"- Selected sub-module events: `{events_path}`",
    ]
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(comparison.to_string(index=False))
    print("\nselected_top3=")
    print(selected[["is_rank", "profit_profile", "loss_profile", "sharpe", "max_drawdown_pct", "cumulative_return_pct"]].to_string(index=False))
    print(f"wrote {report_path}")


if __name__ == "__main__":
    main()
