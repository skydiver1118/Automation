"""
Top-2 Skip-Momentum Strategy on SPMO-Replicated Universe
=========================================================
Run: pip install yfinance pandas openpyxl requests
     python spmo_universe_top2.py

Approach
--------
  SPMO tracks the top ~100 S&P 500 stocks by volatility-adjusted momentum,
  rebalanced semi-annually (May and November).

  We replicate this by:
    1. At each signal date, rank all S&P 500 point-in-time members by
       skip-momentum score = Close[t-21td] / Close[t-126td] - 1
    2. Take the top 100 as our "SPMO universe"
    3. Within that top-100, pick the top-2 by the same score
    4. Hold equal-weight, trade at next month open

  Period: 2024-01-01 through 2024-12-31
  Benchmark: SPMO ETF itself (same open-to-open method)
"""

import io, warnings, requests
import pandas as pd
import numpy as np
import yfinance as yf
warnings.filterwarnings("ignore")

SPMO_UNIVERSE_SIZE = 100   # replicate SPMO's ~100-stock universe
TOP_N = 2                  # pick top-2 within that universe
START_DT = "2024-01-01"
END_DT   = "2024-12-31"

# ── 1. Point-in-time S&P 500 membership ───────────────────────────────────
BASE_URL   = "https://raw.githubusercontent.com/fja05680/sp500/master/"
HIST_FILE  = "S%26P%20500%20Historical%20Components%20%26%20Changes.csv"
SINCE_FILE = "sp500_changes_since_2019.csv"

print("Downloading S&P 500 point-in-time data …")

def gh_csv(fn):
    r = requests.get(BASE_URL + fn, timeout=30)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text))

hist_df  = gh_csv(HIST_FILE)
since_df = gh_csv(SINCE_FILE)
hist_df.columns  = [c.strip() for c in hist_df.columns]
since_df.columns = [c.strip() for c in since_df.columns]

date_col = hist_df.columns[0]
tkr_col  = hist_df.columns[1] if len(hist_df.columns) > 1 else hist_df.columns[0]
hist_snapshots = {}
for _, row in hist_df.iterrows():
    try:
        d   = pd.to_datetime(str(row[date_col])).date()
        tks = {t.strip() for t in str(row[tkr_col]).split(",") if t.strip()}
        hist_snapshots[d] = tks
    except Exception:
        continue

add_col  = [c for c in since_df.columns if 'add'   in c.lower()]
rem_col  = [c for c in since_df.columns if 'remov' in c.lower() or 'delet' in c.lower()]
dc2      = since_df.columns[0]
additions, removals = {}, {}
for _, row in since_df.iterrows():
    try:
        d = pd.to_datetime(str(row[dc2])).date()
        if add_col:
            additions.setdefault(d, set()).update(
                {t.strip() for t in str(row[add_col[0]]).split(",")
                 if t.strip() and t.strip() != 'nan'})
        if rem_col:
            removals.setdefault(d, set()).update(
                {t.strip() for t in str(row[rem_col[0]]).split(",")
                 if t.strip() and t.strip() != 'nan'})
    except Exception:
        continue

sorted_snap = sorted(hist_snapshots.keys())
base_date   = max(d for d in sorted_snap if d <= pd.Timestamp("2019-01-01").date())
cur_members = set(hist_snapshots[base_date])
timeline    = [(base_date, frozenset(cur_members))]
for d in sorted(set(list(additions) + list(removals))):
    if d < base_date:
        continue
    cur_members = (cur_members | additions.get(d, set())) - removals.get(d, set())
    timeline.append((d, frozenset(cur_members)))

def get_sp500_on(qdate):
    if isinstance(qdate, pd.Timestamp):
        qdate = qdate.date()
    members = frozenset()
    for d, m in timeline:
        if d <= qdate:
            members = m
        else:
            break
    return set(members)

print(f"  Timeline events: {len(timeline)}")

# ── 2. Download prices ─────────────────────────────────────────────────────
all_tickers = set()
for _, m in timeline:
    all_tickers.update(m)
all_tickers.add("SPMO")

print(f"Downloading prices for {len(all_tickers)} tickers …")
raw = yf.download(
    sorted(all_tickers),
    start="2023-06-01",   # need 126td lookback before Jan 2024
    end="2025-01-05",
    auto_adjust=True,
    progress=True,
)
close_df = raw["Close"]
open_df  = raw["Open"]
print(f"Price data: {close_df.shape}  ({close_df.index[0].date()} → {close_df.index[-1].date()})")

# ── 3. Month boundaries ────────────────────────────────────────────────────
td = close_df.index

