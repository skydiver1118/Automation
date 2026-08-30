from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

from signal_policy import entry_quality, long_term_rating, short_put_eligible, trend_label

ROOT = Path(__file__).resolve().parent
LATEST = ROOT / "latest_scores.csv"
OUT = ROOT / "canonical_market.json"
DIAG_LABELS = ["Price", "Market cap", "RSI 14", "MACD histogram", "ADX 14", "20DMA distance", "50DMA distance", "200DMA distance", "1M RS", "3M RS", "6M RS", "12M RS", "Forward revenue growth", "Forward EPS growth", "EPS revision signal", "Forward P/E", "EV / Sales", "EV / EBITDA", "FCF yield", "FCF margin", "ROIC proxy", "Gross margin", "Operating margin", "Debt / Equity"]


def finite(v):
    try:
        x = float(v)
        return x if np.isfinite(x) else None
    except Exception:
        return None


def r2(v):
    x = finite(v)
    return round(x, 2) if x is not None else None


def absolute_ma(price, distance):
    p, d = finite(price), finite(distance)
    if p is None or d is None or abs(1 + d) < 1e-9:
        return None
    return p / (1 + d)


def technical_levels(ticker: str, as_of: str) -> dict:
    """Build support/Fibonacci from one canonical daily series, capped at Stock V2 as_of."""
    try:
        h = yf.Ticker(ticker).history(period="18mo", interval="1d", auto_adjust=True, actions=False)
        if h.empty:
            return {}
        h = h[["High", "Low", "Close"]].dropna()
        cutoff = pd.Timestamp(as_of)
        if h.index.tz is not None:
            cutoff = cutoff.tz_localize(h.index.tz)
        h = h[h.index <= cutoff + pd.Timedelta(hours=23, minutes=59)]
        if h.empty:
            return {}
        price = float(h.Close.iloc[-1])
        high, low, close = h.High, h.Low, h.Close
        sma20 = float(close.rolling(20).mean().iloc[-1]) if len(close) >= 20 else None
        sma50 = float(close.rolling(50).mean().iloc[-1]) if len(close) >= 50 else None
        sma200 = float(close.rolling(200).mean().iloc[-1]) if len(close) >= 200 else None
        low20 = float(low.tail(20).min()) if len(low) >= 20 else None
        low60 = float(low.tail(60).min()) if len(low) >= 60 else None
        window = min(126, len(close))
        six_high, six_low = float(high.tail(window).max()), float(low.tail(window).min())
        span = six_high - six_low
        fib = {f"{ratio:.3f}": six_high - ratio * span for ratio in (0.236, 0.382, 0.500, 0.618, 0.786)} if span > 0 else {}

        candidates = []
        for value, source in [(sma20, "20DMA"), (sma50, "50DMA"), (sma200, "200DMA"), (low20, "20D low"), (low60, "60D low")]:
            if value is not None and value < price * 1.002:
                candidates.append((float(value), source))
        for k, value in fib.items():
            if value <= price * 1.002:
                candidates.append((float(value), f"6M Fib {k}"))
        recent = low.tail(min(100, len(low)))
        local_min = recent[recent == recent.rolling(5, center=True, min_periods=3).min()]
        candidates.extend((float(v), "swing low") for v in local_min.tail(8).tolist() if float(v) <= price * 1.002)
        candidates.sort(reverse=True, key=lambda x: x[0])

        clustered = []
        avg_range = float((high - low).tail(14).mean()) if len(h) >= 14 else price * .02
        min_gap = max(price * 0.012, avg_range * .4)
        for value, source in candidates:
            match = next((x for x in clustered if abs(value - x["level"]) < min_gap), None)
            if match:
                if source not in match["source"]:
                    match["source"] += f" + {source}"
            else:
                clustered.append({"level": round(value, 2), "source": source})
            if len(clustered) >= 3:
                break
        return {
            "series_as_of": h.index[-1].date().isoformat(),
            "sma20": r2(sma20), "sma50": r2(sma50), "sma200": r2(sma200),
            "fib_6m": {k: r2(v) for k, v in fib.items()},
            "supports": clustered,
            "key_support": clustered[0]["level"] if clustered else None,
        }
    except Exception as exc:
        print(f"WARN canonical levels {ticker}: {exc}")
        return {}


