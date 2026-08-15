from __future__ import annotations

from itertools import product
from pathlib import Path
import math
import sys

import numpy as np
import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
sys.path.insert(0, str(ROOT / "scripts"))

from soxl_tqqq_dca_overlay_search import END_EXCLUSIVE, START, SYMBOLS, load_best_rotation_inputs  # noqa: E402


SPLIT_DATE = pd.Timestamp("2020-01-01")


def fetch_adjusted_ohlc() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = yf.download(
        SYMBOLS,
        start=START,
        end=END_EXCLUSIVE,
        interval="1d",
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    if raw.empty:
        raise RuntimeError("No yfinance OHLC data returned.")
    open_px = raw["Open"].copy() if isinstance(raw.columns, pd.MultiIndex) else raw[["Open"]].copy()
    close_px = raw["Close"].copy() if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]].copy()
    open_px = open_px[SYMBOLS].dropna(how="all")
    close_px = close_px[SYMBOLS].dropna(how="all")
    open_px.index = pd.to_datetime(open_px.index).tz_localize(None)
    close_px.index = pd.to_datetime(close_px.index).tz_localize(None)
    return open_px, close_px


def max_drawdown(values: np.ndarray) -> float:
    return float(np.min(values / np.maximum.accumulate(values) - 1) * 100)


def sharpe_ratio(values: np.ndarray) -> float:
    if len(values) < 2:
        return np.nan
    returns = np.empty(len(values), dtype=float)
    returns[0] = 0.0
    returns[1:] = values[1:] / values[:-1] - 1
    std = float(np.std(returns))
    if std == 0 or not np.isfinite(std):
        return np.nan
    return float(np.mean(returns) / std * math.sqrt(252))


def metrics(equity: np.ndarray, dates: pd.DatetimeIndex, mask: np.ndarray) -> dict[str, object]:
    sub = equity[mask]
    sub_dates = dates[mask]
    norm = sub / sub[0]
    return {
        "range": f"{sub_dates[0].date()} to {sub_dates[-1].date()}",
        "return_pct": round((float(norm[-1]) - 1) * 100, 2),
        "max_drawdown_pct": round(max_drawdown(norm), 2),
        "sharpe": round(sharpe_ratio(norm), 3),
    }


def variant_name(params: dict[str, object]) -> str:
    return (
        f"unit={params['unit_exposure']:.2f}, cap={params['max_exposure']:.2f}, "
        f"anchor={params['anchor_mode']}, add={params['add1_drop']:.0%}/{params['add2_drop']:.0%}, "
        f"sell={params['sell_mode']} {params['sell_param']:.0%}, "
        f"max_days={params['max_extra_days'] if params['max_extra_days'] is not None else 'none'}, "
        f"trend_sma={params['trend_guard_sma'] if params['trend_guard_sma'] is not None else 'none'}, "
        f"trend_exp={params['trend_guard_exposure'] if params['trend_guard_exposure'] is not None else 'none'}, "
        f"dd_guard={params['equity_dd_guard'] if params['equity_dd_guard'] is not None else 'none'}, "
        f"dd_exp={params['equity_dd_guard_exposure'] if params['equity_dd_guard_exposure'] is not None else 'none'}"
    )