def month_boundaries(trading_days, start, end):
    out = []
    for m in pd.Series(trading_days).dt.to_period("M").unique():
        days = trading_days[trading_days.to_period("M") == m]
        if not len(days):
            continue
        trade_date  = days[0]
        prior       = trading_days[trading_days < trade_date]
        if not len(prior):
            continue
        signal_date = prior[-1]
        if pd.Timestamp(start) <= trade_date <= pd.Timestamp(end):
            out.append((str(m), signal_date, trade_date))
    return out

bounds = month_boundaries(td, START_DT, END_DT)
print(f"Strategy months: {len(bounds)}")

# ── 4. Run strategy ────────────────────────────────────────────────────────
rows = []

for i, (month, signal_date, trade_date) in enumerate(bounds):
    sig_idx  = td.get_loc(signal_date)
    skip_idx = sig_idx - 21
    look_idx = sig_idx - 126
    if skip_idx < 0 or look_idx < 0:
        continue

    skip_date   = td[skip_idx]
    look_date   = td[look_idx]
    sp500_today = get_sp500_on(signal_date)
    is_last     = (i == len(bounds) - 1)
    next_trade  = bounds[i + 1][2] if not is_last else None

    # Score all S&P 500 members
    scores = {}
    for tk in close_df.columns:
        if tk == "SPMO" or tk not in sp500_today:
            continue
        cs = close_df.loc[skip_date, tk]
        cl = close_df.loc[look_date, tk]
        if pd.notna(cs) and pd.notna(cl) and cl > 0 and cs > 0:
            scores[tk] = float(cs) / float(cl) - 1

    if not scores:
        print(f"  [{month}] ⚠ No valid scores")
        continue

    # Build SPMO-like universe: top-100 by score
    ranked_all  = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    spmo_pool   = [tk for tk, _ in ranked_all[:SPMO_UNIVERSE_SIZE]]
    spmo_scores = {tk: scores[tk] for tk in spmo_pool}

    # Within that pool, pick top-2
    top2 = [(tk, scores[tk]) for tk in spmo_pool[:TOP_N]]

    # Calculate returns
    rets = []
    entries, exits = {}, {}
    for tk, sc in top2:
        entry = open_df.loc[trade_date, tk] if tk in open_df.columns else np.nan
        if is_last:
            avail = close_df.loc[close_df.index >= trade_date, tk].dropna()
            ex = float(avail.iloc[-1]) if len(avail) else np.nan
        else:
            ex = open_df.loc[next_trade, tk] if tk in open_df.columns else np.nan
        entries[tk] = float(entry) if pd.notna(entry) else None
        exits[tk]   = float(ex)    if pd.notna(ex)    else None
        if entries[tk] and exits[tk] and entries[tk] > 0:
            rets.append(exits[tk] / entries[tk] - 1)

    monthly_ret = float(np.mean(rets)) if rets else None

    # SPMO ETF return for same month
    spmo_entry = open_df.loc[trade_date, "SPMO"] if "SPMO" in open_df.columns else np.nan
    spmo_exit  = (open_df.loc[next_trade, "SPMO"] if (next_trade and "SPMO" in open_df.columns)
                  else (close_df.loc[close_df.index >= trade_date, "SPMO"].dropna().iloc[-1]
                        if is_last else np.nan))
    spmo_ret   = (float(spmo_exit) / float(spmo_entry) - 1
                  if pd.notna(spmo_entry) and pd.notna(spmo_exit) else None)

    rows.append(dict(
        month       = month,
        signal_date = signal_date.date(),
        trade_date  = trade_date.date(),
        top2        = top2,
        entries     = entries,
        exits       = exits,
        monthly_ret = monthly_ret,
        spmo_ret    = spmo_ret,
        spmo_pool_top5 = ranked_all[:5],   # top-5 of SPMO universe for reference
        is_last     = is_last,
    ))

# ── 5. Equity curves ───────────────────────────────────────────────────────
strat_eq, spmo_eq = 1.0, 1.0
for r in rows:
    if r["monthly_ret"] is not None:
        strat_eq *= 1 + r["monthly_ret"]
    if r["spmo_ret"] is not None:
        spmo_eq  *= 1 + r["spmo_ret"]
    r["strat_equity"] = round(strat_eq, 6)
    r["spmo_equity"]  = round(spmo_eq, 6)

strat_total = strat_eq - 1
spmo_total  = spmo_eq  - 1

