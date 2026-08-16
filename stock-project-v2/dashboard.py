from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
HISTORY = ROOT / "history"
OUT = ROOT / "dashboard"
STOCKS_OUT = OUT / "stocks"

TICKERS = ["NVDA", "MU", "SPCX", "LITE", "META", "NBIS", "MRVL", "RKLB", "AXTI", "APLD", "IREN"]
COLORS = ["#65a7ff", "#54d6a6", "#f6c85f", "#b184ff", "#ff7f7f", "#6dd5ed", "#ff9f5a", "#7bdff2", "#f08fc0", "#9ee493", "#d7aefb"]


def fnum(v, digits=1, suffix=""):
    try:
        if pd.isna(v):
            return "—"
        return f"{float(v):,.{digits}f}{suffix}"
    except Exception:
        return "—"


def fpct(v, digits=1):
    try:
        if pd.isna(v):
            return "—"
        return f"{float(v)*100:.{digits}f}%"
    except Exception:
        return "—"


def money(v):
    try:
        if pd.isna(v):
            return "—"
        v = float(v)
        if abs(v) >= 1e12:
            return f"${v/1e12:.2f}T"
        if abs(v) >= 1e9:
            return f"${v/1e9:.2f}B"
        if abs(v) >= 1e6:
            return f"${v/1e6:.1f}M"
        return f"${v:,.0f}"
    except Exception:
        return "—"


def load_history() -> pd.DataFrame:
    frames = []
    if HISTORY.exists():
        for path in sorted(HISTORY.glob("*.csv")):
            try:
                x = pd.read_csv(path)
                if "as_of" not in x.columns:
                    x["as_of"] = path.stem
                frames.append(x)
            except Exception as exc:
                print(f"WARN history {path.name}: {exc}")
    latest = ROOT / "latest_scores.csv"
    if latest.exists():
        try:
            frames.append(pd.read_csv(latest))
        except Exception as exc:
            print(f"WARN latest: {exc}")
    if not frames:
        raise RuntimeError("No score history available")
    df = pd.concat(frames, ignore_index=True, sort=False)
    df["as_of"] = pd.to_datetime(df["as_of"], errors="coerce").dt.strftime("%Y-%m-%d")
    df = df.dropna(subset=["as_of", "ticker"])
    df = df.sort_values(["as_of", "ticker"]).drop_duplicates(["as_of", "ticker"], keep="last")
    return df


def score_class(v):
    try:
        v = float(v)
        if v >= 85:
            return "excellent"
        if v >= 75:
            return "good"
        if v >= 65:
            return "neutral"
        return "weak"
    except Exception:
        return "neutral"


