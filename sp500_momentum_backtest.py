"""
S&P 500 Top-1 Monthly Skip-Momentum Backtest  (Point-in-Time Universe)
======================================================================
Run in VS Code:
    pip install yfinance pandas openpyxl requests
    python sp500_momentum_backtest.py

Strategy
--------
  Universe  : S&P 500 constituents as of the signal date (point-in-time)
  Signal    : Last trading day before each month start
  Score     : Close[t-21 trading days] / Close[t-126 trading days] - 1
  Selection : Top-1 scorer that was ALREADY in S&P 500 on signal date
  Trade     : First trading day open of the month
  Return    : Open-to-open (completed months); latest close (current month)
  Period    : 2025-01 through 2026-05

Point-in-time S&P 500 data
---------------------------
Downloaded from: https://github.com/fja05680/sp500
  - S&P 500 Historical Components & Changes.csv  (pre-2019 base)
  - sp500_changes_since_2019.csv                 (2019 onward additions/removals)
These are fetched automatically at runtime.
"""

import io, warnings
import requests
import pandas as pd
import numpy as np
import yfinance as yf
warnings.filterwarnings("ignore")

# ── 1. Load point-in-time S&P 500 membership ──────────────────────────────

BASE_URL    = "https://raw.githubusercontent.com/fja05680/sp500/master/"
HIST_FILE   = "S%26P%20500%20Historical%20Components%20%26%20Changes.csv"
SINCE_FILE  = "sp500_changes_since_2019.csv"

print("Downloading S&P 500 point-in-time constituent data from GitHub…")

def gh_csv(filename):
    url = BASE_URL + filename
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text))

hist_df   = gh_csv(HIST_FILE)
since_df  = gh_csv(SINCE_FILE)

print(f"  Historical file : {hist_df.shape[0]} rows")
print(f"  Since-2019 file : {since_df.shape[0]} rows")

# The historical file has columns: date, tickers (comma-separated list)
# Parse it into a dict of {date -> set(tickers)}
hist_df.columns = [c.strip() for c in hist_df.columns]
# First column is date, rest (or combined) is tickers
date_col = hist_df.columns[0]
tkr_col  = hist_df.columns[1] if len(hist_df.columns) > 1 else hist_df.columns[0]

hist_snapshots = {}
for _, row in hist_df.iterrows():
    try:
        d = pd.to_datetime(str(row[date_col])).date()
        tickers_raw = str(row[tkr_col]) if tkr_col != date_col else str(row.iloc[1])
        tks = {t.strip() for t in tickers_raw.split(",") if t.strip()}
        hist_snapshots[d] = tks
    except Exception:
        continue

print(f"  Parsed {len(hist_snapshots)} historical snapshots")

# since_2019 file has columns: date, added, removed
since_df.columns = [c.strip() for c in since_df.columns]
print(f"  Since-2019 columns: {list(since_df.columns)}")

# Build additions and removals indexed by effective date
additions = {}   # date -> set of tickers added
removals  = {}   # date -> set of tickers removed

add_col = [c for c in since_df.columns if 'add' in c.lower()]
rem_col = [c for c in since_df.columns if 'remov' in c.lower() or 'delet' in c.lower()]
date_col2 = since_df.columns[0]

for _, row in since_df.iterrows():
    try:
        d = pd.to_datetime(str(row[date_col2])).date()
        if add_col:
            adds = {t.strip() for t in str(row[add_col[0]]).split(",") if t.strip() and t.strip() != 'nan'}
            additions.setdefault(d, set()).update(adds)
        if rem_col:
            rems = {t.strip() for t in str(row[rem_col[0]]).split(",") if t.strip() and t.strip() != 'nan'}
            removals.setdefault(d, set()).update(rems)
    except Exception:
        continue

print(f"  Change events parsed: {len(additions)} addition dates, {len(removals)} removal dates")

# ── Build a function to get S&P 500 members on any given date ─────────────

# Start from the most recent historical snapshot before 2019-01-01
# then apply all changes forward

sorted_snap_dates = sorted(hist_snapshots.keys())
# Use the snapshot closest to (but before) 2019-01-01
base_date = max(d for d in sorted_snap_dates if d <= pd.Timestamp("2019-01-01").date())
current_members = set(hist_snapshots[base_date])
print(f"\n  Base snapshot date: {base_date} ({len(current_members)} tickers)")

# Apply all changes from that date onward, building a timeline
all_change_dates = sorted(set(list(additions.keys()) + list(removals.keys())))
all_change_dates = [d for d in all_change_dates if d >= base_date]

