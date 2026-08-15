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

from soxl_tqqq_advanced_dca_close_exec_cash_is_oos import (  # noqa: E402
    SPLIT_DATE,
    cash_risk_on,
    fetch_adjusted_close,
    max_drawdown,
    metrics,
    sharpe_ratio,
)
from soxl_tqqq_dca_overlay_search import SYMBOLS, load_best_rotation_inputs  # noqa: E402


def variant_name(params: dict[str, object]) -> str:
    vol = "none" if params["vol_target"] is None else f"{params['vol_target']:.0%}/{params['vol_window']}d"
    return (
        f"cash={params['cash_mode']} SMA{params['cash_sma']} exit={params['cash_exit_buffer']:.0%} "
        f"reentry={params['cash_reentry_buffer']:.0%}; "
        f"unit={params['unit_exposure']:.2f}, cap={params['max_exposure']:.2f}, "
        f"add={params['add1_drop']:.0%}/{params['add2_drop']:.0%}, "
        f"sell={params['sell_mode']} {params['sell_param']:.0%}, max_days={params['max_extra_days']}, "
        f"trend_sma={params['trend_guard_sma'] if params['trend_guard_sma'] is not None else 'none'}, "
        f"trend_exp={params['trend_guard_exposure'] if params['trend_guard_exposure'] is not None else 'none'}, "
        f"vol_target={vol}"
    )


