"""
Top-2 SPMO Universe Strategy with 8% Intra-Month Stop-Loss
===========================================================
Run: pip install yfinance pandas openpyxl requests
     python spmo_top2_stoploss.py

Stop-loss logic
---------------
  At each trading day within the month, check each holding.
  If price drops 8% below the entry open → sell at that day's close.
  Cash earns 0% for the rest of the month.
  At month end, redeploy into next month's top-2 picks as normal.

  If both positions stop out, the strategy is flat for the remainder
  of that month.

Data needed: daily LOW prices to detect intraday breaches.
  We use daily CLOSE as a proxy (conservative — real stop would use low).
  Alternatively, we check if the daily LOW breached the stop level.
"""

import io, warnings, requests
import pandas as pd
import numpy as np
import yfinance as yf
warnings.filterwarnings("ignore")

SPMO_UNIVERSE_SIZE = 100
TOP_N              = 2
STOP_LOSS          = 0.15    # 15% below entry open
START_DT           = "2020-01-01"
END_DT             = "2024-12-31"

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

# ── 2. Download prices (OHLC) ─────────────────────────────────────────────
all_tickers = set()
for _, m in timeline:
    all_tickers.update(m)
all_tickers.add("SPMO")

print(f"Downloading prices for {len(all_tickers)} tickers (3-5 min) …")
raw = yf.download(
    sorted(all_tickers),
    start="2019-06-01",
    end="2025-01-05",
    auto_adjust=True,
    progress=True,
)
close_df = raw["Close"]
open_df  = raw["Open"]
low_df   = raw["Low"]   # for stop-loss detection

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
            out.append((str(m), signal_date, trade_date, days))
    return out

bounds = month_boundaries(td, START_DT, END_DT)
print(f"Strategy months: {len(bounds)}")

# ── 4. Stop-loss return calculator ────────────────────────────────────────
def calc_return_with_stoploss(tk, entry_open, month_days, exit_open, is_last):
    """
    Simulate holding tk from entry_open through the month.
    Stop trigger: daily LOW drops 8% below entry_open.
    If triggered, sell at that day's CLOSE (conservative proxy).
    Otherwise, exit at next month open (or latest close if last month).
    Returns (actual_return, stopped_out, stop_date)
    """
    stop_price = entry_open * (1 - STOP_LOSS)

    if tk not in low_df.columns or tk not in close_df.columns:
        return None, False, None

    # Check each trading day in the month (starting day after entry)
    for day in month_days[1:]:  # skip entry day itself
        if day not in low_df.index:
            continue
        daily_low = low_df.loc[day, tk]
        if pd.isna(daily_low):
            continue
        if float(daily_low) <= stop_price:
            # Stopped out — sell at close of that day
            exit_price = close_df.loc[day, tk]
            if pd.isna(exit_price):
                exit_price = stop_price
            ret = float(exit_price) / entry_open - 1
            return ret, True, day

    # No stop triggered — normal exit
    if is_last:
        avail = close_df.loc[close_df.index >= month_days[0], tk].dropna()
        ep = float(avail.iloc[-1]) if len(avail) else np.nan
    else:
        ep = open_df.loc[exit_open, tk] if exit_open in open_df.index and tk in open_df.columns else np.nan

    if pd.notna(ep) and entry_open > 0:
        return ep / entry_open - 1, False, None
    return None, False, None

# ── 5. Run strategy ────────────────────────────────────────────────────────
rows_sl  = []   # with stop-loss
rows_no  = []   # without stop-loss (baseline for direct comparison)

