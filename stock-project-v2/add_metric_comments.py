from __future__ import annotations

import html
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
LATEST = ROOT / "latest_scores.csv"
STOCKS = ROOT / "dashboard" / "stocks"


def finite(v):
    try:
        x = float(v)
        return x if np.isfinite(x) else None
    except Exception:
        return None


def signal(label: str, row: pd.Series) -> tuple[str, str, str]:
    """Return (classification, css_class, concise interpretation)."""
    rsi = finite(row.get("rsi14"))
    macd = finite(row.get("macd_hist"))
    adx = finite(row.get("adx14"))
    d20 = finite(row.get("dist_20dma"))
    d50 = finite(row.get("dist_50dma"))
    d200 = finite(row.get("dist_200dma"))

    if label == "Price":
        return "Context", "metric-context", "Price itself is not directional; interpret it versus support, moving averages and valuation."
    if label == "Market cap":
        return "Context", "metric-context", "Company size is a risk/liquidity characteristic, not a bullish or bearish signal by itself."
    if label == "RSI 14":
        if rsi is None: return "N/A", "metric-context", "RSI unavailable."
        if rsi >= 70: return "Bearish risk", "metric-bearish", "Overbought; momentum is extended and pullback risk is elevated."
        if rsi >= 60: return "Bullish", "metric-bullish", "Positive momentum without a formal overbought signal."
        if rsi <= 30: return "Bullish setup", "metric-bullish", "Oversold; rebound potential is elevated, but confirmation is needed."
        if rsi <= 40: return "Bearish", "metric-bearish", "Weak momentum; approaching oversold territory."
        return "Neutral", "metric-neutral", "Momentum is balanced."
    if label == "MACD histogram":
        if macd is None: return "N/A", "metric-context", "MACD unavailable."
        return ("Bullish", "metric-bullish", "Positive histogram indicates upside momentum acceleration.") if macd > 0 else ("Bearish", "metric-bearish", "Negative histogram indicates downside momentum / weakening trend.")
    if label == "ADX 14":
        if adx is None: return "N/A", "metric-context", "ADX unavailable."
        if adx >= 25:
            direction = "Bullish trend" if ((d20 or 0) > 0 and (macd or 0) > 0) else "Bearish trend" if ((d20 or 0) < 0 and (macd or 0) < 0) else "Strong trend"
            cls = "metric-bullish" if direction == "Bullish trend" else "metric-bearish" if direction == "Bearish trend" else "metric-neutral"
            return direction, cls, "ADX ≥25 confirms a meaningful trend; direction comes from price/MACD, not ADX itself."
        if adx < 20: return "Neutral", "metric-neutral", "Weak or range-bound trend; directional signals have lower conviction."
        return "Developing", "metric-neutral", "Trend strength is developing but not yet strong."

    if label in {"20DMA distance", "50DMA distance", "200DMA distance"}:
        key = {"20DMA distance": d20, "50DMA distance": d50, "200DMA distance": d200}[label]
        if key is None: return "N/A", "metric-context", "Moving-average distance unavailable."
        if key > 0.20: return "Bullish / extended", "metric-neutral", "Price is above the moving average, but >20% extension increases mean-reversion risk."
        if key > 0: return "Bullish", "metric-bullish", "Price is above this moving average, supporting an uptrend."
        if key < -0.10: return "Bearish", "metric-bearish", "Price is materially below this moving average, indicating trend weakness."
        return "Cautious", "metric-bearish", "Price is below this moving average; trend confirmation is lacking."

    if label in {"1M RS", "3M RS", "6M RS", "12M RS"}:
        col = {"1M RS":"rs_1m", "3M RS":"rs_3m", "6M RS":"rs_6m", "12M RS":"rs_12m"}[label]
        v = finite(row.get(col))
        if v is None: return "N/A", "metric-context", "Relative-strength data unavailable."
        if v > 0.10: return "Bullish", "metric-bullish", "Strong outperformance versus the weighted SMH/QQQ benchmark."
        if v > 0: return "Bullish", "metric-bullish", "Outperforming the weighted SMH/QQQ benchmark."
        if v < -0.10: return "Bearish", "metric-bearish", "Material underperformance versus the weighted SMH/QQQ benchmark."
        return "Slightly bearish", "metric-bearish", "Modest underperformance versus the weighted SMH/QQQ benchmark."

    if label == "Forward revenue growth":
        v = finite(row.get("forward_revenue_growth"))
        if v is None: return "N/A", "metric-context", "Estimate unavailable."
        if v >= .20: return "Bullish", "metric-bullish", "Forward revenue growth ≥20% supports a strong growth profile."
        if v > 0: return "Positive", "metric-bullish", "Forward revenue is expected to grow."
        return "Bearish", "metric-bearish", "Forward revenue contraction is expected."
    if label == "Forward EPS growth":
        v = finite(row.get("forward_eps_growth"))
        if v is None: return "N/A", "metric-context", "Estimate unavailable."
        if v >= .20: return "Bullish", "metric-bullish", "Forward EPS growth ≥20% is a strong earnings-growth signal."
        if v > 0: return "Positive", "metric-bullish", "Forward EPS is expected to grow."
        return "Bearish", "metric-bearish", "Forward EPS contraction is expected."
    if label == "EPS revision signal":
        v = finite(row.get("eps_revision_signal"))
        if v is None: return "N/A", "metric-context", "Revision data unavailable."
        if v >= .20: return "Bullish", "metric-bullish", "Analyst estimate revisions are meaningfully positive."
        if v > 0: return "Positive", "metric-bullish", "More upward than downward estimate revisions."
        if v <= -.20: return "Bearish", "metric-bearish", "Analyst estimate revisions are meaningfully negative."
        if v < 0: return "Negative", "metric-bearish", "More downward than upward estimate revisions."
        return "Neutral", "metric-neutral", "No clear revision bias."

    if label == "Forward P/E":
        v = finite(row.get("forward_pe"))
        if v is None or v <= 0: return "Context", "metric-context", "P/E is unavailable or not economically meaningful; compare with growth and peers."
        if v < 20: return "Favorable", "metric-bullish", "Relatively low forward P/E; favorable if estimates are durable."
        if v > 50: return "Expensive", "metric-bearish", "High forward P/E raises valuation risk unless growth is exceptional."
        return "Context", "metric-neutral", "Mid-range valuation; interpret versus growth, margins and peer multiples."
    if label == "EV / Sales":
        v = finite(row.get("ev_sales"))
        if v is None or v < 0: return "Context", "metric-context", "EV/Sales unavailable or not meaningful."
        if v < 8: return "Favorable", "metric-bullish", "Relatively moderate sales multiple for a growth/technology company."
        if v > 20: return "Expensive", "metric-bearish", "Very high sales multiple increases valuation sensitivity."
        return "Context", "metric-neutral", "Valuation depends heavily on growth rate and future margins."
    if label == "EV / EBITDA":
        v = finite(row.get("ev_ebitda"))
        if v is None or v <= 0: return "Context", "metric-context", "EV/EBITDA unavailable or not meaningful for current profitability."
        if v < 20: return "Favorable", "metric-bullish", "Relatively moderate EBITDA multiple."
        if v > 40: return "Expensive", "metric-bearish", "High EBITDA multiple implies substantial growth expectations."
        return "Context", "metric-neutral", "Valuation is neither clearly cheap nor extreme without peer context."

    if label == "FCF yield":
        v = finite(row.get("fcf_yield"))
        if v is None: return "N/A", "metric-context", "FCF yield unavailable."
        if v >= .04: return "Bullish", "metric-bullish", "Healthy free-cash-flow yield provides valuation support."
        if v > 0: return "Positive", "metric-neutral", "Positive free cash flow, though yield is modest."
        return "Bearish", "metric-bearish", "Negative free-cash-flow yield signals cash burn."
    if label == "FCF margin":
        v = finite(row.get("fcf_margin"))
        if v is None: return "N/A", "metric-context", "FCF margin unavailable."
        if v >= .15: return "Bullish", "metric-bullish", "Strong cash conversion / free-cash-flow profitability."
        if v > 0: return "Positive", "metric-neutral", "Business is free-cash-flow positive."
        return "Bearish", "metric-bearish", "Negative FCF margin indicates cash consumption."
    if label == "ROIC proxy":
        v = finite(row.get("roic_proxy"))
        if v is None: return "N/A", "metric-context", "ROIC proxy unavailable."
        if v >= .15: return "Bullish", "metric-bullish", "High estimated return on invested capital supports quality."
        if v >= .08: return "Positive", "metric-neutral", "Acceptable capital efficiency."
        if v < 0: return "Bearish", "metric-bearish", "Negative estimated ROIC indicates value destruction / early-stage investment burden."
        return "Weak", "metric-bearish", "Low estimated capital efficiency."
    if label == "Gross margin":
        v = finite(row.get("gross_margin"))
        if v is None: return "N/A", "metric-context", "Gross margin unavailable."
        if v >= .60: return "Bullish", "metric-bullish", "High gross margin supports pricing power and operating leverage."
        if v >= .35: return "Positive", "metric-neutral", "Healthy but not exceptional gross margin."
        return "Weak", "metric-bearish", "Low gross margin can constrain operating leverage."
    if label == "Operating margin":
        v = finite(row.get("operating_margin"))
        if v is None: return "N/A", "metric-context", "Operating margin unavailable."
        if v >= .20: return "Bullish", "metric-bullish", "Strong operating profitability."
        if v > 0: return "Positive", "metric-neutral", "Profitable operations, though margin is moderate."
        return "Bearish", "metric-bearish", "Negative operating margin indicates current operating losses."
    if label == "Debt / Equity":
        v = finite(row.get("debt_to_equity"))
        if v is None: return "N/A", "metric-context", "Leverage data unavailable."
        # Yahoo may return this field either as a ratio or percentage-like value; use broad bands.
        if v < 50: return "Favorable", "metric-bullish", "Lower leverage generally improves financial resilience."
        if v > 150: return "Bearish", "metric-bearish", "High leverage increases balance-sheet and refinancing risk."
        return "Moderate", "metric-neutral", "Leverage is meaningful but not automatically excessive; compare with cash flow."

    return "Context", "metric-context", "No standalone bullish/bearish interpretation is assigned."


