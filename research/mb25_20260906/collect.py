#!/usr/bin/env python3
"""Read-only research collection. Never writes dashboard data or the production list."""
from __future__ import annotations
import hashlib, json, math, os, sys, time
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import pandas as pd
import requests
import yfinance as yf

ASOF = '2026-09-04'
CUTOFF = '2026-09-06'
NEW = ['KTOS','AVAV','HUBB','VST','ETN']
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'research_output_mb25'
OUT.mkdir(exist_ok=True)
SNAPSHOT_PATH = ROOT/'stock-project-v2/data/multi_bagger/pass_scores/latest.json'
snapshot_bytes = SNAPSHOT_PATH.read_bytes()
snapshot = json.loads(snapshot_bytes)
OLD = [s['ticker'] for s in snapshot['stocks']]
TICKERS = list(dict.fromkeys(OLD + NEW))
assert len(TICKERS) == 25

def clean(x):
    if isinstance(x, dict): return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)): return [clean(v) for v in x]
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (float,np.floating)): return float(x) if math.isfinite(x) else None
    if isinstance(x, (pd.Timestamp,datetime)): return x.isoformat()
    if x is pd.NA: return None
    return x

def save(name, obj):
    (OUT/name).write_text(json.dumps(clean(obj),indent=2,allow_nan=False,default=str)+'\n')

def frame_json(df):
    if df is None or df.empty: return {}
    return {str(c):{str(i):clean(v) for i,v in df[c].items()} for c in df.columns}

def safe_call(fn):
    try: return fn(),None
    except Exception as e: return None,type(e).__name__+': '+str(e)[:250]

raw = yf.download(TICKERS+['QQQ','SMH','SPY'],start='2024-09-01',end='2026-09-05',auto_adjust=False,group_by='ticker',threads=True,progress=False)

def get_frame(t):
    if isinstance(raw.columns,pd.MultiIndex):
        if t in raw.columns.get_level_values(0): return raw[t].dropna(subset=['Close']).copy()
        if t in raw.columns.get_level_values(1): return raw.xs(t,axis=1,level=1).dropna(subset=['Close']).copy()
    return pd.DataFrame()

def technical(f):
    if f.empty: return {'error':'No prices'}
    f=f.loc[pd.to_datetime(f.index).date<=pd.Timestamp(ASOF).date()].copy()
    c=f['Close'];h=f['High'];l=f['Low'];v=f['Volume'];a=f['Adj Close'] if 'Adj Close' in f else c
    d=c.diff(); up=d.clip(lower=0).ewm(alpha=1/14,adjust=False).mean(); dn=(-d.clip(upper=0)).ewm(alpha=1/14,adjust=False).mean()
    rsi=100-100/(1+up/dn.replace(0,np.nan))
    macd=c.ewm(span=12,adjust=False).mean()-c.ewm(span=26,adjust=False).mean(); sig=macd.ewm(span=9,adjust=False).mean()
    tr=pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1);atr=tr.ewm(alpha=1/14,adjust=False).mean()
    u=h.diff();dwn=-l.diff();pdm=u.where((u>dwn)&(u>0),0.);mdm=dwn.where((dwn>u)&(dwn>0),0.)
    pdi=100*pdm.ewm(alpha=1/14,adjust=False).mean()/atr;mdi=100*mdm.ewm(alpha=1/14,adjust=False).mean()/atr
    adx=(100*(pdi-mdi).abs()/(pdi+mdi).replace(0,np.nan)).ewm(alpha=1/14,adjust=False).mean()
    out={'price_date':str(f.index[-1].date()),'price':c.iloc[-1],'rows':len(f),'rsi14':rsi.iloc[-1],'macd':macd.iloc[-1],'macd_signal':sig.iloc[-1],'macd_hist':(macd-sig).iloc[-1],'adx14':adx.iloc[-1],'plus_di':pdi.iloc[-1],'minus_di':mdi.iloc[-1],'atr14':atr.iloc[-1],'volume_ratio20':v.iloc[-1]/v.tail(20).mean(),'high20':h.tail(20).max(),'low20':l.tail(20).min(),'prior_high20':h.iloc[-21:-1].max(),'prior_low20':l.iloc[-21:-1].min(),'high252':h.tail(252).max(),'low252':l.tail(252).min()}
    for n in [20,50,200]:
        ma=c.rolling(n).mean();out[f'ma{n}']=ma.iloc[-1];out[f'ma{n}_slope20']=ma.iloc[-1]/ma.iloc[-21]-1 if len(ma)>n+20 else None
    for key,n in [('1m',21),('3m',63),('6m',126),('12m',252)]: out['return_'+key]=a.iloc[-1]/a.iloc[-1-n]-1 if len(a)>n else None
    return clean(out)

