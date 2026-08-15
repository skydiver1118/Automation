from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path
import math
import sys

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
sys.path.insert(0, str(ROOT / "scripts"))

from soxl_vix_threshold_is_oos import (  # noqa: E402
    SPLIT_DATE,
    fetch_inputs,
    max_drawdown,
    sharpe_ratio,
)


OUTPUT_STEM = "soxl_vix_drawdown_variant_search"


@dataclass(frozen=True)
class Variant:
    name: str
    exit_vix_below: float
    trailing_stop_pct: float | None
    stop_loss_pct: float | None
    trend_exit_sma: int | None
    max_hold_days: int | None
    cooldown_days: int


def cagr_pct(equity: pd.Series) -> float:
    years = max((equity.index[-1] - equity.index[0]).days, 1) / 365.25
    return float(((equity.iloc[-1] / equity.iloc[0]) ** (1.0 / years) - 1.0) * 100)


def simulate_variant(frame: pd.DataFrame, variant: Variant) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = frame.copy()
    if variant.trend_exit_sma is not None:
        frame[f"SOXL_sma_{variant.trend_exit_sma}"] = frame["SOXL_close"].rolling(variant.trend_exit_sma).mean()

    dates = frame.index
    opens = frame["SOXL_open"].to_numpy(dtype=float)
    closes = frame["SOXL_close"].to_numpy(dtype=float)
    vix = frame["VIX_close"].to_numpy(dtype=float)
    trend_sma = (
        frame[f"SOXL_sma_{variant.trend_exit_sma}"].to_numpy(dtype=float)
        if variant.trend_exit_sma is not None
        else None
    )

    capital = 1.0
    in_position = False
    pending: str | None = None
    pending_reason = ""
    entry_date: pd.Timestamp | None = None
    entry_price: float | None = None
    entry_close: float | None = None
    high_close: float | None = None
    cooldown_remaining = 0

    daily_rows: list[dict[str, object]] = []
    trades: list[dict[str, object]] = []

    for i, date in enumerate(dates):
        action = "HOLD"
        action_reason = ""
        execution_price = np.nan

        if i == 0:
            equity = capital
        else:
            previous_close = closes[i - 1]
            open_equity = capital * (opens[i] / previous_close) if in_position else capital

            if pending == "BUY" and not in_position:
                in_position = True
                entry_date = date
                entry_price = float(opens[i])
                entry_close = float(closes[i])
                high_close = float(closes[i])
                execution_price = float(opens[i])
                action = "BUY"
                action_reason = pending_reason
                equity = open_equity * (closes[i] / opens[i])
            elif pending == "SELL" and in_position:
                exit_price = float(opens[i])
                trade_return = exit_price / float(entry_price) - 1.0
                trades.append(
                    {
                        "entry_date": entry_date.date().isoformat(),
                        "exit_date": date.date().isoformat(),
                        "symbol": "SOXL",
                        "exit_to": "CASH",
                        "entry_price": round(float(entry_price), 4),
                        "exit_price": round(exit_price, 4),
                        "return_pct": round(trade_return * 100, 2),
                        "outcome": "win" if trade_return > 0 else "loss",
                        "exit_reason": pending_reason,
                        "holding_calendar_days": int((date - entry_date).days),
                        "holding_trading_days": int(len(dates[(dates >= entry_date) & (dates <= date)]) - 1),
                    }
                )
                capital = open_equity
                in_position = False
                entry_date = None
                entry_price = None
                entry_close = None
                high_close = None
                cooldown_remaining = variant.cooldown_days
                execution_price = exit_price
                action = "SELL"
                action_reason = pending_reason
                equity = capital
            else:
                equity = capital * (closes[i] / previous_close) if in_position else capital

        capital = float(equity)
        if in_position:
            high_close = max(float(high_close), float(closes[i])) if high_close is not None else float(closes[i])

        pending = None
        pending_reason = ""
        signal = "NONE"

        if in_position:
            exit_reasons: list[str] = []
            if vix[i] < variant.exit_vix_below:
                exit_reasons.append(f"vix_below_{variant.exit_vix_below:g}")
            if variant.trailing_stop_pct is not None and high_close is not None:
                if closes[i] <= high_close * (1 - variant.trailing_stop_pct):
                    exit_reasons.append(f"trail_{variant.trailing_stop_pct:.0%}")
            if variant.stop_loss_pct is not None and entry_close is not None:
                if closes[i] <= entry_close * (1 - variant.stop_loss_pct):
                    exit_reasons.append(f"stop_{variant.stop_loss_pct:.0%}")
            if trend_sma is not None and np.isfinite(trend_sma[i]) and closes[i] < trend_sma[i]:
                exit_reasons.append(f"below_sma_{variant.trend_exit_sma}")
            if variant.max_hold_days is not None and entry_date is not None:
                if len(dates[(dates >= entry_date) & (dates <= date)]) - 1 >= variant.max_hold_days:
                    exit_reasons.append(f"max_hold_{variant.max_hold_days}")
            if exit_reasons:
                pending = "SELL"
                pending_reason = "+".join(exit_reasons)
                signal = "SELL_NEXT_OPEN"
        elif cooldown_remaining > 0:
            cooldown_remaining -= 1
        elif vix[i] > 35:
            pending = "BUY"
            pending_reason = "vix_above_35"
            signal = "BUY_NEXT_OPEN"

        daily_rows.append(
            {
                "date": date.date().isoformat(),
                "equity": capital,
                "target": "SOXL" if in_position else "CASH",
                "action": action,
                "action_reason": action_reason,
                "execution_price": execution_price,
                "signal": signal,
                "pending_next_open": pending or "",
                "pending_reason": pending_reason,
                "SOXL_open": opens[i],
                "SOXL_close": closes[i],
                "VIX_close": vix[i],
                "benchmark_soxl_buy_hold": closes[i] / closes[0],
            }
        )

    if in_position and entry_date is not None and entry_price is not None:
        final_date = dates[-1]
        final_price = float(closes[-1])
        trade_return = final_price / entry_price - 1.0
        trades.append(
            {
                "entry_date": entry_date.date().isoformat(),
                "exit_date": final_date.date().isoformat(),
                "symbol": "SOXL",
                "exit_to": "OPEN",
                "entry_price": round(entry_price, 4),
                "exit_price": round(final_price, 4),
                "return_pct": round(trade_return * 100, 2),
                "outcome": "win" if trade_return > 0 else "loss",
                "exit_reason": "open",
                "holding_calendar_days": int((final_date - entry_date).days),
                "holding_trading_days": int(len(dates[dates >= entry_date]) - 1),
            }
        )

    daily = pd.DataFrame(daily_rows)
    daily["date"] = pd.to_datetime(daily["date"])
    return daily.set_index("date"), pd.DataFrame(trades)


