from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from add_metric_comments import interp, sentiment_summary

ROOT = Path(__file__).resolve().parent
HISTORY = ROOT / "history"
OUT = ROOT / "sentiment_history.csv"
TRANSITIONS = ROOT / "sentiment_transitions.json"

LABELS = [
    "Price", "Market cap", "RSI 14", "MACD histogram", "ADX 14",
    "20DMA distance", "50DMA distance", "200DMA distance",
    "1M RS", "3M RS", "6M RS", "12M RS",
    "Forward revenue growth", "Forward EPS growth", "EPS revision signal",
    "Forward P/E", "EV / Sales", "EV / EBITDA", "FCF yield", "FCF margin",
    "ROIC proxy", "Gross margin", "Operating margin", "Debt / Equity",
]


def regime(score: float) -> str:
    if score >= 70: return "Bullish"
    if score >= 55: return "Moderately bullish"
    if score <= 30: return "Bearish"
    if score <= 45: return "Moderately bearish"
    return "Mixed / neutral"


def polarity(reg: str) -> str:
    if "bullish" in reg.lower(): return "bullish"
    if "bearish" in reg.lower(): return "bearish"
    return "neutral"


def main():
    rows = []
    for path in sorted(HISTORY.glob("*.csv")):
        try:
            df = pd.read_csv(path)
        except Exception:
            continue
        date = path.stem
        for _, row in df.iterrows():
            ticker = str(row.get("ticker", "")).strip()
            if not ticker: continue
            counts, score, overall, _ = sentiment_summary(row, LABELS)
            rows.append({
                "date": date, "ticker": ticker, "sentiment_score": score,
                "regime": overall, "polarity": polarity(overall),
                "bullish": counts["bullish"], "favorable": counts["favorable"],
                "bearish": counts["bearish"], "neutral": counts["neutral"],
                "context": counts["context"],
            })
    hist = pd.DataFrame(rows)
    if hist.empty:
        OUT.write_text("date,ticker,sentiment_score,regime,polarity,bullish,favorable,bearish,neutral,context\n")
        TRANSITIONS.write_text(json.dumps({"latest_date": None, "transitions": []}, indent=2))
        return
    hist = hist.sort_values(["ticker", "date"])
    hist.to_csv(OUT, index=False)
    events = []
    for ticker, g in hist.groupby("ticker"):
        g = g.sort_values("date").reset_index(drop=True)
        for i in range(1, len(g)):
            prev, cur = g.iloc[i-1], g.iloc[i]
            if prev.polarity != cur.polarity:
                events.append({
                    "ticker": ticker, "date": cur.date, "previous_date": prev.date,
                    "from": prev.regime, "to": cur.regime,
                    "from_score": int(prev.sentiment_score), "to_score": int(cur.sentiment_score),
                    "direction": f"{prev.polarity}_to_{cur.polarity}",
                })
    latest = str(hist.date.max())
    latest_events = [e for e in events if e["date"] == latest]
    TRANSITIONS.write_text(json.dumps({"latest_date": latest, "transitions": latest_events, "all_transition_count": len(events)}, indent=2))
    print(f"Sentiment history: {len(hist)} records; latest transitions: {len(latest_events)}")
    for e in latest_events:
        print(f"{e['ticker']}: {e['from']} ({e['from_score']}%) -> {e['to']} ({e['to_score']}%)")


if __name__ == "__main__":
    main()
