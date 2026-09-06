from __future__ import annotations

import json
import argparse
import hashlib
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import pandas_market_calendars as mcal
import yfinance as yf

ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "config.json").read_text())
TZ = ZoneInfo(CONFIG["refresh"]["timezone"])
TODAY = datetime.now(TZ).date()


def is_trading_day(day) -> bool:
    return not mcal.get_calendar("NYSE").schedule(start_date=day, end_date=day).empty


def pct_return(close: pd.Series, trading_days: int) -> float:
    s = close.dropna()
    if len(s) <= trading_days:
        return np.nan
    return float(s.iloc[-1] / s.iloc[-1-trading_days] - 1)


def rsi(close: pd.Series, n: int = 14) -> float:
    d = close.diff(); up = d.clip(lower=0).ewm(alpha=1/n, adjust=False).mean(); dn = (-d.clip(upper=0)).ewm(alpha=1/n, adjust=False).mean()
    return float((100 - 100/(1 + up/dn.replace(0, np.nan))).iloc[-1])


def macd(close: pd.Series):
    e12 = close.ewm(span=12, adjust=False).mean(); e26 = close.ewm(span=26, adjust=False).mean(); m = e12-e26; sig = m.ewm(span=9, adjust=False).mean()
    return float(m.iloc[-1]), float(sig.iloc[-1]), float((m-sig).iloc[-1])


def adx(high: pd.Series, low: pd.Series, close: pd.Series, n: int = 14) -> float:
    up = high.diff(); down = -low.diff(); plus_dm = up.where((up>down)&(up>0),0.0); minus_dm = down.where((down>up)&(down>0),0.0)
    tr = pd.concat([(high-low),(high-close.shift()).abs(),(low-close.shift()).abs()],axis=1).max(axis=1); atr = tr.ewm(alpha=1/n, adjust=False).mean()
    plus_di = 100*plus_dm.ewm(alpha=1/n,adjust=False).mean()/atr; minus_di = 100*minus_dm.ewm(alpha=1/n,adjust=False).mean()/atr
    dx = 100*(plus_di-minus_di).abs()/(plus_di+minus_di).replace(0,np.nan)
    return float(dx.ewm(alpha=1/n,adjust=False).mean().iloc[-1])


def dist_ma(close: pd.Series, n: int) -> float:
    ma = close.rolling(n).mean().iloc[-1]
    return float(close.iloc[-1]/ma-1) if pd.notna(ma) and ma else np.nan


def safe_info(t: yf.Ticker) -> dict:
    try: return t.get_info() or {}
    except Exception:
        try: return t.info or {}
        except Exception: return {}


def eps_revision_score(t: yf.Ticker) -> float:
    try:
        df=t.eps_revisions
        if df is None or df.empty:return np.nan
        vals=[]
        for _,row in df.iterrows():
            up=float(row.get("upLast30days",0) or 0)+.5*float(row.get("upLast7days",0) or 0); dn=float(row.get("downLast30Days",0) or 0)+.5*float(row.get("downLast7Days",0) or 0); total=up+dn
            if total>0:vals.append((up-dn)/total)
        return float(np.nanmean(vals)) if vals else np.nan
    except Exception:return np.nan


def revenue_growth_estimate(t: yf.Ticker) -> float:
    try:
        df=t.revenue_estimate
        if df is None or df.empty:return np.nan
        for idx in ["+1y","0y","+1q","0q"]:
            if idx in df.index and "growth" in df.columns and pd.notna(df.loc[idx,"growth"]):return float(df.loc[idx,"growth"])
    except Exception:pass
    return np.nan


def eps_growth_estimate(t: yf.Ticker) -> float:
    try:
        df=t.earnings_estimate
        if df is None or df.empty:return np.nan
        for idx in ["+1y","0y","+1q","0q"]:
            if idx in df.index and "growth" in df.columns and pd.notna(df.loc[idx,"growth"]):return float(df.loc[idx,"growth"])
    except Exception:pass
    return np.nan