def summarize_equity(equity: pd.Series) -> dict[str, float]:
    norm = equity / equity.iloc[0]
    returns = norm.pct_change().dropna()
    return {
        "return_pct": round((norm.iloc[-1] - 1.0) * 100, 2),
        "cagr_pct": round(cagr_pct(equity), 2),
        "max_drawdown_pct": round(max_drawdown(equity), 2),
        "sharpe": round(sharpe_ratio(equity), 3),
        "volatility_pct": round(returns.std(ddof=0) * math.sqrt(252) * 100, 2),
    }


def row_for_variant(variant: Variant, daily: pd.DataFrame, trades: pd.DataFrame) -> dict[str, object]:
    is_daily = daily.loc[daily.index < SPLIT_DATE]
    oos_daily = daily.loc[daily.index >= SPLIT_DATE]
    full = summarize_equity(daily["equity"])
    is_metrics = summarize_equity(is_daily["equity"])
    oos_metrics = summarize_equity(oos_daily["equity"])
    benchmark_oos = oos_daily["benchmark_soxl_buy_hold"] / oos_daily["benchmark_soxl_buy_hold"].iloc[0]
    return {
        "variant": variant.name,
        "exit_vix_below": variant.exit_vix_below,
        "trailing_stop_pct": variant.trailing_stop_pct,
        "stop_loss_pct": variant.stop_loss_pct,
        "trend_exit_sma": variant.trend_exit_sma,
        "max_hold_days": variant.max_hold_days,
        "cooldown_days": variant.cooldown_days,
        "is_return_pct": is_metrics["return_pct"],
        "is_cagr_pct": is_metrics["cagr_pct"],
        "is_max_drawdown_pct": is_metrics["max_drawdown_pct"],
        "is_sharpe": is_metrics["sharpe"],
        "oos_return_pct": oos_metrics["return_pct"],
        "oos_cagr_pct": oos_metrics["cagr_pct"],
        "oos_max_drawdown_pct": oos_metrics["max_drawdown_pct"],
        "oos_sharpe": oos_metrics["sharpe"],
        "full_return_pct": full["return_pct"],
        "full_max_drawdown_pct": full["max_drawdown_pct"],
        "full_sharpe": full["sharpe"],
        "oos_soxl_buy_hold_return_pct": round((benchmark_oos.iloc[-1] - 1.0) * 100, 2),
        "oos_soxl_buy_hold_max_drawdown_pct": round(max_drawdown(benchmark_oos), 2),
        "full_exposure_days_pct": round(daily["target"].eq("SOXL").mean() * 100, 2),
        "oos_exposure_days_pct": round(oos_daily["target"].eq("SOXL").mean() * 100, 2),
        "trades": len(trades),
    }


