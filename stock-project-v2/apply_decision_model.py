from __future__ import annotations

import html
import json
from pathlib import Path

import pandas as pd

from signal_policy import entry_quality, long_term_rating, short_put_eligible

ROOT = Path(__file__).resolve().parent
LATEST = ROOT / "latest_scores.csv"
CANONICAL = ROOT / "canonical_market.json"
DASH = ROOT / "dashboard"
STOCKS = DASH / "stocks"


def score(v):
    try:
        return f"{float(v):.1f}"
    except Exception:
        return "—"


def state(row):
    raw_rating = row.get("long_term_rating")
    rating = str(raw_rating) if raw_rating is not None and not pd.isna(raw_rating) else long_term_rating(row.get("long_term_score"))
    raw_entry = row.get("entry_score")
    es = raw_entry if raw_entry is not None and not pd.isna(raw_entry) else row.get("short_term_score")
    raw_quality = row.get("entry_quality")
    quality = str(raw_quality) if raw_quality is not None and not pd.isna(raw_quality) else entry_quality(es)
    eligible = short_put_eligible(rating)
    return rating, es, quality, eligible


def explanation(rating: str, quality: str, eligible: bool) -> str:
    if not eligible:
        return f"No short-put SELL: long-term rating is {rating}; BUY/STRONG BUY is required."
    if quality in {"EXCELLENT", "GOOD"}:
        return "Long-term ownership gate passes; equity timing is favorable. Option trade still needs its own premium/IV/risk gates."
    return "Long-term ownership gate passes, but equity timing is not ideal. Option dashboard may remain WAIT."


def main_panel(df: pd.DataFrame) -> str:
    rows = []
    for _, r in df.sort_values(["long_term_score", "entry_score"], ascending=False).iterrows():
        rating, es, quality, eligible = state(r)
        t = html.escape(str(r["ticker"]))
        rows.append(
            f"<tr><td><a class='ticker' href='stocks/{t}.html'>{t}</a></td>"
            f"<td><b>{html.escape(rating)}</b> · {score(r.get('long_term_score'))}</td>"
            f"<td><b>{html.escape(quality)}</b> · {score(es)}</td>"
            f"<td class='{'excellent' if eligible else 'weak'}'>{'YES' if eligible else 'NO'}</td>"
            f"<td style='text-align:left;white-space:normal'>{html.escape(explanation(rating, quality, eligible))}</td></tr>"
        )
    return """<section class='panel' id='decision-model'><div class='panel-head'><div><h2>Ownership vs entry decision model</h2><div class='sub'>Long-Term Rating answers whether the business is attractive to own. Entry Quality answers whether equity timing is favorable. A short-put SELL is permitted only for BUY / STRONG BUY stocks, then the options engine applies separate execution gates.</div></div></div><div class='table-wrap'><table><thead><tr><th>Ticker</th><th>Long-Term Rating</th><th>Entry Quality</th><th>Put eligible</th><th style='text-align:left'>Interpretation</th></tr></thead><tbody>""" + "".join(rows) + "</tbody></table></div></section>"


def detail_panel(row, canonical: dict) -> str:
    rating, es, quality, eligible = state(row)
    t = str(row["ticker"])
    c = (canonical.get("stocks") or {}).get(t, {})
    tech = c.get("technical") or {}
    support = c.get("support") or {}
    trend = tech.get("trend") or "—"
    key_support = support.get("key_support")
    sentiment = (c.get("diagnostic_sentiment") or {}).get("label") or "—"
    support_text = f"${float(key_support):,.2f}" if key_support is not None else "—"
    return f"""<section class='panel' id='signal-reconciliation'><div class='panel-head'><div><h2>Signal reconciliation</h2><div class='sub'>Ownership conviction and execution timing are intentionally separate.</div></div></div><div class='grid kpis'><div class='kpi'><div class='label'>Long-Term Rating</div><div class='value'>{html.escape(rating)} · {score(row.get('long_term_score'))}</div></div><div class='kpi'><div class='label'>Entry Quality</div><div class='value'>{html.escape(quality)} · {score(es)}</div></div><div class='kpi'><div class='label'>Short-put ownership gate</div><div class='value {'excellent' if eligible else 'weak'}'>{'ELIGIBLE' if eligible else 'NO TRADE'}</div></div><div class='kpi'><div class='label'>Canonical trend / support</div><div class='value'>{html.escape(str(trend))}</div><div class='sub'>{support_text} · sentiment {html.escape(str(sentiment))}</div></div></div><div class='sub'>{html.escape(explanation(rating, quality, eligible))}</div></section>"""


def main() -> int:
    df = pd.read_csv(LATEST)
    if "entry_score" not in df.columns:
        df["entry_score"] = df["short_term_score"]
    canonical = json.loads(CANONICAL.read_text(encoding="utf-8")) if CANONICAL.exists() else {"stocks": {}}

    index = DASH / "index.html"
    page = index.read_text(encoding="utf-8")
    replacements = {
        "Top Buy-Now": "Top Overall Opportunity",
        "Top 3 Buy-Now: Entry & Support Map": "Top 3 Composite Opportunities: Entry & Support Map",
        "BUY-NOW": "COMPOSITE",
        "Buy-Now score": "Composite opportunity score",
        ">Buy-Now</option>": ">Composite</option>",
        "Sorted by Buy-Now score.": "Composite opportunity rank. Long-Term Rating and Entry Quality are separate decisions.",
        "<th>Buy-now</th>": "<th>Composite</th>",
    }
    for a, b in replacements.items():
        page = page.replace(a, b)
    marker = "<section><div class='panel-head'><div><h2>Stock detail</h2>"
    if "id='decision-model'" not in page and marker in page:
        page = page.replace(marker, main_panel(df) + marker, 1)
    index.write_text(page, encoding="utf-8")

    by_ticker = df.set_index("ticker")
    for ticker, row in by_ticker.iterrows():
        path = STOCKS / f"{ticker}.html"
        if not path.exists():
            continue
        p = path.read_text(encoding="utf-8")
        p = p.replace("<div class='stamp'>Buy-Now<br>", "<div class='stamp'>Composite<br>")
        p = p.replace("Long-Term, Short-Term and Buy-Now movement.", "Long-Term, Entry/Short-Term and composite-score movement.")
        p = p.replace("label:'Buy-Now'", "label:'Composite'")
        marker2 = "<div class='grid detail-grid'>"
        if "id='signal-reconciliation'" not in p and marker2 in p:
            row = row.copy(); row["ticker"] = ticker
            p = p.replace(marker2, detail_panel(row, canonical) + marker2, 1)
        path.write_text(p, encoding="utf-8")
    print("Applied Long-Term Rating / Entry Quality UI and reconciliation panels.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
