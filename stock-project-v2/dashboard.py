from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
HISTORY = ROOT / "history"
OUT = ROOT / "dashboard"
STOCKS_OUT = OUT / "stocks"
TICKERS = ["NVDA", "MU", "SPCX", "LITE", "META", "NBIS", "MRVL", "RKLB", "AXTI", "APLD", "IREN"]
COLORS = ["#65a7ff", "#54d6a6", "#f6c85f", "#b184ff", "#ff7f7f", "#6dd5ed", "#ff9f5a", "#7bdff2", "#f08fc0", "#9ee493", "#d7aefb"]
DIAG_LABELS = ["Price", "Market cap", "RSI 14", "MACD histogram", "ADX 14", "20DMA distance", "50DMA distance", "200DMA distance", "1M RS", "3M RS", "6M RS", "12M RS", "Forward revenue growth", "Forward EPS growth", "EPS revision signal", "Forward P/E", "EV / Sales", "EV / EBITDA", "FCF yield", "FCF margin", "ROIC proxy", "Gross margin", "Operating margin", "Debt / Equity"]


def fnum(v, digits=1, suffix=""):
    try:
        if pd.isna(v): return "—"
        return f"{float(v):,.{digits}f}{suffix}"
    except Exception:
        return "—"


def fpct(v, digits=1):
    try:
        if pd.isna(v): return "—"
        return f"{float(v)*100:.{digits}f}%"
    except Exception:
        return "—"


def money(v):
    try:
        if pd.isna(v): return "—"
        v = float(v)
        if abs(v) >= 1e12: return f"${v/1e12:.2f}T"
        if abs(v) >= 1e9: return f"${v/1e9:.2f}B"
        if abs(v) >= 1e6: return f"${v/1e6:.1f}M"
        return f"${v:,.0f}"
    except Exception:
        return "—"


def load_history():
    frames = []
    if HISTORY.exists():
        for path in sorted(HISTORY.glob("*.csv")):
            try:
                x = pd.read_csv(path)
                if "as_of" not in x.columns: x["as_of"] = path.stem
                frames.append(x)
            except Exception as exc:
                print(f"WARN history {path.name}: {exc}")
    latest = ROOT / "latest_scores.csv"
    if latest.exists():
        frames.append(pd.read_csv(latest))
    if not frames:
        raise RuntimeError("No score history available")
    df = pd.concat(frames, ignore_index=True, sort=False)
    df["as_of"] = pd.to_datetime(df["as_of"], errors="coerce").dt.strftime("%Y-%m-%d")
    return df.dropna(subset=["as_of", "ticker"]).sort_values(["as_of", "ticker"]).drop_duplicates(["as_of", "ticker"], keep="last")


def score_class(v):
    try:
        v = float(v)
        if v >= 85: return "excellent"
        if v >= 75: return "good"
        if v >= 65: return "neutral"
        return "weak"
    except Exception:
        return "neutral"


def diagnostic_sentiment(row):
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    from add_metric_comments import sentiment_summary
    _, score, overall, _ = sentiment_summary(row, DIAG_LABELS)
    return int(score), overall


def sentiment_cell(row):
    try:
        score, overall = diagnostic_sentiment(row)
        lo = overall.lower()
        cls = "sent-bear" if "bearish" in lo else "sent-bull" if "bullish" in lo else "sent-mixed"
        return f"<span class='sentiment {cls}'>{overall}<b>{score}%</b></span>"
    except Exception as exc:
        print(f"WARN sentiment {row.get('ticker','?')}: {exc}")
        return "<span class='sentiment sent-mixed'>N/A</span>"