def variant_name(
    exit_vix_below: float,
    trailing_stop: float | None,
    stop_loss: float | None,
    trend_exit_sma: int | None,
    max_hold_days: int | None,
    cooldown_days: int,
) -> str:
    parts = [f"exit VIX<{exit_vix_below:g}"]
    if trailing_stop is not None:
        parts.append(f"trail {trailing_stop:.0%}")
    if stop_loss is not None:
        parts.append(f"stop {stop_loss:.0%}")
    if trend_exit_sma is not None:
        parts.append(f"exit below SMA{trend_exit_sma}")
    if max_hold_days is not None:
        parts.append(f"max {max_hold_days}d")
    if cooldown_days:
        parts.append(f"cooldown {cooldown_days}d")
    return "; ".join(parts)


def build_variants() -> list[Variant]:
    variants: list[Variant] = [
        Variant("base exit VIX<10", 10, None, None, None, None, 0),
    ]
    exit_vix_values = [10, 15, 20, 25, 30]
    trailing_values = [None, 0.25, 0.35, 0.50]
    stop_values = [None]
    trend_values = [None, 50, 100, 200]
    max_hold_values = [None, 126, 252, 504]
    cooldown_values = [0, 21]

    for exit_vix, trailing, stop_loss, trend_sma, max_hold, cooldown in product(
        exit_vix_values,
        trailing_values,
        stop_values,
        trend_values,
        max_hold_values,
        cooldown_values,
    ):
        active_overlays = sum(value is not None for value in [trailing, stop_loss, trend_sma, max_hold])
        if active_overlays > 2:
            continue
        if trailing is None and stop_loss is None and trend_sma is None and max_hold is None and cooldown:
            continue
        variants.append(
            Variant(
                variant_name(exit_vix, trailing, stop_loss, trend_sma, max_hold, cooldown),
                exit_vix,
                trailing,
                stop_loss,
                trend_sma,
                max_hold,
                cooldown,
            )
        )
    # Preserve insertion order while removing duplicates.
    return list(dict.fromkeys(variants))