def main() -> int:
    if not LATEST.exists():
        raise RuntimeError("latest_scores.csv missing")
    df = pd.read_csv(LATEST).set_index("ticker")

    css = """
<style id='metric-comments-css'>
.metric-comment{display:block;margin-top:7px;padding-top:7px;border-top:1px solid #1e314b;font-size:11px;line-height:1.35;font-weight:600}.metric-bullish{color:#54d6a6}.metric-bearish{color:#ff8c8c}.metric-neutral{color:#f6c85f}.metric-context{color:#91a4bd}.metric-comment b{font-weight:850}
</style>
"""

    pattern = re.compile(r"(<div class='metric'><small>([^<]+)</small><strong>.*?</strong>)(</div>)", re.S)

    for ticker, row in df.iterrows():
        path = STOCKS / f"{ticker}.html"
        if not path.exists():
            continue
        page = path.read_text(encoding="utf-8")
        if "id='metric-comments-css'" not in page and 'id="metric-comments-css"' not in page:
            page = page.replace("</head>", css + "</head>")

        def repl(m):
            label = html.unescape(m.group(2)).strip()
            cls_label, css_cls, comment = signal(label, row)
            extra = f"<span class='metric-comment {css_cls}'><b>{html.escape(cls_label)}</b> — {html.escape(comment)}</span>"
            return m.group(1) + extra + m.group(3)

        # Avoid duplicate comments when script is rerun by stripping old spans first.
        page = re.sub(r"<span class='metric-comment [^']*'><b>.*?</b> — .*?</span>", "", page, flags=re.S)
        page = pattern.sub(repl, page)
        path.write_text(page, encoding="utf-8")
        print(f"Added metric comments: {ticker}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
