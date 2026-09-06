from __future__ import annotations

import csv
import html
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
DASH = ROOT / "dashboard" / "index.html"
STOCKS_DIR = ROOT / "dashboard" / "stocks"
ENTRY = ROOT / "entry_analysis.json"
LATEST = ROOT / "latest_scores.csv"
TZ = ZoneInfo("America/New_York")


def money(v):
    return f"${float(v):,.2f}" if v is not None else "—"


def rsi_condition(v):
    try:
        rsi = float(v)
    except Exception:
        return "RSI unavailable", "neutral", "No RSI classification available."
    if rsi >= 70:
        return "Overbought", "overbought", f"RSI {rsi:.1f} ≥ 70: momentum is extended; pullback risk is elevated."
    if rsi <= 30:
        return "Oversold", "oversold", f"RSI {rsi:.1f} ≤ 30: selling is extended; rebound potential is elevated."
    if rsi >= 65:
        return "Near overbought", "near-overbought", f"RSI {rsi:.1f}: approaching the standard 70 overbought threshold."
    if rsi <= 35:
        return "Near oversold", "near-oversold", f"RSI {rsi:.1f}: approaching the standard 30 oversold threshold."
    return "Neutral", "neutral", f"RSI {rsi:.1f}: neither overbought nor oversold by standard RSI thresholds."


def load_latest():
    out = {}
    if not LATEST.exists():
        return out
    with LATEST.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row.get("ticker", "")] = row
    return out


def add_report_metadata(page: str, created_text: str) -> str:
    # Main dashboard: append report creation timestamp in the existing top-right stamp.
    marker = "Latest trading session<br><b>"
    if marker in page and "Report created" not in page:
        page = page.replace(
            marker,
            "Latest trading session<br><b>",
            1,
        )
        close = "</b></div></div>"
        if close in page:
            page = page.replace(close, f"</b><br><span class='report-created'>Report created<br><b>{html.escape(created_text)}</b></span></div></div>", 1)
    return page


def enhance_stock_pages(latest, created_text):
    if not STOCKS_DIR.exists():
        return
    css = """
<style id='market-condition-css'>
.report-created{display:inline-block;margin-top:8px;color:#8fa4bf;font-size:11px;line-height:1.35}.condition-panel{display:flex;justify-content:space-between;gap:16px;align-items:center;background:#0d192a;border:1px solid #28415f;border-radius:13px;padding:13px 15px;margin:0 0 16px}.condition-panel .condition-copy{color:#9fb2c9}.condition-pill{display:inline-flex;align-items:center;padding:7px 11px;border-radius:999px;font-weight:850;white-space:nowrap}.condition-pill.overbought{background:#3a1820;color:#ff9ba7;border:1px solid #6a2836}.condition-pill.oversold{background:#123328;color:#77e7b4;border:1px solid #245e49}.condition-pill.near-overbought{background:#3a2d13;color:#ffd27a;border:1px solid #6d5221}.condition-pill.near-oversold{background:#173044;color:#8ed6ff;border:1px solid #2d5874}.condition-pill.neutral{background:#17263b;color:#b9c9dc;border:1px solid #2d4668}@media(max-width:700px){.condition-panel{align-items:flex-start;flex-direction:column}}
</style>
"""
    for ticker, row in latest.items():
        path = STOCKS_DIR / f"{ticker}.html"
        if not path.exists():
            continue
        page = path.read_text(encoding="utf-8")
        if "id='market-condition-css'" not in page and 'id="market-condition-css"' not in page:
            page = page.replace("</head>", css + "</head>")
        label, cls, explanation = rsi_condition(row.get("rsi14"))
        block = f"""
<section class='condition-panel'>
  <div><div class='eyebrow'>Market condition</div><div class='condition-copy'>{html.escape(explanation)}</div><div class='report-created'>Report created: <b>{html.escape(created_text)}</b></div></div>
  <span class='condition-pill {cls}'>{html.escape(label)}</span>
</section>
"""
        if "Market condition" not in page:
            marker = "<div class='grid kpis'>"
            if marker in page:
                page = page.replace(marker, block + marker, 1)
            else:
                page = page.replace("<section class='panel'>", block + "<section class='panel'>", 1)
        path.write_text(page, encoding="utf-8")