def common_css():
    return """
:root{--bg:#08101d;--panel:#101b2d;--panel2:#0d1727;--text:#edf4ff;--muted:#8fa4bf;--line:#223550;--accent:#65a7ff;--green:#54d6a6;--amber:#f6c85f;--red:#ff7f7f}
*{box-sizing:border-box} body{margin:0;background:linear-gradient(180deg,#08101d,#0b1423 45%,#08101d);color:var(--text);font:14px/1.45 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
a{color:inherit;text-decoration:none}.wrap{max-width:1500px;margin:auto;padding:28px}.topbar{display:flex;justify-content:space-between;gap:20px;align-items:end;margin-bottom:20px}.eyebrow{text-transform:uppercase;letter-spacing:.14em;font-size:11px;color:var(--accent);font-weight:800}.title{font-size:32px;font-weight:850;letter-spacing:-.03em;margin:4px 0}.sub{color:var(--muted);max-width:900px}.stamp{color:var(--muted);text-align:right;white-space:nowrap}.grid{display:grid;gap:16px}.kpis{grid-template-columns:repeat(4,minmax(0,1fr));margin-bottom:16px}.kpi,.panel,.stock-card{background:rgba(16,27,45,.92);border:1px solid var(--line);border-radius:16px;box-shadow:0 12px 30px rgba(0,0,0,.14)}.kpi{padding:17px}.kpi .label{color:var(--muted);font-size:12px}.kpi .value{font-size:25px;font-weight:800;margin-top:4px}.panel{padding:18px;margin-bottom:16px}.panel-head{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:10px}.panel h2{font-size:17px;margin:0}.controls select{background:#0b1423;color:var(--text);border:1px solid var(--line);border-radius:8px;padding:7px 10px}.chartbox{height:360px}.table-wrap{overflow:auto;border-radius:12px}table{width:100%;border-collapse:collapse;min-width:980px}th,td{padding:12px 10px;border-bottom:1px solid #1d2d44;text-align:right;white-space:nowrap}th{font-size:11px;color:var(--muted);text-transform:uppercase;letter-spacing:.06em;position:sticky;top:0;background:var(--panel)}th:nth-child(1),td:nth-child(1),th:nth-child(2),td:nth-child(2){text-align:left}.ticker{font-weight:850;font-size:15px}.ticker:hover{color:var(--accent)}.rank{color:var(--muted)}.score{font-weight:800}.excellent{color:var(--green)}.good{color:#90d7ff}.neutral{color:var(--amber)}.weak{color:var(--red)}.badge{display:inline-flex;padding:4px 8px;border-radius:999px;background:#16263c;border:1px solid #28415f;color:#bcd0e8;font-size:11px}.cards{grid-template-columns:repeat(3,minmax(0,1fr))}.stock-card{padding:16px;transition:.18s ease}.stock-card:hover{transform:translateY(-2px);border-color:#39577c}.stock-head{display:flex;justify-content:space-between;align-items:start}.stock-name{font-size:20px;font-weight:850}.bigscore{font-size:30px;font-weight:900}.triplet{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px}.mini{background:#0b1423;border:1px solid #1e314b;border-radius:10px;padding:9px}.mini span{display:block;color:var(--muted);font-size:10px;text-transform:uppercase}.mini b{font-size:16px}.footer{color:var(--muted);font-size:12px;padding:16px 0 30px}.back{display:inline-block;color:var(--accent);font-weight:700;margin-bottom:12px}.detail-grid{grid-template-columns:1.2fr .8fr}.factor-grid{grid-template-columns:repeat(2,1fr)}.factor{padding:10px 0}.factor-line{display:flex;justify-content:space-between;margin-bottom:5px}.bar{height:7px;background:#182942;border-radius:8px;overflow:hidden}.bar>i{display:block;height:100%;background:linear-gradient(90deg,#65a7ff,#54d6a6);border-radius:8px}.metrics{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.metric{background:#0b1423;border:1px solid #1e314b;border-radius:10px;padding:11px}.metric small{display:block;color:var(--muted);margin-bottom:2px}.metric strong{font-size:16px}.positive{color:var(--green)}.negative{color:var(--red)}
@media(max-width:900px){.wrap{padding:16px}.kpis,.cards,.detail-grid,.factor-grid{grid-template-columns:1fr}.topbar{align-items:start;flex-direction:column}.stamp{text-align:left}.chartbox{height:300px}.metrics{grid-template-columns:repeat(2,1fr)}}
"""


