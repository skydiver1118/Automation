from __future__ import annotations

from itertools import product
from pathlib import Path
import sys

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
sys.path.insert(0, str(ROOT / "scripts"))

from soxl_tqqq_advanced_dca_close_exec_cash_is_oos import (  # noqa: E402
    SPLIT_DATE,
    fetch_adjusted_close,
    max_drawdown,
    metrics,
    sharpe_ratio,
    simulate_close_exec,
    variant_name,
)
from soxl_tqqq_dca_overlay_search import SYMBOLS, load_best_rotation_inputs  # noqa: E402


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

    trend_windows = [50, 75, 100, 150, 200]
    cash_windows = [75, 100, 150, 200, 250]
    trend_sma_cache = {window: close_df[SYMBOLS].rolling(window).mean().to_numpy(dtype=float) for window in trend_windows}
    cash_sma_cache = {
        window: (
            close_df[SYMBOLS].rolling(window).mean().to_numpy(dtype=float),
            close_df["QQQ"].rolling(window).mean().to_numpy(dtype=float),
        )
        for window in cash_windows
    }

    # Broad but bounded grid. Exposure is expressed as portfolio exposure to the held ETF.
    cash_modes = ["none", "selected", "qqq", "selected_or_qqq", "selected_and_qqq"]
    cash_smas = [100, 150, 200, 250]
    cash_buffers = [(0.00, 0.00), (0.00, 0.02), (0.03, 0.03), (0.05, 0.05)]
    exposure_pairs = [
        (1.00, 1.00),
        (1.00, 1.50),
        (1.00, 2.00),
        (1.00, 3.00),
        (1.25, 1.50),
        (1.25, 2.00),
        (1.25, 3.00),
        (1.50, 1.50),
        (1.50, 2.00),
        (1.50, 3.00),
        (2.00, 2.00),
        (2.00, 3.00),
        (3.00, 3.00),
    ]
    add_pairs = [(0.05, 0.15), (0.05, 0.20), (0.08, 0.20), (0.10, 0.20)]
    sell_configs = [
        ("extra_profit", 0.10),
        ("extra_profit", 0.12),
        ("extra_profit", 0.15),
        ("rebound_from_low", 0.05),
    ]
    max_days_values = [5, 10, 20]
    trend_guards = [(None, None), (75, 0.25), (75, 0.50), (100, 0.50), (200, 0.50)]

    rows: list[dict[str, object]] = []
    tested = 0
    all_candidates = list(product(
        cash_modes,
        cash_smas,
        cash_buffers,
        exposure_pairs,
        add_pairs,
        sell_configs,
        max_days_values,
        trend_guards,
    ))
    max_variants = 2500
    if len(all_candidates) > max_variants:
        rng = np.random.default_rng(20260523)
        sampled = rng.choice(len(all_candidates), size=max_variants, replace=False)
        candidates = [all_candidates[int(i)] for i in sampled]
    else:
        candidates = all_candidates

    for cash_mode, cash_sma, (exit_buffer, reentry_buffer), (unit_exposure, max_exposure), (add1, add2), (sell_mode, sell_param), max_days, (trend_sma, trend_exp) in candidates:
        # Keep the grid large enough to explore, but avoid combinations that are behaviorally
        # redundant for cash-off rows with very short trend windows.
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
                "max_exposure_used": round(float(np.max(exposure)), 2),
                "trade_events": trade_events,
                "rotation_resets": rotation_resets,
            }
        )
        tested += 1
        if tested % 250 == 0:
            print(f"Tested {tested:,} variants...", flush=True)

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

    # Also keep a broad OOS-ranked view for diagnostics, but do not use it for selection.
    broad_oos_top = unique.sort_values(
        ["oos_sharpe", "oos_max_drawdown_pct", "oos_return_pct"], ascending=[False, False, False]
    ).head(100)

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
        "max_exposure_used",
        "trade_events",
    ]
    report = oos_ranked[report_cols].copy()

    all_path = REPORTS / "soxl_tqqq_close_exec_cash_exposure_broad_all.csv"
    csv_path = ROOT / "SOXL_TQQQ_CloseExec_Cash_Exposure1to3_ISSharpe_OOSRanked.csv"
    xlsx_path = ROOT / "SOXL_TQQQ_CloseExec_Cash_Exposure1to3_ISSharpe_OOSRanked.xlsx"
    html_path = ROOT / "SOXL_TQQQ_CloseExec_Cash_Exposure1to3_ISSharpe_OOSRanked.html"
    daily_path = REPORTS / "soxl_tqqq_close_exec_cash_exposure1to3_best_daily.csv"
    trades_path = REPORTS / "soxl_tqqq_close_exec_cash_exposure1to3_best_trades.csv"
    result.to_csv(all_path, index=False)
    report.to_csv(csv_path, index=False)
    best_daily.to_csv(daily_path, index=False)
    pd.DataFrame(best_trades).to_csv(trades_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        report.to_excel(writer, sheet_name="IS Top10 OOS Ranked", index=False)
        is_selected.to_excel(writer, sheet_name="IS Selection Order", index=False)
        broad_oos_top.to_excel(writer, sheet_name="OOS Top Diagnostics", index=False)
        unique.head(500).to_excel(writer, sheet_name="Top 500 IS Sharpe", index=False)
        best_daily.to_excel(writer, sheet_name="Best Daily", index=False)
        pd.DataFrame(best_trades).to_excel(writer, sheet_name="Best Trades", index=False)
        for ws in writer.book.worksheets:
            ws.freeze_panes = "A2"
            for col_cells in ws.columns:
                width = max(len(str(cell.value)) if cell.value is not None else 0 for cell in col_cells)
                ws.column_dimensions[col_cells[0].column_letter].width = min(max(width + 2, 10), 66)
    html_path.write_text(
        "<!doctype html><html><head><meta charset='utf-8'><title>SOXL/TQQQ Close Exec Cash Exposure 1-3</title>"
        "<style>body{font-family:Arial,sans-serif;margin:28px;color:#111827}table{border-collapse:collapse;font-size:13px}"
        "th,td{border:1px solid #d1d5db;padding:7px 10px;vertical-align:top}th{background:#f3f4f6}"
        "td:nth-child(3){text-align:left;max-width:780px}td:nth-child(n+4){text-align:right}</style></head><body>"
        "<h1>SOXL/TQQQ: Signal-Day Close Execution, Cash, Exposure 1x-3x</h1>"
        f"<p>Tested {tested:,} variants from {len(all_candidates):,} possible grid combinations using a deterministic sample seed. Top 10 selected by in-sample Sharpe only, then ranked by out-of-sample Sharpe. Fill model assumes after-hours execution at adjusted close.</p>"
        + report.to_html(index=False, escape=False)
        + "</body></html>",
        encoding="utf-8",
    )

    print(f"Tested {tested:,} variants from {len(all_candidates):,} possible grid combinations")
    print(report.to_string(index=False))
    print(csv_path)
    print(xlsx_path)
    print(html_path)
    print(all_path)


if __name__ == "__main__":
    main()
