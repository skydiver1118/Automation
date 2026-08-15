from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
REPORTS = ROOT / "reports"
sys.path.insert(0, str(SCRIPTS))

from soxl_tqqq_dca_advanced_search import apply_advanced_dca  # noqa: E402
from soxl_tqqq_dca_overlay_search import cagr_pct, load_best_rotation_inputs, max_drawdown, sharpe_pct  # noqa: E402


PARAMS = {
    "unit_exposure": 0.67,
    "max_exposure": 2.00,
    "anchor_mode": "rolling_high",
    "add1_drop": 0.10,
    "add2_drop": 0.20,
    "sell_mode": "extra_profit",
    "sell_param": 0.20,
    "max_extra_days": 20,
    "trend_guard_sma": 200,
    "trend_guard_exposure": 0.75,
    "equity_dd_guard": 0.45,
    "equity_dd_guard_exposure": 0.75,
}


def pct_return(series: pd.Series) -> float:
    return (float(series.iloc[-1]) / float(series.iloc[0]) - 1) * 100


def metrics(equity: pd.Series) -> dict[str, float]:
    returns = equity.pct_change().fillna(0).to_numpy(dtype=float)
    values = (equity / equity.iloc[0]).to_numpy(dtype=float)
    return {
        "total_return_pct": round((float(values[-1]) - 1) * 100, 2),
        "cagr_pct": round(cagr_pct(values, equity.index), 2),
        "max_drawdown_pct": round(max_drawdown(values), 2),
        "sharpe": round(sharpe_pct(returns), 2),
    }


