#!/usr/bin/env python3
"""Public evidence collection only. Never scores, promotes, publishes or sends mail."""
from __future__ import annotations
import concurrent.futures, hashlib, json, math, re, time
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
import requests
import numpy as np
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup
APP=Path(__file__).resolve().parents[2]
OUT=Path('v22_current_evidence');OUT.mkdir(exist_ok=True)
CUTOFF='2026-09-29'
registry=json.loads((APP/'watchlist_registry.json').read_text())
old=json.loads((APP/'monitoring/latest.json').read_text())
TICKERS=[s['ticker'] for s in registry['stocks'] if s['tier'] in ['action','candidate']]
PRIOR={s['ticker']:s for s in old['stocks']}
def clean(x):
 if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [clean(v) for v in x]
 if isinstance(x,(float,np.floating)):return float(x) if math.isfinite(x) else None
 if isinstance(x,np.integer):return int(x)
 return str(x) if isinstance(x,(pd.Timestamp,datetime,date)) else x
def save(p,x):
 p=OUT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(clean(x),default=str,allow_nan=False,ensure_ascii=False,indent=2)+'\n')
def frame(d):return {} if d is None or d.empty else {str(c):{str(k):clean(v) for k,v in d[c].items()} for c in d}
INFO='longName currency financialCurrency marketCap enterpriseValue sharesOutstanding impliedSharesOutstanding totalCash totalDebt mostRecentQuarter lastFiscalYearEnd revenueGrowth grossMargins operatingMargins totalRevenue trailingPE forwardPE regularMarketPrice regularMarketTime'.split()
def company(ticker):
 existing=OUT/ticker/'vendor.json'
 if existing.exists():
  r=json.loads(existing.read_text());assert r['ticker']==ticker;print('REUSE',ticker,r['retrieved_at'],flush=True);return r
 t=yf.Ticker(ticker);r={'ticker':ticker,'retrieved_at':datetime.now(timezone.utc).isoformat(),'errors':{}}
 try:i=t.get_info();r['info']={k:i.get(k) for k in INFO}
 except Exception as e:r['errors']['info']=str(e)
 for n,fn in [('income_quarterly',lambda:t.get_income_stmt(freq='quarterly')),('cashflow_quarterly',lambda:t.get_cashflow(freq='quarterly')),('balance_quarterly',lambda:t.get_balance_sheet(freq='quarterly')),('income_annual',lambda:t.get_income_stmt(freq='yearly')),('cashflow_annual',lambda:t.get_cashflow(freq='yearly')),('balance_annual',lambda:t.get_balance_sheet(freq='yearly')),('revenue_estimate',t.get_revenue_estimate),('earnings_estimate',t.get_earnings_estimate)]:
  try:r[n]=frame(fn())
  except Exception as e:r['errors'][n]=str(e)
 try:r['filings']=clean(t.get_sec_filings() or [])
 except Exception as e:r['filings']=[];r['errors']['filings']=str(e)
 save(Path(ticker)/'vendor.json',r);print('VENDOR',ticker,len(r['filings']),r['errors'],flush=True);return r
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:companies=list(ex.map(company,TICKERS))
jobs=[]
for r in companies:
 t=r['ticker'];annual=quarter=0
 for f in sorted(r.get('filings',[]),key=lambda f:str(f.get('date','')),reverse=True):
  filed=str(f.get('date',''))[:10];form=f.get('type','');ex=f.get('exhibits',{})
  if filed>CUTOFF:continue
  keys=[]
  if form in ['10-K','20-F','40-F'] and annual<1:keys=[form];annual+=1
  elif form=='10-Q' and quarter<1:keys=[form];quarter+=1
  elif form in ['8-K','6-K'] and filed>='2026-09-01':keys=[form]+[k for k in ex if k.startswith('EX-99')][:2]
  for k in keys:
   u=ex.get(k)
   if not u:continue
   if u.startswith('https://cdn.yahoofinance.com/prod/sec-filings/'):
    parts=u.split('/prod/sec-filings/')[1].split('/')
    canonical='https://www.sec.gov/Archives/edgar/data/'+str(int(parts[0]))+'/'+parts[1]+'/'+parts[2]
   elif urlparse(u).hostname=='www.sec.gov':canonical=u
   else:continue
   jobs.append({'ticker':t,'form':form,'filed':filed,'exhibit':k,'url':canonical,'retrieval_url':u})
jobs=list({x['retrieval_url']:x for x in jobs}.values())
def document(row):
 r=dict(row);r['retrieved_at']=datetime.now(timezone.utc).isoformat()
 try:
  h=requests.get(r['retrieval_url'],headers={'User-Agent':'MultiBaggerResearch skydiver1118@users.noreply.github.com'},timeout=25);h.raise_for_status()
  r['sha256']=hashlib.sha256(h.content).hexdigest();s=BeautifulSoup(h.content,'lxml')
  r['table_rows']=[[c.get_text(' ',strip=True) for c in tr.find_all(['td','th'],recursive=False)] for tr in s.find_all('tr')]
  for n in s(['script','style']):n.decompose()
  r['text']=s.get_text(' ',strip=True);r['status']='retrieved'
 except Exception as e:r.update(status='unavailable',error=str(e)[:250])
 save(Path(r['ticker'])/(r['filed']+'-'+r['form']+'-'+hashlib.sha256(r['url'].encode()).hexdigest()[:10]+'.json'),r)
 print('DOC',r['ticker'],r['filed'],r['exhibit'],r['status'],flush=True)
 return {k:v for k,v in r.items() if k not in ['text','table_rows']}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:docs=list(ex.map(document,jobs))
save(Path('documents.json'),docs)
save(Path('summary.json'),{'information_cutoff':CUTOFF,'companies':len(companies),'documents':len(docs),'retrieved_documents':sum(d['status']=='retrieved' for d in docs),'source_snapshot_sha256':hashlib.sha256((APP/'monitoring/latest.json').read_bytes()).hexdigest(),'production_modified':False})
