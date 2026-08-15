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
CONTEXT_SYMBOLS = ["SOXL", "TQQQ", "QQQ"]


def fetch_adjusted_close() -> pd.DataFrame:
    raw = yf.download(
        CONTEXT_SYMBOLS,
        start=START,
        end=END_EXCLUSIVE,
        interval="1d",
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    if raw.empty:
        raise RuntimeError("No yfinance close data returned.")
    close = raw["Close"].copy() if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]].copy()
    close = close[CONTEXT_SYMBOLS].dropna(how="all")
    close.index = pd.to_datetime(close.index).tz_localize(None)
    return close


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


def metrics(equity: np.ndarray, dates: pd.DatetimeIndex, mask: np.ndarray, cash: np.ndarray) -> dict[str, object]:
    sub = equity[mask]
    sub_dates = dates[mask]
    norm = sub / sub[0]
    return {
        "range": f"{sub_dates[0].date()} to {sub_dates[-1].date()}",
        "return_pct": round((float(norm[-1]) - 1) * 100, 2),
        "max_drawdown_pct": round(max_drawdown(norm), 2),
        "sharpe": round(sharpe_ratio(norm), 3),
        "cash_days_pct": round(float(np.mean(cash[mask]) * 100), 2),
    }


def cash_risk_on(
    *,
    mode: str,
    selected: int,
    close_row: np.ndarray,
    asset_sma_row: np.ndarray,
    qqq_sma: float,
    prior_risk_on: bool,
    exit_buffer: float,
    reentry_buffer: float,
) -> bool:
    if mode == "none":
        return True
    selected_exit = np.isfinite(asset_sma_row[selected]) and close_row[selected] < asset_sma_row[selected] * (1 - exit_buffer)
    selected_reentry = np.isfinite(asset_sma_row[selected]) and close_row[selected] >= asset_sma_row[selected] * (1 + reentry_buffer)
    qqq_exit = np.isfinite(qqq_sma) and close_row[2] < qqq_sma * (1 - exit_buffer)
    qqq_reentry = np.isfinite(qqq_sma) and close_row[2] >= qqq_sma * (1 + reentry_buffer)
    if mode == "selected":
        if prior_risk_on:
            return not selected_exit
        return bool(selected_reentry)
    if mode == "qqq":
        if prior_risk_on:
            return not qqq_exit
        return bool(qqq_reentry)
    if mode == "selected_or_qqq":
        if prior_risk_on:
            return not (selected_exit and qqq_exit)
        return bool(selected_reentry or qqq_reentry)
    if mode == "selected_and_qqq":
        if prior_risk_on:
            return not (selected_exit or qqq_exit)
        return bool(selected_reentry and qqq_reentry)
    raise ValueError(f"Unknown cash mode: {mode}")


def variant_name(params: dict[str, object]) -> str:
    return (
        f"cash={params['cash_mode']} SMA{params['cash_sma']} exit={params['cash_exit_buffer']:.0%} "
        f"reentry={params['cash_reentry_buffer']:.0%}; "
        f"unit={params['unit_exposure']:.2f}, cap={params['max_exposure']:.2f}, "
        f"add={params['add1_drop']:.0%}/{params['add2_drop']:.0%}, "
        f"sell={params['sell_mode']} {params['sell_param']:.0%}, max_days={params['max_extra_days']}, "
        f"trend_sma={params['trend_guard_sma'] if params['trend_guard_sma'] is not None else 'none'}, "
        f"trend_exp={params['trend_guard_exposure'] if params['trend_guard_exposure'] is not None else 'none'}"
    )