def annual_tables(curves: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    return_rows: list[dict[str, object]] = []
    dd_rows: list[dict[str, object]] = []
    value_cols = [column for column in curves.columns if column != "date"]
    curves = curves.sort_values("date").copy()
    curves["year"] = curves["date"].dt.year
    for year, group in curves.groupby("year"):
        period = f"{group['date'].iloc[0].date()} to {group['date'].iloc[-1].date()}"
        ret_row: dict[str, object] = {"Year": int(year), "Period": period}
        dd_row: dict[str, object] = {"Year": int(year), "Period": period}
        for column in value_cols:
            series = group[column].astype(float)
            ret_row[column] = round((series.iloc[-1] / series.iloc[0] - 1) * 100, 2)
            dd_row[column] = round((series / series.cummax() - 1).min() * 100, 2)
        return_rows.append(ret_row)
        dd_rows.append(dd_row)
    return pd.DataFrame(return_rows), pd.DataFrame(dd_rows)


def period_drawdown_details(equity: pd.Series, *, year: int) -> dict[str, object]:
    period = equity[equity.index.year == year].copy()
    running_peak = period.cummax()
    drawdown = period / running_peak - 1
    trough_date = drawdown.idxmin()
    peak_date = period.loc[:trough_date].idxmax()
    return {
        "Year": year,
        "Peak date": peak_date.date().isoformat(),
        "Trough date": trough_date.date().isoformat(),
        "Peak equity": round(float(period.loc[peak_date]), 6),
        "Trough equity": round(float(period.loc[trough_date]), 6),
        "Peak-to-trough drawdown %": round(float(drawdown.loc[trough_date] * 100), 2),
        "Year return %": round((float(period.iloc[-1]) / float(period.iloc[0]) - 1) * 100, 2),
    }


def year_detail_tables(
    *,
    year: int,
    curves: pd.DataFrame,
    trades_df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    year_curves = curves[curves["date"].dt.year == year].copy()
    monthly_rows: list[dict[str, object]] = []
    value_cols = [
        "Verified DCA",
        "Base SOXL/TQQQ rotation",
        "SOXL-only",
        "SOXL buy-hold",
        "TQQQ buy-hold",
    ]
    for month, group in year_curves.groupby(year_curves["date"].dt.to_period("M")):
        row: dict[str, object] = {
            "Month": str(month),
            "Period": f"{group['date'].iloc[0].date()} to {group['date'].iloc[-1].date()}",
            "Average exposure": round(float(group["exposure"].mean()), 3),
            "Max exposure": round(float(group["exposure"].max()), 2),
            "Days exposure > 1x": int((group["exposure"] > 1).sum()),
            "SOXL days": int((group["allocation"] == "SOXL").sum()),
            "TQQQ days": int((group["allocation"] == "TQQQ").sum()),
        }
        for column in value_cols:
            series = group[column].astype(float)
            row[f"{column} return %"] = round((series.iloc[-1] / series.iloc[0] - 1) * 100, 2)
            row[f"{column} max DD %"] = round((series / series.cummax() - 1).min() * 100, 2)
        monthly_rows.append(row)

    trades = trades_df.copy()
    if "date" in trades:
        trades["date"] = pd.to_datetime(trades["date"], errors="coerce")
        year_trades = trades[trades["date"].dt.year == year].copy()
    else:
        year_trades = pd.DataFrame()
    event_counts = (
        year_trades.groupby("action", dropna=False)
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
        if not year_trades.empty
        else pd.DataFrame(columns=["action", "count"])
    )
    allocation_summary = (
        year_curves.groupby("allocation")
        .agg(
            days=("allocation", "size"),
            avg_exposure=("exposure", "mean"),
            max_exposure=("exposure", "max"),
            avg_units=("units", "mean"),
            max_units=("units", "max"),
        )
        .reset_index()
    )
    for column in ["avg_exposure", "max_exposure", "avg_units", "max_units"]:
        allocation_summary[column] = allocation_summary[column].round(3)

    dd_details = pd.DataFrame(
        [
            period_drawdown_details(
                pd.Series(year_curves[column].to_numpy(dtype=float), index=year_curves["date"]),
                year=year,
            )
            | {"Strategy": column}
            for column in value_cols
        ]
    )
    return pd.DataFrame(monthly_rows), event_counts, allocation_summary, dd_details


def autosize_xlsx(path: Path, sheets: dict[str, pd.DataFrame]) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for sheet_name, frame in sheets.items():
            frame.to_excel(writer, sheet_name=sheet_name[:31], index=False)
        workbook = writer.book
        for worksheet in workbook.worksheets:
            worksheet.freeze_panes = "A2"
            for column_cells in worksheet.columns:
                max_len = 0
                column = column_cells[0].column_letter
                for cell in column_cells:
                    value = "" if cell.value is None else str(cell.value)
                    max_len = max(max_len, len(value))
                worksheet.column_dimensions[column].width = min(max(max_len + 2, 10), 54)


def html_table(frame: pd.DataFrame) -> str:
    headers = "".join(f"<th>{column}</th>" for column in frame.columns)
    rows = []
    for _, row in frame.iterrows():
        rows.append("<tr>" + "".join(f"<td>{value}</td>" for value in row.tolist()) + "</tr>")
    return "<table><thead><tr>" + headers + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"


def run() -> None:
    close, allocation, source_curve = load_best_rotation_inputs()
    equity, units, exposure, trades = apply_advanced_dca(close, allocation, **PARAMS)

    verified = equity / equity.iloc[0]
    base_rotation = source_curve["best_rotation_equity"] / source_curve["best_rotation_equity"].iloc[0]
    soxl_only = source_curve["soxl_only_equity"] / source_curve["soxl_only_equity"].iloc[0]
    soxl_buy_hold = source_curve["soxl_buy_hold_equity"] / source_curve["soxl_buy_hold_equity"].iloc[0]
    tqqq_buy_hold = source_curve["tqqq_buy_hold_equity"] / source_curve["tqqq_buy_hold_equity"].iloc[0]

    saved_summary = pd.read_csv(ROOT / "SOXL_TQQQ_DCA_Advanced_Summary.csv")
    saved_row = saved_summary[saved_summary["case"] == "Best return with DD better than SOXL-only"].iloc[0]

    summary = pd.DataFrame(
        [
            {
                "Metric": "Total return %",
                "Saved grid": round(float(saved_row["net_return_pct"]), 2),
                "Recomputed": metrics(verified)["total_return_pct"],
                "Difference": round(metrics(verified)["total_return_pct"] - float(saved_row["net_return_pct"]), 2),
            },
            {
                "Metric": "CAGR %",
                "Saved grid": round(float(saved_row["cagr_pct"]), 2),
                "Recomputed": metrics(verified)["cagr_pct"],
                "Difference": round(metrics(verified)["cagr_pct"] - float(saved_row["cagr_pct"]), 2),
            },
            {
                "Metric": "Max drawdown %",
                "Saved grid": round(float(saved_row["max_drawdown_pct"]), 2),
                "Recomputed": metrics(verified)["max_drawdown_pct"],
                "Difference": round(metrics(verified)["max_drawdown_pct"] - float(saved_row["max_drawdown_pct"]), 2),
            },
            {
                "Metric": "DCA trade events",
                "Saved grid": int(saved_row["dca_trade_events"]),
                "Recomputed": len([t for t in trades if str(t["action"]).startswith(("BUY_EXTRA", "SELL_EXTRAS"))]),
                "Difference": len([t for t in trades if str(t["action"]).startswith(("BUY_EXTRA", "SELL_EXTRAS"))]) - int(saved_row["dca_trade_events"]),
            },
        ]
    )

    parameters = pd.DataFrame([{
        "Parameter": key,
        "Value": value if value is not None else "none",
    } for key, value in PARAMS.items()])

    strategy_compare = pd.DataFrame(
        [
            {"Strategy": "Verified DCA: best return with DD better than SOXL-only", **metrics(verified)},
            {"Strategy": "Base SOXL/TQQQ rotation", **metrics(base_rotation)},
            {"Strategy": "SOXL-only SMA50/SMA63 10% stop", **metrics(soxl_only)},
            {"Strategy": "SOXL buy and hold", **metrics(soxl_buy_hold)},
            {"Strategy": "TQQQ buy and hold", **metrics(tqqq_buy_hold)},
        ]
    )

    curves = pd.DataFrame(
        {
            "date": close.index,
            "Verified DCA": verified.values,
            "Base SOXL/TQQQ rotation": base_rotation.values,
            "SOXL-only": soxl_only.values,
            "SOXL buy-hold": soxl_buy_hold.values,
            "TQQQ buy-hold": tqqq_buy_hold.values,
            "units": units.values,
            "exposure": exposure.values,
            "allocation": allocation.values,
        }
    )
    annual_returns, annual_drawdowns = annual_tables(
        curves[
            [
                "date",
                "Verified DCA",
                "Base SOXL/TQQQ rotation",
                "SOXL-only",
                "SOXL buy-hold",
                "TQQQ buy-hold",
            ]
        ]
    )

    trades_df = pd.DataFrame(trades)
    if trades_df.empty:
        trades_df = pd.DataFrame(columns=["date", "action", "symbol", "price"])

    dca_events = trades_df[trades_df["action"].astype(str).str.startswith(("BUY_EXTRA", "SELL_EXTRAS"), na=False)].copy()

    monthly_2022, event_counts_2022, allocation_2022, drawdown_2022 = year_detail_tables(
        year=2022,
        curves=curves,
        trades_df=trades_df,
    )

    output_xlsx = ROOT / "SOXL_TQQQ_DCA_Verified_Trades_20260522.xlsx"
    output_html = ROOT / "SOXL_TQQQ_DCA_Verified_Trades_20260522.html"
    output_csv = ROOT / "SOXL_TQQQ_DCA_Verified_Annual_Returns_20260522.csv"
    drawdown_csv = ROOT / "SOXL_TQQQ_DCA_Verified_Annual_Drawdowns_20260522.csv"
    trades_csv = ROOT / "SOXL_TQQQ_DCA_Verified_Trade_Details_20260522.csv"
    detail_2022_csv = ROOT / "SOXL_TQQQ_DCA_2022_Detail_20260522.csv"

    sheets = {
        "Summary": summary,
        "Parameters": parameters,
        "Strategy Compare": strategy_compare,
        "Annual Return %": annual_returns,
        "Annual Drawdown %": annual_drawdowns,
        "2022 Monthly Detail": monthly_2022,
        "2022 Event Counts": event_counts_2022,
        "2022 Allocation Exposure": allocation_2022,
        "2022 Drawdown Detail": drawdown_2022,
        "Trade Details": trades_df,
        "DCA Events Only": dca_events,
        "Daily Equity": curves,
    }
    autosize_xlsx(output_xlsx, sheets)
    annual_returns.to_csv(output_csv, index=False)
    annual_drawdowns.to_csv(drawdown_csv, index=False)
    monthly_2022.to_csv(detail_2022_csv, index=False)
    trades_df.to_csv(trades_csv, index=False)

    html = (
        "<!doctype html><html><head><meta charset='utf-8'><title>SOXL/TQQQ DCA Verified Trades</title>"
        "<style>body{font-family:Arial,sans-serif;margin:28px;color:#111827}table{border-collapse:collapse;font-size:13px;margin-bottom:26px}"
        "th,td{border:1px solid #d1d5db;padding:7px 10px;text-align:right;vertical-align:top}th{background:#f3f4f6}"
        "th:nth-child(1),td:nth-child(1),th:nth-child(2),td:nth-child(2){text-align:left}</style></head><body>"
        "<h1>SOXL/TQQQ DCA Verification</h1>"
        "<h2>Verification</h2>"
        + html_table(summary)
        + "<h2>Strategy Comparison</h2>"
        + html_table(strategy_compare)
        + "<h2>Annual Return %</h2>"
        + html_table(annual_returns)
        + "<h2>Annual Max Drawdown %</h2>"
        + html_table(annual_drawdowns)
        + "<h2>2022 Monthly Detail</h2>"
        + html_table(monthly_2022)
        + "<h2>2022 Event Counts</h2>"
        + html_table(event_counts_2022)
        + "<h2>2022 Allocation Exposure</h2>"
        + html_table(allocation_2022)
        + "<h2>2022 Drawdown Detail</h2>"
        + html_table(drawdown_2022)
        + "<h2>DCA Events Only</h2>"
        + html_table(dca_events.head(100))
        + "</body></html>"
    )
    output_html.write_text(html, encoding="utf-8")

    print(output_xlsx)
    print(output_html)
    print(output_csv)
    print(drawdown_csv)
    print(detail_2022_csv)
    print(trades_csv)
    print(summary.to_string(index=False))
    print()
    print(annual_returns.to_string(index=False))
    print()
    print(annual_drawdowns.to_string(index=False))
    print()
    print(monthly_2022.to_string(index=False))
    print()
    print(event_counts_2022.to_string(index=False))
    print()
    print(drawdown_2022.to_string(index=False))


if __name__ == "__main__":
    run()
