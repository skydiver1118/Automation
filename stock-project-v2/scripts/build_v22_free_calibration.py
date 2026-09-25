#!/usr/bin/env python3
"""Build free-data point-in-time Multi-Bagger calibration cohorts.

Primary fundamentals: SEC Financial Statement Data Sets (FSDS).
Prices/outcomes: user-supplied free daily-price extract (e.g. Stooq) normalized to the
documented schema. This script fails closed on unverifiable terminal outcomes.
"""
from __future__ import annotations
import argparse, io, json, math, re, zipfile
from dataclasses import dataclass
from pathlib import Path
from urllib.request import Request, urlopen
import pandas as pd

SEC_UA="skydiver1118 Multi-Bagger research contact via GitHub repository"
TAGS={
 "revenue":["Revenues","RevenueFromContractWithCustomerExcludingAssessedTax","SalesRevenueNet"],
 "operating_income":["OperatingIncomeLoss"],
 "net_income":["NetIncomeLoss","ProfitLoss"],
 "cash":["CashAndCashEquivalentsAtCarryingValue","CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"],
 "debt":["LongTermDebtAndFinanceLeaseObligationsCurrent","LongTermDebtCurrent","LongTermDebtNoncurrent","LongTermDebt"],
 "cfo":["NetCashProvidedByUsedInOperatingActivities"],
 "capex":["PaymentsToAcquirePropertyPlantAndEquipment"],
 "shares":["CommonStockSharesOutstanding"],
}

def fetch_zip(url:str)->zipfile.ZipFile:
    req=Request(url,headers={"User-Agent":SEC_UA,"Accept-Encoding":"gzip, deflate"})
    with urlopen(req,timeout=60) as h: data=h.read()
    return zipfile.ZipFile(io.BytesIO(data))

def sec_quarter_url(year:int,q:int)->str:
    return f"https://www.sec.gov/files/dera/data/financial-statement-data-sets/{year}q{q}.zip"

def read_fsds(year:int,q:int,cache:Path)->dict[str,pd.DataFrame]:
    cache.mkdir(parents=True,exist_ok=True); zpath=cache/f"{year}q{q}.zip"
    if not zpath.exists():
        z=fetch_zip(sec_quarter_url(year,q)); zpath.write_bytes(z.fp.getvalue() if hasattr(z.fp,"getvalue") else b"")
        if zpath.stat().st_size==0:
            # robust fallback when ZipExtFile backing object is not BytesIO
            req=Request(sec_quarter_url(year,q),headers={"User-Agent":SEC_UA})
            with urlopen(req,timeout=60) as h:zpath.write_bytes(h.read())
    with zipfile.ZipFile(zpath) as z:
        def tab(name):return pd.read_csv(z.open(name),sep="\t",low_memory=False)
        return {k:tab(k+".txt") for k in ["sub","num","pre"]}

def formation_quarters(start=2010,end=2021):
    # June 30 formation uses filings submitted no later than June 30; Q2 FSDS contains them.
    return [(y,2,f"{y}-06-30") for y in range(start,end+1)]

def latest_fact(num:pd.DataFrame,adsh:str,tags:list[str],filed:str,instant:bool=False):
    x=num[(num.adsh==adsh)&(num.tag.isin(tags))].copy()
    if x.empty:return None
    x=x[pd.to_datetime(x.ddate,format="%Y%m%d",errors="coerce")<=pd.Timestamp(filed)]
    if x.empty:return None
    # Prefer USD (shares for share tags), then latest period end. FSDS values are already as filed.
    if "uom" in x:
        pref=x[x.uom.isin(["USD","shares"])]
        if not pref.empty:x=pref
    x=x.sort_values(["ddate","qtrs"],na_position="first")
    v=x.iloc[-1].value
    return float(v) if pd.notna(v) else None

def build_snapshot(frames:dict,formation_date:str)->pd.DataFrame:
    sub,num=frames["sub"],frames["num"]
    sub=sub[pd.to_datetime(sub.filed.astype(str),format="%Y%m%d",errors="coerce")<=pd.Timestamp(formation_date)].copy()
    # one latest filing per CIK available at formation date
    sub=sub.sort_values(["cik","filed"]).groupby("cik",as_index=False).tail(1)
    rows=[]
    for s in sub.itertuples():
        adsh=s.adsh; filed=str(int(s.filed))
        vals={k:latest_fact(num,adsh,v,filed,k in ["cash","debt","shares"]) for k,v in TAGS.items()}
        cfo,capex=vals["cfo"],vals["capex"]
        fcf=(cfo-abs(capex)) if cfo is not None and capex is not None else None
        rows.append({"formation_date":formation_date,"cik":int(s.cik),"ticker":getattr(s,"instance",None),
          "company":s.name,"sic":getattr(s,"sic",None),"filed":filed,**vals,"fcf":fcf,
          "fundamentals_point_in_time":True})
    return pd.DataFrame(rows)

