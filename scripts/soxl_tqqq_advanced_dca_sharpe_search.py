from __future__ import annotations

from itertools import product
from pathlib import Path
import math
import sys

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
sys.path.insert(0, str(ROOT / "scripts"))

from soxl_tqqq_dca_advanced_search import apply_advanced_dca  # noqa: E402
from soxl_tqqq_dca_overlay_search import SYMBOLS, load_best_rotation_inputs  # noqa: E402


SPLIT_DATE = pd.Timestamp("2020-01-01")


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


def period_metrics(equity: np.ndarray, dates: pd.DatetimeIndex, mask: np.ndarray) -> dict[str, float | str]:
    sub = equity[mask]
    sub_dates = dates[mask]
    norm = sub / sub[0]
    return {
        "range": f"{sub_dates[0].date()} to {sub_dates[-1].date()}",
        "return_pct": round((float(norm[-1]) - 1) * 100, 2),
        "max_drawdown_pct": round(max_drawdown(norm), 2),
        "sharpe": round(sharpe_ratio(norm), 3),
    }


def simulate_fast(
    prices: np.ndarray,
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
) -> tuple[np.ndarray, np.ndarray, int, int]:
    returns = np.vstack([np.zeros(2), prices[1:] / prices[:-1] - 1])
    sma = sma_cache[trend_guard_sma] if trend_guard_sma is not None else None

    equity = np.ones(len(dates), dtype=float)
    exposure_history = np.zeros(len(dates), dtype=float)
    trade_events = 0
    rotation_resets = 0

    symbol = int(selected_codes[0])
    units = 1
    entry_price = float(prices[0, symbol])
    anchor = entry_price
    high = entry_price
    low_since_extra = entry_price
    extra_avg_cost = np.nan
    extra_entry_i: int | None = None
    equity_peak = 1.0

    for i in range(1, len(dates)):
        today_symbol = int(selected_codes[i])
        if today_symbol != symbol:
            rotation_resets += 1
            symbol = today_symbol
            units = 1
            entry_price = float(prices[i, symbol])
            anchor = entry_price
            high = entry_price
            low_since_extra = entry_price
            extra_avg_cost = np.nan
            extra_entry_i = None

        exposure = min(units * unit_exposure, max_exposure)
        if sma is not None and np.isfinite(sma[i, symbol]) and prices[i, symbol] < sma[i, symbol]:
            exposure = min(exposure, trend_guard_exposure if trend_guard_exposure is not None else exposure)
        prev_dd = equity[i - 1] / equity_peak - 1
        if equity_dd_guard is not None and prev_dd <= -equity_dd_guard:
            exposure = min(exposure, equity_dd_guard_exposure if equity_dd_guard_exposure is not None else exposure)

        exposure_history[i] = exposure
        equity[i] = equity[i - 1] * (1 + exposure * float(returns[i, symbol]))
        equity_peak = max(equity_peak, equity[i])

        price = float(prices[i, symbol])
        high = max(high, price)
        if anchor_mode == "rolling_high":
            anchor = high

        if units > 1:
            low_since_extra = min(low_since_extra, price)
            sell_extra = False
            if sell_mode == "recover_to_anchor":
                sell_extra = price >= anchor * (1 - sell_param)
            elif sell_mode == "rebound_from_low":
                sell_extra = price >= low_since_extra * (1 + sell_param)
            elif sell_mode == "extra_profit":
                sell_extra = bool(np.isfinite(extra_avg_cost)) and price >= extra_avg_cost * (1 + sell_param)
            else:
                raise ValueError(f"Unknown sell mode: {sell_mode}")
            if max_extra_days is not None and extra_entry_i is not None and (i - extra_entry_i) >= max_extra_days:
                sell_extra = True
            if sell_extra:
                trade_events += 1
                units = 1
                low_since_extra = price
                extra_avg_cost = np.nan
                extra_entry_i = None

        drop_from_anchor = price / anchor - 1
        if units == 1 and drop_from_anchor <= -add1_drop:
            units = 2
            extra_avg_cost = price
            extra_entry_i = i
            low_since_extra = price
            trade_events += 1
        elif units == 2 and drop_from_anchor <= -add2_drop:
            units = 3
            extra_avg_cost = float(np.mean([extra_avg_cost, price])) if np.isfinite(extra_avg_cost) else price
            trade_events += 1

    return equity, exposure_history, trade_events, rotation_resets


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


