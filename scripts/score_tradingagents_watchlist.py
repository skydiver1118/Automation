from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from datetime import date
from pathlib import Path

import pandas as pd

WORKSPACE = Path(__file__).resolve().parents[1]
SCRIPTS = WORKSPACE / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_tradingagents_dashboard_data import merged_watchlist_rows
from stock_technical_framework import (
    add_indicators,
    build_entry_plans,
    fetch_daily_data,
    score_setup,
    support_resistance,
)


DEFAULT_OUT_DIR = WORKSPACE / "reports" / "technical_framework"
DEFAULT_DASHBOARD_DATA = WORKSPACE / "tradingagents_dashboard" / "data" / "dashboard-data.js"


def load_dashboard_scores(path: Path) -> dict[str, dict[str, object]]:
    if not path.exists():
        return {}

    text = path.read_text(encoding="utf-8")
    if "=" not in text:
        return {}
    payload = text.split("=", 1)[1].strip()
    if payload.endswith(";"):
        payload = payload[:-1].strip()

    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return {}

    scores: dict[str, dict[str, object]] = {}
    for stock in data.get("stocks", []):
        symbol = str(stock.get("symbol", "")).upper().strip()
        if not symbol:
            continue
        scores[symbol] = {
            "dashboard_trading": (stock.get("scores") or {}).get("trading"),
            "dashboard_investment": (stock.get("scores") or {}).get("investment"),
            "dashboard_near_term": (stock.get("scores") or {}).get("nearTerm"),
            "flag": stock.get("flag", ""),
            "risk": stock.get("risk", ""),
            "next_earnings": stock.get("nextEarningsDate", ""),
            "decision": stock.get("decision", ""),
            "source": stock.get("source", ""),
        }
    return scores


def fmt(value: object, decimals: int = 2) -> str:
    try:
        num = float(value)
    except (TypeError, ValueError):
        return ""
    if not math.isfinite(num):
        return ""
    return f"{num:.{decimals}f}"


def trading_view(label: str, score: int) -> str:
    if label == "Bullish" and score >= 85:
        return "Strong trade"
    if label == "Bullish":
        return "Trade candidate"
    if label == "Neutral" and score >= 65:
        return "Watch / constructive"
    if label == "Neutral":
        return "Weak / neutral"
    return "Avoid short-term"


def investment_view(score: object) -> str:
    try:
        value = float(score)
    except (TypeError, ValueError):
        return ""
    if value >= 85:
        return "Strong long-term buy"
    if value >= 70:
        return "Buy / accumulate"
    if value >= 55:
        return "Hold / watch"
    if value >= 40:
        return "Speculative / avoid new"
    return "Avoid long-term"


def score_symbol(symbol: str, period: str) -> dict[str, object]:
    df = add_indicators(fetch_daily_data(symbol, period))
    ready = df.dropna()
    if len(ready) < 30:
        raise RuntimeError(f"Only {len(ready)} indicator-ready rows")

    score, label, _score_df = score_setup(df)
    supports, resistances = support_resistance(df)
    entries = build_entry_plans(df, supports, resistances, label)
    latest = ready.iloc[-1]
    first_entry = entries[0] if entries else None

    return {
        "latest_date": df.index[-1].date().isoformat(),
        "last": float(latest["Close"]),
        "chg_pct": float(latest["Close"] / ready["Close"].iloc[-2] - 1) * 100,
        "technical_score": score,
        "technical_label": label,
        "trading_view": trading_view(label, score),
        "rsi14": float(latest["RSI14"]),
        "macd": float(latest["MACD"]),
        "macd_signal": float(latest["MACDSignal"]),
        "adx14": float(latest["ADX14"]),
        "atr_pct": float(latest["ATR14"] / latest["Close"] * 100),
        "ema8": float(latest["EMA8"]),
        "sma20": float(latest["SMA20"]),
        "sma50": float(latest["SMA50"]),
        "sma200": float(latest["SMA200"]),
        "support": supports[-1] if supports else "",
        "resistance": resistances[0] if resistances else "",
        "entry_plan": first_entry.name if first_entry else "",
        "entry_zone": (
            f"{first_entry.zone_low:.2f}-{first_entry.zone_high:.2f}"
            if first_entry
            else ""
        ),
        "entry_trigger": first_entry.trigger if first_entry else "",
        "stop": first_entry.stop if first_entry else "",
        "target_1": first_entry.target_1 if first_entry else "",
        "target_2": first_entry.target_2 if first_entry else "",
    }