for i, (month, signal_date, trade_date, month_days) in enumerate(bounds):
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
        continue

    ranked_all = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    pool       = ranked_all[:SPMO_UNIVERSE_SIZE]
    top2       = pool[:TOP_N]

    # SPMO ETF benchmark return
    spmo_entry = open_df.loc[trade_date, "SPMO"] if "SPMO" in open_df.columns else np.nan
    if is_last:
        avail = close_df.loc[close_df.index >= trade_date, "SPMO"].dropna()
        spmo_exit = float(avail.iloc[-1]) if len(avail) else np.nan
    else:
        spmo_exit = open_df.loc[next_trade, "SPMO"] if "SPMO" in open_df.columns else np.nan
    spmo_ret = (float(spmo_exit) / float(spmo_entry) - 1
                if pd.notna(spmo_entry) and pd.notna(spmo_exit) else None)

    # ── WITH stop-loss ──
    sl_rets  = []
    sl_notes = []
    for tk, sc in top2:
        entry = open_df.loc[trade_date, tk] if tk in open_df.columns and trade_date in open_df.index else np.nan
        if pd.isna(entry) or entry <= 0:
            continue
        ret, stopped, stop_day = calc_return_with_stoploss(
            tk, float(entry), month_days, next_trade, is_last)
        if ret is not None:
            sl_rets.append(ret)
            note = f"STOP {stop_day.date() if stop_day else ''}" if stopped else "HELD"
            sl_notes.append(f"{tk}:{note}({ret*100:.1f}%)")

    sl_monthly = float(np.mean(sl_rets)) if sl_rets else None

    # ── WITHOUT stop-loss (baseline) ──
    no_rets = []
    for tk, sc in top2:
        entry = open_df.loc[trade_date, tk] if tk in open_df.columns and trade_date in open_df.index else np.nan
        if is_last:
            avail = close_df.loc[close_df.index >= trade_date, tk].dropna()
            ex = float(avail.iloc[-1]) if len(avail) else np.nan
        else:
            ex = open_df.loc[next_trade, tk] if tk in open_df.columns else np.nan
        if pd.notna(entry) and pd.notna(ex) and entry > 0:
            no_rets.append(ex / entry - 1)
    no_monthly = float(np.mean(no_rets)) if no_rets else None

    rows_sl.append(dict(
        month=month, trade_date=trade_date,
        tickers=[tk for tk, _ in top2],
        scores=[round(sc, 4) for _, sc in top2],
        sl_notes=sl_notes,
        monthly_ret=sl_monthly,
        no_sl_ret=no_monthly,
        spmo_ret=spmo_ret,
    ))
    rows_no.append(dict(month=month, monthly_ret=no_monthly, spmo_ret=spmo_ret))

# ── 6. Build equity curves ─────────────────────────────────────────────────
eq_sl, eq_no, eq_sp = 1.0, 1.0, 1.0
for r in rows_sl:
    if r["monthly_ret"]  is not None: eq_sl *= 1 + r["monthly_ret"]
    if r["no_sl_ret"]    is not None: eq_no *= 1 + r["no_sl_ret"]
    if r["spmo_ret"]     is not None: eq_sp *= 1 + r["spmo_ret"]
    r["eq_sl"] = round(eq_sl, 6)
    r["eq_no"] = round(eq_no, 6)
    r["eq_sp"] = round(eq_sp, 6)

# ── 7. Annual summary ──────────────────────────────────────────────────────
def ann(rows, key):
    df = pd.DataFrame(rows)
    df["year"] = df["month"].str[:4]
    out = {}
    for yr, grp in df.groupby("year"):
        rets = grp[key].dropna()
        out[yr] = {
            "ret":   (1 + rets).prod() - 1,
            "wins":  int((rets > 0).sum()),
            "n":     int(len(rets)),
            "best":  float(rets.max()) if len(rets) else 0,
            "worst": float(rets.min()) if len(rets) else 0,
        }
    return out

years = ["2020","2021","2022","2023","2024"]
ann_sl   = ann(rows_sl, "monthly_ret")
ann_no   = ann(rows_sl, "no_sl_ret")
ann_spmo = ann(rows_sl, "spmo_ret")

# ── 8. Print ───────────────────────────────────────────────────────────────
print("\n" + "="*80)
print("  TOP-2 WITHIN SPMO UNIVERSE  |  15% STOP-LOSS vs NO STOP  |  2020–2024")
print("="*80)

print(f"\n{'Strategy':<18}", end="")
for yr in years: print(f"  {yr:>8}", end="")
total_eqs = {}
for lbl, a in [("Top-2 +SL", ann_sl), ("Top-2 NoSL", ann_no), ("SPMO", ann_spmo)]:
    eq = 1.0
    for yr in years: eq *= 1 + a.get(yr,{}).get("ret",0)
    total_eqs[lbl] = eq
print(f"  {'Total':>8}  {'CAGR':>6}  {'Best Mo':>8}  {'Worst Mo':>9}")
print("-"*80)

for lbl, a in [("Top-2 +SL", ann_sl), ("Top-2 NoSL", ann_no), ("SPMO", ann_spmo)]:
    eq = 1.0
    print(f"{lbl:<18}", end="")
    best_all, worst_all = -999, 999
    for yr in years:
        r = a.get(yr,{}).get("ret",0)
        eq *= 1 + r
        best_all  = max(best_all,  a.get(yr,{}).get("best",0))
        worst_all = min(worst_all, a.get(yr,{}).get("worst",0))
        print(f"  {r*100:>7.1f}%", end="")
    total_ret = eq - 1
    cagr      = eq**(1/5) - 1
    print(f"  {total_ret*100:>7.1f}%  {cagr*100:>5.1f}%  {best_all*100:>7.1f}%  {worst_all*100:>8.1f}%")