bench={t:technical(get_frame(t)) for t in ['QQQ','SMH','SPY']}
save('benchmarks.json',bench)
info_keys=['longName','shortName','currency','financialCurrency','exchange','sector','industry','marketCap','enterpriseValue','sharesOutstanding','impliedSharesOutstanding','floatShares','totalCash','totalDebt','totalRevenue','revenueGrowth','grossMargins','operatingMargins','profitMargins','ebitda','ebitdaMargins','freeCashflow','operatingCashflow','trailingPE','forwardPE','forwardEps','trailingEps','priceToSalesTrailing12Months','enterpriseToRevenue','enterpriseToEbitda','mostRecentQuarter','lastFiscalYearEnd','nextFiscalYearEnd','heldPercentInstitutions','lastSplitFactor','lastSplitDate','regularMarketPrice','regularMarketTime','returnOnEquity','returnOnAssets','debtToEquity','currentRatio','bookValue']
records=[]
for ticker in TICKERS:
    t=yf.Ticker(ticker); f=get_frame(ticker); errors={}
    info,error=safe_call(t.get_info);info=info or {}
    if error:errors['info']=error
    rec={'ticker':ticker,'group':'candidate' if ticker in NEW else 'incumbent','technical':technical(f),'info':{k:info.get(k) for k in info_keys},'retrieved_at':datetime.now(timezone.utc).isoformat(),'errors':errors}
    if not f.empty:f.to_csv(OUT/f'{ticker}_daily.csv')
    for name,fn in [('income_quarterly',lambda:t.get_income_stmt(freq='quarterly')),('balance_quarterly',lambda:t.get_balance_sheet(freq='quarterly')),('cashflow_quarterly',lambda:t.get_cashflow(freq='quarterly')),('income_annual',lambda:t.get_income_stmt(freq='yearly')),('cashflow_annual',lambda:t.get_cashflow(freq='yearly')),('revenue_estimate',t.get_revenue_estimate),('earnings_estimate',t.get_earnings_estimate),('eps_revisions',t.get_eps_revisions),('eps_trend',t.get_eps_trend)]:
        df,error=safe_call(fn)
        rec[name]=frame_json(df)
        if error:errors[name]=error
    records.append(rec); save(f'{ticker}_vendor.json',rec)
    print('MARKET '+json.dumps({'ticker':ticker,**rec['technical'],'info':rec['info']},default=str),flush=True)
    time.sleep(.15)

# Primary-source inventory and a filtered XBRL evidence panel, not assumed complete.
sec=requests.Session();sec.headers.update({'User-Agent':'MultiBaggerResearch skydiver1118@users.noreply.github.com','Accept-Encoding':'gzip, deflate'})
def secget(url):
    time.sleep(.35);r=sec.get(url,timeout=25);r.raise_for_status();return r.json()
try:
    mapping=secget('https://www.sec.gov/files/company_tickers.json')
    cikmap={v['ticker'].upper():int(v['cik_str']) for v in mapping.values()}
except Exception as e:
    cikmap={};save('sec_mapping_error.json',{'error':str(e)})
