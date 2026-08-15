"""
S&P 500 Skip-Momentum Backtest: Top-1 vs Top-2 vs Top-3 vs SPMO
================================================================
Run: pip install yfinance pandas openpyxl requests
     python sp500_momentum_multi.py

Strategy
--------
  Universe  : S&P 500 constituents (point-in-time via fja05680/sp500)
  Signal    : Last trading day before each month start
  Score     : Close[t-21 td] / Close[t-126 td] - 1
  Selection : Top-N scorers already in S&P 500 on signal date (equal weight)
  Trade     : First trading day open of the month
  Return    : Open-to-open (equal-weight avg of N holdings)
  Period    : 2020-01 through 2024-12  (5 full calendar years)
  Benchmark : SPMO (S&P 500 Momentum ETF)
"""

import io, warnings, requests
import pandas as pd
import numpy as np
import yfinance as yf
warnings.filterwarnings("ignore")

STRATS   = [1, 2, 3]
START_DT = "2020-01-01"
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

# Parse historical snapshots
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

# Parse additions / removals since 2019
add_col  = [c for c in since_df.columns if 'add'    in c.lower()]
rem_col  = [c for c in since_df.columns if 'remov'  in c.lower() or 'delet' in c.lower()]
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

# Build membership timeline
sorted_snap = sorted(hist_snapshots.keys())
base_date   = max(d for d in sorted_snap if d <= pd.Timestamp("2019-01-01").date())
cur_members = set(hist_snapshots[base_date])
timeline    = [(base_date, frozenset(cur_members))]
for d in sorted(set(list(additions) + list(removals))):
    if d < base_date:
        continue
    cur_members = set(cur_members)
    cur_members |= additions.get(d, set())
    cur_members -= removals.get(d,  set())
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
all_tickers.add("SPMO")   # benchmark

