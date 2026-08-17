from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parent
LATEST = ROOT / "latest_scores.csv"
OUT = ROOT / "entry_analysis.json"


def atr14(high: pd.Series, low: pd.Series, close: pd.Series) -> float:
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs(),
    ], axis=1).max(axis=1)
    return float(tr.ewm(alpha=1 / 14, adjust=False).mean().iloc[-1])


def rsi14(close: pd.Series) -> float:
    d = close.diff()
    up = d.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean()
    dn = (-d.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
    rs = up / dn.replace(0, np.nan)
    return float((100 - 100 / (1 + rs)).iloc[-1])


def adx14(high: pd.Series, low: pd.Series, close: pd.Series) -> float:
    up = high.diff()
    down = -low.diff()
    plus_dm = up.where((up > down) & (up > 0), 0.0)
    minus_dm = down.where((down > up) & (down > 0), 0.0)
    tr = pd.concat([(high-low), (high-close.shift()).abs(), (low-close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1/14, adjust=False).mean()
    plus_di = 100 * plus_dm.ewm(alpha=1/14, adjust=False).mean() / atr
    minus_di = 100 * minus_dm.ewm(alpha=1/14, adjust=False).mean() / atr
    dx = 100 * (plus_di-minus_di).abs() / (plus_di+minus_di).replace(0, np.nan)
    return float(dx.ewm(alpha=1/14, adjust=False).mean().iloc[-1])


def cluster_levels(levels: list[tuple[float, str]], price: float, atr: float) -> list[dict]:
    levels = [(float(v), str(src)) for v, src in levels if np.isfinite(v) and v < price * 0.999]
    levels.sort(key=lambda x: x[0], reverse=True)
    out: list[dict] = []
    min_gap = max(price * 0.012, atr * 0.45)
    for value, src in levels:
        if not out or all(abs(value - x["level"]) >= min_gap for x in out):
            out.append({"level": round(value, 2), "source": src})
        elif out:
            # If two technical references cluster, preserve that confluence in the nearest bucket.
            for x in out:
                if abs(value - x["level"]) < min_gap:
                    if src not in x["source"]:
                        x["source"] += f" + {src}"
                    break
        if len(out) >= 3:
            break
    return out


def analyze(ticker: str, p: pd.DataFrame, buy_score: float, rank: int) -> dict:
    p = p.dropna(how="all").copy()
    close = p["Close"].dropna()
    high = p["High"].reindex(close.index)
    low = p["Low"].reindex(close.index)
    price = float(close.iloc[-1])
    atr = atr14(high, low, close)
    rsi = rsi14(close)
    adx = adx14(high, low, close)

    sma20 = float(close.rolling(20).mean().iloc[-1]) if len(close) >= 20 else np.nan
    sma50 = float(close.rolling(50).mean().iloc[-1]) if len(close) >= 50 else np.nan
    sma200 = float(close.rolling(200).mean().iloc[-1]) if len(close) >= 200 else np.nan
    low20 = float(low.tail(20).min()) if len(low) >= 20 else np.nan
    low60 = float(low.tail(60).min()) if len(low) >= 60 else np.nan

    recent = low.tail(min(100, len(low)))
    local_min = recent[(recent == recent.rolling(5, center=True, min_periods=3).min())]
    swing_levels = [(float(v), "swing low") for v in local_min.tail(8).tolist()]

    window = min(126, len(close))
    six_high = float(high.tail(window).max())
    six_low = float(low.tail(window).min())
    span = six_high - six_low
    fibs = []
    if span > 0:
        for ratio in (0.236, 0.382, 0.50, 0.618):
            fibs.append((six_high - ratio * span, f"6M Fib {ratio:.3f}"))

    levels = [
        (sma20, "20DMA"), (sma50, "50DMA"), (sma200, "200DMA"),
        (low20, "20D low"), (low60, "60D low"),
    ] + swing_levels + fibs
    supports = cluster_levels(levels, price, atr)
    while len(supports) < 3:
        fallback = price - atr * (1.5 + len(supports))
        supports.append({"level": round(fallback, 2), "source": "ATR fallback"})

    s1, s2, s3 = [x["level"] for x in supports[:3]]
    zone_half = max(0.35 * atr, price * 0.004)
    entry_low = max(0, s1 - zone_half)
    entry_high = s1 + zone_half
    deep_low = max(0, s2 - zone_half)
    deep_high = s2 + zone_half

    prior20_high = float(high.iloc[-21:-1].max()) if len(high) >= 21 else float(high.tail(20).max())
    breakout = prior20_high + 0.10 * atr
    stop_ref = max(0, s2 - 0.80 * atr)

    d_atr = (price - s1) / atr if atr > 0 else np.nan
    if d_atr <= 0.55:
        stance = "Near support — starter entry acceptable"
    elif d_atr <= 1.25:
        stance = "Prefer pullback into first support"
    elif rsi >= 68:
        stance = "Extended — avoid chasing; wait for support"
    else:
        stance = "Wait for pullback or confirmed breakout"

    breakout_ok = price >= breakout
    if breakout_ok:
        stance = "Breakout active — prefer retest/hold rather than chase"

    return {
        "rank": int(rank), "ticker": ticker, "buy_now_score": round(float(buy_score), 1),
        "price": round(price, 2), "atr14": round(atr, 2), "rsi14": round(rsi, 1), "adx14": round(adx, 1),
        "sma20": round(sma20, 2) if np.isfinite(sma20) else None,
        "sma50": round(sma50, 2) if np.isfinite(sma50) else None,
        "sma200": round(sma200, 2) if np.isfinite(sma200) else None,
        "supports": supports[:3],
        "entry_zone": [round(entry_low, 2), round(entry_high, 2)],
        "deep_entry_zone": [round(deep_low, 2), round(deep_high, 2)],
        "breakout_trigger": round(breakout, 2),
        "stop_reference": round(stop_ref, 2),
        "stance": stance,
        "distance_to_support_pct": round((price / s1 - 1) * 100, 1) if s1 else None,
        "method": "Support confluence from 20/50/200DMA, 20D/60D lows, recent swing lows, 6M Fibonacci retracements, ATR spacing; entry zones are ±0.35 ATR around support."
    }


def main() -> int:
    latest = pd.read_csv(LATEST).sort_values("buy_now_score", ascending=False).head(3)
    tickers = latest["ticker"].tolist()
    raw = yf.download(tickers, period="18mo", interval="1d", auto_adjust=True, group_by="ticker", threads=True, progress=False)
    results = []
    for rank, (_, row) in enumerate(latest.iterrows(), 1):
        t = row["ticker"]
        if len(tickers) == 1:
            p = raw
        else:
            p = raw[t]
        results.append(analyze(t, p, row["buy_now_score"], rank))
    payload = {"as_of": str(latest["as_of"].iloc[0]), "top3": results}
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