def main_dashboard(hist: pd.DataFrame):
    latest_date = hist["as_of"].max()
    latest = hist[hist["as_of"] == latest_date].copy().sort_values("buy_now_score", ascending=False)
    latest["rank"] = range(1, len(latest) + 1)
    top = latest.iloc[0]

    history_payload = {"dates": sorted(hist["as_of"].unique().tolist()), "series": {}}
    for ticker in TICKERS:
        td = hist[hist.ticker == ticker].set_index("as_of")
        history_payload["series"][ticker] = {}
        for metric in ["buy_now_score", "long_term_score", "short_term_score"]:
            vals = []
            for d in history_payload["dates"]:
                vals.append(float(td.loc[d, metric]) if d in td.index and metric in td.columns and pd.notna(td.loc[d, metric]) else None)
            history_payload["series"][ticker][metric] = vals

    table_rows = []
    cards = []
    for _, r in latest.iterrows():
        t = r["ticker"]
        table_rows.append(f"""
<tr><td class='rank'>#{int(r['rank'])}</td><td><a class='ticker' href='stocks/{t}.html'>{t}</a></td><td>{fnum(r.get('price'),2)}</td><td>{money(r.get('market_cap'))}</td><td class='score {score_class(r.get('long_term_score'))}'>{fnum(r.get('long_term_score'))}</td><td class='score {score_class(r.get('short_term_score'))}'>{fnum(r.get('short_term_score'))}</td><td class='score {score_class(r.get('buy_now_score'))}'>{fnum(r.get('buy_now_score'))}</td><td>{fnum(r.get('valuation_score'))}</td><td>{fnum(r.get('quality_score'))}</td><td>{fnum(r.get('growth_score'))}</td><td>{fnum(r.get('technical_score'))}</td><td>{fnum(r.get('rsi14'))}</td></tr>""")
        cards.append(f"""
<a class='stock-card' href='stocks/{t}.html'><div class='stock-head'><div><div class='stock-name'>{t}</div><div class='sub'>{money(r.get('market_cap'))} · ${fnum(r.get('price'),2)}</div></div><div><span class='badge'>Rank #{int(r['rank'])}</span></div></div><div class='bigscore {score_class(r.get('buy_now_score'))}'>{fnum(r.get('buy_now_score'))}</div><div class='sub'>Buy-Now score</div><div class='triplet'><div class='mini'><span>Long term</span><b>{fnum(r.get('long_term_score'))}</b></div><div class='mini'><span>Short term</span><b>{fnum(r.get('short_term_score'))}</b></div><div class='mini'><span>RS</span><b>{fnum(r.get('relative_strength_score'))}</b></div></div></a>""")

    html = f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Stock Project V2 Dashboard</title><script src='https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js'></script><style>{common_css()}</style></head><body><main class='wrap'>