def common_css():
    return """
:root{--bg:#08101d;--panel:#101b2d;--text:#edf4ff;--muted:#8fa4bf;--line:#223550;--accent:#65a7ff;--green:#54d6a6;--amber:#f6c85f;--red:#ff7f7f}
*{box-sizing:border-box}body{margin:0;background:#08101d;color:var(--text);font:14px/1.45 Inter,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:inherit;text-decoration:none}.wrap{max-width:1500px;margin:auto;padding:28px}.topbar{display:flex;justify-content:space-between;gap:20px;align-items:end;margin-bottom:20px}.eyebrow{text-transform:uppercase;letter-spacing:.14em;font-size:11px;color:var(--accent);font-weight:800}.title{font-size:32px;font-weight:850;margin:4px 0}.sub{color:var(--muted);max-width:900px}.stamp{color:var(--muted);text-align:right;white-space:nowrap}.grid{display:grid;gap:16px}.kpis{grid-template-columns:repeat(4,minmax(0,1fr));margin-bottom:16px}.kpi,.panel,.stock-card{background:#101b2d;border:1px solid var(--line);border-radius:16px}.kpi{padding:17px}.kpi .label{color:var(--muted);font-size:12px}.kpi .value{font-size:25px;font-weight:800;margin-top:4px}.panel{padding:18px;margin-bottom:16px}.panel-head{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:10px}.panel h2{font-size:17px;margin:0}.chartbox{height:360px}.table-wrap{overflow:auto;border-radius:12px}table{width:100%;border-collapse:collapse;min-width:1120px}th,td{padding:12px 10px;border-bottom:1px solid #1d2d44;text-align:right;white-space:nowrap}th{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;background:#101b2d}th:nth-child(1),td:nth-child(1),th:nth-child(2),td:nth-child(2){text-align:left}.ticker{font-weight:850;font-size:15px}.rank{color:var(--muted)}.score{font-weight:800}.excellent{color:var(--green)}.good{color:#90d7ff}.neutral{color:var(--amber)}.weak{color:var(--red)}.sentiment{display:inline-flex;gap:6px;align-items:center;font-weight:750}.sentiment b{font-size:14px}.sent-bull{color:var(--green)}.sent-bear{color:var(--red)}.sent-mixed{color:var(--amber)}.badge{display:inline-flex;padding:4px 8px;border-radius:999px;background:#16263c;border:1px solid #28415f;color:#bcd0e8;font-size:11px}.cards{grid-template-columns:repeat(3,minmax(0,1fr))}.stock-card{padding:16px}.stock-head{display:flex;justify-content:space-between}.stock-name{font-size:20px;font-weight:850}.bigscore{font-size:30px;font-weight:900}.triplet{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px}.mini,.metric{background:#0b1423;border:1px solid #1e314b;border-radius:10px;padding:10px}.mini span,.metric small{display:block;color:var(--muted);font-size:11px}.mini b,.metric strong{font-size:16px}.detail-grid{grid-template-columns:1.2fr .8fr}.factor-grid{grid-template-columns:repeat(2,1fr)}.factor-line{display:flex;justify-content:space-between;margin:8px 0}.bar{height:7px;background:#182942;border-radius:8px;overflow:hidden}.bar i{display:block;height:100%;background:#65a7ff}.metrics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.back{display:inline-block;color:var(--accent);font-weight:700;margin-bottom:12px}.footer{color:var(--muted);font-size:12px;padding:16px 0 30px}
@media(max-width:900px){.wrap{padding:16px}.kpis,.cards,.detail-grid,.factor-grid{grid-template-columns:1fr}.topbar{align-items:start;flex-direction:column}.stamp{text-align:left}.metrics{grid-template-columns:repeat(2,1fr)}.chartbox{height:300px}}
"""


def main_dashboard(hist):
    latest_date = hist["as_of"].max()
    latest = hist[hist["as_of"] == latest_date].copy().sort_values("buy_now_score", ascending=False)
    latest["rank"] = range(1, len(latest)+1)
    top = latest.iloc[0]
    dates = sorted(hist["as_of"].unique().tolist())
    series = {}
    for ticker in TICKERS:
        td = hist[hist.ticker == ticker].set_index("as_of")
        series[ticker] = {}
        for metric in ["buy_now_score", "long_term_score", "short_term_score"]:
            series[ticker][metric] = [float(td.loc[d, metric]) if d in td.index and metric in td.columns and pd.notna(td.loc[d, metric]) else None for d in dates]
    rows, cards = [], []
    for _, r in latest.iterrows():
        t = r["ticker"]
        rows.append(f"<tr><td class='rank'>#{int(r['rank'])}</td><td><a class='ticker' href='stocks/{t}.html'>{t}</a></td><td>{fnum(r.get('price'),2)}</td><td>{money(r.get('market_cap'))}</td><td>{fnum(r.get('long_term_score'))}</td><td>{fnum(r.get('short_term_score'))}</td><td class='score {score_class(r.get('buy_now_score'))}'>{fnum(r.get('buy_now_score'))}</td><td>{fnum(r.get('valuation_score'))}</td><td>{fnum(r.get('quality_score'))}</td><td>{fnum(r.get('growth_score'))}</td><td>{fnum(r.get('technical_score'))}</td><td>{fnum(r.get('rsi14'))}</td><td>{sentiment_cell(r)}</td></tr>")
        cards.append(f"<a class='stock-card' href='stocks/{t}.html'><div class='stock-head'><div><div class='stock-name'>{t}</div><div class='sub'>{money(r.get('market_cap'))} · ${fnum(r.get('price'),2)}</div></div><span class='badge'>Rank #{int(r['rank'])}</span></div><div class='bigscore {score_class(r.get('buy_now_score'))}'>{fnum(r.get('buy_now_score'))}</div><div class='sub'>Buy-Now score</div><div class='triplet'><div class='mini'><span>Long term</span><b>{fnum(r.get('long_term_score'))}</b></div><div class='mini'><span>Short term</span><b>{fnum(r.get('short_term_score'))}</b></div><div class='mini'><span>RS</span><b>{fnum(r.get('relative_strength_score'))}</b></div></div></a>")
    payload = json.dumps({"dates": dates, "series": series})
    html = f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Stock Project V2 Dashboard</title><script src='https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js'></script><style>{common_css()}</style></head><body><main class='wrap'>