print("-"*80)

# Win months
print(f"\n{'Strategy':<18}", end="")
for yr in years: print(f"  {yr:>8}", end="")
print(f"  {'Total':>8}")
print("-"*60)
for lbl, a in [("Top-2 +SL", ann_sl), ("Top-2 NoSL", ann_no), ("SPMO", ann_spmo)]:
    tw, tm = 0, 0
    print(f"{lbl:<18}", end="")
    for yr in years:
        w = a.get(yr,{}).get("wins",0)
        n = a.get(yr,{}).get("n",0)
        tw += w; tm += n
        print(f"  {w:>3}/{n:<3}", end="")
    print(f"  {tw:>3}/{tm}")

# Monthly detail
print(f"\n{'='*90}")
print(f"  TOP-2 + 15% STOP-LOSS  MONTHLY DETAIL")
print(f"{'='*90}")
print(f"{'Month':<10} {'Tickers':<25} {'SL Ret':>8} {'NoSL':>8} {'SPMO':>8} {'vs NoSL':>8} {'Eq(SL)':>9}  Notes")
print("-"*90)

for r in rows_sl:
    tk_str  = ", ".join(r["tickers"])
    slr     = f"{r['monthly_ret']*100:.2f}%"  if r["monthly_ret"]  is not None else "?"
    nor     = f"{r['no_sl_ret']*100:.2f}%"    if r["no_sl_ret"]    is not None else "?"
    spr     = f"{r['spmo_ret']*100:.2f}%"     if r["spmo_ret"]     is not None else "?"
    diff    = ((r["monthly_ret"] or 0) - (r["no_sl_ret"] or 0)) * 100
    diff_s  = f"{diff:+.2f}pp"
    eq_s    = f"{r['eq_sl']:.4f}x"
    notes   = " | ".join(r.get("sl_notes",[]))
    print(f"{r['month']:<10} {tk_str:<25} {slr:>8} {nor:>8} {spr:>8} {diff_s:>8} {eq_s:>9}  {notes}")

print(f"\n  Final equity  With SL: {eq_sl:.4f}x  |  No SL: {eq_no:.4f}x  |  SPMO: {eq_sp:.4f}x")
print(f"  Total return  With SL: {(eq_sl-1)*100:.2f}%  |  No SL: {(eq_no-1)*100:.2f}%  |  SPMO: {(eq_sp-1)*100:.2f}%")

# ── 9. Save Excel ──────────────────────────────────────────────────────────
out_path = "spmo_top2_stoploss15_2020_2024.xlsx"
with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    # Annual summary
    ann_out = []
    for lbl, a in [("Top-2 +8%SL", ann_sl), ("Top-2 NoSL", ann_no), ("SPMO", ann_spmo)]:
        row = {"Strategy": lbl}
        eq = 1.0
        for yr in years:
            r = a.get(yr,{}).get("ret",0)
            eq *= 1 + r
            row[f"{yr} Ret%"]  = round(r*100, 2)
            row[f"{yr} Wins"]  = a.get(yr,{}).get("wins",0)
        row["Total Ret%"] = round((eq-1)*100, 2)
        row["CAGR%"]      = round((eq**0.2-1)*100, 2)
        ann_out.append(row)
    pd.DataFrame(ann_out).to_excel(writer, sheet_name="Annual Summary", index=False)

    # Monthly detail
    monthly_out = []
    for r in rows_sl:
        monthly_out.append({
            "Month":        r["month"],
            "Tickers":      ", ".join(r["tickers"]),
            "Scores":       ", ".join(f"{s*100:.1f}%" for s in r["scores"]),
            "SL Notes":     " | ".join(r.get("sl_notes",[])),
            "Ret% (SL)":    round(r["monthly_ret"]*100,2) if r["monthly_ret"] else None,
            "Ret% (NoSL)":  round(r["no_sl_ret"]*100,2)  if r["no_sl_ret"]   else None,
            "SPMO Ret%":    round(r["spmo_ret"]*100,2)    if r["spmo_ret"]    else None,
            "vs NoSL pp":   round(((r["monthly_ret"] or 0)-(r["no_sl_ret"] or 0))*100, 2),
            "Equity (SL)":  r["eq_sl"],
            "Equity (NoSL)":r["eq_no"],
            "SPMO Equity":  r["eq_sp"],
        })
    pd.DataFrame(monthly_out).to_excel(writer, sheet_name="Monthly Detail", index=False)

print(f"\n  Saved: {out_path}")
print("="*80)