def calc_roic_proxy(t: yf.Ticker) -> float:
    try:
        inc=t.income_stmt; bal=t.balance_sheet
        if inc is None or inc.empty or bal is None or bal.empty:return np.nan
        col=inc.columns[0]; bcol=bal.columns[0]; op=float(inc.loc["Operating Income",col]) if "Operating Income" in inc.index else np.nan
        pretax=float(inc.loc["Pretax Income",col]) if "Pretax Income" in inc.index else np.nan; tax=float(inc.loc["Tax Provision",col]) if "Tax Provision" in inc.index else np.nan
        tax_rate=np.clip(tax/pretax,0,.35) if pretax and np.isfinite(pretax) and np.isfinite(tax) else .21
        assets=float(bal.loc["Total Assets",bcol]) if "Total Assets" in bal.index else np.nan; curr=float(bal.loc["Current Liabilities",bcol]) if "Current Liabilities" in bal.index else 0.0
        keys=[k for k in ["Cash Cash Equivalents And Short Term Investments","Cash And Cash Equivalents"] if k in bal.index]; cash=float(bal.loc[keys[0],bcol]) if keys else 0.0; invested=assets-curr-cash
        return float(op*(1-tax_rate)/invested) if invested>0 and np.isfinite(op) else np.nan
    except Exception:return np.nan


def row_for(ticker: str, price_df: pd.DataFrame, bench_returns: dict) -> dict:
    asset_type = CONFIG.get("asset_types",{}).get(ticker,"Stock")
    t=yf.Ticker(ticker); p=price_df[ticker].dropna(how="all"); close,high,low,vol=p["Close"],p["High"],p["Low"],p["Volume"]; info=safe_info(t); m,ms,mh=macd(close)
    stock_ret={h:pct_return(close,d) for h,d in {"1M":21,"3M":63,"6M":126,"12M":252}.items()}; rs={}
    for h in stock_ret:
        rs[h]=np.nan if np.isnan(stock_ret[h]) else sum(w*(stock_ret[h]-bench_returns[b][h]) for b,w in CONFIG["benchmarks"].items() if not np.isnan(bench_returns[b][h]))
    market_cap = info.get("totalAssets",np.nan) if asset_type=="ETF" else info.get("marketCap",np.nan)
    base={"ticker":ticker,"asset_type":asset_type,"price":float(close.iloc[-1]),"market_cap":market_cap,"rs_1m":rs["1M"],"rs_3m":rs["3M"],"rs_6m":rs["6M"],"rs_12m":rs["12M"],"rsi14":rsi(close),"macd":m,"macd_signal":ms,"macd_hist":mh,"adx14":adx(high,low,close),"dist_20dma":dist_ma(close,20),"dist_50dma":dist_ma(close,50),"dist_200dma":dist_ma(close,200),"volume_ratio_20d":float(vol.iloc[-1]/vol.rolling(20).mean().iloc[-1]) if len(vol)>=20 else np.nan}
    if asset_type=="ETF":
        base.update({k:np.nan for k in ["forward_revenue_growth","forward_eps_growth","eps_revision_signal","forward_pe","ev_sales","ev_ebitda","fcf_yield","fcf_margin","roic_proxy","gross_margin","operating_margin","debt_to_equity","shares_growth"]})
        return base
    fcf=info.get("freeCashflow",np.nan); revenue=info.get("totalRevenue",np.nan)
    base.update({"forward_revenue_growth":revenue_growth_estimate(t),"forward_eps_growth":eps_growth_estimate(t),"eps_revision_signal":eps_revision_score(t),"forward_pe":info.get("forwardPE",np.nan),"ev_sales":info.get("enterpriseToRevenue",np.nan),"ev_ebitda":info.get("enterpriseToEbitda",np.nan),"fcf_yield":fcf/market_cap if market_cap and np.isfinite(fcf) else np.nan,"fcf_margin":fcf/revenue if revenue and np.isfinite(fcf) else np.nan,"roic_proxy":calc_roic_proxy(t),"gross_margin":info.get("grossMargins",np.nan),"operating_margin":info.get("operatingMargins",np.nan),"debt_to_equity":info.get("debtToEquity",np.nan),"shares_growth":info.get("sharesPercentSharesOut",np.nan)})
    return base


def pct_rank(s: pd.Series, higher_better=True) -> pd.Series:
    x=s.replace([np.inf,-np.inf],np.nan).astype(float)
    valid=x.notna()
    result=pd.Series(50.0,index=s.index)
    if valid.sum()<2:return result
    x=x[valid].clip(x[valid].quantile(.05),x[valid].quantile(.95))
    if x.nunique()<2:return result
    # The observed universe is identical in both ranking directions.
    ranks=x.rank(method="average",ascending=higher_better)
    result.loc[valid]=(ranks-1)/(len(x)-1)*100
    return result


def weighted_mean(frame: pd.DataFrame, pairs) -> pd.Series:
    num=pd.Series(0.0,index=frame.index); den=pd.Series(0.0,index=frame.index)
    for col,w in pairs:
        valid=frame[col].notna(); num+=frame[col].fillna(0)*w; den+=valid.astype(float)*w
    return num/den.replace(0,np.nan)