TAGS={'RevenueFromContractWithCustomerExcludingAssessedTax','RevenueFromContractWithCustomerIncludingAssessedTax','Revenues','SalesRevenueNet','OperatingRevenue','Revenue','GrossProfit','OperatingIncomeLoss','ProfitLossFromOperatingActivities','NetIncomeLoss','ProfitLoss','NetCashProvidedByUsedInOperatingActivities','CashFlowsFromUsedInOperatingActivities','PaymentsToAcquirePropertyPlantAndEquipment','PurchaseOfPropertyPlantAndEquipment','CashAndCashEquivalentsAtCarryingValue','CashAndCashEquivalents','ShortTermInvestments','LongTermDebtCurrent','LongTermDebtNoncurrent','ShortTermBorrowings','LongTermDebt','StockholdersEquity','Equity','Assets','Liabilities','WeightedAverageNumberOfDilutedSharesOutstanding','WeightedAverageNumberOfSharesOutstandingBasic','CommonStockSharesOutstanding','EntityCommonStockSharesOutstanding','ShareBasedCompensation','SharebasedPaymentArrangementNoncashExpense'}
for rec in records:
    ticker=rec['ticker'];cik=cikmap.get(ticker);rec['sec']={'cik':cik,'status':'unavailable'}
    if cik:
        try:
            sub=secget(f'https://data.sec.gov/submissions/CIK{cik:010d}.json');recent=sub['filings']['recent'];filings=[]
            for i,form in enumerate(recent['form']):
                filed=recent['filingDate'][i]
                if '2025-01-01'<=filed<=CUTOFF and form in ['10-K','10-Q','20-F','40-F','6-K','8-K','10-K/A','10-Q/A','20-F/A']:
                    accession=recent['accessionNumber'][i];doc=recent['primaryDocument'][i]
                    filings.append({'form':form,'filed':filed,'report_date':recent['reportDate'][i],'accession':accession,'url':f'https://www.sec.gov/Archives/edgar/data/{cik}/{accession.replace("-","")}/{doc}'})
            facts=secget(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json');panel={}
            for tax,tags in facts.get('facts',{}).items():
                for tag,values in tags.items():
                    if tag not in TAGS:continue
                    units={}
                    for unit,obs in values.get('units',{}).items():
                        kept=[x for x in obs if x.get('filed','9999')<=CUTOFF and x.get('end','')>='2023-01-01']
                        if kept:units[unit]=kept
                    if units:panel[tax+':'+tag]=units
            save(f'{ticker}_sec.json',{'cik':cik,'entity_name':sub.get('name'),'filings':filings,'facts':panel,'retrieved_at':datetime.now(timezone.utc).isoformat()})
            rec['sec']={'cik':cik,'status':'retrieved','filings':filings[:8],'tags':len(panel)}
        except Exception as e:rec['sec']['error']=str(e)[:300]
    print('SEC '+json.dumps({'ticker':ticker,**rec['sec']},default=str),flush=True)

result={'study':'MB25_RESEARCH_20260906','official_scores_recomputed':False,'production_modified':False,'market_date':ASOF,'information_cutoff':CUTOFF,'generated_at':datetime.now(timezone.utc).isoformat(),'baseline_sha256':hashlib.sha256(snapshot_bytes).hexdigest(),'baseline':snapshot,'benchmarks':bench,'stocks':records,'versions':{'python':sys.version,'yfinance':yf.__version__,'pandas':pd.__version__}}
save('collection.json',result)
assert SNAPSHOT_PATH.read_bytes()==snapshot_bytes,'Production snapshot changed unexpectedly'
print('COLLECTION_DONE '+json.dumps({'stocks':len(records),'price_exact_date':sum(x['technical'].get('price_date')==ASOF for x in records),'sec_retrieved':sum(x['sec']['status']=='retrieved' for x in records),'production_modified':False}),flush=True)
