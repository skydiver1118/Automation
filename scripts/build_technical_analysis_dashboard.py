from __future__ import annotations

import argparse
import csv
import json
import math
import shutil
from datetime import datetime
from pathlib import Path

from score_tradingagents_watchlist import rows_for_watchlist
from stock_technical_framework import run as run_technical_report


WORKSPACE = Path(__file__).resolve().parents[1]
REPORTS_DIR = WORKSPACE / "reports" / "technical_framework"
DASHBOARD_DIR = WORKSPACE / "technical_analysis_dashboard"
DATA_DIR = DASHBOARD_DIR / "data"
CHART_DIR = DASHBOARD_DIR / "charts"


def as_float(value: object) -> float | None:
    if value in (None, ""):
        return None
    try:
        number = float(str(value).replace(",", ""))
    except ValueError:
        return None
    if not math.isfinite(number):
        return None
    return number


def parse_zone(value: object) -> dict[str, float | None | str]:
    text = str(value or "").strip()
    if "-" not in text:
        return {"text": text, "low": None, "high": None}
    left, right = text.split("-", 1)
    return {
        "text": text,
        "low": as_float(left),
        "high": as_float(right),
    }


def clean_row(row: dict[str, object], chart_path: Path | None, report_path: Path | None) -> dict[str, object]:
    zone = parse_zone(row.get("Entry Zone"))
    markdown = ""
    if report_path and report_path.exists():
        markdown = report_path.read_text(encoding="utf-8")

    copied_chart = ""
    if chart_path and chart_path.exists():
        CHART_DIR.mkdir(parents=True, exist_ok=True)
        target = CHART_DIR / chart_path.name
        shutil.copy2(chart_path, target)
        copied_chart = f"charts/{target.name}"

    return {
        "symbol": row.get("Symbol", ""),
        "watchlistSource": row.get("Watchlist Source", ""),
        "assetType": row.get("Asset Type", ""),
        "note": row.get("Watchlist Note", ""),
        "latestDate": row.get("Latest Date", ""),
        "last": as_float(row.get("Last")),
        "chgPct": as_float(row.get("Chg%")),
        "tradingScore": as_float(row.get("Trading Score")),
        "tradingView": row.get("Trading View", ""),
        "technicalLabel": row.get("Technical Label", ""),
        "investmentScore": as_float(row.get("Investment Score")),
        "investmentView": row.get("Investment View", ""),
        "dashboardTradingScore": as_float(row.get("Dashboard Trading Score")),
        "dashboardNearTermScore": as_float(row.get("Dashboard Near-Term Score")),
        "dashboardFlag": row.get("Dashboard Flag", ""),
        "dashboardRisk": row.get("Dashboard Risk", ""),
        "nextEarnings": row.get("Next Earnings", ""),
        "indicators": {
            "rsi14": as_float(row.get("RSI14")),
            "macd": as_float(row.get("MACD")),
            "macdSignal": as_float(row.get("MACD Signal")),
            "adx14": as_float(row.get("ADX14")),
            "atrPct": as_float(row.get("ATR%")),
            "ema8": as_float(row.get("EMA8")),
            "sma20": as_float(row.get("SMA20")),
            "sma50": as_float(row.get("SMA50")),
            "sma200": as_float(row.get("SMA200")),
        },
        "levels": {
            "nearestSupport": as_float(row.get("Nearest Support")),
            "nearestResistance": as_float(row.get("Nearest Resistance")),
        },
        "entry": {
            "plan": row.get("Entry Plan", ""),
            "zone": zone["text"],
            "zoneLow": zone["low"],
            "zoneHigh": zone["high"],
            "trigger": row.get("Entry Trigger", ""),
            "stop": as_float(row.get("Stop")),
            "target1": as_float(row.get("Target 1")),
            "target2": as_float(row.get("Target 2")),
        },
        "scoreError": row.get("Score Error", ""),
        "investmentNote": row.get("Investment Note", ""),
        "chartPath": copied_chart,
        "reportMarkdown": markdown,
    }


