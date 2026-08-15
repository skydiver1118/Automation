from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from soxl_tqqq_dca_overlay_search import (
    REPORTS,
    ROOT,
    SYMBOLS,
    cagr_pct,
    load_best_rotation_inputs,
    max_drawdown,
    sharpe_pct,
)


def apply_advanced_dca(
    close: pd.DataFrame,
    allocation: pd.Series,
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
) -> tuple[pd.Series, pd.Series, pd.Series, list[dict[str, object]]]:
    symbols = allocation.map({"SOXL": 0, "TQQQ": 1}).to_numpy(dtype=int)
    prices = close[SYMBOLS].to_numpy(dtype=float)
    asset_returns = np.vstack([np.zeros(2), prices[1:] / prices[:-1] - 1])
    sma = None
    if trend_guard_sma is not None:
        sma = close[SYMBOLS].rolling(trend_guard_sma).mean().to_numpy(dtype=float)

    equity = np.ones(len(close), dtype=float)
    units_history = np.ones(len(close), dtype=float)
    exposure_history = np.zeros(len(close), dtype=float)
    trades: list[dict[str, object]] = []

    symbol = int(symbols[0])
    units = 1
    entry_price = float(prices[0, symbol])
    anchor = entry_price
    high = entry_price
    low_since_extra = entry_price
    extra_avg_cost = np.nan
    extra_entry_i: int | None = None
    equity_peak = 1.0

    for i in range(1, len(close)):
        today_symbol = int(symbols[i])
        if today_symbol != symbol:
            trades.append(
                {
                    "date": close.index[i].date().isoformat(),
                    "action": "RESET_ON_ROTATION",
                    "from_symbol": SYMBOLS[symbol],
                    "to_symbol": SYMBOLS[today_symbol],
                    "units_before": units,
                    "price": round(float(prices[i, today_symbol]), 4),
                }
            )
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
        equity[i] = equity[i - 1] * (1 + exposure * float(asset_returns[i, symbol]))
        equity_peak = max(equity_peak, equity[i])

        price = float(prices[i, symbol])
        high = max(high, price)
        if anchor_mode == "rolling_high":
            anchor = high

        if units > 1:
            low_since_extra = min(low_since_extra, price)
            sell_extra = False
            reason = ""
            if sell_mode == "recover_to_anchor":
                sell_extra = price >= anchor * (1 - sell_param)
                reason = f"price >= anchor minus {sell_param:.0%}"
            elif sell_mode == "rebound_from_low":
                sell_extra = price >= low_since_extra * (1 + sell_param)
                reason = f"price rebounded {sell_param:.0%} from DCA low"
            elif sell_mode == "extra_profit":
                sell_extra = bool(np.isfinite(extra_avg_cost)) and price >= extra_avg_cost * (1 + sell_param)
                reason = f"extra shares profit >= {sell_param:.0%}"
            if max_extra_days is not None and extra_entry_i is not None and (i - extra_entry_i) >= max_extra_days:
                sell_extra = True
                reason = f"extra shares max holding days {max_extra_days}"
            if sell_extra:
                trades.append(
                    {
                        "date": close.index[i].date().isoformat(),
                        "action": "SELL_EXTRAS",
                        "symbol": SYMBOLS[symbol],
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
            trades.append(
                {
                    "date": close.index[i].date().isoformat(),
                    "action": "BUY_EXTRA_1",
                    "symbol": SYMBOLS[symbol],
                    "units_after": units,
                    "price": round(price, 4),
                    "drop_from_anchor_pct": round(drop_from_anchor * 100, 2),
                }
            )
        elif units == 2 and drop_from_anchor <= -add2_drop:
            units = 3
            extra_avg_cost = float(np.mean([extra_avg_cost, price])) if np.isfinite(extra_avg_cost) else price
            trades.append(
                {
                    "date": close.index[i].date().isoformat(),
                    "action": "BUY_EXTRA_2",
                    "symbol": SYMBOLS[symbol],
                    "units_after": units,
                    "price": round(price, 4),
                    "drop_from_anchor_pct": round(drop_from_anchor * 100, 2),
                }
            )
        units_history[i] = units

    return (
        pd.Series(equity, index=close.index),
        pd.Series(units_history, index=close.index),
        pd.Series(exposure_history, index=close.index),
        trades,
    )


def metric_row(
    *,
    close: pd.DataFrame,
    equity: pd.Series,
    exposure: pd.Series,
    trades: list[dict[str, object]],
    variant: str,
    base_rotation: pd.Series,
    soxl_only: pd.Series,
    params: dict[str, object],
) -> dict[str, object]:
    values = equity.to_numpy(dtype=float)
    returns = equity.pct_change().fillna(0).to_numpy(dtype=float)
    base = (base_rotation / base_rotation.iloc[0]).to_numpy(dtype=float)
    soxl = (soxl_only / soxl_only.iloc[0]).to_numpy(dtype=float)
    dd = max_drawdown(values)
    cagr = cagr_pct(values, equity.index)
    return {
        "variant": variant,
        **params,
        "net_return_pct": round((float(values[-1]) - 1) * 100, 2),
        "cagr_pct": round(cagr, 2),
        "max_drawdown_pct": round(dd, 2),
        "calmar": round(cagr / abs(dd), 3) if dd != 0 else np.nan,
        "sharpe": round(sharpe_pct(returns), 2),
        "dca_trade_events": len([t for t in trades if str(t["action"]).startswith(("BUY_EXTRA", "SELL_EXTRAS"))]),
        "rotation_resets": len([t for t in trades if t["action"] == "RESET_ON_ROTATION"]),
        "max_exposure_used": round(float(exposure.max()), 2),
        "avg_exposure": round(float(exposure.mean()), 3),
        "days_above_1x_pct": round(float((exposure > 1.0).mean() * 100), 2),
        "base_rotation_return_pct": round((base[-1] - 1) * 100, 2),
        "base_rotation_max_drawdown_pct": round(max_drawdown(base), 2),
        "soxl_only_return_pct": round((soxl[-1] - 1) * 100, 2),
        "soxl_only_max_drawdown_pct": round(max_drawdown(soxl), 2),
        "beats_base_return": bool(values[-1] > base[-1]),
        "reduces_base_drawdown": bool(dd > max_drawdown(base)),
        "beats_soxl_only_return": bool(values[-1] > soxl[-1]),
        "reduces_soxl_only_drawdown": bool(dd > max_drawdown(soxl)),
    }


def markdown_table(frame: pd.DataFrame) -> str:
    headers = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row.tolist()) + " |")
    return "\n".join(lines)


