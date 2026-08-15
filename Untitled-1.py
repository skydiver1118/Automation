"""
Nasdaq-100 Top-1 Monthly Skip-Momentum Strategy — Backtest Replication
Run: pip install yfinance pandas openpyxl && python backtest.py

Replicates the strategy from the PDF exactly:
  Score  = Close[t-21td] / Close[t-126td] - 1   (signal at month-end close)
  Trade  = first trading day open of following month
  Return = open-to-open (completed months); latest close (current month)
  Period = 2025-01 through 2026-05
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import date
import warnings
warnings.filterwarnings("ignore")

# ── Nasdaq-100 tickers (current list — note survivorship bias caveat) ───────
NDX = [
    "AAPL","MSFT","NVDA","AMZN","META","GOOGL","GOOG","TSLA","AVGO","COST",
    "NFLX","TMUS","AMD","LIN","ISRG","CSCO","AMGN","TXN","INTU","QCOM",
    "CMCSA","HON","AMAT","BKNG","ADI","REGN","VRTX","MU","PANW","LRCX",
    "GILD","KLAC","SNPS","CDNS","MRVL","CRWD","ADP","CTAS","MDLZ","FTNT",
    "CEG","ABNB","NXPI","ORLY","WDAY","DXCM","ROP","ROST","PCAR","MNST",
    "ODFL","GEHC","FAST","CPRT","EXC","IDXX","MCHP","PAYX","CTSH","VRSK",
    "AEP","DDOG","BIIB","ON","XEL","ZS","TEAM","ANSS","CDW","DLTR","ILMN",
    "GFS","SIRI","TTWO","WBD","ALGN","ENPH","DOCU","OKTA","PYPL",
    "APP","PLTR","SNDK","WDC","MSTR","AXON","HOOD","ARM","SMCI","COIN",
]
NDX = list(dict.fromkeys(NDX))  # dedupe

PDF_DECISIONS = {
    "2025-01": ("BUY",    "APP"),
    "2025-02": ("HOLD",   "APP"),
    "2025-03": ("HOLD",   "APP"),
    "2025-04": ("HOLD",   "APP"),
    "2025-05": ("SWITCH", "PLTR"),
    "2025-06": ("HOLD",   "PLTR"),
    "2025-07": ("HOLD",   "PLTR"),
    "2025-08": ("HOLD",   "PLTR"),
    "2025-09": ("HOLD",   "PLTR"),
    "2025-10": ("SWITCH", "WDC"),
    "2025-11": ("SWITCH", "SNDK"),
    "2025-12": ("HOLD",   "SNDK"),
    "2026-01": ("HOLD",   "SNDK"),
    "2026-02": ("HOLD",   "SNDK"),
    "2026-03": ("HOLD",   "SNDK"),
    "2026-04": ("HOLD",   "SNDK"),
    "2026-05": ("HOLD",   "SNDK"),
}

# ── 1. Download prices ──────────────────────────────────────────────────────
print("Downloading prices (this takes ~30s)...")
raw = yf.download(
    NDX,
    start="2024-06-01",
    end="2026-05-17",
    auto_adjust=True,
    progress=True,
)
close = raw["Close"]
open_ = raw["Open"]
print(f"Data: {close.shape}  ({close.index[0].date()} → {close.index[-1].date()})")

# ── 2. Build month boundaries ───────────────────────────────────────────────
td = close.index  # all trading days

def month_boundaries(trading_days):
    s = pd.Series(trading_days)
    months = s.dt.to_period("M").unique()
    out = []
    for m in months:
        days = trading_days[trading_days.to_period("M") == m]
        if len(days) == 0:
            continue
        trade_date  = days[0]
        prior       = trading_days[trading_days < trade_date]
        if len(prior) == 0:
            continue
        signal_date = prior[-1]
        out.append((str(m), signal_date, trade_date))
    return out

bounds = [
    (m, sig, trd) for m, sig, trd in month_boundaries(td)
    if trd >= pd.Timestamp("2025-01-01") and sig <= pd.Timestamp("2026-05-16")
]
print(f"\nStrategy months: {len(bounds)}")

# ── 3. Run strategy ─────────────────────────────────────────────────────────
rows = []
holding = None

for i, (month, signal_date, trade_date) in enumerate(bounds):
    sig_idx  = td.get_loc(signal_date)
    skip_idx = sig_idx - 21
    look_idx = sig_idx - 126
    if skip_idx < 0 or look_idx < 0:
        continue

    skip_date = td[skip_idx]
    look_date = td[look_idx]

    # Momentum scores
    scores = {}
    for tk in NDX:
        if tk not in close.columns:
            continue
        cs = close.loc[skip_date, tk]
        cl = close.loc[look_date, tk]
        if pd.notna(cs) and pd.notna(cl) and cl > 0:
            scores[tk] = float(cs) / float(cl) - 1

    if not scores:
        continue

    winner   = max(scores, key=scores.get)
    top_score = scores[winner]
    action   = "BUY" if holding is None else ("SWITCH" if winner != holding else "HOLD")
    is_last  = (i == len(bounds) - 1)

    entry_open = open_.loc[trade_date, winner] if winner in open_.columns else np.nan

    if is_last:
        avail = close.loc[close.index >= trade_date, winner].dropna()
        exit_price = float(avail.iloc[-1]) if len(avail) else np.nan
        exit_label = f"close {avail.index[-1].date()}" if len(avail) else "?"
    else:
        next_trade = bounds[i + 1][2]
        exit_price = open_.loc[next_trade, winner] if winner in open_.columns else np.nan
        exit_label = f"open {next_trade.date()}"

    monthly_ret = (float(exit_price) / float(entry_open) - 1) if (
        pd.notna(entry_open) and pd.notna(exit_price) and entry_open > 0
    ) else np.nan

    pdf_a, pdf_t = PDF_DECISIONS.get(month, ("?", "?"))
    match = (action == pdf_a and winner == pdf_t)

    # Top-5 for display
    top5 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:5]

    rows.append(dict(
        month=month, signal=signal_date.date(), trade=trade_date.date(),
        action=action, ticker=winner, score=top_score,
        entry_open=float(entry_open) if pd.notna(entry_open) else None,
        exit_price=float(exit_price) if pd.notna(exit_price) else None,
        exit_label=exit_label,
        monthly_ret=monthly_ret if pd.notna(monthly_ret) else None,
        is_last=is_last,
        pdf_action=pdf_a, pdf_ticker=pdf_t, match=match,
        top5=top5,
    ))
    holding = winner

# ── 4. Compound returns ────────────────────────────────────────────────────
equity = 1.0
for r in rows:
    if r["monthly_ret"] is not None:
        equity *= 1 + r["monthly_ret"]
    r["equity"] = equity

total_ret   = equity - 1
match_count = sum(r["match"] for r in rows)

# ── 5. Print results ───────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("  NASDAQ-100 TOP-1 SKIP-MOMENTUM BACKTEST RESULTS")
print("=" * 80)
print(f"\n{'Month':<10} {'Action':<8} {'Ticker':<7} {'Score':>7} {'Entry':>8} {'Exit':>8} {'Ret%':>8} {'Equity':>9}  {'vs PDF'}")
print("-" * 78)
for r in rows:
    sc  = f"{r['score']*100:.1f}%" if r["score"] is not None else "?"
    en  = f"${r['entry_open']:.2f}" if r["entry_open"] else "?"
    ex  = f"${r['exit_price']:.2f}" if r["exit_price"] else "?"
    ret = f"{r['monthly_ret']*100:.2f}%" if r["monthly_ret"] is not None else "?"
    eq  = f"{r['equity']:.4f}x"
    mk  = "✓" if r["match"] else f"✗ (PDF: {r['pdf_action']} {r['pdf_ticker']})"
    star = "*" if r["is_last"] else ""
    print(f"{r['month']+star:<10} {r['action']:<8} {r['ticker']:<7} {sc:>7} {en:>8} {ex:>8} {ret:>8} {eq:>9}  {mk}")
    t5 = ", ".join(f"{t}:{v*100:.0f}%" for t,v in r["top5"][:3])
    print(f"{'':10} Top3: {t5}")

print("-" * 78)
print(f"\n  Months        : {len(rows)}")
print(f"  BUY           : {sum(1 for r in rows if r['action']=='BUY')}")
print(f"  SWITCH        : {sum(1 for r in rows if r['action']=='SWITCH')}")
print(f"  HOLD          : {sum(1 for r in rows if r['action']=='HOLD')}")
print(f"\n  Total return  : {total_ret*100:.2f}%")
print(f"  Final equity  : {equity:.4f}x")
print(f"\n  PDF claimed   : 1005.28%  /  11.0528x")
print(f"  Return diff   : {abs(total_ret - 10.0528)*100:.2f}pp")
print(f"  Decision match: {match_count}/{len(rows)} months")

# ── 6. Save Excel ──────────────────────────────────────────────────────────
df = pd.DataFrame([{k: v for k, v in r.items() if k != "top5"} for r in rows])
df.to_excel("ndx_momentum_backtest.xlsx", index=False)
print("\n  Saved: ndx_momentum_backtest.xlsx")
print("=" * 80)