def sentiment(row: pd.Series) -> dict:
    try:
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
        from add_metric_comments import sentiment_summary
        counts, score, overall, _ = sentiment_summary(row, DIAG_LABELS)
        return {"label": overall, "positive_pct": int(score), "counts": counts}
    except Exception as exc:
        return {"label": "N/A", "positive_pct": None, "error": str(exc)}


def main() -> int:
    df = pd.read_csv(LATEST)
    if df.empty:
        raise RuntimeError("latest_scores.csv is empty")
    as_of = str(df["as_of"].iloc[0])
    stocks = {}
    for _, row in df.iterrows():
        ticker = str(row["ticker"])
        lt_score = finite(row.get("long_term_score"))
        entry_score = finite(row.get("entry_score"))
        if entry_score is None:
            entry_score = finite(row.get("short_term_score"))
        raw_rating = row.get("long_term_rating")
        rating = str(raw_rating) if raw_rating is not None and not pd.isna(raw_rating) else long_term_rating(lt_score)
        raw_quality = row.get("entry_quality")
        quality = str(raw_quality) if raw_quality is not None and not pd.isna(raw_quality) else entry_quality(entry_score)
        levels = technical_levels(ticker, as_of)
        price = finite(row.get("price"))
        s20 = absolute_ma(price, row.get("dist_20dma")) or levels.get("sma20")
        s50 = absolute_ma(price, row.get("dist_50dma")) or levels.get("sma50")
        s200 = absolute_ma(price, row.get("dist_200dma")) or levels.get("sma200")
        levels.update({"sma20": r2(s20), "sma50": r2(s50), "sma200": r2(s200)})
        stocks[ticker] = {
            "ticker": ticker,
            "as_of": as_of,
            "price": r2(price),
            "long_term_score": r2(lt_score),
            "long_term_rating": rating,
            "entry_score": r2(entry_score),
            "entry_quality": quality,
            "composite_score": r2(row.get("buy_now_score")),
            "short_put_eligible": short_put_eligible(rating),
            "technical": {
                "rsi14": r2(row.get("rsi14")),
                "macd": r2(row.get("macd")),
                "macd_signal": r2(row.get("macd_signal")),
                "macd_hist": r2(row.get("macd_hist")),
                "adx14": r2(row.get("adx14")),
                "dist_20dma": finite(row.get("dist_20dma")),
                "dist_50dma": finite(row.get("dist_50dma")),
                "dist_200dma": finite(row.get("dist_200dma")),
                "sma20": r2(s20), "sma50": r2(s50), "sma200": r2(s200),
                "trend": trend_label(price, s20, s50, s200, row.get("macd_hist")),
            },
            "support": {
                "key_support": levels.get("key_support"),
                "supports": levels.get("supports", []),
                "fib_6m": levels.get("fib_6m", {}),
                "series_as_of": levels.get("series_as_of"),
            },
            "diagnostic_sentiment": sentiment(row),
        }

    payload = {
        "schema_version": 1,
        "as_of": as_of,
        "source": "Stock Project V2 canonical daily market/technical layer",
        "policy": {
            "long_term_rating_thresholds": {"STRONG BUY": ">=65", "BUY": "55-64.9", "HOLD": "45-54.9", "AVOID": "<45"},
            "entry_quality_thresholds": {"EXCELLENT": ">=75", "GOOD": "65-74.9", "FAIR": "55-64.9", "WAIT": "<55"},
            "short_put_eligible_ratings": ["BUY", "STRONG BUY"],
        },
        "stocks": stocks,
    }
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Canonical layer written for {len(stocks)} stocks: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