print(f"Downloading prices for {len(all_tickers)} tickers (2–3 min) …")
raw = yf.download(
    sorted(all_tickers),
    start="2019-06-01",   # need ~126 td of lookback before 2020-01
    end="2025-01-02",
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
        if len(days) == 0:
            continue
        trade_date  = days[0]
        prior       = trading_days[trading_days < trade_date]
        if len(prior) == 0:
            continue
        signal_date = prior[-1]
        if trade_date >= pd.Timestamp(start) and trade_date <= pd.Timestamp(end):
            out.append((str(m), signal_date, trade_date))
    return out

bounds = month_boundaries(td, START_DT, END_DT)
print(f"Strategy months: {len(bounds)}")

# ── 4. Run strategies ──────────────────────────────────────────────────────
# Returns dict: {n: [monthly_ret, ...]}
strat_rows = {n: [] for n in STRATS}

for i, (month, signal_date, trade_date) in enumerate(bounds):
    sig_idx  = td.get_loc(signal_date)
    skip_idx = sig_idx - 21
    look_idx = sig_idx - 126
    if skip_idx < 0 or look_idx < 0:
        continue

    skip_date    = td[skip_idx]
    look_date    = td[look_idx]
    sp500_today  = get_sp500_on(signal_date)
    is_last      = (i == len(bounds) - 1)
    next_trade   = bounds[i + 1][2] if not is_last else None

    # Score eligible tickers
    scores = {}
    for tk in close_df.columns:
        if tk == "SPMO" or tk not in sp500_today:
            continue
        cs = close_df.loc[skip_date, tk]
        cl = close_df.loc[look_date, tk]
        if pd.notna(cs) and pd.notna(cl) and cl > 0 and cs > 0:
            scores[tk] = float(cs) / float(cl) - 1

    if not scores:
        for n in STRATS:
            strat_rows[n].append(dict(month=month, trade_date=trade_date,
                                      tickers=[], monthly_ret=None))
        continue

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    for n in STRATS:
        top_n = [tk for tk, _ in ranked[:n]]
        # Equal-weight return for this month
        rets = []
        for tk in top_n:
            entry = open_df.loc[trade_date, tk] if tk in open_df.columns else np.nan
            if is_last or next_trade is None:
                avail = close_df.loc[close_df.index >= trade_date, tk].dropna()
                ex = float(avail.iloc[-1]) if len(avail) else np.nan
            else:
                ex = open_df.loc[next_trade, tk] if tk in open_df.columns else np.nan
            if pd.notna(entry) and pd.notna(ex) and entry > 0:
                rets.append(ex / entry - 1)

        monthly_ret = float(np.mean(rets)) if rets else None
        strat_rows[n].append(dict(
            month=month,
            trade_date=trade_date,
            tickers=top_n,
            scores=[round(scores[tk], 4) for tk in top_n],
            monthly_ret=monthly_ret,
        ))

# ── 5. SPMO benchmark monthly returns ─────────────────────────────────────
spmo_monthly = {}
if "SPMO" in close_df.columns and "SPMO" in open_df.columns:
    for i, (month, signal_date, trade_date) in enumerate(bounds):
        is_last    = (i == len(bounds) - 1)
        next_trade = bounds[i + 1][2] if not is_last else None
        entry = open_df.loc[trade_date, "SPMO"] if trade_date in open_df.index else np.nan
        if is_last or next_trade is None:
            avail = close_df.loc[close_df.index >= trade_date, "SPMO"].dropna()
            ex = float(avail.iloc[-1]) if len(avail) else np.nan
        else:
            ex = open_df.loc[next_trade, "SPMO"] if next_trade in open_df.index else np.nan
        if pd.notna(entry) and pd.notna(ex) and entry > 0:
            spmo_monthly[month] = ex / entry - 1
        else:
            spmo_monthly[month] = None

# ── 6. Compute equity curves ───────────────────────────────────────────────
def equity_curve(rows):
    eq = 1.0
    out = []
    for r in rows:
        if r["monthly_ret"] is not None:
            eq *= 1 + r["monthly_ret"]
        r = dict(r)
        r["equity"] = eq
        out.append(r)
    return out

for n in STRATS:
    strat_rows[n] = equity_curve(strat_rows[n])

spmo_eq   = 1.0
spmo_rows = []
for month, _, _ in bounds:
    ret = spmo_monthly.get(month)
    if ret is not None:
        spmo_eq *= 1 + ret
    spmo_rows.append({"month": month, "monthly_ret": ret, "equity": spmo_eq})

# ── 7. Annual summary ──────────────────────────────────────────────────────
def annual_stats(rows, label):
    df = pd.DataFrame(rows)
    df["year"] = df["month"].str[:4]
    annual = {}
    for yr, grp in df.groupby("year"):
        rets  = grp["monthly_ret"].dropna()
        eq_s  = (1 + rets).prod() - 1
        eq_e  = grp["equity"].iloc[-1]
        annual[yr] = {"label": label, "year": yr,
                      "annual_ret": eq_s, "end_equity": eq_e,
                      "months": len(rets), "wins": (rets > 0).sum(),
                      "max_dd": rets.min()}
    return annual

stats = {}
for n in STRATS:
    stats[f"Top-{n}"] = annual_stats(strat_rows[n], f"Top-{n}")
stats["SPMO"] = annual_stats(spmo_rows, "SPMO")

# ── 8. Print results ───────────────────────────────────────────────────────
years = ["2020","2021","2022","2023","2024"]
labels = [f"Top-{n}" for n in STRATS] + ["SPMO"]

print("\n" + "=" * 72)
print("  ANNUAL RETURNS COMPARISON  (equal-weight, open-to-open)")
print("  Universe: S&P 500 point-in-time  |  Score: Close[t-21]/Close[t-126]-1")
print("=" * 72)
print(f"{'Strategy':<10}", end="")
for yr in years:
    print(f"  {yr:>8}", end="")
print(f"  {'Total':>8}  {'CAGR':>6}")
print("-" * 72)

for lbl in labels:
    s = stats[lbl]
    total_eq = list(s.values())[-1]["end_equity"] if s else 1.0
    total_ret = total_eq - 1
    n_years   = len(years)
    cagr      = (total_eq ** (1/n_years) - 1) if total_eq > 0 else 0
    print(f"{lbl:<10}", end="")
    for yr in years:
        r = s.get(yr, {}).get("annual_ret")
        if r is not None:
            print(f"  {r*100:>7.1f}%", end="")
        else:
            print(f"  {'?':>8}", end="")
    print(f"  {total_ret*100:>7.1f}%  {cagr*100:>5.1f}%")

print("-" * 72)

# Monthly detail per strategy
for n in STRATS:
    print(f"\n── Top-{n} Monthly Detail ──────────────────────────────────────────────")
    print(f"{'Month':<10} {'Tickers':<30} {'Ret%':>8} {'Equity':>9}")
    print("-" * 60)
    for r in strat_rows[n]:
        tk_str = ", ".join(r.get("tickers", []))
        ret    = r["monthly_ret"]
        ret_s  = f"{ret*100:.2f}%" if ret is not None else "?"
        print(f"{r['month']:<10} {tk_str:<30} {ret_s:>8} {r['equity']:.4f}x")

# ── 9. Save Excel ──────────────────────────────────────────────────────────
out_path = "sp500_top123_vs_spmo.xlsx"
with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    # Annual summary sheet
    ann_rows = []
    for lbl in labels:
        for yr in years:
            s = stats[lbl].get(yr, {})
            ann_rows.append({
                "Strategy": lbl, "Year": yr,
                "Annual Return %": round(s.get("annual_ret",0)*100, 2) if s else None,
                "End Equity": round(s.get("end_equity",1), 4) if s else None,
                "Win Months": s.get("wins"),
                "Worst Month %": round(s.get("max_dd",0)*100, 2) if s else None,
            })
    pd.DataFrame(ann_rows).to_excel(writer, sheet_name="Annual Summary", index=False)

    # Monthly detail per strategy
    for n in STRATS:
        rows_out = []
        for r in strat_rows[n]:
            rows_out.append({
                "Month":       r["month"],
                "Tickers":     ", ".join(r.get("tickers",[])),
                "Scores":      ", ".join(f"{s*100:.1f}%" for s in r.get("scores",[])),
                "Monthly Ret": round(r["monthly_ret"]*100, 2) if r["monthly_ret"] is not None else None,
                "Equity":      round(r["equity"], 6),
            })
        pd.DataFrame(rows_out).to_excel(writer, sheet_name=f"Top-{n} Monthly", index=False)

    # SPMO sheet
    spmo_out = [{"Month": r["month"],
                 "Monthly Ret %": round(r["monthly_ret"]*100, 2) if r["monthly_ret"] else None,
                 "Equity": round(r["equity"], 6)} for r in spmo_rows]
    pd.DataFrame(spmo_out).to_excel(writer, sheet_name="SPMO Monthly", index=False)

print(f"\n  Saved: {out_path}")
print("=" * 72)
