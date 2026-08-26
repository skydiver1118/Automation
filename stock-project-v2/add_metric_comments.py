from __future__ import annotations

import html
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
LATEST = ROOT / "latest_scores.csv"
STOCKS = ROOT / "dashboard" / "stocks"


def val(row, key):
    try:
        x = float(row.get(key))
        return x if np.isfinite(x) else None
    except Exception:
        return None


def interp(label: str, r: pd.Series):
    rsi, macd, adx = val(r,"rsi14"), val(r,"macd_hist"), val(r,"adx14")
    d20, d50, d200 = val(r,"dist_20dma"), val(r,"dist_50dma"), val(r,"dist_200dma")
    if label == "Price": return "Context","metric-context","Use versus support, moving averages and valuation; price alone is not directional."
    if label == "Market cap": return "Context","metric-context","Size affects risk/liquidity but is not bullish or bearish by itself."
    if label == "RSI 14":
        if rsi is None: return "N/A","metric-context","RSI unavailable."
        if rsi >= 70: return "Overbought / caution","metric-bearish","Momentum is extended; pullback risk is elevated."
        if rsi >= 60: return "Bullish","metric-bullish","Positive momentum without a formal overbought signal."
        if rsi <= 30: return "Oversold / rebound setup","metric-bullish","Potential rebound setup, but price confirmation is required."
        if rsi <= 40: return "Bearish","metric-bearish","Weak momentum and approaching oversold conditions."
        return "Neutral","metric-neutral","Momentum is balanced."
    if label == "MACD histogram":
        if macd is None: return "N/A","metric-context","MACD unavailable."
        return ("Bullish","metric-bullish","Positive histogram indicates improving upside momentum.") if macd > 0 else ("Bearish","metric-bearish","Negative histogram indicates weakening/downside momentum.")
    if label == "ADX 14":
        if adx is None: return "N/A","metric-context","ADX unavailable."
        if adx >= 25:
            if (d20 or 0) > 0 and (macd or 0) > 0: return "Bullish trend","metric-bullish","ADX confirms a strong trend and price/MACD point upward."
            if (d20 or 0) < 0 and (macd or 0) < 0: return "Bearish trend","metric-bearish","ADX confirms a strong trend and price/MACD point downward."
            return "Strong trend","metric-neutral","ADX confirms trend strength, but direction is mixed."
        if adx < 20: return "Neutral","metric-neutral","Weak/range-bound trend; directional signals have lower conviction."
        return "Developing","metric-neutral","Trend strength is developing but not yet strong."
    if label in {"20DMA distance","50DMA distance","200DMA distance"}:
        x={"20DMA distance":d20,"50DMA distance":d50,"200DMA distance":d200}[label]
        if x is None: return "N/A","metric-context","Moving-average distance unavailable."
        if x > .20: return "Bullish / extended","metric-neutral","Above trend support, but >20% extension raises mean-reversion risk."
        if x > 0: return "Bullish","metric-bullish","Price is above this moving average, supporting the uptrend."
        if x < -.10: return "Bearish","metric-bearish","Materially below this moving average; trend is weak."
        return "Cautious","metric-bearish","Below this moving average; trend confirmation is lacking."
    if label in {"1M RS","3M RS","6M RS","12M RS"}:
        k={"1M RS":"rs_1m","3M RS":"rs_3m","6M RS":"rs_6m","12M RS":"rs_12m"}[label]; x=val(r,k)
        if x is None: return "N/A","metric-context","Relative-strength data unavailable."
        if x > .10: return "Bullish","metric-bullish","Strong outperformance versus weighted SMH/QQQ."
        if x > 0: return "Bullish","metric-bullish","Outperforming weighted SMH/QQQ."
        if x < -.10: return "Bearish","metric-bearish","Material underperformance versus weighted SMH/QQQ."
        return "Slightly bearish","metric-bearish","Modest underperformance versus weighted SMH/QQQ."
    if label == "Forward revenue growth":
        x=val(r,"forward_revenue_growth")
        if x is None:return "N/A","metric-context","Estimate unavailable."
        if x>=.20:return "Bullish","metric-bullish","Forward revenue growth ≥20% supports a strong growth profile."
        if x>0:return "Positive","metric-bullish","Forward revenue is expected to grow."
        return "Bearish","metric-bearish","Forward revenue contraction is expected."
    if label == "Forward EPS growth":
        x=val(r,"forward_eps_growth")
        if x is None:return "N/A","metric-context","Estimate unavailable."
        if x>=.20:return "Bullish","metric-bullish","Forward EPS growth ≥20% is a strong earnings-growth signal."
        if x>0:return "Positive","metric-bullish","Forward EPS is expected to grow."
        return "Bearish","metric-bearish","Forward EPS contraction is expected."
    if label == "EPS revision signal":
        x=val(r,"eps_revision_signal")
        if x is None:return "N/A","metric-context","Revision data unavailable."
        if x>=.20:return "Bullish","metric-bullish","Analyst estimate revisions are meaningfully positive."
        if x>0:return "Positive","metric-bullish","More upward than downward revisions."
        if x<=-.20:return "Bearish","metric-bearish","Analyst estimate revisions are meaningfully negative."
        if x<0:return "Negative","metric-bearish","More downward than upward revisions."
        return "Neutral","metric-neutral","No clear revision bias."
    if label == "Forward P/E":
        x=val(r,"forward_pe")
        if x is None or x<=0:return "Context","metric-context","Not economically meaningful; compare with growth and peers."
        if x<20:return "Favorable","metric-bullish","Relatively low forward P/E if estimates are durable."
        if x>50:return "Expensive","metric-bearish","High forward P/E raises valuation risk unless growth is exceptional."
        return "Context","metric-neutral","Mid-range valuation; compare with growth and peers."
    if label == "EV / Sales":
        x=val(r,"ev_sales")
        if x is None or x<0:return "Context","metric-context","Metric unavailable or not meaningful."
        if x<8:return "Favorable","metric-bullish","Relatively moderate sales multiple for a growth company."
        if x>20:return "Expensive","metric-bearish","Very high sales multiple increases valuation sensitivity."
        return "Context","metric-neutral","Interpret versus growth rate and future margins."
    if label == "EV / EBITDA":
        x=val(r,"ev_ebitda")
        if x is None or x<=0:return "Context","metric-context","Unavailable or not meaningful for current profitability."
        if x<20:return "Favorable","metric-bullish","Relatively moderate EBITDA multiple."
        if x>40:return "Expensive","metric-bearish","High EBITDA multiple implies substantial growth expectations."
        return "Context","metric-neutral","Neither clearly cheap nor extreme without peer context."
    if label == "FCF yield":
        x=val(r,"fcf_yield")
        if x is None:return "N/A","metric-context","FCF yield unavailable."
        if x>=.04:return "Bullish","metric-bullish","Healthy free-cash-flow yield provides valuation support."
        if x>0:return "Positive","metric-neutral","Positive free cash flow, though yield is modest."
        return "Bearish","metric-bearish","Negative FCF yield indicates cash burn."
    if label == "FCF margin":
        x=val(r,"fcf_margin")
        if x is None:return "N/A","metric-context","FCF margin unavailable."
        if x>=.15:return "Bullish","metric-bullish","Strong cash conversion / FCF profitability."
        if x>0:return "Positive","metric-neutral","Business is free-cash-flow positive."
        return "Bearish","metric-bearish","Negative FCF margin indicates cash consumption."
    if label == "ROIC proxy":
        x=val(r,"roic_proxy")
        if x is None:return "N/A","metric-context","ROIC proxy unavailable."
        if x>=.15:return "Bullish","metric-bullish","High estimated return on invested capital supports quality."
        if x>=.08:return "Positive","metric-neutral","Acceptable capital efficiency."
        if x<0:return "Bearish","metric-bearish","Negative estimated ROIC indicates poor current capital returns."
        return "Weak","metric-bearish","Low estimated capital efficiency."
    if label == "Gross margin":
        x=val(r,"gross_margin")
        if x is None:return "N/A","metric-context","Gross margin unavailable."
        if x>=.60:return "Bullish","metric-bullish","High gross margin supports pricing power and operating leverage."
        if x>=.35:return "Positive","metric-neutral","Healthy but not exceptional gross margin."
        return "Weak","metric-bearish","Low gross margin can constrain operating leverage."
    if label == "Operating margin":
        x=val(r,"operating_margin")
        if x is None:return "N/A","metric-context","Operating margin unavailable."
        if x>=.20:return "Bullish","metric-bullish","Strong operating profitability."
        if x>0:return "Positive","metric-neutral","Profitable operations with moderate margin."
        return "Bearish","metric-bearish","Negative operating margin indicates current operating losses."
    if label == "Debt / Equity":
        x=val(r,"debt_to_equity")
        if x is None:return "N/A","metric-context","Leverage data unavailable."
        if x<50:return "Favorable","metric-bullish","Lower leverage generally improves financial resilience."
        if x>150:return "Bearish","metric-bearish","High leverage raises balance-sheet/refinancing risk."
        return "Moderate","metric-neutral","Meaningful leverage; interpret with cash flow and liquidity."
    return "Context","metric-context","No standalone bullish/bearish interpretation assigned."


