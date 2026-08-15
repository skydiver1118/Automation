"""
Top-1, 2, 3 within SPMO-Replicated Universe  2020–2024
=======================================================
Run: pip install yfinance pandas openpyxl requests
     python spmo_universe_top123.py

Universe at each signal date: top-100 S&P 500 stocks by skip-momentum score
Strategy: equal-weight top-N within that pool, monthly rebalance
Benchmark: SPMO ETF
"""

import io, warnings, requests
import pandas as pd
import numpy as np
import yfinance as yf
warnings.filterwarnings("ignore")

SPMO_UNIVERSE_SIZE = 100
TOP_NS   = [1, 2, 3]
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

add_col = [c for c in since_df.columns if 'add'   in c.lower()]
rem_col = [c for c in since_df.columns if 'remov' in c.lower() or 'delet' in c.lower()]
dc2     = since_df.columns[0]
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

print(f"Downloading prices for {len(all_tickers)} tickers (3–5 min) …")
raw = yf.download(
    sorted(all_tickers),
    start="2019-06-01",   # need 126td lookback before Jan 2020
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

# ── 4. Run all strategies in one pass ─────────────────────────────────────
# For each month, compute scores once, then slice top-N for each strategy
all_rows = {n: [] for n in TOP_NS}
spmo_rows = []

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
        for n in TOP_NS:
            all_rows[n].append(dict(month=month, trade_date=trade_date,
                                    tickers=[], monthly_ret=None))
        spmo_rows.append(dict(month=month, spmo_ret=None))
        continue

    # SPMO-replicated universe: top-100
    ranked_all = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    pool       = ranked_all[:SPMO_UNIVERSE_SIZE]

    def get_ret(tk):
        entry = open_df.loc[trade_date, tk] if tk in open_df.columns else np.nan
        if is_last:
            avail = close_df.loc[close_df.index >= trade_date, tk].dropna()
            ex = float(avail.iloc[-1]) if len(avail) else np.nan
        else:
            ex = open_df.loc[next_trade, tk] if tk in open_df.columns else np.nan
        if pd.notna(entry) and pd.notna(ex) and entry > 0:
            return ex / entry - 1
        return None

    # Pre-compute returns for pool members we'll need
    pool_rets = {}
    for tk, sc in pool[:max(TOP_NS)]:
        pool_rets[tk] = get_ret(tk)

    for n in TOP_NS:
        top_n   = [(tk, sc) for tk, sc in pool[:n]]
        rets    = [pool_rets[tk] for tk, _ in top_n if pool_rets.get(tk) is not None]
        monthly = float(np.mean(rets)) if rets else None
        all_rows[n].append(dict(
            month=month, trade_date=trade_date,
            tickers=[tk for tk, _ in top_n],
            scores=[round(sc, 4) for _, sc in top_n],
            monthly_ret=monthly,
        ))

    # SPMO ETF benchmark
    entry_s = open_df.loc[trade_date, "SPMO"] if "SPMO" in open_df.columns else np.nan
    if is_last:
        avail = close_df.loc[close_df.index >= trade_date, "SPMO"].dropna()
        ex_s  = float(avail.iloc[-1]) if len(avail) else np.nan
    else:
        ex_s = open_df.loc[next_trade, "SPMO"] if "SPMO" in open_df.columns else np.nan
    spmo_ret = (float(ex_s) / float(entry_s) - 1
                if pd.notna(entry_s) and pd.notna(ex_s) else None)
    spmo_rows.append(dict(month=month, spmo_ret=spmo_ret))

# ── 5. Equity curves ───────────────────────────────────────────────────────
def build_equity(rows, ret_key="monthly_ret"):
    eq = 1.0
    for r in rows:
        ret = r.get(ret_key)
        if ret is not None:
            eq *= 1 + ret
        r["equity"] = round(eq, 6)
    return rows

for n in TOP_NS:
    all_rows[n] = build_equity(all_rows[n])

spmo_eq = 1.0
for r in spmo_rows:
    if r["spmo_ret"] is not None:
        spmo_eq *= 1 + r["spmo_ret"]
    r["spmo_equity"] = round(spmo_eq, 6)

# Merge spmo equity into strategy rows for easy printing
spmo_by_month = {r["month"]: r for r in spmo_rows}
for n in TOP_NS:
    for r in all_rows[n]:
        sr = spmo_by_month.get(r["month"], {})
        r["spmo_ret"]    = sr.get("spmo_ret")
        r["spmo_equity"] = sr.get("spmo_equity")

# ── 6. Annual summary ──────────────────────────────────────────────────────
def annual_stats(rows, ret_key="monthly_ret"):
    df = pd.DataFrame(rows)
    df["year"] = df["month"].str[:4]
    out = {}
    for yr, grp in df.groupby("year"):
        rets = grp[ret_key].dropna()
        out[yr] = {
            "annual_ret": (1 + rets).prod() - 1,
            "win":        int((rets > 0).sum()),
            "n":          int(len(rets)),
            "worst":      float(rets.min()) if len(rets) else 0,
            "best":       float(rets.max()) if len(rets) else 0,
        }
    return out

stats = {}
for n in TOP_NS:
    stats[f"Top-{n}"] = annual_stats(all_rows[n])
stats["SPMO"] = annual_stats(spmo_rows, ret_key="spmo_ret")

years = ["2020","2021","2022","2023","2024"]

# ── 7. Print results ───────────────────────────────────────────────────────
print("\n" + "=" * 85)
print("  TOP-N WITHIN SPMO UNIVERSE  |  2020–2024  |  S&P 500 point-in-time")
print("=" * 85)
print(f"\n{'Strategy':<10}", end="")
for yr in years:
    print(f"  {yr:>8}", end="")
total_eq_all = {}
for lbl in [f"Top-{n}" for n in TOP_NS] + ["SPMO"]:
    s = stats[lbl]
    eqs = []
    eq  = 1.0
    for yr in years:
        eq *= 1 + s.get(yr, {}).get("annual_ret", 0)
        eqs.append(eq)
    total_eq_all[lbl] = eq
print(f"  {'Total':>8}  {'CAGR':>6}  {'Best Mo':>8}  {'Worst Mo':>9}")
print("-" * 85)

for lbl in [f"Top-{n}" for n in TOP_NS] + ["SPMO"]:
    s  = stats[lbl]
    eq = 1.0
    print(f"{lbl:<10}", end="")
    for yr in years:
        r = s.get(yr, {}).get("annual_ret", 0)
        eq *= 1 + r
        print(f"  {r*100:>7.1f}%", end="")
    total_ret = eq - 1
    cagr      = eq ** (1/5) - 1

    # best/worst month across all years
    all_rets_key = "monthly_ret" if lbl != "SPMO" else "spmo_ret"
    if lbl != "SPMO":
        n_val  = int(lbl.split("-")[1])
        rets   = [r["monthly_ret"] for r in all_rows[n_val] if r["monthly_ret"] is not None]
    else:
        rets   = [r["spmo_ret"] for r in spmo_rows if r["spmo_ret"] is not None]
    best  = max(rets) if rets else 0
    worst = min(rets) if rets else 0
    print(f"  {total_ret*100:>7.1f}%  {cagr*100:>5.1f}%  {best*100:>7.1f}%  {worst*100:>8.1f}%")

print("-" * 85)

# Win-month count table
print(f"\n{'Strategy':<10}", end="")
for yr in years:
    print(f"  {yr:>8}", end="")
print(f"  {'Total wins':>10}")
print("-" * 70)
for lbl in [f"Top-{n}" for n in TOP_NS] + ["SPMO"]:
    s = stats[lbl]
    total_wins = 0
    total_months = 0
    print(f"{lbl:<10}", end="")
    for yr in years:
        w = s.get(yr, {}).get("win", 0)
        n = s.get(yr, {}).get("n", 0)
        total_wins   += w
        total_months += n
        print(f"  {w:>3}/{n:<3}", end="")
    print(f"  {total_wins:>3}/{total_months}")

# Detailed monthly tables
for n in TOP_NS:
    print(f"\n{'='*75}")
    print(f"  TOP-{n} MONTHLY DETAIL")
    print(f"{'='*75}")
    print(f"{'Month':<10} {'Tickers & Scores':<35} {'Ret%':>8} {'SPMO%':>8} {'vs':>7} {'Equity':>9}")
    print("-" * 75)
    for r in all_rows[n]:
        tk_str = ", ".join(f"{t}({s*100:.0f}%)" for t, s in zip(r["tickers"], r.get("scores",[])))
        ret_s  = f"{r['monthly_ret']*100:.2f}%" if r["monthly_ret"] is not None else "?"
        spmo_s = f"{r['spmo_ret']*100:.2f}%"   if r["spmo_ret"]   is not None else "?"
        diff   = ((r["monthly_ret"] or 0) - (r["spmo_ret"] or 0)) * 100
        diff_s = f"{diff:+.2f}pp"
        eq_s   = f"{r['equity']:.4f}x"
        print(f"{r['month']:<10} {tk_str:<35} {ret_s:>8} {spmo_s:>8} {diff_s:>8} {eq_s:>9}")

# ── 8. Save Excel ──────────────────────────────────────────────────────────
out_path = "spmo_universe_top123_2020_2024.xlsx"
with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    # Annual summary
    ann_rows_out = []
    for lbl in [f"Top-{n}" for n in TOP_NS] + ["SPMO"]:
        s = stats[lbl]
        row_out = {"Strategy": lbl}
        eq = 1.0
        for yr in years:
            r = s.get(yr, {}).get("annual_ret", 0)
            eq *= 1 + r
            row_out[f"{yr} Return %"] = round(r * 100, 2)
            row_out[f"{yr} Wins"]     = s.get(yr, {}).get("win", 0)
        row_out["Total Return %"] = round((eq - 1) * 100, 2)
        row_out["CAGR %"]         = round((eq ** 0.2 - 1) * 100, 2)
        ann_rows_out.append(row_out)
    pd.DataFrame(ann_rows_out).to_excel(writer, sheet_name="Annual Summary", index=False)

    # Monthly detail per strategy
    for n in TOP_NS:
        out = []
        for r in all_rows[n]:
            out.append({
                "Month":       r["month"],
                "Tickers":     ", ".join(r.get("tickers", [])),
                "Scores":      ", ".join(f"{s*100:.1f}%" for s in r.get("scores", [])),
                "Monthly Ret%": round(r["monthly_ret"]*100, 2) if r["monthly_ret"] else None,
                "SPMO Ret%":   round(r["spmo_ret"]*100, 2)    if r["spmo_ret"]    else None,
                "vs SPMO pp":  round(((r["monthly_ret"] or 0)-(r["spmo_ret"] or 0))*100, 2),
                "Equity":      r["equity"],
                "SPMO Equity": r.get("spmo_equity"),
            })
        pd.DataFrame(out).to_excel(writer, sheet_name=f"Top-{n} Monthly", index=False)

    # SPMO monthly
    pd.DataFrame([{
        "Month": r["month"],
        "SPMO Ret%": round(r["spmo_ret"]*100,2) if r["spmo_ret"] else None,
        "SPMO Equity": r["spmo_equity"],
    } for r in spmo_rows]).to_excel(writer, sheet_name="SPMO Monthly", index=False)

print(f"\n\nSaved: {out_path}")
print("=" * 85)