def rows_for_watchlist(period: str, dashboard_data: Path) -> list[dict[str, object]]:
    dashboard_scores = load_dashboard_scores(dashboard_data)
    rows: list[dict[str, object]] = []
    for source_row in merged_watchlist_rows():
        symbol = str(source_row.get("Symbol", "")).upper().strip()
        if not symbol:
            continue

        dashboard = dashboard_scores.get(symbol, {})
        row: dict[str, object] = {
            "Symbol": symbol,
            "Watchlist Source": source_row.get("Source", ""),
            "Asset Type": source_row.get("Asset Type", ""),
            "Watchlist Note": source_row.get("Note", ""),
            "Dashboard Trading Score": fmt(dashboard.get("dashboard_trading"), 1),
            "Dashboard Near-Term Score": fmt(dashboard.get("dashboard_near_term"), 1),
            "Dashboard Flag": dashboard.get("flag", ""),
            "Dashboard Risk": dashboard.get("risk", ""),
            "Next Earnings": dashboard.get("next_earnings", ""),
        }

        try:
            scored = score_symbol(symbol, period)
            row.update(
                {
                    "Latest Date": scored["latest_date"],
                    "Last": fmt(scored["last"], 4),
                    "Chg%": fmt(scored["chg_pct"], 2),
                    "Trading Score": fmt(scored["technical_score"], 1),
                    "Trading View": scored["trading_view"],
                    "Technical Label": scored["technical_label"],
                    "RSI14": fmt(scored["rsi14"], 1),
                    "MACD": fmt(scored["macd"], 2),
                    "MACD Signal": fmt(scored["macd_signal"], 2),
                    "ADX14": fmt(scored["adx14"], 1),
                    "ATR%": fmt(scored["atr_pct"], 2),
                    "EMA8": fmt(scored["ema8"], 2),
                    "SMA20": fmt(scored["sma20"], 2),
                    "SMA50": fmt(scored["sma50"], 2),
                    "SMA200": fmt(scored["sma200"], 2),
                    "Nearest Support": fmt(scored["support"], 2),
                    "Nearest Resistance": fmt(scored["resistance"], 2),
                    "Entry Plan": scored["entry_plan"],
                    "Entry Zone": scored["entry_zone"],
                    "Entry Trigger": scored["entry_trigger"],
                    "Stop": fmt(scored["stop"], 2),
                    "Target 1": fmt(scored["target_1"], 2),
                    "Target 2": fmt(scored["target_2"], 2),
                    "Score Error": "",
                }
            )
        except Exception as exc:
            row.update(
                {
                    "Latest Date": "",
                    "Last": "",
                    "Chg%": "",
                    "Trading Score": "",
                    "Trading View": "",
                    "Technical Label": "",
                    "RSI14": "",
                    "MACD": "",
                    "MACD Signal": "",
                    "ADX14": "",
                    "ATR%": "",
                    "EMA8": "",
                    "SMA20": "",
                    "SMA50": "",
                    "SMA200": "",
                    "Nearest Support": "",
                    "Nearest Resistance": "",
                    "Entry Plan": "",
                    "Entry Zone": "",
                    "Entry Trigger": "",
                    "Stop": "",
                    "Target 1": "",
                    "Target 2": "",
                    "Score Error": f"{type(exc).__name__}: {exc}",
                }
            )

        investment_score = dashboard.get("dashboard_investment")
        row["Investment Score"] = fmt(investment_score, 1)
        row["Investment View"] = investment_view(investment_score)
        row["Investment Note"] = str(dashboard.get("decision", ""))[:500]
        rows.append(row)

    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    columns = [
        "Symbol",
        "Watchlist Source",
        "Asset Type",
        "Latest Date",
        "Last",
        "Chg%",
        "Trading Score",
        "Trading View",
        "Technical Label",
        "Investment Score",
        "Investment View",
        "Dashboard Trading Score",
        "Dashboard Near-Term Score",
        "Dashboard Flag",
        "Dashboard Risk",
        "Next Earnings",
        "RSI14",
        "MACD",
        "MACD Signal",
        "ADX14",
        "ATR%",
        "EMA8",
        "SMA20",
        "SMA50",
        "SMA200",
        "Nearest Support",
        "Nearest Resistance",
        "Entry Plan",
        "Entry Zone",
        "Entry Trigger",
        "Stop",
        "Target 1",
        "Target 2",
        "Score Error",
        "Watchlist Note",
        "Investment Note",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score the merged TradingAgents automation watchlist.")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Output directory.")
    parser.add_argument("--date", default=date.today().isoformat(), help="Snapshot date YYYY-MM-DD.")
    parser.add_argument("--period", default="2y", help="yfinance period for indicator warmup.")
    parser.add_argument(
        "--dashboard-data",
        default=str(DEFAULT_DASHBOARD_DATA),
        help="Generated TradingAgents dashboard data JS file.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    out_dir = Path(args.out_dir)
    rows = rows_for_watchlist(args.period, Path(args.dashboard_data))
    output = out_dir / f"tradingagents_watchlist_scores_raw_{args.date}.csv"
    write_csv(output, rows)
    scored = sum(1 for row in rows if row.get("Trading Score"))
    failed = len(rows) - scored
    print(f"Watchlist symbols: {len(rows)}")
    print(f"Scored symbols: {scored}")
    print(f"Failed symbols: {failed}")
    print(f"Raw score CSV: {output}")

    ranked = sorted(
        [row for row in rows if row.get("Trading Score")],
        key=lambda row: float(row["Trading Score"]),
        reverse=True,
    )
    print("Top scored symbols:")
    for row in ranked[:10]:
        print(
            f"{row['Symbol']}: {row['Trading Score']} {row['Technical Label']} "
            f"entry={row['Entry Zone']} last={row['Last']}"
        )


if __name__ == "__main__":
    main()