def main() -> int:
    if not DASH.exists() or not ENTRY.exists():
        raise RuntimeError("Dashboard or entry analysis missing")

    now = datetime.now(TZ)
    created_text = now.strftime("%A, %b %d, %Y · %I:%M %p %Z").replace(" 0", " ")
    page = DASH.read_text(encoding="utf-8")
    if 'content="investment-v3"' in page:
        enhance_stock_pages(load_latest(), created_text)
        print("Investment overview already contains entry cards; detail pages enhanced.")
        return 0
    data = json.loads(ENTRY.read_text(encoding="utf-8"))

    cards = []
    for x in data.get("top3", []):
        supports = x.get("supports", [])
        srows = "".join(
            f"<div class='entry-support'><span>S{i}</span><b>{money(s.get('level'))}</b><small>{html.escape(str(s.get('source','')))}</small></div>"
            for i, s in enumerate(supports, 1)
        )
        ez = x.get("entry_zone", [None, None])
        dz = x.get("deep_entry_zone", [None, None])
        cards.append(f"""
<a class='entry-card' href='stocks/{html.escape(x['ticker'])}.html'>
  <div class='entry-head'>
    <div><span class='entry-rank'>#{x['rank']} BUY-NOW</span><h3>{html.escape(x['ticker'])}</h3></div>
    <div class='entry-score'>{x['buy_now_score']:.1f}</div>
  </div>
  <div class='entry-price'>Price <b>{money(x['price'])}</b> · RSI {x['rsi14']:.1f} · ADX {x['adx14']:.1f}</div>
  <div class='entry-stance'>{html.escape(x['stance'])}</div>
  <div class='entry-zones'>
    <div><small>Preferred entry zone</small><b>{money(ez[0])} – {money(ez[1])}</b></div>
    <div><small>Deeper entry zone</small><b>{money(dz[0])} – {money(dz[1])}</b></div>
  </div>
  <div class='entry-supports'>{srows}</div>
  <div class='entry-foot'><span>Breakout trigger <b>{money(x['breakout_trigger'])}</b></span><span>Risk/stop reference <b>{money(x['stop_reference'])}</b></span></div>
</a>""")

    block = f"""
<section class='panel entry-panel'>
  <div class='panel-head'><div><h2>Top 3 Buy-Now: Entry & Support Map</h2><div class='sub'>Updated from the latest completed session ({html.escape(str(data.get('as_of','')))}). Support is calculated from moving averages, swing lows, Fibonacci retracements and ATR. Click a stock for full analysis.</div></div></div>
  <div class='entry-grid'>{''.join(cards)}</div>
</section>
"""

    css = """
<style id='entry-support-css'>
.entry-panel{border-color:#2d4668}.entry-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.entry-card{display:block;background:linear-gradient(180deg,#12243b,#0d192a);border:1px solid #294766;border-radius:14px;padding:16px;transition:.18s ease}.entry-card:hover{transform:translateY(-2px);border-color:#5b87b7}.entry-head{display:flex;justify-content:space-between;align-items:start}.entry-head h3{font-size:25px;margin:2px 0 0}.entry-rank{font-size:10px;letter-spacing:.12em;color:#65a7ff;font-weight:800}.entry-score{font-size:30px;font-weight:900;color:#54d6a6}.entry-price{color:#9fb2c9;margin-top:5px}.entry-stance{margin:12px 0;padding:9px 10px;background:#0a1423;border-left:3px solid #65a7ff;border-radius:6px;font-weight:700}.entry-zones{display:grid;grid-template-columns:1fr 1fr;gap:8px}.entry-zones>div{background:#0a1423;border:1px solid #20364f;border-radius:9px;padding:9px}.entry-zones small,.entry-support small{display:block;color:#8299b4;font-size:10px}.entry-zones b{display:block;margin-top:3px}.entry-supports{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:9px}.entry-support{background:#0a1423;border:1px solid #20364f;border-radius:9px;padding:8px}.entry-support span{display:block;color:#65a7ff;font-size:10px;font-weight:800}.entry-support b{display:block;font-size:15px}.entry-support small{white-space:normal;line-height:1.2;margin-top:2px}.entry-foot{display:flex;justify-content:space-between;gap:10px;margin-top:10px;color:#95a9c0;font-size:11px}.entry-foot b{color:#eaf2ff}.report-created{display:inline-block;margin-top:8px;color:#8fa4bf;font-size:11px;line-height:1.35}@media(max-width:1000px){.entry-grid{grid-template-columns:1fr}.entry-zones{grid-template-columns:1fr 1fr}}@media(max-width:560px){.entry-zones,.entry-supports{grid-template-columns:1fr}.entry-foot{flex-direction:column}}
</style>
"""

    if "id='entry-support-css'" not in page and 'id="entry-support-css"' not in page:
        page = page.replace("</head>", css + "</head>")
    marker = "<div class='grid kpis'>"
    if marker in page:
        page = page.replace(marker, block + marker, 1)
    else:
        page = page.replace("<section class='panel'>", block + "<section class='panel'>", 1)

    # Add creation timestamp to the main dashboard without altering the trading-session date.
    stamp_marker = "</b></div></div>"
    if "Report created" not in page and stamp_marker in page:
        page = page.replace(stamp_marker, f"</b><br><span class='report-created'>Report created<br><b>{html.escape(created_text)}</b></span></div></div>", 1)

    DASH.write_text(page, encoding="utf-8")
    enhance_stock_pages(load_latest(), created_text)
    print(f"Enhanced dashboard with {len(cards)} entry cards; report timestamp={created_text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