def run() -> None:
    close, allocation, curve = load_best_rotation_inputs()
    base_rotation = curve["best_rotation_equity"]
    soxl_only = curve["soxl_only_equity"]

    unit_exposures = [0.50, 0.67, 0.75, 1.00]
    max_exposures = [1.00, 1.50, 2.00]
    add_pairs = [(0.05, 0.20), (0.05, 0.40), (0.10, 0.20), (0.10, 0.30)]
    sell_configs = [
        ("extra_profit", 0.15),
        ("extra_profit", 0.20),
        ("rebound_from_low", 0.20),
    ]
    max_days_values: list[int | None] = [10, 20]
    guard_configs = [
        (None, None, None, None),
        (100, 1.00, None, None),
        (200, 1.00, None, None),
        (None, None, 0.35, 0.50),
        (None, None, 0.45, 0.75),
        (200, 0.75, 0.45, 0.75),
    ]

    rows: list[dict[str, object]] = []
    curve_store: dict[str, pd.Series] = {}
    exposure_store: dict[str, pd.Series] = {}
    trade_store: dict[str, list[dict[str, object]]] = {}

    for unit_exposure in unit_exposures:
        for max_exposure in max_exposures:
            if max_exposure < unit_exposure:
                continue
            if max_exposure > unit_exposure * 3:
                continue
            for anchor_mode in ["entry", "rolling_high"]:
                for add1, add2 in add_pairs:
                    for sell_mode, sell_param in sell_configs:
                        for max_days in max_days_values:
                            for trend_sma, trend_exposure, dd_guard, dd_exposure in guard_configs:
                                params = {
                                    "unit_exposure": unit_exposure,
                                    "max_exposure": max_exposure,
                                    "anchor_mode": anchor_mode,
                                    "add1_drop_pct": round(add1 * 100, 2),
                                    "add2_drop_pct": round(add2 * 100, 2),
                                    "sell_mode": sell_mode,
                                    "sell_param_pct": round(sell_param * 100, 2),
                                    "max_extra_days": max_days if max_days is not None else "none",
                                    "trend_guard_sma": trend_sma if trend_sma is not None else "none",
                                    "trend_guard_exposure": trend_exposure if trend_exposure is not None else "none",
                                    "equity_dd_guard_pct": round(dd_guard * 100, 2) if dd_guard is not None else "none",
                                    "equity_dd_guard_exposure": dd_exposure if dd_exposure is not None else "none",
                                }
                                variant = (
                                    f"unit={unit_exposure:.2f}, cap={max_exposure:.2f}, anchor={anchor_mode}, "
                                    f"add={add1:.0%}/{add2:.0%}, sell={sell_mode} {sell_param:.0%}, "
                                    f"max_days={params['max_extra_days']}, trend_sma={params['trend_guard_sma']}, "
                                    f"dd_guard={params['equity_dd_guard_pct']}"
                                )
                                equity, _units, exposure, trades = apply_advanced_dca(
                                    close,
                                    allocation,
                                    unit_exposure=unit_exposure,
                                    max_exposure=max_exposure,
                                    anchor_mode=anchor_mode,
                                    add1_drop=add1,
                                    add2_drop=add2,
                                    sell_mode=sell_mode,
                                    sell_param=sell_param,
                                    max_extra_days=max_days,
                                    trend_guard_sma=trend_sma,
                                    trend_guard_exposure=trend_exposure,
                                    equity_dd_guard=dd_guard,
                                    equity_dd_guard_exposure=dd_exposure,
                                )
                                row = metric_row(
                                    close=close,
                                    equity=equity,
                                    exposure=exposure,
                                    trades=trades,
                                    variant=variant,
                                    base_rotation=base_rotation,
                                    soxl_only=soxl_only,
                                    params=params,
                                )
                                rows.append(row)
                                for key, predicate, sort_value in [
                                    ("best_return_under_soxl_dd", row["reduces_soxl_only_drawdown"], row["net_return_pct"]),
                                    ("best_return_under_60dd", row["max_drawdown_pct"] >= -60, row["net_return_pct"]),
                                    ("best_return_under_50dd", row["max_drawdown_pct"] >= -50, row["net_return_pct"]),
                                    ("best_calmar", True, row["calmar"]),
                                ]:
                                    if not predicate:
                                        continue
                                    current = curve_store.get(key)
                                    current_score = getattr(current, "attrs", {}).get("score", -np.inf) if current is not None else -np.inf
                                    if float(sort_value) > float(current_score):
                                        equity.attrs["score"] = float(sort_value)
                                        curve_store[key] = equity
                                        exposure_store[key] = exposure
                                        trade_store[key] = trades

    result = pd.DataFrame(rows)
    result = result.sort_values(["reduces_soxl_only_drawdown", "net_return_pct"], ascending=[False, False]).reset_index(drop=True)
    result.insert(0, "rank_balanced", np.arange(1, len(result) + 1))

    all_path = REPORTS / "soxl_tqqq_dca_advanced_search_all.csv"
    balanced_path = REPORTS / "soxl_tqqq_dca_advanced_balanced.csv"
    report_path = REPORTS / "soxl_tqqq_dca_advanced_report.md"
    curves_path = REPORTS / "soxl_tqqq_dca_advanced_curves.csv"
    exposure_path = REPORTS / "soxl_tqqq_dca_advanced_exposure.csv"
    result.to_csv(all_path, index=False)
    result.head(100).to_csv(balanced_path, index=False)

    summary_rows = []
    categories = [
        ("Best return with DD better than SOXL-only", result[result["reduces_soxl_only_drawdown"]].sort_values("net_return_pct", ascending=False)),
        ("Best return with DD <= 60%", result[result["max_drawdown_pct"] >= -60].sort_values("net_return_pct", ascending=False)),
        ("Best return with DD <= 50%", result[result["max_drawdown_pct"] >= -50].sort_values("net_return_pct", ascending=False)),
        ("Best Calmar", result.sort_values("calmar", ascending=False)),
        ("Best raw return", result.sort_values("net_return_pct", ascending=False)),
    ]
    for label, frame in categories:
        if frame.empty:
            continue
        row = frame.iloc[0].to_dict()
        row["case"] = label
        summary_rows.append(row)
    summary = pd.DataFrame(summary_rows)
    summary_path = ROOT / "SOXL_TQQQ_DCA_Advanced_Summary.csv"
    summary_xlsx = ROOT / "SOXL_TQQQ_DCA_Advanced_Summary.xlsx"
    summary_txt = ROOT / "SOXL_TQQQ_DCA_Advanced_Summary.txt"
    summary_html = ROOT / "SOXL_TQQQ_DCA_Advanced_Summary.html"
    selected_cols = [
        "case",
        "variant",
        "net_return_pct",
        "cagr_pct",
        "max_drawdown_pct",
        "calmar",
        "sharpe",
        "max_exposure_used",
        "avg_exposure",
        "days_above_1x_pct",
        "dca_trade_events",
        "base_rotation_return_pct",
        "base_rotation_max_drawdown_pct",
        "soxl_only_return_pct",
        "soxl_only_max_drawdown_pct",
    ]
    summary[selected_cols].to_csv(summary_path, index=False)
    summary[selected_cols].to_excel(summary_xlsx, index=False)
    summary_txt.write_text(summary[selected_cols].to_string(index=False), encoding="utf-8")

    curves = pd.DataFrame(
        {
            "date": close.index,
            "base_rotation": base_rotation / base_rotation.iloc[0],
            "soxl_only": soxl_only / soxl_only.iloc[0],
        }
    )
    exposures = pd.DataFrame({"date": close.index})
    for key, equity in curve_store.items():
        curves[key] = equity.values
        exposures[key] = exposure_store[key].values
        pd.DataFrame(trade_store[key]).to_csv(REPORTS / f"soxl_tqqq_dca_advanced_{key}_trades.csv", index=False)
    curves.to_csv(curves_path, index=False)
    exposures.to_csv(exposure_path, index=False)

    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(13, 7))
        plot_cols = [
            ("base_rotation", "Base rotation"),
            ("soxl_only", "SOXL-only"),
            ("best_return_under_soxl_dd", "Best return under SOXL-only DD"),
            ("best_return_under_60dd", "Best return DD <= 60%"),
            ("best_return_under_50dd", "Best return DD <= 50%"),
        ]
        for col, label in plot_cols:
            if col in curves:
                ax.plot(pd.to_datetime(curves["date"]), curves[col], label=label, linewidth=2 if col.startswith("best") else 1.4)
        ax.set_yscale("log")
        ax.set_title("Advanced DCA Variants: Return vs Drawdown")
        ax.set_ylabel("Growth of $1, log scale")
        ax.grid(True, which="both", alpha=0.25)
        ax.legend()
        fig.tight_layout()
        fig.savefig(ROOT / "SOXL_TQQQ_DCA_Advanced_Curves.png", dpi=180)
        fig.savefig(REPORTS / "soxl_tqqq_dca_advanced_curves.png", dpi=180)
        plt.close(fig)
    except Exception:
        pass

    def html_table(frame: pd.DataFrame) -> str:
        headers = "".join(f"<th>{column}</th>" for column in frame.columns)
        body = []
        for _, row in frame.iterrows():
            body.append("<tr>" + "".join(f"<td>{value}</td>" for value in row.tolist()) + "</tr>")
        return "<table><thead><tr>" + headers + "</tr></thead><tbody>" + "".join(body) + "</tbody></table>"

    summary_html.write_text(
        "<!doctype html><html><head><meta charset='utf-8'><title>SOXL/TQQQ Advanced DCA Summary</title>"
        "<style>body{font-family:Arial,sans-serif;margin:28px;color:#111827}table{border-collapse:collapse;font-size:13px}"
        "th,td{border:1px solid #d1d5db;padding:7px 10px;text-align:right;vertical-align:top}th{background:#f3f4f6}"
        "th:nth-child(1),td:nth-child(1),th:nth-child(2),td:nth-child(2){text-align:left}td:nth-child(2){max-width:560px}</style></head><body>"
        "<h1>SOXL/TQQQ Advanced DCA Summary</h1>"
        "<p>Expanded DCA search with partial reserve sizing, exposure caps, trend guards, and equity drawdown guards.</p>"
        + html_table(summary[selected_cols])
        + "</body></html>",
        encoding="utf-8",
    )

    lines = [
        "# SOXL/TQQQ Advanced DCA Search",
        "",
        f"Tested {len(result):,} variants with partial reserve sizing, exposure caps, trend guards, and equity drawdown guards.",
        "",
        "## Summary Cases",
        "",
        markdown_table(summary[selected_cols]),
        "",
        "## Files",
        "",
        f"- Full grid: `{all_path}`",
        f"- Top balanced rows: `{balanced_path}`",
        f"- Curves: `{curves_path}`",
        f"- Exposure history: `{exposure_path}`",
        f"- Easy-open summary: `{summary_html}`",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Tested {len(result):,} variants")
    print(summary[selected_cols].to_string(index=False))
    print(summary_html)


if __name__ == "__main__":
    run()