<div class='topbar'><div><div class='eyebrow'>Stock Project V2.0</div><div class='title'>AI / Semiconductor Ranking Dashboard</div><div class='sub'>11-stock systematic ranking. Click any ticker for detailed analysis.</div></div><div class='stamp'>Latest trading session<br><b>{latest_date}</b></div></div>
<div class='grid kpis'><div class='kpi'><div class='label'>Top Buy-Now</div><div class='value'>{top['ticker']} · {fnum(top.get('buy_now_score'))}</div></div><div class='kpi'><div class='label'>Universe</div><div class='value'>{len(latest)} stocks</div></div><div class='kpi'><div class='label'>Best Long-Term</div><div class='value'>{latest.loc[latest.long_term_score.idxmax(),'ticker']} · {fnum(latest.long_term_score.max())}</div></div><div class='kpi'><div class='label'>Best Short-Term</div><div class='value'>{latest.loc[latest.short_term_score.idxmax(),'ticker']} · {fnum(latest.short_term_score.max())}</div></div></div>
<section class='panel'><div class='panel-head'><div><h2>Score movement</h2><div class='sub'>Historical score trajectory by completed trading session.</div></div><select id='metric'><option value='buy_now_score'>Buy-Now</option><option value='long_term_score'>Long-Term</option><option value='short_term_score'>Short-Term</option></select></div><div class='chartbox'><canvas id='historyChart'></canvas></div></section>
<section class='panel'><div class='panel-head'><div><h2>Current ranking</h2><div class='sub'>Sorted by Buy-Now score. Last column uses the same diagnostic positive breadth as each detail page.</div></div></div><div class='table-wrap'><table><thead><tr><th>Rank</th><th>Ticker</th><th>Price</th><th>Market cap</th><th>Long-term</th><th>Short-term</th><th>Buy-now</th><th>Value</th><th>Quality</th><th>Growth</th><th>Technical</th><th>RSI</th><th>Diag sentiment</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
<section><div class='panel-head'><div><h2>Stock detail</h2><div class='sub'>Open a card for full V2 diagnostics.</div></div></div><div class='grid cards'>{''.join(cards)}</div></section><div class='footer'>Model outputs are not guarantees or individualized investment advice.</div>
<script>const H={payload},C={json.dumps(COLORS)},T={json.dumps(TICKERS)};let chart;function render(metric){{const ds=T.map((t,i)=>({{label:t,data:H.series[t][metric],borderColor:C[i],backgroundColor:C[i],borderWidth:2,pointRadius:2,tension:.22,spanGaps:true}}));if(chart)chart.destroy();chart=new Chart(document.getElementById('historyChart'),{{type:'line',data:{{labels:H.dates,datasets:ds}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{labels:{{color:'#b9c9dc'}}}}}},scales:{{x:{{ticks:{{color:'#7f95b1'}},grid:{{color:'#172940'}}}},y:{{min:0,max:100,ticks:{{color:'#7f95b1'}},grid:{{color:'#172940'}}}}}}}}}})}}render('buy_now_score');document.getElementById('metric').addEventListener('change',e=>render(e.target.value));</script></main></body></html>"""
    (OUT / "index.html").write_text(html, encoding="utf-8")


def stock_detail(hist, ticker):
    td = hist[hist.ticker == ticker].sort_values("as_of").copy()
    if td.empty: return
    r = td.iloc[-1]
    trend = {"dates": td["as_of"].tolist(), "lt": [None if pd.isna(x) else float(x) for x in td["long_term_score"]], "st": [None if pd.isna(x) else float(x) for x in td["short_term_score"]], "bn": [None if pd.isna(x) else float(x) for x in td["buy_now_score"]]}
    factors = [("Valuation","valuation_score"),("Quality","quality_score"),("Growth","growth_score"),("Revisions","revision_score"),("Technical","technical_score"),("Relative strength","relative_strength_score")]
    factor_html = "".join(f"<div><div class='factor-line'><span>{name}</span><b>{fnum(r.get(col))}</b></div><div class='bar'><i style='width:{max(0,min(100,float(r.get(col,0) or 0)))}%'></i></div></div>" for name,col in factors)
    metrics = [
        ("Price", f"${fnum(r.get('price'),2)}"), ("Market cap", money(r.get('market_cap'))), ("RSI 14", fnum(r.get('rsi14'))), ("MACD histogram", fnum(r.get('macd_hist'),3)), ("ADX 14", fnum(r.get('adx14'))),
        ("20DMA distance", fpct(r.get('dist_20dma'))), ("50DMA distance", fpct(r.get('dist_50dma'))), ("200DMA distance", fpct(r.get('dist_200dma'))), ("1M RS", fpct(r.get('rs_1m'))), ("3M RS", fpct(r.get('rs_3m'))), ("6M RS", fpct(r.get('rs_6m'))), ("12M RS", fpct(r.get('rs_12m'))),
        ("Forward revenue growth", fpct(r.get('forward_revenue_growth'))), ("Forward EPS growth", fpct(r.get('forward_eps_growth'))), ("EPS revision signal", fnum(r.get('eps_revision_signal'),2)), ("Forward P/E", fnum(r.get('forward_pe'),1,"×")), ("EV / Sales", fnum(r.get('ev_sales'),1,"×")), ("EV / EBITDA", fnum(r.get('ev_ebitda'),1,"×")),
        ("FCF yield", fpct(r.get('fcf_yield'))), ("FCF margin", fpct(r.get('fcf_margin'))), ("ROIC proxy", fpct(r.get('roic_proxy'))), ("Gross margin", fpct(r.get('gross_margin'))), ("Operating margin", fpct(r.get('operating_margin'))), ("Debt / Equity", fnum(r.get('debt_to_equity'),1)),
    ]
    metric_html = "".join(f"<div class='metric'><small>{name}</small><strong>{value}</strong></div>" for name,value in metrics)
    html = f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{ticker} · Stock Project V2</title><script src='https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js'></script><style>{common_css()}</style></head><body><main class='wrap'><a class='back' href='../index.html'>← Back to dashboard</a><div class='topbar'><div><div class='eyebrow'>Stock Project V2.0 · Detail</div><div class='title'>{ticker}</div><div class='sub'>Factor diagnostics and score history through {r.get('as_of')}.</div></div><div class='stamp'>Buy-Now<br><span class='bigscore {score_class(r.get('buy_now_score'))}'>{fnum(r.get('buy_now_score'))}</span></div></div>
<div class='grid kpis'><div class='kpi'><div class='label'>Long-Term</div><div class='value'>{fnum(r.get('long_term_score'))}</div></div><div class='kpi'><div class='label'>Short-Term</div><div class='value'>{fnum(r.get('short_term_score'))}</div></div><div class='kpi'><div class='label'>Price</div><div class='value'>${fnum(r.get('price'),2)}</div></div><div class='kpi'><div class='label'>Market cap</div><div class='value'>{money(r.get('market_cap'))}</div></div></div>
<div class='grid detail-grid'><section class='panel'><div class='panel-head'><div><h2>Score history</h2><div class='sub'>Long-Term, Short-Term and Buy-Now movement.</div></div></div><div class='chartbox'><canvas id='trend'></canvas></div></section><section class='panel'><div class='panel-head'><div><h2>Factor scores</h2><div class='sub'>Current cross-sectional percentile scores.</div></div></div><div class='grid factor-grid'>{factor_html}</div></section></div>
<section class='panel'><div class='panel-head'><div><h2>Raw V2 diagnostics</h2><div class='sub'>Current data used by the scoring engine. Relative strength is versus the weighted SMH / QQQ benchmark.</div></div></div><div class='metrics'>{metric_html}</div></section><div class='footer'>Diagnostic labels are descriptive, not guarantees.</div>
<script>const D={json.dumps(trend)};new Chart(document.getElementById('trend'),{{type:'line',data:{{labels:D.dates,datasets:[{{label:'Long-Term',data:D.lt,borderColor:'#65a7ff'}},{{label:'Short-Term',data:D.st,borderColor:'#f6c85f'}},{{label:'Buy-Now',data:D.bn,borderColor:'#54d6a6'}}]}},options:{{responsive:true,maintainAspectRatio:false,scales:{{y:{{min:0,max:100}}}}}}}});</script></main></body></html>"""
    (STOCKS_OUT / f"{ticker}.html").write_text(html, encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    STOCKS_OUT.mkdir(exist_ok=True)
    hist = load_history()
    main_dashboard(hist)
    for ticker in TICKERS:
        stock_detail(hist, ticker)
    print(f"Dashboard generated: {OUT/'index.html'}")


if __name__ == "__main__":
    main()