membership_timeline = [(base_date, frozenset(current_members))]

for d in all_change_dates:
    current_members = set(current_members)
    current_members |= additions.get(d, set())
    current_members -= removals.get(d, set())
    membership_timeline.append((d, frozenset(current_members)))

print(f"  Timeline events: {len(membership_timeline)}")

def get_sp500_on(query_date):
    """Return the set of S&P 500 tickers on a given date."""
    if isinstance(query_date, pd.Timestamp):
        query_date = query_date.date()
    members = frozenset()
    for d, m in membership_timeline:
        if d <= query_date:
            members = m
        else:
            break
    return set(members)

# Quick sanity check
test_date = pd.Timestamp("2025-01-02").date()
sp500_jan2025 = get_sp500_on(test_date)
print(f"\n  S&P 500 on 2025-01-02: {len(sp500_jan2025)} members")
for chk in ["APP","PLTR","HOOD","SNDK","NVDA","AAPL","MSFT"]:
    print(f"    {chk}: {'✓ IN' if chk in sp500_jan2025 else '✗ NOT IN'}")

# ── 2. Download price data ────────────────────────────────────────────────

# Get full universe — all tickers that ever appeared in S&P 500 during our period
all_tickers = set()
for _, members in membership_timeline:
    all_tickers.update(members)

# Filter to ones likely to have yfinance data and appear in our period
# Just use all of them and let yfinance handle failures

print(f"\nDownloading prices for up to {len(all_tickers)} tickers (this takes ~2 min)…")
tickers_list = sorted(all_tickers)

raw = yf.download(
    tickers_list,
    start="2024-06-01",
    end="2026-05-17",
    auto_adjust=True,
    progress=True,
)

close_df = raw["Close"]
open_df  = raw["Open"]
print(f"\nPrice data: {close_df.shape}  ({close_df.index[0].date()} → {close_df.index[-1].date()})")

# ── 3. Build month boundaries ─────────────────────────────────────────────

td = close_df.index  # DatetimeIndex of all trading days

def month_boundaries(trading_days):
    out = []
    months = pd.Series(trading_days).dt.to_period("M").unique()
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

# ── 4. Run strategy ───────────────────────────────────────────────────────

rows    = []
holding = None

for i, (month, signal_date, trade_date) in enumerate(bounds):
    sig_idx  = td.get_loc(signal_date)
    skip_idx = sig_idx - 21
    look_idx = sig_idx - 126
    if skip_idx < 0 or look_idx < 0:
        continue

    skip_date = td[skip_idx]
    look_date = td[look_idx]

    # Point-in-time S&P 500 universe on signal date
    sp500_today = get_sp500_on(signal_date)

    # Score every eligible ticker
    scores = {}
    skipped_not_in_sp500 = []
    for tk in close_df.columns:
        if tk not in sp500_today:
            continue  # enforce point-in-time membership
        cs = close_df.loc[skip_date, tk]
        cl = close_df.loc[look_date, tk]
        if pd.notna(cs) and pd.notna(cl) and cl > 0 and cs > 0:
            scores[tk] = float(cs) / float(cl) - 1

    if not scores:
        print(f"  [{month}] ⚠ No valid scores — skipping")
        continue

    # Rank all — walk down until we find one that was IN S&P 500 on signal date
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    top5   = ranked[:5]

    # The winner is already guaranteed to be in S&P 500 (we pre-filtered)
    winner, top_score = ranked[0]

    # Double-check (redundant but explicit)
    if winner not in sp500_today:
        print(f"  [{month}] ⚠ Top scorer {winner} not in S&P 500 — skipping to next")
        for tk, sc in ranked[1:]:
            if tk in sp500_today:
                winner, top_score = tk, sc
                break

    action = "BUY" if holding is None else ("SWITCH" if winner != holding else "HOLD")
    is_last = (i == len(bounds) - 1)

    entry_open = open_df.loc[trade_date, winner] if winner in open_df.columns else np.nan

    if is_last:
        avail = close_df.loc[close_df.index >= trade_date, winner].dropna()
        exit_price = float(avail.iloc[-1]) if len(avail) else np.nan
        exit_label = f"close {avail.index[-1].date()}" if len(avail) else "?"
    else:
        next_trade = bounds[i + 1][2]
        exit_price = open_df.loc[next_trade, winner] if winner in open_df.columns else np.nan
        exit_label = f"open {next_trade.date()}"

    entry_open_f = float(entry_open) if pd.notna(entry_open) else None
    exit_price_f = float(exit_price)  if pd.notna(exit_price)  else None

    monthly_ret = (exit_price_f / entry_open_f - 1) if (entry_open_f and exit_price_f) else None

    sp500_members_count = len(sp500_today)

    rows.append(dict(
        month        = month,
        signal_date  = signal_date.date(),
        trade_date   = trade_date.date(),
        action       = action,
        ticker       = winner,
        score        = round(top_score, 4),
        entry_open   = round(entry_open_f, 4) if entry_open_f else None,
        exit_price   = round(exit_price_f, 4) if exit_price_f else None,
        exit_label   = exit_label,
        monthly_ret  = round(monthly_ret, 6)  if monthly_ret  else None,
        is_last      = is_last,
        top5         = [(t, round(s, 3)) for t, s in top5],
        sp500_size   = sp500_members_count,
    ))
    holding = winner