<div class='topbar'><div><div class='eyebrow'>Stock Project V2.0</div><div class='title'>AI / Semiconductor Ranking Dashboard</div><div class='sub'>11-stock systematic ranking. Scores update only after a completed NYSE trading session. Click any ticker for its detailed factor and technical analysis.</div></div><div class='stamp'>Latest trading session<br><b>{latest_date}</b></div></div>
<div class='grid kpis'><div class='kpi'><div class='label'>Top Buy-Now</div><div class='value'>{top['ticker']} · {fnum(top.get('buy_now_score'))}</div></div><div class='kpi'><div class='label'>Universe</div><div class='value'>{len(latest)} stocks</div></div><div class='kpi'><div class='label'>Best Long-Term</div><div class='value'>{latest.loc[latest.long_term_score.idxmax(),'ticker']} · {fnum(latest.long_term_score.max())}</div></div><div class='kpi'><div class='label'>Best Short-Term</div><div class='value'>{latest.loc[latest.short_term_score.idxmax(),'ticker']} · {fnum(latest.short_term_score.max())}</div></div></div>
<section class='panel'><div class='panel-head'><div><h2>Score movement</h2><div class='sub'>Historical score trajectory by completed trading session.</div></div><div class='controls'><select id='metric'><option value='buy_now_score'>Buy-Now</option><option value='long_term_score'>Long-Term</option><option value='short_term_score'>Short-Term</option></select></div></div><div class='chartbox'><canvas id='historyChart'></canvas></div></section>
<section class='panel'><div class='panel-head'><div><h2>Current ranking</h2><div class='sub'>Sorted by Buy-Now score.</div></div></div><div class='table-wrap'><table><thead><tr><th>Rank</th><th>Ticker</th><th>Price</th><th>Market cap</th><th>Long-term</th><th>Short-term</th><th>Buy-now</th><th>Value</th><th>Quality</th><th>Growth</th><th>Technical</th><th>RSI</th></tr></thead><tbody>{''.join(table_rows)}</tbody></table></div></section>
<section><div class='panel-head'><div><h2>Stock detail</h2><div class='sub'>Open a card for full V2 factor diagnostics.</div></div></div><div class='grid cards'>{''.join(cards)}</div></section>
<div class='footer'>V2 scores are model outputs, not guarantees or individualized investment advice. Missing point-in-time data is neutralized rather than fabricated.</div>
<script>const H={json.dumps(history_payload)}; const C={json.dumps(COLORS)}; const T={json.dumps(TICKERS)}; let chart; function render(metric){{const datasets=T.map((t,i)=>({{label:t,data:H.series[t][metric],borderColor:C[i],backgroundColor:C[i],borderWidth:2,pointRadius:H.dates.length<10?3:1.5,pointHoverRadius:5,tension:.22,spanGaps:true}})); if(chart)chart.destroy(); chart=new Chart(document.getElementById('historyChart'),{{type:'line',data:{{labels:H.dates,datasets}},options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},plugins:{{legend:{{labels:{{color:'#b9c9dc',boxWidth:14,usePointStyle:true}}}},tooltip:{{callbacks:{{label:(c)=>`${{c.dataset.label}}: ${{c.parsed.y?.toFixed(1)??'NA'}}`}}}}}},scales:{{x:{{ticks:{{color:'#7f95b1',maxRotation:0,autoSkip:true}},grid:{{color:'#172940'}}}},y:{{min:0,max:100,ticks:{{color:'#7f95b1'}},grid:{{color:'#172940'}}}}}}}}}});}} render('buy_now_score'); document.getElementById('metric').addEventListener('change',e=>render(e.target.value));</script></main></body></html>"""
    (OUT / "index.html").write_text(html, encoding="utf-8")


def stock_detail(hist: pd.DataFrame, ticker: str):
    td = hist[hist.ticker == ticker].sort_values("as_of").copy()
    if td.empty:
        return
    r = td.iloc[-1]
    dates = td["as_of"].tolist()
    trend = {
        "dates": dates,
        "lt": [None if pd.isna(x) else float(x) for x in td.get("long_term_score", pd.Series([np.nan]*len(td)))],
        "st": [None if pd.isna(x) else float(x) for x in td.get("short_term_score", pd.Series([np.nan]*len(td)))],
        "bn": [None if pd.isna(x) else float(x) for x in td.get("buy_now_score", pd.Series([np.nan]*len(td)))],
    }
    factors = [("Valuation", r.get("valuation_score")), ("Quality", r.get("quality_score")), ("Growth", r.get("growth_score")), ("Revisions", r.get("revision_score")), ("Technical", r.get("technical_score")), ("Relative strength", r.get("relative_strength_score"))]
    factor_html = "".join([f"<div class='factor'><div class='factor-line'><span>{name}</span><b>{fnum(val)}</b></div><div class='bar'><i style='width:{max(0,min(100,float(val) if pd.notna(val) else 0))}%'></i></div></div>" for name,val in factors])
    metrics = [
        ("Price", "$"+fnum(r.get("price"),2)), ("Market cap", money(r.get("market_cap"))), ("RSI 14", fnum(r.get("rsi14"))),
        ("MACD histogram", fnum(r.get("macd_hist"),3)), ("ADX 14", fnum(r.get("adx14"))), ("20DMA distance", fpct(r.get("dist_20dma"))),
        ("50DMA distance", fpct(r.get("dist_50dma"))), ("200DMA distance", fpct(r.get("dist_200dma"))), ("1M RS", fpct(r.get("rs_1m"))),
        ("3M RS", fpct(r.get("rs_3m"))), ("6M RS", fpct(r.get("rs_6m"))), ("12M RS", fpct(r.get("rs_12m"))),
        ("Forward revenue growth", fpct(r.get("forward_revenue_growth"))), ("Forward EPS growth", fpct(r.get("forward_eps_growth"))), ("EPS revision signal", fnum(r.get("eps_revision_signal"),2)),
        ("Forward P/E", fnum(r.get("forward_pe"),1)+"×" if pd.notna(r.get("forward_pe")) else "—"), ("EV / Sales", fnum(r.get("ev_sales"),1)+"×" if pd.notna(r.get("ev_sales")) else "—"), ("EV / EBITDA", fnum(r.get("ev_ebitda"),1)+"×" if pd.notna(r.get("ev_ebitda")) else "—"),
        ("FCF yield", fpct(r.get("fcf_yield"))), ("FCF margin", fpct(r.get("fcf_margin"))), ("ROIC proxy", fpct(r.get("roic_proxy"))),
        ("Gross margin", fpct(r.get("gross_margin"))), ("Operating margin", fpct(r.get("operating_margin"))), ("Debt / Equity", fnum(r.get("debt_to_equity"),1)),
    ]
    metric_html = "".join([f"<div class='metric'><small>{name}</small><strong>{val}</strong></div>" for name,val in metrics])
    html = f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{ticker} · Stock Project V2</title><script src='https://cdn.jsdelivr.net/npm/chart.js@4.4.4/dist/chart.umd.min.js'></script><style>{common_css()}</style></head><body><main class='wrap'><a class='back' href='../index.html'>← Back to dashboard</a><div class='topbar'><div><div class='eyebrow'>Stock Project V2.0 · Detail</div><div class='title'>{ticker}</div><div class='sub'>Factor diagnostics and score history through {r.get('as_of','—')}.</div></div><div class='stamp'>Buy-Now<br><span class='bigscore {score_class(r.get('buy_now_score'))}'>{fnum(r.get('buy_now_score'))}</span></div></div>
<div class='grid kpis'><div class='kpi'><div class='label'>Long-Term</div><div class='value {score_class(r.get('long_term_score'))}'>{fnum(r.get('long_term_score'))}</div></div><div class='kpi'><div class='label'>Short-Term</div><div class='value {score_class(r.get('short_term_score'))}'>{fnum(r.get('short_term_score'))}</div></div><div class='kpi'><div class='label'>Price</div><div class='value'>${fnum(r.get('price'),2)}</div></div><div class='kpi'><div class='label'>Market cap</div><div class='value'>{money(r.get('market_cap'))}</div></div></div>
<div class='grid detail-grid'><section class='panel'><div class='panel-head'><div><h2>Score history</h2><div class='sub'>Long-Term, Short-Term and Buy-Now movement.</div></div></div><div class='chartbox'><canvas id='trend'></canvas></div></section><section class='panel'><div class='panel-head'><div><h2>Factor scores</h2><div class='sub'>Current cross-sectional percentile scores.</div></div></div><div class='grid factor-grid'>{factor_html}</div></section></div>
<section class='panel'><div class='panel-head'><div><h2>Raw V2 diagnostics</h2><div class='sub'>Current data used by the scoring engine. Relative strength is versus the weighted SMH / QQQ benchmark.</div></div></div><div class='metrics'>{metric_html}</div></section>
<div class='footer'>Model values can change substantially after earnings, revisions or major price moves. Point-in-time data limitations are preserved as missing rather than estimated.</div>
<script>const D={json.dumps(trend)}; new Chart(document.getElementById('trend'),{{type:'line',data:{{labels:D.dates,datasets:[{{label:'Buy-Now',data:D.bn,borderColor:'#54d6a6',backgroundColor:'#54d6a6',borderWidth:3,tension:.2}},{{label:'Long-Term',data:D.lt,borderColor:'#65a7ff',backgroundColor:'#65a7ff',borderWidth:2,tension:.2}},{{label:'Short-Term',data:D.st,borderColor:'#f6c85f',backgroundColor:'#f6c85f',borderWidth:2,tension:.2}}]}},options:{{responsive:true,maintainAspectRatio:false,interaction:{{mode:'index',intersect:false}},plugins:{{legend:{{labels:{{color:'#b9c9dc'}}}}}},scales:{{x:{{ticks:{{color:'#7f95b1'}},grid:{{color:'#172940'}}}},y:{{min:0,max:100,ticks:{{color:'#7f95b1'}},grid:{{color:'#172940'}}}}}}}}}});</script></main></body></html>"""
    (STOCKS_OUT / f"{ticker}.html").write_text(html, encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    STOCKS_OUT.mkdir(parents=True, exist_ok=True)
    hist = load_history()
    main_dashboard(hist)
    for ticker in TICKERS:
        stock_detail(hist, ticker)
    print(f"Dashboard generated: {OUT / 'index.html'}")


if __name__ == "__main__":
    main()