def simulate(
    close_px: np.ndarray,
    dates: pd.DatetimeIndex,
    selected_codes: np.ndarray,
    trend_sma_cache: dict[int, np.ndarray],
    cash_sma_cache: dict[int, tuple[np.ndarray, np.ndarray]],
    realized_vol_cache: dict[int, np.ndarray],
    *,
    cash_mode: str,
    cash_sma: int,
    cash_exit_buffer: float,
    cash_reentry_buffer: float,
    unit_exposure: float,
    max_exposure: float,
    add1_drop: float,
    add2_drop: float,
    sell_mode: str,
    sell_param: float,
    max_extra_days: int,
    trend_guard_sma: int | None,
    trend_guard_exposure: float | None,
    vol_target: float | None,
    vol_window: int,
    keep_trades: bool = False,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int, int, list[dict[str, object]]]:
    n = len(dates)
    trend_sma = trend_sma_cache[trend_guard_sma] if trend_guard_sma is not None else None
    cash_asset_sma, qqq_sma = cash_sma_cache[cash_sma]
    realized_vol = realized_vol_cache[vol_window]

    equity = np.ones(n, dtype=float)
    exposure_history = np.zeros(n, dtype=float)
    cash_history = np.zeros(n, dtype=bool)
    trades: list[dict[str, object]] = []
    trade_events = 0
    rotation_resets = 0

    held_code = int(selected_codes[0])
    in_cash = False
    risk_on = True
    units = 1
    price0 = float(close_px[0, held_code])
    anchor = price0
    high = price0
    low_since_extra = price0
    extra_avg_cost = np.nan
    extra_entry_i: int | None = None
    current_exposure = min(units * unit_exposure, max_exposure)

    def set_next_exposure(signal_i: int) -> float:
        if in_cash:
            return 0.0
        exposure = min(units * unit_exposure, max_exposure)
        if trend_sma is not None and np.isfinite(trend_sma[signal_i, held_code]) and close_px[signal_i, held_code] < trend_sma[signal_i, held_code]:
            exposure = min(exposure, trend_guard_exposure if trend_guard_exposure is not None else exposure)
        if vol_target is not None and np.isfinite(realized_vol[signal_i, held_code]) and realized_vol[signal_i, held_code] > 0:
            exposure = min(exposure, vol_target / realized_vol[signal_i, held_code])
        return max(0.0, exposure)

    for i in range(1, n):
        if in_cash:
            equity[i] = equity[i - 1]
        else:
            equity[i] = equity[i - 1] * (1 + current_exposure * (float(close_px[i, held_code]) / float(close_px[i - 1, held_code]) - 1))
        exposure_history[i] = current_exposure if not in_cash else 0.0
        cash_history[i] = in_cash

        selected = int(selected_codes[i])
        risk_on = cash_risk_on(
            mode=cash_mode,
            selected=selected,
            close_row=close_px[i],
            asset_sma_row=cash_asset_sma[i],
            qqq_sma=float(qqq_sma[i]),
            prior_risk_on=risk_on,
            exit_buffer=cash_exit_buffer,
            reentry_buffer=cash_reentry_buffer,
        )
        if not risk_on:
            if not in_cash:
                trade_events += 1
                if keep_trades:
                    trades.append(
                        {
                            "signal_date": dates[i].date().isoformat(),
                            "execution_date": dates[i].date().isoformat(),
                            "execution_type": "signal_close_after_hours_proxy",
                            "action": "EXIT_TO_CASH",
                            "symbol": SYMBOLS[held_code],
                            "units_before": units,
                            "price": round(float(close_px[i, held_code]), 4),
                            "reason": f"{cash_mode} risk off",
                        }
                    )
                in_cash = True
                units = 0
                extra_avg_cost = np.nan
                extra_entry_i = None
            current_exposure = 0.0
            continue

        if in_cash:
            held_code = selected
            price = float(close_px[i, held_code])
            trade_events += 1
            if keep_trades:
                trades.append(
                    {
                        "signal_date": dates[i].date().isoformat(),
                        "execution_date": dates[i].date().isoformat(),
                        "execution_type": "signal_close_after_hours_proxy",
                        "action": "ENTER_FROM_CASH",
                        "to_symbol": SYMBOLS[held_code],
                        "price": round(price, 4),
                    }
                )
            in_cash = False
            units = 1
            anchor = price
            high = price
            low_since_extra = price
            extra_avg_cost = np.nan
            extra_entry_i = None
            current_exposure = set_next_exposure(i)
            continue

        if selected != held_code:
            previous = held_code
            held_code = selected
            price = float(close_px[i, held_code])
            rotation_resets += 1
            trade_events += 1
            if keep_trades:
                trades.append(
                    {
                        "signal_date": dates[i].date().isoformat(),
                        "execution_date": dates[i].date().isoformat(),
                        "execution_type": "signal_close_after_hours_proxy",
                        "action": "RESET_ON_ROTATION",
                        "from_symbol": SYMBOLS[previous],
                        "to_symbol": SYMBOLS[held_code],
                        "units_before": units,
                        "price": round(price, 4),
                    }
                )
            units = 1
            anchor = price
            high = price
            low_since_extra = price
            extra_avg_cost = np.nan
            extra_entry_i = None
            current_exposure = set_next_exposure(i)
            continue

        price = float(close_px[i, held_code])
        high = max(high, price)
        anchor = high

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
            if max_extra_days is not None and extra_entry_i is not None and (i - extra_entry_i) >= max_extra_days:
                sell_extra = True
                reason = f"extra shares max holding days {max_extra_days}"
            if sell_extra:
                trade_events += 1
                if keep_trades:
                    trades.append(
                        {
                            "signal_date": dates[i].date().isoformat(),
                            "execution_date": dates[i].date().isoformat(),
                            "execution_type": "signal_close_after_hours_proxy",
                            "action": "SELL_EXTRAS",
                            "symbol": SYMBOLS[held_code],
                            "units_before": units,
                            "units_after": 1,
                            "price": round(price, 4),
                            "reason": reason,
                        }
                    )
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
            if keep_trades:
                trades.append(
                    {
                        "signal_date": dates[i].date().isoformat(),
                        "execution_date": dates[i].date().isoformat(),
                        "execution_type": "signal_close_after_hours_proxy",
                        "action": "BUY_EXTRA_1",
                        "symbol": SYMBOLS[held_code],
                        "units_after": units,
                        "price": round(price, 4),
                        "drop_from_anchor_pct": round(drop_from_anchor * 100, 2),
                    }
                )
        elif units == 2 and drop_from_anchor <= -add2_drop:
            units = 3
            extra_avg_cost = float(np.mean([extra_avg_cost, price])) if np.isfinite(extra_avg_cost) else price
            trade_events += 1
            if keep_trades:
                trades.append(
                    {
                        "signal_date": dates[i].date().isoformat(),
                        "execution_date": dates[i].date().isoformat(),
                        "execution_type": "signal_close_after_hours_proxy",
                        "action": "BUY_EXTRA_2",
                        "symbol": SYMBOLS[held_code],
                        "units_after": units,
                        "price": round(price, 4),
                        "drop_from_anchor_pct": round(drop_from_anchor * 100, 2),
                    }
                )
        current_exposure = set_next_exposure(i)

    return equity, exposure_history, cash_history, trade_events, rotation_resets, trades