def write_score_csv(rows: list[dict[str, object]], path: Path) -> None:
    if not rows:
        return
    columns: list[str] = []
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def build_payload(rows: list[dict[str, object]], date_text: str, period: str) -> dict[str, object]:
    stocks: list[dict[str, object]] = []
    latest_dates = []

    for row in rows:
        symbol = str(row.get("Symbol", "")).upper().strip()
        chart_path: Path | None = None
        report_path: Path | None = None
        if symbol and row.get("Trading Score"):
            try:
                chart_path, report_path, _score, _label = run_technical_report(
                    ticker=symbol,
                    out_dir=REPORTS_DIR,
                    period=period,
                    chart_months=3,
                )
                if row.get("Latest Date"):
                    latest_dates.append(str(row["Latest Date"]))
            except Exception as exc:
                row["Score Error"] = f"{type(exc).__name__}: {exc}"
        stocks.append(clean_row(row, chart_path, report_path))

    scored = [stock for stock in stocks if stock.get("tradingScore") is not None]
    score_values = [float(stock["tradingScore"]) for stock in scored]
    labels = [str(stock.get("technicalLabel", "")) for stock in scored]
    sorted_scored = sorted(scored, key=lambda stock: (-(stock.get("tradingScore") or -1), stock["symbol"]))

    summary = {
        "watchlistCount": len(stocks),
        "scoredCount": len(scored),
        "failedCount": len(stocks) - len(scored),
        "averageTradingScore": round(sum(score_values) / len(score_values), 1) if score_values else None,
        "bullishCount": labels.count("Bullish"),
        "neutralCount": labels.count("Neutral"),
        "bearishCount": labels.count("Bearish"),
        "topSymbols": [stock["symbol"] for stock in sorted_scored[:8]],
        "latestMarketDate": max(latest_dates) if latest_dates else "",
        "stance": "Technical Watchlist Command Center",
        "dataNote": (
            "Scores use the local technical framework: trend, momentum, volume confirmation, "
            "risk context, support/resistance, and conditional entry zones. Charts are candlestick "
            "daily bars on a trading-session axis, so weekends are skipped."
        ),
    }

    return {
        "generatedAt": datetime.now().astimezone().isoformat(timespec="seconds"),
        "snapshotDate": date_text,
        "sources": {
            "watchlist": str(WORKSPACE / "tradingagents_dashboard" / "watchlist.local.json"),
            "scoreReports": str(REPORTS_DIR),
            "dataBuilder": str(WORKSPACE / "scripts" / "build_technical_analysis_dashboard.py"),
        },
        "summary": summary,
        "stocks": stocks,
    }


def write_dashboard_data(payload: dict[str, object]) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / "dashboard-data.js"
    path.write_text(
        "window.TECHNICAL_ANALYSIS_DASHBOARD_DATA = "
        + json.dumps(payload, indent=2)
        + ";\n",
        encoding="utf-8",
    )
    return path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build the static technical-analysis dashboard data bundle.")
    parser.add_argument("--date", default=datetime.now().date().isoformat(), help="Snapshot date YYYY-MM-DD.")
    parser.add_argument("--period", default="2y", help="yfinance period for indicator warmup.")
    parser.add_argument("--out-dir", default=str(REPORTS_DIR), help="Report/chart output directory.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    global REPORTS_DIR
    REPORTS_DIR = Path(args.out_dir)

    rows = rows_for_watchlist(period=args.period, dashboard_data=WORKSPACE / "tradingagents_dashboard" / "data" / "dashboard-data.js")
    write_score_csv(rows, REPORTS_DIR / f"technical_dashboard_scores_{args.date}.csv")
    payload = build_payload(rows, date_text=args.date, period=args.period)
    data_path = write_dashboard_data(payload)

    print(f"Dashboard data: {data_path}")
    print(f"Watchlist: {payload['summary']['watchlistCount']}")
    print(f"Scored: {payload['summary']['scoredCount']}")
    print(f"Failed: {payload['summary']['failedCount']}")
    print(f"Latest market date: {payload['summary']['latestMarketDate']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