def markdown_table(frame: pd.DataFrame) -> str:
    text = frame.fillna("").astype(str)
    lines = [
        "| " + " | ".join(text.columns) + " |",
        "| " + " | ".join(["---"] * len(text.columns)) + " |",
    ]
    for _, row in text.iterrows():
        lines.append("| " + " | ".join(str(row[column]).replace("|", "\\|") for column in text.columns) + " |")
    return "\n".join(lines)


def write_outputs(results: pd.DataFrame, best_daily: pd.DataFrame, best_trades: pd.DataFrame, selected: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    all_path = REPORTS / f"{OUTPUT_STEM}_all.csv"
    selected_path = REPORTS / f"{OUTPUT_STEM}_selected.csv"
    daily_path = REPORTS / f"{OUTPUT_STEM}_best_daily.csv"
    trades_path = REPORTS / f"{OUTPUT_STEM}_best_trades.csv"
    md_path = REPORTS / f"{OUTPUT_STEM}.md"

    results.to_csv(all_path, index=False)
    selected.to_csv(selected_path, index=False)
    best_daily.to_csv(daily_path)
    best_trades.to_csv(trades_path, index=False)

    show_cols = [
        "selection_rank",
        "variant",
        "is_return_pct",
        "is_max_drawdown_pct",
        "is_sharpe",
        "oos_return_pct",
        "oos_max_drawdown_pct",
        "oos_sharpe",
        "oos_exposure_days_pct",
        "trades",
    ]
    lines = [
        "# SOXL VIX Drawdown Variant Search",
        "",
        "Base idea: buy SOXL after VIX closes above 35, execute next open. Variants add risk exits, still next-open execution.",
        f"IS/OOS split: IS before {SPLIT_DATE.date()}, OOS from {SPLIT_DATE.date()} onward.",
        "",
        "Selection: top rows are ranked by IS drawdown first, then IS Sharpe and IS return. OOS columns are validation only.",
        "",
        "## Selected Variants",
        "",
        markdown_table(selected[show_cols]),
        "",
        "## Outputs",
        "",
        f"- All variants: `{all_path}`",
        f"- Selected variants: `{selected_path}`",
        f"- Best selected daily curve: `{daily_path}`",
        f"- Best selected trades: `{trades_path}`",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(md_path)
    print(selected[show_cols].to_string(index=False))


def main() -> None:
    frame = fetch_inputs()
    variants = build_variants()
    rows: list[dict[str, object]] = []
    daily_by_variant: dict[str, pd.DataFrame] = {}
    trades_by_variant: dict[str, pd.DataFrame] = {}

    for index, variant in enumerate(variants, start=1):
        daily, trades = simulate_variant(frame, variant)
        rows.append(row_for_variant(variant, daily, trades))
        daily_by_variant[variant.name] = daily
        trades_by_variant[variant.name] = trades
        if index % 500 == 0:
            print(f"Tested {index:,} variants...", flush=True)

    results = pd.DataFrame(rows)
    results = results.drop_duplicates(
        subset=[
            "is_return_pct",
            "is_max_drawdown_pct",
            "is_sharpe",
            "oos_return_pct",
            "oos_max_drawdown_pct",
            "oos_sharpe",
            "full_exposure_days_pct",
            "trades",
        ]
    ).reset_index(drop=True)

    eligible = results[
        (results["is_return_pct"] > 0)
        & (results["oos_return_pct"] > 0)
        & (results["oos_exposure_days_pct"] >= 10)
    ].copy()
    selected = eligible.sort_values(
        ["is_max_drawdown_pct", "is_sharpe", "is_return_pct"],
        ascending=[False, False, False],
    ).head(20)
    selected.insert(0, "selection_rank", np.arange(1, len(selected) + 1))

    best_name = str(selected.iloc[0]["variant"])
    write_outputs(results, daily_by_variant[best_name], trades_by_variant[best_name], selected)


if __name__ == "__main__":
    main()