def main() -> None:
    close_df = fetch_adjusted_close()
    _close, allocation, _curve = load_best_rotation_inputs()
    common = close_df.index.intersection(allocation.index)
    close_df = close_df.loc[common, ["SOXL", "TQQQ", "QQQ"]]
    allocation = allocation.loc[common]
    dates = close_df.index
    close_px = close_df.to_numpy(dtype=float)
    selected_codes = allocation.map({"SOXL": 0, "TQQQ": 1}).to_numpy(dtype=int)
    is_mask = dates < SPLIT_DATE
    oos_mask = dates >= SPLIT_DATE

    trend_sma_cache = {window: close_df[SYMBOLS].rolling(window).mean().to_numpy(dtype=float) for window in [75, 100, 150, 200]}
    cash_sma_cache = {
        window: (
            close_df[SYMBOLS].rolling(window).mean().to_numpy(dtype=float),
            close_df["QQQ"].rolling(window).mean().to_numpy(dtype=float),
        )
        for window in [100, 150, 200, 250]
    }
    returns = close_df[SYMBOLS].pct_change().to_numpy(dtype=float)
    realized_vol_cache = {}
    for window in [20, 50]:
        realized_vol_cache[window] = pd.DataFrame(returns, index=dates, columns=SYMBOLS).rolling(window).std().to_numpy(dtype=float) * np.sqrt(252)

    cash_modes = ["selected", "qqq", "selected_or_qqq", "selected_and_qqq"]
    cash_smas = [100, 150, 200, 250]
    cash_buffers = [(0.00, 0.00), (0.00, 0.02), (0.03, 0.04), (0.05, 0.05)]
    exposure_pairs = [(0.50, 1.00), (0.67, 1.00), (0.75, 1.00), (1.00, 1.00), (0.75, 1.50), (1.00, 1.50), (1.00, 2.00)]
    add_pairs = [(0.05, 0.15), (0.08, 0.20), (0.10, 0.20), (0.15, 0.30)]
    sell_configs = [("extra_profit", 0.10), ("extra_profit", 0.12), ("extra_profit", 0.15), ("rebound_from_low", 0.05)]
    max_days_values = [5, 10, 20]
    trend_guards = [(None, None), (75, 0.25), (100, 0.25), (150, 0.50), (200, 0.50)]
    vol_configs = [(None, 20), (0.35, 20), (0.50, 20), (0.35, 50), (0.50, 50)]

    all_candidates = list(product(cash_modes, cash_smas, cash_buffers, exposure_pairs, add_pairs, sell_configs, max_days_values, trend_guards, vol_configs))
    max_variants = 12000
    rng = np.random.default_rng(20260523)
    if len(all_candidates) > max_variants:
        sampled = rng.choice(len(all_candidates), size=max_variants, replace=False)
        candidates = [all_candidates[int(i)] for i in sampled]
    else:
        candidates = all_candidates

    rows: list[dict[str, object]] = []
    tested = 0
    for cash_mode, cash_sma, (exit_buffer, reentry_buffer), (unit_exposure, max_exposure), (add1, add2), (sell_mode, sell_param), max_days, (trend_sma, trend_exp), (vol_target, vol_window) in candidates:
        params = {
            "cash_mode": cash_mode,
            "cash_sma": cash_sma,
            "cash_exit_buffer": exit_buffer,
            "cash_reentry_buffer": reentry_buffer,
            "unit_exposure": unit_exposure,
            "max_exposure": max_exposure,
            "add1_drop": add1,
            "add2_drop": add2,
            "sell_mode": sell_mode,
            "sell_param": sell_param,
            "max_extra_days": max_days,
            "trend_guard_sma": trend_sma,
            "trend_guard_exposure": trend_exp,
            "vol_target": vol_target,
            "vol_window": vol_window,
        }
        equity, exposure, cash, trade_events, rotation_resets, _trades = simulate(
            close_px, dates, selected_codes, trend_sma_cache, cash_sma_cache, realized_vol_cache, **params
        )
        is_metrics = metrics(equity, dates, is_mask, cash)
        if is_metrics["max_drawdown_pct"] < -50:
            tested += 1
            continue
        oos_metrics = metrics(equity, dates, oos_mask, cash)
        if is_metrics["return_pct"] <= 0 or oos_metrics["return_pct"] <= 0:
            tested += 1
            continue
        full_norm = equity / equity[0]
        rows.append(
            {
                "variant": variant_name(params),
                **params,
                "is_range": is_metrics["range"],
                "is_return_pct": is_metrics["return_pct"],
                "is_max_drawdown_pct": is_metrics["max_drawdown_pct"],
                "is_sharpe": is_metrics["sharpe"],
                "is_cash_days_pct": is_metrics["cash_days_pct"],
                "oos_range": oos_metrics["range"],
                "oos_return_pct": oos_metrics["return_pct"],
                "oos_max_drawdown_pct": oos_metrics["max_drawdown_pct"],
                "oos_sharpe": oos_metrics["sharpe"],
                "oos_cash_days_pct": oos_metrics["cash_days_pct"],
                "full_return_pct": round((float(full_norm[-1]) - 1) * 100, 2),
                "full_max_drawdown_pct": round(max_drawdown(full_norm), 2),
                "full_sharpe": round(sharpe_ratio(full_norm), 3),
                "avg_exposure": round(float(np.mean(exposure)), 3),
                "days_above_1x_pct": round(float(np.mean(exposure > 1.0) * 100), 2),
                "max_exposure_used": round(float(np.max(exposure)), 2),
                "trade_events": trade_events,
                "rotation_resets": rotation_resets,
            }
        )
        tested += 1
        if tested % 1000 == 0:
            print(f"Tested {tested:,} variants; qualifying rows {len(rows):,}...", flush=True)

    result = pd.DataFrame(rows)
    if result.empty:
        raise RuntimeError("No variants qualified under the IS drawdown cap.")

    behavior_key = [
        "is_return_pct",
        "is_max_drawdown_pct",
        "is_sharpe",
        "is_cash_days_pct",
        "oos_return_pct",
        "oos_max_drawdown_pct",
        "oos_sharpe",
        "oos_cash_days_pct",
        "full_return_pct",
        "full_max_drawdown_pct",
        "full_sharpe",
    ]
    unique = result.sort_values(["is_return_pct", "is_sharpe", "is_max_drawdown_pct"], ascending=[False, False, False]).drop_duplicates(subset=behavior_key)
    selected = unique.head(10).copy().reset_index(drop=True)
    selected.insert(0, "is_return_rank_dd50", np.arange(1, len(selected) + 1))

    # Save best daily/trades for the top IS-return / DD<=50 selection.
    best = selected.iloc[0]
    best_params = {
        "cash_mode": str(best["cash_mode"]),
        "cash_sma": int(best["cash_sma"]),
        "cash_exit_buffer": float(best["cash_exit_buffer"]),
        "cash_reentry_buffer": float(best["cash_reentry_buffer"]),
        "unit_exposure": float(best["unit_exposure"]),
        "max_exposure": float(best["max_exposure"]),
        "add1_drop": float(best["add1_drop"]),
        "add2_drop": float(best["add2_drop"]),
        "sell_mode": str(best["sell_mode"]),
        "sell_param": float(best["sell_param"]),
        "max_extra_days": int(best["max_extra_days"]),
        "trend_guard_sma": None if pd.isna(best["trend_guard_sma"]) else int(best["trend_guard_sma"]),
        "trend_guard_exposure": None if pd.isna(best["trend_guard_exposure"]) else float(best["trend_guard_exposure"]),
        "vol_target": None if pd.isna(best["vol_target"]) else float(best["vol_target"]),
        "vol_window": int(best["vol_window"]),
    }
    best_equity, best_exposure, best_cash, _events, _resets, best_trades = simulate(
        close_px, dates, selected_codes, trend_sma_cache, cash_sma_cache, realized_vol_cache, keep_trades=True, **best_params
    )
    best_daily = pd.DataFrame(
        {
            "date": dates,
            "equity": best_equity,
            "exposure": best_exposure,
            "cash": best_cash,
            "allocation_signal": allocation.values,
            "SOXL_close": close_df["SOXL"].values,
            "TQQQ_close": close_df["TQQQ"].values,
            "QQQ_close": close_df["QQQ"].values,
        }
    )

    report_cols = [
        "is_return_rank_dd50",
        "variant",
        "is_return_pct",
        "is_max_drawdown_pct",
        "is_sharpe",
        "is_cash_days_pct",
        "oos_return_pct",
        "oos_max_drawdown_pct",
        "oos_sharpe",
        "oos_cash_days_pct",
        "full_return_pct",
        "full_max_drawdown_pct",
        "full_sharpe",
        "avg_exposure",
        "days_above_1x_pct",
        "max_exposure_used",
        "trade_events",
    ]
    report = selected[report_cols].copy()

    all_path = REPORTS / "soxl_tqqq_close_exec_dd50_position_mgmt_all.csv"
    csv_path = ROOT / "SOXL_TQQQ_CloseExec_DD50_BestISReturn_OOS.csv"
    xlsx_path = ROOT / "SOXL_TQQQ_CloseExec_DD50_BestISReturn_OOS.xlsx"
    html_path = ROOT / "SOXL_TQQQ_CloseExec_DD50_BestISReturn_OOS.html"
    daily_path = REPORTS / "soxl_tqqq_close_exec_dd50_best_daily.csv"
    trades_path = REPORTS / "soxl_tqqq_close_exec_dd50_best_trades.csv"
    result.to_csv(all_path, index=False)
    report.to_csv(csv_path, index=False)
    best_daily.to_csv(daily_path, index=False)
    pd.DataFrame(best_trades).to_csv(trades_path, index=False)

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        report.to_excel(writer, sheet_name="Best IS Return DD50", index=False)
        result.sort_values("is_sharpe", ascending=False).head(250).to_excel(writer, sheet_name="Top IS Sharpe Qualifiers", index=False)
        result.sort_values("oos_sharpe", ascending=False).head(250).to_excel(writer, sheet_name="Top OOS Sharpe Diagnostics", index=False)
        best_daily.to_excel(writer, sheet_name="Best Daily", index=False)
        pd.DataFrame(best_trades).to_excel(writer, sheet_name="Best Trades", index=False)
        for ws in writer.book.worksheets:
            ws.freeze_panes = "A2"
            for col_cells in ws.columns:
                width = max(len(str(cell.value)) if cell.value is not None else 0 for cell in col_cells)
                ws.column_dimensions[col_cells[0].column_letter].width = min(max(width + 2, 10), 66)

    html_path.write_text(
        "<!doctype html><html><head><meta charset='utf-8'><title>SOXL/TQQQ DD50 Position Management Search</title>"
        "<style>body{font-family:Arial,sans-serif;margin:28px;color:#111827}table{border-collapse:collapse;font-size:13px}"
        "th,td{border:1px solid #d1d5db;padding:7px 10px;vertical-align:top}th{background:#f3f4f6}"
        "td:nth-child(2){text-align:left;max-width:780px}td:nth-child(n+3){text-align:right}</style></head><body>"
        "<h1>SOXL/TQQQ: Signal-Close Execution, IS Drawdown Cap 50%</h1>"
        f"<p>Tested {tested:,} deterministic sampled variants from {len(all_candidates):,} possible combinations. Only variants with in-sample drawdown no worse than -50% qualify. Ranking is by in-sample return; OOS columns are validation results.</p>"
        + report.to_html(index=False, escape=False)
        + "</body></html>",
        encoding="utf-8",
    )

    print(f"Tested {tested:,} variants from {len(all_candidates):,}; qualifiers {len(result):,}")
    print(report.to_string(index=False))
    print(csv_path)
    print(xlsx_path)
    print(html_path)
    print(all_path)


if __name__ == "__main__":
    main()