def simulate_next_open(
    open_px: np.ndarray,
    close_px: np.ndarray,
    dates: pd.DatetimeIndex,
    selected_codes: np.ndarray,
    sma_cache: dict[int, np.ndarray],
    *,
    unit_exposure: float,
    max_exposure: float,
    anchor_mode: str,
    add1_drop: float,
    add2_drop: float,
    sell_mode: str,
    sell_param: float,
    max_extra_days: int | None,
    trend_guard_sma: int | None,
    trend_guard_exposure: float | None,
    equity_dd_guard: float | None,
    equity_dd_guard_exposure: float | None,
    keep_trades: bool = False,
) -> tuple[np.ndarray, np.ndarray, int, int, int, list[dict[str, object]]]:
    n = len(dates)
    sma = sma_cache[trend_guard_sma] if trend_guard_sma is not None else None

    equity = np.ones(n, dtype=float)
    exposure_history = np.zeros(n, dtype=float)
    trades: list[dict[str, object]] = []
    fallback_count = 0
    trade_events = 0
    rotation_resets = 0

    symbol = int(selected_codes[0])
    units = 1
    entry_price = float(close_px[0, symbol])
    anchor = entry_price
    high = entry_price
    low_since_extra = entry_price
    extra_avg_cost = np.nan
    extra_entry_i: int | None = None
    current_exposure = min(units * unit_exposure, max_exposure)
    equity_peak = 1.0
    pending: dict[str, object] | None = None

    def execution_price(i: int, code: int) -> tuple[float, str]:
        nonlocal fallback_count
        price = float(open_px[i, code])
        if np.isfinite(price):
            return price, "next_open"
        fallback_count += 1
        return float(close_px[i, code]), "next_close_fallback"

    def exposure_for(signal_i: int) -> float:
        exposure = min(units * unit_exposure, max_exposure)
        if sma is not None and np.isfinite(sma[signal_i, symbol]) and close_px[signal_i, symbol] < sma[signal_i, symbol]:
            exposure = min(exposure, trend_guard_exposure if trend_guard_exposure is not None else exposure)
        prev_dd = equity[signal_i] / equity_peak - 1 if equity_peak > 0 else 0.0
        if equity_dd_guard is not None and prev_dd <= -equity_dd_guard:
            exposure = min(exposure, equity_dd_guard_exposure if equity_dd_guard_exposure is not None else exposure)
        return exposure

    for i in range(1, n):
        old_symbol = symbol
        prior_close = float(close_px[i - 1, old_symbol])
        open_price = float(open_px[i, old_symbol])
        if not np.isfinite(open_price):
            open_price = float(close_px[i, old_symbol])
            fallback_count += 1
        equity_after_open = equity[i - 1] * (1 + current_exposure * (open_price / prior_close - 1))

        # Execute yesterday's completed-close signal at today's adjusted open.
        if pending is not None:
            action = str(pending["action"])
            if action == "ROTATE":
                previous_symbol = symbol
                symbol = int(pending["to_code"])
                px, exec_type = execution_price(i, symbol)
                rotation_resets += 1
                trade_events += 1
                if keep_trades:
                    trades.append(
                        {
                            "signal_date": pending["signal_date"],
                            "execution_date": dates[i].date().isoformat(),
                            "execution_type": exec_type,
                            "action": "RESET_ON_ROTATION",
                            "from_symbol": SYMBOLS[previous_symbol],
                            "to_symbol": SYMBOLS[symbol],
                            "units_before": units,
                            "price": round(px, 4),
                        }
                    )
                units = 1
                entry_price = px
                anchor = px
                high = px
                low_since_extra = px
                extra_avg_cost = np.nan
                extra_entry_i = None
            elif action == "SELL_EXTRAS":
                px, exec_type = execution_price(i, symbol)
                trade_events += 1
                if keep_trades:
                    trades.append(
                        {
                            "signal_date": pending["signal_date"],
                            "execution_date": dates[i].date().isoformat(),
                            "execution_type": exec_type,
                            "action": "SELL_EXTRAS",
                            "symbol": SYMBOLS[symbol],
                            "units_before": units,
                            "units_after": 1,
                            "price": round(px, 4),
                            "reason": pending.get("reason", ""),
                        }
                    )
                units = 1
                low_since_extra = px
                extra_avg_cost = np.nan
                extra_entry_i = None
            elif action == "BUY_EXTRA_1" and units == 1:
                px, exec_type = execution_price(i, symbol)
                units = 2
                extra_avg_cost = px
                extra_entry_i = i
                low_since_extra = px
                trade_events += 1
                if keep_trades:
                    trades.append(
                        {
                            "signal_date": pending["signal_date"],
                            "execution_date": dates[i].date().isoformat(),
                            "execution_type": exec_type,
                            "action": "BUY_EXTRA_1",
                            "symbol": SYMBOLS[symbol],
                            "units_after": units,
                            "price": round(px, 4),
                            "drop_from_anchor_pct": pending.get("drop_from_anchor_pct", np.nan),
                        }
                    )
            elif action == "BUY_EXTRA_2" and units == 2:
                px, exec_type = execution_price(i, symbol)
                units = 3
                extra_avg_cost = float(np.mean([extra_avg_cost, px])) if np.isfinite(extra_avg_cost) else px
                trade_events += 1
                if keep_trades:
                    trades.append(
                        {
                            "signal_date": pending["signal_date"],
                            "execution_date": dates[i].date().isoformat(),
                            "execution_type": exec_type,
                            "action": "BUY_EXTRA_2",
                            "symbol": SYMBOLS[symbol],
                            "units_after": units,
                            "price": round(px, 4),
                            "drop_from_anchor_pct": pending.get("drop_from_anchor_pct", np.nan),
                        }
                    )
            pending = None

        current_exposure = exposure_for(i - 1)
        intraday_close = float(close_px[i, symbol])
        intraday_open = float(open_px[i, symbol])
        if not np.isfinite(intraday_open):
            intraday_open = intraday_close
        equity[i] = equity_after_open * (1 + current_exposure * (intraday_close / intraday_open - 1))
        equity_peak = max(equity_peak, equity[i])
        exposure_history[i] = current_exposure

        # Generate a new signal after today's close for next trading day's open.
        price = intraday_close
        high = max(high, price)
        if anchor_mode == "rolling_high":
            anchor = high

        next_target = int(selected_codes[i])
        if next_target != symbol:
            pending = {"action": "ROTATE", "signal_date": dates[i].date().isoformat(), "to_code": next_target}
            continue

        if units > 1:
            low_since_extra = min(low_since_extra, price)
            sell_extra = False
            reason = ""
            if sell_mode == "extra_profit":
                sell_extra = bool(np.isfinite(extra_avg_cost)) and price >= extra_avg_cost * (1 + sell_param)
                reason = f"extra shares profit >= {sell_param:.0%}"
            elif sell_mode == "rebound_from_low":
                sell_extra = price >= low_since_extra * (1 + sell_param)
                reason = f"price rebounded {sell_param:.0%} from DCA low"
            elif sell_mode == "recover_to_anchor":
                sell_extra = price >= anchor * (1 - sell_param)
                reason = f"price >= anchor minus {sell_param:.0%}"
            else:
                raise ValueError(f"Unknown sell_mode: {sell_mode}")
            if max_extra_days is not None and extra_entry_i is not None and (i - extra_entry_i) >= max_extra_days:
                sell_extra = True
                reason = f"extra shares max holding days {max_extra_days}"
            if sell_extra:
                pending = {"action": "SELL_EXTRAS", "signal_date": dates[i].date().isoformat(), "reason": reason}
                continue

        drop_from_anchor = price / anchor - 1
        if units == 1 and drop_from_anchor <= -add1_drop:
            pending = {
                "action": "BUY_EXTRA_1",
                "signal_date": dates[i].date().isoformat(),
                "drop_from_anchor_pct": round(drop_from_anchor * 100, 2),
            }
        elif units == 2 and drop_from_anchor <= -add2_drop:
            pending = {
                "action": "BUY_EXTRA_2",
                "signal_date": dates[i].date().isoformat(),
                "drop_from_anchor_pct": round(drop_from_anchor * 100, 2),
            }

    return equity, exposure_history, trade_events, rotation_resets, fallback_count, trades