def score(df: pd.DataFrame) -> pd.DataFrame:
    df=df.copy()
    df["macd_hist_pct"]=df["macd_hist"]/df["price"].where(df["price"]>0)
    for c in ["rs_1m","rs_3m","rs_6m","rs_12m","macd_hist_pct","adx14","volume_ratio_20d"]:df[c+"_p"]=pct_rank(df[c],True)
    for c in ["dist_20dma","dist_50dma","dist_200dma"]:
        sweet=1-((df[c].clip(-.30,.60)-.08).abs()/.38).clip(0,1); df[c+"_p"]=pct_rank(sweet,True)
    df["rsi_p"]=pct_rank(1-((df["rsi14"]-62).abs()/38).clip(0,1),True)
    rs=weighted_mean(df,[("rs_1m_p",.15),("rs_3m_p",.30),("rs_6m_p",.30),("rs_12m_p",.25)])
    tech=weighted_mean(df,[("rsi_p",.10),("macd_hist_pct_p",.20),("adx14_p",.15),("dist_20dma_p",.15),("dist_50dma_p",.15),("dist_200dma_p",.15),("volume_ratio_20d_p",.10)])
    for c in ["forward_revenue_growth","forward_eps_growth","eps_revision_signal","fcf_yield","fcf_margin","roic_proxy","gross_margin","operating_margin"]:df[c+"_p"]=pct_rank(df[c],True)
    for c in ["forward_pe","ev_sales","ev_ebitda","debt_to_equity"]:df[c+"_p"]=pct_rank(df[c],False)
    revisions=weighted_mean(df,[("eps_revision_signal_p",.55),("forward_eps_growth_p",.25),("forward_revenue_growth_p",.20)]); growth=weighted_mean(df,[("forward_revenue_growth_p",.55),("forward_eps_growth_p",.45)]); quality=weighted_mean(df,[("roic_proxy_p",.30),("fcf_margin_p",.25),("gross_margin_p",.20),("operating_margin_p",.15),("debt_to_equity_p",.10)]); valuation=weighted_mean(df,[("forward_pe_p",.30),("ev_sales_p",.25),("ev_ebitda_p",.15),("fcf_yield_p",.30)])
    risk=weighted_mean(df,[("debt_to_equity_p",.35),("fcf_yield_p",.25),("roic_proxy_p",.20),("dist_200dma_p",.20)]); secular=pd.Series(50.0,index=df.index)
    stock_mask=df["asset_type"].ne("ETF"); etf_mask=~stock_mask
    df["long_term_score"]=(.30*((growth+revisions)/2)+.25*quality+.20*valuation+.15*secular+.10*risk).round(1)
    df["short_term_score"]=(.40*rs+.30*tech+.20*revisions+.10*valuation).round(1)
    df["buy_now_score"]=(.55*df["long_term_score"]+.30*df["short_term_score"]+.15*valuation).round(1)
    df["valuation_score"]=valuation.round(1); df["quality_score"]=quality.round(1); df["growth_score"]=growth.round(1); df["revision_score"]=revisions.round(1); df["technical_score"]=tech.round(1); df["relative_strength_score"]=rs.round(1)
    if etf_mask.any():
        trend_risk=weighted_mean(df,[("dist_200dma_p",.40),("adx14_p",.25),("rsi_p",.20),("volume_ratio_20d_p",.15)])
        etf_lt=(.45*rs+.30*tech+.25*trend_risk); etf_st=(.55*rs+.35*tech+.10*df["volume_ratio_20d_p"]); etf_bn=(.35*etf_lt+.50*etf_st+.15*tech)
        for idx in df.index[etf_mask]:
            ticker=df.at[idx,"ticker"]; penalty=CONFIG.get("etf_scoring",{}).get("leveraged_long_term_penalty",15) if CONFIG.get("etf_metadata",{}).get(ticker,{}).get("leveraged",False) else 0
            df.at[idx,"long_term_score"]=round(max(0,etf_lt.loc[idx]-penalty),1); df.at[idx,"short_term_score"]=round(etf_st.loc[idx],1); df.at[idx,"buy_now_score"]=round(.35*df.at[idx,"long_term_score"]+.50*df.at[idx,"short_term_score"]+.15*tech.loc[idx],1)
            for c in ["valuation_score","quality_score","growth_score","revision_score"]:df.at[idx,c]=np.nan
    return df


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--latest-completed",action="store_true")
    args=parser.parse_args()
    now=pd.Timestamp.now(tz=TZ)
    schedule=mcal.get_calendar("NYSE").schedule(start_date=TODAY-pd.Timedelta(days=14),end_date=TODAY)
    completed=schedule[schedule["market_close"]+pd.Timedelta(minutes=15)<=now]
    if completed.empty:raise RuntimeError("No completed NYSE session found")
    as_of=completed.index[-1].date() if args.latest_completed else TODAY
    if not args.latest_completed and CONFIG["refresh"].get("trading_days_only",True) and not is_trading_day(TODAY):
        print(f"{TODAY} is not an NYSE trading day; no update."); return 0
    symbols=CONFIG["universe"]+list(CONFIG["benchmarks"].keys()); raw=yf.download(symbols,period="18mo",interval="1d",auto_adjust=True,group_by="ticker",threads=True,progress=False)
    if raw.empty:raise RuntimeError("No market data returned")
    raw=raw.loc[raw.index.date<=as_of]
    latest_dates=[raw[b].dropna(how="all").index[-1].date() for b in CONFIG["benchmarks"] if b in raw.columns.get_level_values(0)]
    if len(latest_dates)!=len(CONFIG["benchmarks"]) or any(d!=as_of for d in latest_dates):
        raise RuntimeError(f"Benchmark data does not match completed session {as_of}: {latest_dates}")
    bench_returns={b:{h:pct_return(raw[b]["Close"].dropna(),d) for h,d in {"1M":21,"3M":63,"6M":126,"12M":252}.items()} for b in CONFIG["benchmarks"]}
    rows=[]
    for ticker in CONFIG["universe"]:
        try:
            prices=raw[ticker].dropna(subset=["Close"])
            if prices.empty or prices.index[-1].date()!=as_of:
                raise ValueError(f"Missing completed-session price for {as_of}")
            rows.append(row_for(ticker,raw,bench_returns))
        except Exception as e:print(f"WARN {ticker}: {e}"); rows.append({"ticker":ticker,"asset_type":CONFIG.get("asset_types",{}).get(ticker,"Stock")})
    failed=[r["ticker"] for r in rows if not np.isfinite(r.get("price",np.nan))]
    if failed:raise RuntimeError(f"Incomplete universe; refusing mixed/stale ranking: {failed}")
    df=score(pd.DataFrame(rows)); df["as_of"]=str(as_of); df=df.sort_values(["buy_now_score","long_term_score"],ascending=False).reset_index(drop=True); df.insert(0,"rank",np.arange(1,len(df)+1))
    output_cols=["rank","ticker","asset_type","price","market_cap","long_term_score","short_term_score","buy_now_score","valuation_score","quality_score","growth_score","revision_score","technical_score","relative_strength_score","rsi14","macd_hist","adx14","dist_20dma","dist_50dma","dist_200dma","rs_1m","rs_3m","rs_6m","rs_12m","forward_revenue_growth","forward_eps_growth","eps_revision_signal","forward_pe","ev_sales","ev_ebitda","fcf_yield","fcf_margin","roic_proxy","gross_margin","operating_margin","debt_to_equity","macd_hist_pct","volume_ratio_20d","as_of","scoring_version","universe_size","image_mentions"]
    df["scoring_version"]=CONFIG.get("scoring_version","2.1")
    df["universe_size"]=len(CONFIG["universe"])
    df["image_mentions"]=df["ticker"].map(CONFIG.get("image_mentions",{}).get("all_counts",{})).fillna(0).astype(int)
    for c in output_cols:
        if c not in df.columns:df[c]=np.nan
    # Archive the earlier same-session result before changing the universe or methodology.
    previous=ROOT/"history"/f"{as_of}.csv"
    if previous.exists():
        digest=hashlib.sha256(previous.read_bytes()).hexdigest()[:12]
        archive=ROOT/"history"/"revisions"
        archive.mkdir(parents=True,exist_ok=True)
        backup=archive/f"{as_of}-{digest}.csv"
        if not backup.exists():shutil.copy2(previous,backup)
    out=df[output_cols]; out.to_csv(ROOT/"latest_scores.csv",index=False); (ROOT/"history").mkdir(exist_ok=True); out.to_csv(ROOT/"history"/f"{as_of}.csv",index=False); (ROOT/"latest_scores.json").write_text(out.replace({np.nan:None}).to_json(orient="records",indent=2)); print(out[["rank","ticker","asset_type","long_term_score","short_term_score","buy_now_score"]].to_string(index=False)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