# ── 6. Annual summary ──────────────────────────────────────────────────────
df = pd.DataFrame(rows)
df["year"] = df["month"].str[:4]
ann = df.groupby("year").apply(lambda g: pd.Series({
    "strat_annual": (1 + g["monthly_ret"].dropna()).prod() - 1,
    "spmo_annual":  (1 + g["spmo_ret"].dropna()).prod() - 1,
    "n_months":     len(g),
    "win_months":   (g["monthly_ret"].dropna() > 0).sum(),
})).reset_index()

# ── 7. Print results ───────────────────────────────────────────────────────
print("\n" + "=" * 80)
print("  TOP-2 WITHIN SPMO-REPLICATED UNIVERSE  (top-100 S&P 500 momentum stocks)")
print("  Period: 2024-01 to 2024-12  |  Score: Close[t-21]/Close[t-126]-1")
print("=" * 80)
print(f"\n{'Month':<10} {'Top-2 Picks':<28} {'Strat Ret':>10} {'SPMO Ret':>10}"
      f" {'Strat Eq':>10} {'SPMO Eq':>10}  SPMO Pool Top-3")
print("-" * 90)

for r in rows:
    t2_str   = ", ".join(f"{tk}({sc*100:.0f}%)" for tk, sc in r["top2"])
    ret_s    = f"{r['monthly_ret']*100:.2f}%" if r["monthly_ret"] is not None else "?"
    spmo_s   = f"{r['spmo_ret']*100:.2f}%"   if r["spmo_ret"]   is not None else "?"
    seq_s    = f"{r['strat_equity']:.4f}x"
    beq_s    = f"{r['spmo_equity']:.4f}x"
    pool_top3 = ", ".join(f"{t}:{s*100:.0f}%" for t,s in r["spmo_pool_top5"][:3])
    star = "*" if r["is_last"] else ""
    print(f"{r['month']+star:<10} {t2_str:<28} {ret_s:>10} {spmo_s:>10}"
          f" {seq_s:>10} {beq_s:>10}  {pool_top3}")

print("-" * 90)
print(f"\n  Strategy total return : {strat_total*100:.2f}%   Final equity: {strat_eq:.4f}x")
print(f"  SPMO total return     : {spmo_total*100:.2f}%   Final equity: {spmo_eq:.4f}x")
print(f"  Alpha vs SPMO         : {(strat_total - spmo_total)*100:+.2f}pp")

print(f"\n{'Year':<8} {'Strat':>10} {'SPMO':>10} {'Win Months':>12}")
print("-" * 42)
for _, row in ann.iterrows():
    print(f"{row['year']:<8} {row['strat_annual']*100:>9.1f}% {row['spmo_annual']*100:>9.1f}%"
          f"   {int(row['win_months'])}/{int(row['n_months'])}")

# ── 8. Save Excel ──────────────────────────────────────────────────────────
out_path = "spmo_universe_top2_backtest.xlsx"
with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    out_rows = []
    for r in rows:
        out_rows.append({
            "Month":          r["month"],
            "Signal Date":    r["signal_date"],
            "Trade Date":     r["trade_date"],
            "Ticker 1":       r["top2"][0][0] if len(r["top2"]) > 0 else "",
            "Score 1":        round(r["top2"][0][1]*100,1) if len(r["top2"]) > 0 else "",
            "Entry 1":        r["entries"].get(r["top2"][0][0]) if len(r["top2"]) > 0 else "",
            "Exit 1":         r["exits"].get(r["top2"][0][0])   if len(r["top2"]) > 0 else "",
            "Ticker 2":       r["top2"][1][0] if len(r["top2"]) > 1 else "",
            "Score 2":        round(r["top2"][1][1]*100,1) if len(r["top2"]) > 1 else "",
            "Entry 2":        r["entries"].get(r["top2"][1][0]) if len(r["top2"]) > 1 else "",
            "Exit 2":         r["exits"].get(r["top2"][1][0])   if len(r["top2"]) > 1 else "",
            "Monthly Ret %":  round(r["monthly_ret"]*100, 2) if r["monthly_ret"] else "",
            "SPMO Ret %":     round(r["spmo_ret"]*100, 2)    if r["spmo_ret"]    else "",
            "Strat Equity":   r["strat_equity"],
            "SPMO Equity":    r["spmo_equity"],
            "SPMO Pool Top5": " | ".join(f"{t}:{s*100:.0f}%" for t,s in r["spmo_pool_top5"][:5]),
        })
    pd.DataFrame(out_rows).to_excel(writer, sheet_name="Monthly Trades", index=False)
    ann.to_excel(writer, sheet_name="Annual Summary", index=False)

print(f"\n  Saved: {out_path}")
print("=" * 80)