def simulate_close_exec(
    close_px: np.ndarray,
    dates: pd.DatetimeIndex,
    selected_codes: np.ndarray,
    trend_sma_cache: dict[int, np.ndarray],
    cash_sma_cache: dict[int, tuple[np.ndarray, np.ndarray]],
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
    keep_trades: bool = False,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int, int, list[dict[str, object]]]:
    n = len(dates)
    trend_sma = trend_sma_cache[trend_guard_sma] if trend_guard_sma is not None else None
    cash_asset_sma, qqq_sma = cash_sma_cache[cash_sma]
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
    entry_price = float(close_px[0, held_code])
    anchor = entry_price
    high = entry_price
    low_since_extra = entry_price
    extra_avg_cost = np.nan
    extra_entry_i: int | None = None
    current_exposure = min(units * unit_exposure, max_exposure)

    def set_next_exposure(signal_i: int) -> float:
        if in_cash:
            return 0.0
        exposure = min(units * unit_exposure, max_exposure)
        if trend_sma is not None and np.isfinite(trend_sma[signal_i, held_code]) and close_px[signal_i, held_code] < trend_sma[signal_i, held_code]:
            exposure = min(exposure, trend_guard_exposure if trend_guard_exposure is not None else exposure)
        return exposure

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
        price = float(close_px[i, held_code]) if not in_cash else float(close_px[i, selected])

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
            entry_price = price
            anchor = price
            high = price
            low_since_extra = price
            extra_avg_cost = np.nan
            extra_entry_i = None
            current_exposure = set_next_exposure(i)
            continue

        if selected != held_code:
            previous_symbol = held_code
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
                        "from_symbol": SYMBOLS[previous_symbol],
                        "to_symbol": SYMBOLS[held_code],
                        "units_before": units,
                        "price": round(price, 4),
                    }
                )
            units = 1
            entry_price = price
            anchor = price
            high = price
            low_since_extra = price
            extra_avg_cost = np.nan
            extra_entry_i = None
            current_exposure = set_next_exposure(i)
            continue

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
            else:
                raise ValueError(f"Unknown sell mode: {sell_mode}")
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
    close_df = close_df.loc[common, CONTEXT_SYMBOLS]
    allocation = allocation.loc[common]
    dates = close_df.index
    close_px = close_df.to_numpy(dtype=float)
    selected_codes = allocation.map({"SOXL": 0, "TQQQ": 1}).to_numpy(dtype=int)
    is_mask = dates < SPLIT_DATE
    oos_mask = dates >= SPLIT_DATE
    trend_sma_cache = {window: close_df[SYMBOLS].rolling(window).mean().to_numpy(dtype=float) for window in [75, 100]}
    cash_sma_cache = {
        window: (
            close_df[SYMBOLS].rolling(window).mean().to_numpy(dtype=float),
            close_df["QQQ"].rolling(window).mean().to_numpy(dtype=float),
        )
        for window in [75, 100, 150, 200]
    }

    cash_modes = ["none", "selected", "qqq", "selected_or_qqq", "selected_and_qqq"]
    cash_smas = [75, 100, 150, 200]
    cash_buffers = [(0.00, 0.00), (0.00, 0.02), (0.03, 0.03), (0.05, 0.05)]
    dca_configs = [
        (0.60, 1.00, 0.05, 0.15, "extra_profit", 0.12, 10),
        (0.67, 1.00, 0.05, 0.15, "extra_profit", 0.12, 10),
        (0.75, 1.00, 0.05, 0.15, "extra_profit", 0.12, 10),
        (0.67, 1.50, 0.08, 0.20, "rebound_from_low", 0.05, 10),
        (0.75, 1.50, 0.08, 0.20, "rebound_from_low", 0.05, 10),
    ]
    trend_guards = [(None, None), (75, 0.20), (100, 0.20)]

    rows: list[dict[str, object]] = []
    tested = 0
    for cash_mode, cash_sma, (exit_buffer, reentry_buffer), dca, trend in product(cash_modes, cash_smas, cash_buffers, dca_configs, trend_guards):
        unit_exposure, max_exposure, add1, add2, sell_mode, sell_param, max_days = dca
        trend_sma, trend_exp = trend
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
        }
        equity, exposure, cash, trade_events, rotation_resets, _trades = simulate_close_exec(
            close_px, dates, selected_codes, trend_sma_cache, cash_sma_cache, **params
        )
        is_metrics = metrics(equity, dates, is_mask, cash)
        oos_metrics = metrics(equity, dates, oos_mask, cash)
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
                "trade_events": trade_events,
                "rotation_resets": rotation_resets,
            }
        )
        tested += 1

    result = pd.DataFrame(rows)
    eligible = result[(result["is_return_pct"] > 0) & (result["oos_return_pct"] > 0)].copy()
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
    unique = eligible.sort_values(
        ["is_sharpe", "is_max_drawdown_pct", "is_return_pct"], ascending=[False, False, False]
    ).drop_duplicates(subset=behavior_key)
    is_selected = unique.head(10).copy().reset_index(drop=True)
    is_selected.insert(0, "is_selection_rank", np.arange(1, len(is_selected) + 1))
    oos_ranked = is_selected.sort_values(
        ["oos_sharpe", "oos_max_drawdown_pct", "oos_return_pct"], ascending=[False, False, False]
    ).reset_index(drop=True)
    oos_ranked.insert(0, "oos_sharpe_rank", np.arange(1, len(oos_ranked) + 1))

    best = oos_ranked.iloc[0]
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
    }
    best_equity, best_exposure, best_cash, _events, _resets, best_trades = simulate_close_exec(
        close_px, dates, selected_codes, trend_sma_cache, cash_sma_cache, keep_trades=True, **best_params
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
        "oos_sharpe_rank",
        "is_selection_rank",
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
        "trade_events",
    ]
    report = oos_ranked[report_cols].copy()

    all_path = REPORTS / "soxl_tqqq_advanced_dca_close_exec_cash_all.csv"
    csv_path = ROOT / "SOXL_TQQQ_Advanced_DCA_CloseExec_Cash_IS_Sharpe_Selected_OOS_Ranked.csv"
    xlsx_path = ROOT / "SOXL_TQQQ_Advanced_DCA_CloseExec_Cash_IS_Sharpe_Selected_OOS_Ranked.xlsx"
    html_path = ROOT / "SOXL_TQQQ_Advanced_DCA_CloseExec_Cash_IS_Sharpe_Selected_OOS_Ranked.html"
    daily_path = REPORTS / "soxl_tqqq_advanced_dca_close_exec_cash_best_daily.csv"
    trades_path = REPORTS / "soxl_tqqq_advanced_dca_close_exec_cash_best_trades.csv"
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
        "<!doctype html><html><head><meta charset='utf-8'><title>Advanced DCA Close-Execution IS/OOS</title>"
        "<style>body{font-family:Arial,sans-serif;margin:28px;color:#111827}table{border-collapse:collapse;font-size:13px}"
        "th,td{border:1px solid #d1d5db;padding:7px 10px;vertical-align:top}th{background:#f3f4f6}"
        "td:nth-child(3){text-align:left;max-width:780px}td:nth-child(n+4){text-align:right}</style></head><body>"
        "<h1>Advanced DCA with Cash: Signal-Day Close / After-Hours Proxy</h1>"
        f"<p>Tested {tested:,} variants. Top 10 selected by in-sample Sharpe only, then ranked by out-of-sample Sharpe. Fill model assumes after-hours execution at the same adjusted close.</p>"
        + report.to_html(index=False, escape=False)
        + "</body></html>",
        encoding="utf-8",
    )

    print(f"Tested {tested:,} close-exec variants")
    print(report.to_string(index=False))
    print(csv_path)
    print(xlsx_path)
    print(html_path)
    print(all_path)


if __name__ == "__main__":
    main()