# ── 5. Compound returns ───────────────────────────────────────────────────

equity = 1.0
for r in rows:
    if r["monthly_ret"] is not None:
        equity *= 1 + r["monthly_ret"]
    r["equity"] = round(equity, 6)

total_ret = equity - 1

# ── 6. Print results ──────────────────────────────────────────────────────

print("\n" + "=" * 82)
print("  S&P 500 TOP-1 SKIP-MOMENTUM BACKTEST  (Point-in-Time Universe)")
print("=" * 82)
print(f"{'Month':<10} {'Act':<8} {'Ticker':<7} {'Score':>8} {'Entry':>9} {'Exit':>9}"
      f" {'Ret%':>8} {'Equity':>9}  Top-3 (S&P500 members only)")
print("-" * 82)

for r in rows:
    sc  = f"{r['score']*100:.1f}%"
    en  = f"${r['entry_open']:.2f}"  if r['entry_open']  else "?"
    ex  = f"${r['exit_price']:.2f}"  if r['exit_price']  else "?"
    ret = f"{r['monthly_ret']*100:.2f}%" if r['monthly_ret'] is not None else "?"
    eq  = f"{r['equity']:.4f}x"
    t3  = "  |  " + ", ".join(f"{t}:{v*100:.0f}%" for t, v in r['top5'][:3])
    star = "*" if r["is_last"] else ""
    print(f"{r['month']+star:<10} {r['action']:<8} {r['ticker']:<7} {sc:>8}"
          f" {en:>9} {ex:>9} {ret:>8} {eq:>9}{t3}")

print("-" * 82)
print(f"\n  Months        : {len(rows)}")
print(f"  BUY           : {sum(1 for r in rows if r['action']=='BUY')}")
print(f"  SWITCH        : {sum(1 for r in rows if r['action']=='SWITCH')}")
print(f"  HOLD          : {sum(1 for r in rows if r['action']=='HOLD')}")
print(f"\n  Total return  : {total_ret*100:.2f}%")
print(f"  Final equity  : {equity:.4f}x")
print(f"\n  [Previous NDX-100 backtest: 903.51% / 10.035x]")
print(f"  [NDX backtest had APP/HOOD/SNDK purchased before S&P 500 inclusion]")

# ── 7. Save Excel ─────────────────────────────────────────────────────────

output_rows = [{k: v for k, v in r.items() if k not in ("top5",)} for r in rows]
for r_out, r in zip(output_rows, rows):
    r_out["top_3"] = " | ".join(f"{t}:{v*100:.1f}%" for t, v in r["top5"][:3])

df = pd.DataFrame(output_rows)
out_path = "sp500_momentum_backtest_results.xlsx"
with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Trades", index=False)
    summary = pd.DataFrame({
        "Metric": [
            "Period", "Universe", "Strategy", "Total Return %",
            "Final Equity x", "Months", "BUY", "SWITCH", "HOLD",
        ],
        "Value": [
            "2025-01 to 2026-05",
            "S&P 500 (point-in-time)",
            "Top-1 monthly skip-momentum (t-21/t-126)",
            round(total_ret * 100, 2),
            round(equity, 4),
            len(rows),
            sum(1 for r in rows if r["action"] == "BUY"),
            sum(1 for r in rows if r["action"] == "SWITCH"),
            sum(1 for r in rows if r["action"] == "HOLD"),
        ]
    })
    summary.to_excel(writer, sheet_name="Summary", index=False)

print(f"\n  Saved: {out_path}")
print("=" * 82)
