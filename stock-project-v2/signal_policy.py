from __future__ import annotations

from typing import Any

SHORT_PUT_ELIGIBLE_RATINGS = {"BUY", "STRONG BUY"}


def _score(value: Any) -> float | None:
    try:
        x = float(value)
        return x if x == x else None
    except (TypeError, ValueError):
        return None


def long_term_rating(score: Any) -> str:
    """Absolute ownership rating based on the Stock V2 long-term score."""
    x = _score(score)
    if x is None:
        return "UNRATED"
    if x >= 65:
        return "STRONG BUY"
    if x >= 55:
        return "BUY"
    if x >= 45:
        return "HOLD"
    return "AVOID"


def entry_quality(score: Any) -> str:
    """Equity timing label kept separate from long-term ownership conviction."""
    x = _score(score)
    if x is None:
        return "UNRATED"
    if x >= 75:
        return "EXCELLENT"
    if x >= 65:
        return "GOOD"
    if x >= 55:
        return "FAIR"
    return "WAIT"


def short_put_eligible(rating: Any) -> bool:
    return str(rating or "").strip().upper() in SHORT_PUT_ELIGIBLE_RATINGS


def trend_label(price: Any, sma20: Any, sma50: Any, sma200: Any, macd_hist: Any) -> str:
    vals = [_score(v) for v in (price, sma20, sma50, sma200, macd_hist)]
    p, s20, s50, s200, mh = vals
    if None in (p, s20, s50, s200):
        return "MIXED"
    if p > s20 > s50 > s200 and (mh is None or mh > 0):
        return "STRONG BULLISH"
    if p > s50 > s200:
        return "BULLISH"
    if p < s50 < s200:
        return "BEARISH"
    return "MIXED"