def main() -> None:
    close, allocation, _curve = load_best_rotation_inputs()
    dates = close.index
    prices = close[SYMBOLS].to_numpy(dtype=float)
    selected_codes = allocation.map({"SOXL": 0, "TQQQ": 1}).to_numpy(dtype=int)
    sma_cache = {
        window: close[SYMBOLS].rolling(window).mean().to_numpy(dtype=float)
        for window in [50, 75, 100, 150, 200, 250]
    }
    is_mask = dates < SPLIT_DATE
    oos_mask = dates >= SPLIT_DATE

    # Validation against the original, slower implementation for the known winner.
    validation_params = {
        "unit_exposure": 1.00,
        "max_exposure": 2.00,
        "anchor_mode": "rolling_high",
        "add1_drop": 0.05,
        "add2_drop": 0.20,
        "sell_mode": "extra_profit",
        "sell_param": 0.15,
        "max_extra_days": 20,
        "trend_guard_sma": 100,
        "trend_guard_exposure": 1.00,
        "equity_dd_guard": None,
        "equity_dd_guard_exposure": None,
    }
    slow_equity, _slow_units, _slow_exposure, _slow_trades = apply_advanced_dca(close, allocation, **validation_params)
    fast_equity, _fast_exposure, _events, _resets = simulate_fast(prices, dates, selected_codes, sma_cache, **validation_params)
    validation_max_rel_diff = float(np.max(np.abs(slow_equity.to_numpy(dtype=float) / fast_equity - 1)))

    unit_exposures = [0.33, 0.50, 0.67, 1.00]
    max_exposures = [0.67, 1.00, 1.50, 2.00]
    anchor_modes = ["entry", "rolling_high"]
    add_pairs = [
        (0.05, 0.12),
        (0.05, 0.20),
        (0.10, 0.20),
        (0.15, 0.30),
    ]
    sell_configs = [
        ("extra_profit", 0.10),
        ("extra_profit", 0.15),
        ("rebound_from_low", 0.05),
        ("recover_to_anchor", 0.05),
    ]
    max_days_values: list[int | None] = [10, 20]
    guard_configs = [
        (None, None, None, None),
        (100, 0.25, None, None),
        (100, 0.50, None, None),
        (200, 0.50, None, None),
        (200, 0.75, None, None),
        (None, None, 0.35, 0.50),
        (None, None, 0.45, 0.50),
        (100, 0.50, 0.35, 0.25),
    ]

    rows: list[dict[str, object]] = []
    tested = 0
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
        equity, exposure, trade_events, rotation_resets = simulate_fast(prices, dates, selected_codes, sma_cache, **params)
        is_metrics = period_metrics(equity, dates, is_mask)
        oos_metrics = period_metrics(equity, dates, oos_mask)
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
            }
        )
        tested += 1
        if tested % 500 == 0:
            print(f"Tested {tested:,} variants...", flush=True)

    result = pd.DataFrame(rows)
    # Primary ranking: improve out-of-sample Sharpe. Require positive IS and OOS return to avoid defensive but unusable rows.
    eligible = result[(result["is_return_pct"] > 0) & (result["oos_return_pct"] > 0)].copy()
    top_oos_sharpe = eligible.sort_values(
        ["oos_sharpe", "oos_max_drawdown_pct", "oos_return_pct", "is_sharpe"],
        ascending=[False, False, False, False],
    ).head(25)
    top5 = top_oos_sharpe.head(5).copy()
    top5.insert(0, "rank_by_oos_sharpe", np.arange(1, len(top5) + 1))

    # Secondary view: variants selected by IS Sharpe, then observed OOS.
    top_is_sharpe = eligible.sort_values(
        ["is_sharpe", "is_max_drawdown_pct", "is_return_pct"],
        ascending=[False, False, False],
    ).head(25).copy()
    top_is_sharpe.insert(0, "rank_by_is_sharpe", np.arange(1, len(top_is_sharpe) + 1))

    # Recompute and save daily curve/trades for the top OOS Sharpe variant using the reference implementation.
    best = top5.iloc[0].to_dict()
    best_params = {
        "unit_exposure": float(best["unit_exposure"]),
        "max_exposure": float(best["max_exposure"]),
        "anchor_mode": str(best["anchor_mode"]),
        "add1_drop": float(best["add1_drop_pct"]) / 100,
        "add2_drop": float(best["add2_drop_pct"]) / 100,
        "sell_mode": str(best["sell_mode"]),
        "sell_param": float(best["sell_param_pct"]) / 100,
        "max_extra_days": None if best["max_extra_days"] == "none" else int(best["max_extra_days"]),
        "trend_guard_sma": None if best["trend_guard_sma"] == "none" else int(best["trend_guard_sma"]),
        "trend_guard_exposure": None if best["trend_guard_exposure"] == "none" else float(best["trend_guard_exposure"]),
        "equity_dd_guard": None if best["equity_dd_guard_pct"] == "none" else float(best["equity_dd_guard_pct"]) / 100,
        "equity_dd_guard_exposure": None if best["equity_dd_guard_exposure"] == "none" else float(best["equity_dd_guard_exposure"]),
    }
    best_equity, best_units, best_exposure, best_trades = apply_advanced_dca(close, allocation, **best_params)
    daily = pd.DataFrame(
        {
            "date": dates,
            "equity": best_equity.values,
            "units": best_units.values,
            "exposure": best_exposure.values,
            "allocation": allocation.values,
        }
    )

    all_path = REPORTS / "soxl_tqqq_advanced_dca_sharpe_search_all.csv"
    top_path = ROOT / "SOXL_TQQQ_Advanced_DCA_Sharpe_Top5.csv"
    xlsx_path = ROOT / "SOXL_TQQQ_Advanced_DCA_Sharpe_Search.xlsx"
    html_path = ROOT / "SOXL_TQQQ_Advanced_DCA_Sharpe_Search.html"
    daily_path = REPORTS / "soxl_tqqq_advanced_dca_sharpe_best_daily.csv"
    trades_path = REPORTS / "soxl_tqqq_advanced_dca_sharpe_best_trades.csv"

    result.to_csv(all_path, index=False)
    top5.to_csv(top_path, index=False)
    daily.to_csv(daily_path, index=False)
    pd.DataFrame(best_trades).to_csv(trades_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        top5.to_excel(writer, sheet_name="Top 5 OOS Sharpe", index=False)
        top_is_sharpe.to_excel(writer, sheet_name="Top IS Sharpe", index=False)
        result.sort_values("oos_sharpe", ascending=False).head(1000).to_excel(writer, sheet_name="Top 1000", index=False)
        daily.to_excel(writer, sheet_name="Best Daily", index=False)
        pd.DataFrame(best_trades).to_excel(writer, sheet_name="Best Trades", index=False)
        for ws in writer.book.worksheets:
            ws.freeze_panes = "A2"
            for col_cells in ws.columns:
                width = max(len(str(cell.value)) if cell.value is not None else 0 for cell in col_cells)
                ws.column_dimensions[col_cells[0].column_letter].width = min(max(width + 2, 10), 64)

    display_cols = [
        "rank_by_oos_sharpe",
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
    ]
    html_path.write_text(
        "<!doctype html><html><head><meta charset='utf-8'><title>Advanced DCA Sharpe Search</title>"
        "<style>body{font-family:Arial,sans-serif;margin:28px;color:#111827}table{border-collapse:collapse;font-size:13px}"
        "th,td{border:1px solid #d1d5db;padding:7px 10px;vertical-align:top}th{background:#f3f4f6}"
        "td:nth-child(n+3){text-align:right}td:nth-child(2){text-align:left;max-width:720px}</style></head><body>"
        "<h1>Advanced DCA Sharpe Search</h1>"
        f"<p>Tested {tested:,} variants. Fast simulator max relative validation difference vs original known winner: {validation_max_rel_diff:.8f}.</p>"
        "<h2>Top 5 by Out-of-Sample Sharpe</h2>"
        + top5[display_cols].to_html(index=False, escape=False)
        + "<h2>Top 25 by In-Sample Sharpe</h2>"
        + top_is_sharpe.head(25).to_html(index=False, escape=False)
        + "</body></html>",
        encoding="utf-8",
    )

    print(f"Tested {tested:,} variants")
    print(f"Validation max relative diff vs original known winner: {validation_max_rel_diff:.10f}")
    print(top5[display_cols].to_string(index=False))
    print(top_path)
    print(xlsx_path)
    print(html_path)
    print(all_path)


if __name__ == "__main__":
    main()