def sentiment_summary(row, labels):
    counts = {"bullish":0,"favorable":0,"bearish":0,"neutral":0,"context":0}
    for label in labels:
        tag, cls, _ = interp(label, row)
        tl = tag.lower()
        if tag == "Favorable": counts["favorable"] += 1
        elif cls == "metric-bullish": counts["bullish"] += 1
        elif cls == "metric-bearish": counts["bearish"] += 1
        elif cls == "metric-neutral": counts["neutral"] += 1
        else: counts["context"] += 1
    positive = counts["bullish"] + counts["favorable"]
    directional = positive + counts["bearish"]
    score = round(100 * positive / directional) if directional else 50
    if score >= 70: overall, css = "Bullish", "metric-bullish"
    elif score >= 55: overall, css = "Moderately bullish", "metric-bullish"
    elif score <= 30: overall, css = "Bearish", "metric-bearish"
    elif score <= 45: overall, css = "Moderately bearish", "metric-bearish"
    else: overall, css = "Mixed / neutral", "metric-neutral"
    return counts, score, overall, css


def main():
    df=pd.read_csv(LATEST).set_index("ticker")
    css="""<style id='metric-comments-css'>.metric-comment{display:block;margin-top:7px;padding-top:7px;border-top:1px solid #1e314b;font-size:11px;line-height:1.35;font-weight:600}.metric-bullish{color:#54d6a6}.metric-bearish{color:#ff8c8c}.metric-neutral{color:#f6c85f}.metric-context{color:#91a4bd}.metric-comment b{font-weight:850}.sentiment-summary{margin:12px 0 16px;padding:14px;background:#0b1423;border:1px solid #29415e;border-radius:12px}.sentiment-head{display:flex;justify-content:space-between;gap:12px;align-items:center;margin-bottom:10px}.sentiment-title{font-weight:850;font-size:15px}.sentiment-overall{font-weight:900;font-size:16px}.sentiment-counts{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:8px}.sentiment-count{padding:9px;border:1px solid #1e314b;border-radius:9px;text-align:center}.sentiment-count small{display:block;color:#91a4bd}.sentiment-count b{font-size:20px}.sentiment-note{margin-top:9px;color:#91a4bd;font-size:11px}@media(max-width:700px){.sentiment-counts{grid-template-columns:repeat(2,1fr)}}</style>"""
    pattern=re.compile(r"(<div class='metric'><small>([^<]+)</small><strong>.*?</strong>)(</div>)",re.S)
    for ticker,row in df.iterrows():
        path=STOCKS/f"{ticker}.html"
        if not path.exists():continue
        page=path.read_text(encoding="utf-8")
        page=re.sub(r"<span class='metric-comment [^']*'><b>.*?</b> — .*?</span>","",page,flags=re.S)
        page=re.sub(r"<div class='sentiment-summary'>.*?</div>\s*</div>\s*</div>","",page,flags=re.S)
        if "metric-comments-css" not in page: page=page.replace("</head>",css+"</head>")
        labels=[]
        for m in pattern.finditer(page): labels.append(html.unescape(m.group(2)).strip())
        counts, score, overall, overall_css = sentiment_summary(row, labels)
        summary=f"""<div class='sentiment-summary'><div class='sentiment-head'><div><div class='sentiment-title'>Diagnostic sentiment summary</div><div class='sub'>Directional count across applicable Raw V2 metrics</div></div><div class='sentiment-overall {overall_css}'>{overall} · {score}% positive</div></div><div class='sentiment-counts'><div class='sentiment-count metric-bullish'><small>Bullish / positive</small><b>{counts['bullish']}</b></div><div class='sentiment-count metric-bullish'><small>Favorable valuation</small><b>{counts['favorable']}</b></div><div class='sentiment-count metric-bearish'><small>Bearish / caution</small><b>{counts['bearish']}</b></div><div class='sentiment-count metric-neutral'><small>Neutral</small><b>{counts['neutral']}</b></div><div class='sentiment-count metric-context'><small>Context / N/A</small><b>{counts['context']}</b></div></div><div class='sentiment-note'>Positive % = (bullish/positive + favorable) ÷ directional signals. Neutral and context-only metrics are excluded from the denominator. This is a diagnostic breadth indicator, not the Buy-Now score.</div></div>"""
        raw_marker="<section class='panel'><div class='panel-head'><div><h2>Raw V2 diagnostics</h2>"
        if raw_marker in page:
            pos=page.find("</div></div>",page.find(raw_marker))
            if pos!=-1: page=page[:pos+12]+summary+page[pos+12:]
        def repl(m):
            label=html.unescape(m.group(2)).strip(); tag,cls,comment=interp(label,row)
            extra=f"<span class='metric-comment {cls}'><b>{html.escape(tag)}</b> — {html.escape(comment)}</span>