def main() -> None:
    open_df, close_df = fetch_adjusted_ohlc()
    _close, allocation, _curve = load_best_rotation_inputs()
    common = open_df.index.intersection(close_df.index).intersection(allocation.index)
    open_df = open_df.loc[common, SYMBOLS]
    close_df = close_df.loc[common, SYMBOLS]
    allocation = allocation.loc[common]
    dates = close_df.index
    open_px = open_df.to_numpy(dtype=float)
    close_px = close_df.to_numpy(dtype=float)
    selected_codes = allocation.map({"SOXL": 0, "TQQQ": 1}).to_numpy(dtype=int)
    sma_windows = [50, 75, 100, 150, 200]
    sma_cache = {window: close_df[SYMBOLS].rolling(window).mean().to_numpy(dtype=float) for window in sma_windows}
    is_mask = dates < SPLIT_DATE
    oos_mask = dates >= SPLIT_DATE

    # Focused walk-forward grid: centered on the families that won by IS Sharpe
    # in the earlier same-close research, then revalidated with next-open fills.
    unit_exposures = [0.60, 0.67, 0.75]
    max_exposures = [1.00, 1.50, 2.00]
    anchor_modes = ["rolling_high"]
    add_pairs = [(0.05, 0.15), (0.05, 0.20), (0.08, 0.20)]
    sell_configs = [
        ("extra_profit", 0.12),
        ("extra_profit", 0.18),
        ("rebound_from_low", 0.05),
    ]
    max_days_values: list[int | None] = [10, 15]
    guard_configs = [
        (None, None, None, None),
        (75, 0.20, None, None),
        (75, 0.25, None, None),
        (100, 0.20, None, None),
        (75, 0.20, 0.35, 0.25),
    ]

    rows: list[dict[str, object]] = []
    tested = 0
    total_fallback = 0
    for unit_exposure, max_exposure, anchor_mode, (add1, add2), (sell_mode, sell_param), max_days, guard in product(
        unit_exposures,
        max_exposures,
        anchor_modes,
        add_pairs,
        sell_configs,
        max_days_values,
        guard_configs,
    ):
        if max_exposure < unit_exposure:
            continue
        if max_exposure > unit_exposure * 3.1:
            continue
        trend_sma, trend_exp, dd_guard, dd_exp = guard
        params = {
            "unit_exposure": unit_exposure,
            "max_exposure": max_exposure,
            "anchor_mode": anchor_mode,
            "add1_drop": add1,
            "add2_drop": add2,
            "sell_mode": sell_mode,
            "sell_param": sell_param,
            "max_extra_days": max_days,
            "trend_guard_sma": trend_sma,
            "trend_guard_exposure": trend_exp,
            "equity_dd_guard": dd_guard,
            "equity_dd_guard_exposure": dd_exp,
        }
        equity, exposure, trade_events, rotation_resets, fallback_count, _trades = simulate_next_open(
            open_px, close_px, dates, selected_codes, sma_cache, **params
        )
        total_fallback += fallback_count
        is_metrics = metrics(equity, dates, is_mask)
        oos_metrics = metrics(equity, dates, oos_mask)
        full_norm = equity / equity[0]
        rows.append(
            {
                "variant": variant_name(params),
                "unit_exposure": unit_exposure,
                "max_exposure": max_exposure,
                "anchor_mode": anchor_mode,
                "add1_drop_pct": round(add1 * 100, 2),
                "add2_drop_pct": round(add2 * 100, 2),
                "sell_mode": sell_mode,
                "sell_param_pct": round(sell_param * 100, 2),
                "max_extra_days": max_days if max_days is not None else "none",
                "trend_guard_sma": trend_sma if trend_sma is not None else "none",
                "trend_guard_exposure": trend_exp if trend_exp is not None else "none",
                "equity_dd_guard_pct": round(dd_guard * 100, 2) if dd_guard is not None else "none",
                "equity_dd_guard_exposure": dd_exp if dd_exp is not None else "none",
                "is_range": is_metrics["range"],
                "is_return_pct": is_metrics["return_pct"],
                "is_max_drawdown_pct": is_metrics["max_drawdown_pct"],
                "is_sharpe": is_metrics["sharpe"],
                "oos_range": oos_metrics["range"],
                "oos_return_pct": oos_metrics["return_pct"],
                "oos_max_drawdown_pct": oos_metrics["max_drawdown_pct"],
                "oos_sharpe": oos_metrics["sharpe"],
                "full_return_pct": round((float(full_norm[-1]) - 1) * 100, 2),
                "full_max_drawdown_pct": round(max_drawdown(full_norm), 2),
                "full_sharpe": round(sharpe_ratio(full_norm), 3),
                "avg_exposure": round(float(np.mean(exposure)), 3),
                "days_above_1x_pct": round(float(np.mean(exposure > 1.0) * 100), 2),
                "trade_events": trade_events,
                "rotation_resets": rotation_resets,
                "open_fallback_count": fallback_count,
            }
        )
        tested += 1
        if tested % 100 == 0:
            print(f"Tested {tested:,} variants...", flush=True)

    result = pd.DataFrame(rows)
    eligible = result[(result["is_return_pct"] > 0) & (result["oos_return_pct"] > 0)].copy()
    behavior_key = [
        "is_return_pct",
        "is_max_drawdown_pct",
        "is_sharpe",
        "oos_return_pct",
        "oos_max_drawdown_pct",
        "oos_sharpe",
        "full_return_pct",
        "full_max_drawdown_pct",
        "full_sharpe",
        "avg_exposure",
        "days_above_1x_pct",
    ]
    unique = eligible.sort_values(
        ["is_sharpe", "is_max_drawdown_pct", "is_return_pct"], ascending=[False, False, False]
    ).drop_duplicates(subset=behavior_key)
    is_selected = unique.head(10).copy().reset_index(drop=True)
    is_selected.insert(0, "is_selection_rank", np.arange(1, len(is_selected) + 1))
    oos_ranked = is_selected.sort_values(
        ["oos_sharpe", "oos_max_drawdown_pct", "oos_return_pct"], ascending=[False, False, False]
    ).reset_index(drop=True)
    oos_ranked.insert(0, "oos_sharpe_rank", np.arange(1, len(oos_ranked) + 1))

    # Save the OOS-ranked top strategy's daily curve and trades.
    best = oos_ranked.iloc[0]
    best_params = {
        "unit_exposure": float(best["unit_exposure"]),
        "max_exposure": float(best["max_exposure"]),
        "anchor_mode": str(best["anchor_mode"]),
        "add1_drop": float(best["add1_drop_pct"]) / 100,
        "add2_drop": float(best["add2_drop_pct"]) / 100,
        "sell_mode": str(best["sell_mode"]),
        "sell_param": float(best["sell_param_pct"]) / 100,
        "max_extra_days": int(best["max_extra_days"]),
        "trend_guard_sma": None if str(best["trend_guard_sma"]) == "none" else int(best["trend_guard_sma"]),
        "trend_guard_exposure": None if str(best["trend_guard_exposure"]) == "none" else float(best["trend_guard_exposure"]),
        "equity_dd_guard": None if str(best["equity_dd_guard_pct"]) == "none" else float(best["equity_dd_guard_pct"]) / 100,
        "equity_dd_guard_exposure": None if str(best["equity_dd_guard_exposure"]) == "none" else float(best["equity_dd_guard_exposure"]),
    }
    best_equity, best_exposure, _events, _resets, _fallback, best_trades = simulate_next_open(
        open_px, close_px, dates, selected_codes, sma_cache, keep_trades=True, **best_params
    )
    best_daily = pd.DataFrame(
        {
            "date": dates,
            "equity": best_equity,
            "exposure": best_exposure,
            "allocation_signal": allocation.values,
            "SOXL_open": open_df["SOXL"].values,
            "SOXL_close": close_df["SOXL"].values,
            "TQQQ_open": open_df["TQQQ"].values,
            "TQQQ_close": close_df["TQQQ"].values,
        }
    )

    report_cols = [
        "oos_sharpe_rank",
        "is_selection_rank",
        "variant",
        "is_return_pct",
        "is_max_drawdown_pct",
        "is_sharpe",
        "oos_return_pct",
        "oos_max_drawdown_pct",
        "oos_sharpe",
        "full_return_pct",
        "full_max_drawdown_pct",
        "full_sharpe",
        "avg_exposure",
        "days_above_1x_pct",
        "trade_events",
        "open_fallback_count",
    ]
    report = oos_ranked[report_cols].copy()

    all_path = REPORTS / "soxl_tqqq_advanced_dca_next_open_all.csv"
    csv_path = ROOT / "SOXL_TQQQ_Advanced_DCA_NextOpen_IS_Sharpe_Selected_OOS_Ranked.csv"
    xlsx_path = ROOT / "SOXL_TQQQ_Advanced_DCA_NextOpen_IS_Sharpe_Selected_OOS_Ranked.xlsx"
    html_path = ROOT / "SOXL_TQQQ_Advanced_DCA_NextOpen_IS_Sharpe_Selected_OOS_Ranked.html"
    daily_path = REPORTS / "soxl_tqqq_advanced_dca_next_open_best_daily.csv"
    trades_path = REPORTS / "soxl_tqqq_advanced_dca_next_open_best_trades.csv"

    result.to_csv(all_path, index=False)
    report.to_csv(csv_path, index=False)
    best_daily.to_csv(daily_path, index=False)
    pd.DataFrame(best_trades).to_csv(trades_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        report.to_excel(writer, sheet_name="IS Top10 OOS Ranked", index=False)
        is_selected.to_excel(writer, sheet_name="IS Selection Order", index=False)
        unique.head(250).to_excel(writer, sheet_name="Top 250 IS Sharpe", index=False)
        best_daily.to_excel(writer, sheet_name="Best Daily", index=False)
        pd.DataFrame(best_trades).to_excel(writer, sheet_name="Best Trades", index=False)
        for ws in writer.book.worksheets:
            ws.freeze_panes = "A2"
            for col_cells in ws.columns:
                width = max(len(str(cell.value)) if cell.value is not None else 0 for cell in col_cells)
                ws.column_dimensions[col_cells[0].column_letter].width = min(max(width + 2, 10), 66)
    html_path.write_text(
        "<!doctype html><html><head><meta charset='utf-8'><title>Advanced DCA Next-Open IS/OOS</title>"
        "<style>body{font-family:Arial,sans-serif;margin:28px;color:#111827}table{border-collapse:collapse;font-size:13px}"
        "th,td{border:1px solid #d1d5db;padding:7px 10px;vertical-align:top}th{background:#f3f4f6}"
        "td:nth-child(3){text-align:left;max-width:780px}td:nth-child(n+4){text-align:right}</style></head><body>"
        "<h1>Advanced DCA: Next-Day Open Execution</h1>"
        f"<p>Tested {tested:,} variants. Top 10 selected by in-sample Sharpe only, then ranked by out-of-sample Sharpe. Total open fallback events across all variant simulations: {total_fallback:,}.</p>"
        + report.to_html(index=False, escape=False)
        + "</body></html>",
        encoding="utf-8",
    )

    print(f"Tested {tested:,} variants")
    print(f"Total open fallback events across all variants: {total_fallback:,}")
    print(report.to_string(index=False))
    print(csv_path)
    print(xlsx_path)
    print(html_path)
    print(all_path)


if __name__ == "__main__":
    main()