def normalize_price_file(path:Path)->pd.DataFrame:
    p=pd.read_csv(path)
    need={"ticker","date","close"}
    if not need<=set(p.columns):raise ValueError(f"price file requires {sorted(need)}")
    p["date"]=pd.to_datetime(p.date);p["ticker"]=p.ticker.astype(str).str.upper()
    if "adj_close" not in p:p["adj_close"]=p["close"]
    if "terminal_value_verified" not in p:p["terminal_value_verified"]=False
    return p.sort_values(["ticker","date"])

def attach_outcomes(cohort:pd.DataFrame,prices:pd.DataFrame)->pd.DataFrame:
    out=cohort.copy()
    out["price_history_complete"]=False;out["terminal_value_verified"]=False
    out["outcome_usable"]=False;out["multiple_3y"]=math.nan;out["multiple_5y"]=math.nan
    for i,r in out.iterrows():
        t=str(r.ticker).upper(); px=prices[prices.ticker==t]
        if px.empty:continue
        start=pd.Timestamp(r.formation_date)
        def nearest(dt):
            z=px[(px.date>=dt-pd.Timedelta(days=7))&(px.date<=dt+pd.Timedelta(days=7))]
            return None if z.empty else z.iloc[(z.date-dt).abs().argmin()]
        a,b,c=nearest(start),nearest(start+pd.DateOffset(years=3)),nearest(start+pd.DateOffset(years=5))
        if a is None:continue
        out.at[i,"price_history_complete"]=b is not None and c is not None
        if b is not None:out.at[i,"multiple_3y"]=float(b.adj_close/a.adj_close)
        if c is not None:
            out.at[i,"multiple_5y"]=float(c.adj_close/a.adj_close)
            out.at[i,"outcome_usable"]=True
        else:
            # Missing terminal price is NEVER interpreted as zero.
            term=bool(px.terminal_value_verified.iloc[-1])
            out.at[i,"terminal_value_verified"]=term
    return out

def summarize(df:pd.DataFrame)->pd.DataFrame:
    d=df[df.outcome_usable & df.multiple_5y.notna()].copy()
    if d.empty:return pd.DataFrame()
    if "market_cap" not in d:return pd.DataFrame({"warning":["market_cap unavailable; merge a PIT market-cap source before size calibration"]})
    bins=[0,5e8,1e9,5e9,2e10,5e10,1e11,2.5e11,5e11,1e12,float("inf")]
    labels=["<$500M","$500M-$1B","$1-5B","$5-20B","$20-50B","$50-100B","$100-250B","$250-500B","$500B-$1T",">$1T"]
    d["size_bucket"]=pd.cut(d.market_cap,bins=bins,labels=labels,right=False)
    return d.groupby("size_bucket",observed=False).agg(N=("ticker","size"),hit_3x=("multiple_5y",lambda x:(x>=3).mean()),
      hit_5x=("multiple_5y",lambda x:(x>=5).mean()),median_5y=("multiple_5y","median"),mean_5y=("multiple_5y","mean")).reset_index()

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--cache",type=Path,default=Path(".cache/sec_fsds"))
    ap.add_argument("--output",type=Path,default=Path("stock-project-v2/data/multi_bagger/v22_free"))
    ap.add_argument("--prices",type=Path);ap.add_argument("--start",type=int,default=2010);ap.add_argument("--end",type=int,default=2021)
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True);all_rows=[]
    for y,q,d in formation_quarters(a.start,a.end):
        snap=build_snapshot(read_fsds(y,q,a.cache),d);all_rows.append(snap)
    cohort=pd.concat(all_rows,ignore_index=True);cohort.to_csv(a.output/"sec_pit_cohorts.csv",index=False)
    meta={"source":"SEC Financial Statement Data Sets","formation_dates":[f"{y}-06-30" for y in range(a.start,a.end+1)],
      "point_in_time":True,"prices_attached":bool(a.prices),"calibrated_probability_5x":False}
    if a.prices:
        cohort=attach_outcomes(cohort,normalize_price_file(a.prices));cohort.to_csv(a.output/"cohorts_with_outcomes.csv",index=False)
        summarize(cohort).to_csv(a.output/"size_bucket_summary.csv",index=False)
    (a.output/"metadata.json").write_text(json.dumps(meta,indent=2)+"\n")
    print(json.dumps({"rows":len(cohort),**meta},indent=2))

if __name__=="__main__":main()
