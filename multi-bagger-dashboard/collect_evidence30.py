#!/usr/bin/env python3
"""Evidence collection only. No membership changes, score certification or broker calls."""
from __future__ import annotations
import concurrent.futures, hashlib, io, json, math, re, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
import numpy as np
import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup
from watchlist_runtime import technical, clean

APP=Path(__file__).resolve().parent
OUT=Path('mb30_evidence');OUT.mkdir(exist_ok=True)
CUTOFF='2026-09-06';SESSION='2026-09-04'
REG=json.loads((APP/'watchlist_registry.json').read_text())
TICKERS=[x['ticker'] for x in REG['stocks']]
BASE=json.loads((APP/'monitoring/latest.json').read_text())
PREVIOUS={x['ticker']:x for x in BASE['stocks']}
assert len(TICKERS)==30 and len(set(TICKERS))==30
UA='MultiBaggerResearch skydiver1118@users.noreply.github.com'

def save(name,obj):
 p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(json.dumps(clean(obj),ensure_ascii=False,allow_nan=False,default=str,separators=(',',':'))+'\n')

def frame(df):
 if df is None or df.empty:return {}
 return {str(c):{str(k):clean(v) for k,v in df[c].items()} for c in df}

def get(url,sec=False):
 r=requests.get(url,headers={'User-Agent':UA if sec else 'Mozilla/5.0','Accept':'text/html,application/json,application/xml;q=0.9,*/*;q=0.8'},timeout=25)
 r.raise_for_status();return r

METRICS=['TotalRevenue','GrossProfit','OperatingIncome','NetIncome','DilutedAverageShares','BasicAverageShares','OperatingCashFlow','CapitalExpenditure','DepreciationAndAmortization','CashCashEquivalentsAndShortTermInvestments','TotalDebt','OrdinarySharesNumber']
INFO=['longName','currency','financialCurrency','marketCap','enterpriseValue','sharesOutstanding','impliedSharesOutstanding','totalCash','totalDebt','lastFiscalYearEnd','mostRecentQuarter','regularMarketTime','regularMarketPrice','industry','sector','lastSplitFactor','lastSplitDate','freeCashflow','operatingCashflow','totalRevenue']
raw=yf.download(TICKERS+['QQQ','SMH','SPY'],start='2023-09-01',end='2026-09-05',group_by='ticker',auto_adjust=False,threads=True,progress=False)
bench={t:technical(raw[t],SESSION) for t in ['QQQ','SMH','SPY']};save('benchmarks.json',bench)

def one(ticker):
 t=yf.Ticker(ticker);r={'ticker':ticker,'errors':{},'retrieved_at':datetime.now(timezone.utc).isoformat()}
 d=raw[ticker].dropna(subset=['Close']);d.to_csv(OUT/f'{ticker}_prices.csv')
 try:r['technical']=technical(d,SESSION)
 except Exception as e:r['errors']['technical']=str(e)
 try:i=t.get_info();r['info']={k:i.get(k) for k in INFO}
 except Exception as e:r['errors']['info']=str(e)
 for n,fn in [('income_quarterly',lambda:t.get_income_stmt(freq='quarterly')),('cashflow_quarterly',lambda:t.get_cashflow(freq='quarterly')),('balance_quarterly',lambda:t.get_balance_sheet(freq='quarterly')),('income_annual',lambda:t.get_income_stmt(freq='yearly')),('cashflow_annual',lambda:t.get_cashflow(freq='yearly')),('balance_annual',lambda:t.get_balance_sheet(freq='yearly')),('revenue_estimate',t.get_revenue_estimate),('earnings_estimate',t.get_earnings_estimate),('eps_trend',t.get_eps_trend),('eps_revisions',t.get_eps_revisions)]:
  try:r[n]=frame(fn())
  except Exception as e:r['errors'][n]=str(e)
 try:r['filings']=t.get_sec_filings() or []
 except Exception as e:r['filings']=[];r['errors']['filings']=str(e)
 try:
  u=f'https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/{ticker}'
  r['extended']=t._data.get_raw_json(u,params={'symbol':ticker,'type':','.join('quarterly'+m for m in METRICS),'period1':int(pd.Timestamp('2023-01-01',tz='UTC').timestamp()),'period2':int(pd.Timestamp('2026-09-05',tz='UTC').timestamp())})
 except Exception as e:r['errors']['extended']=str(e)
 save(f'{ticker}/vendor.json',r)
 print('VENDOR',ticker,len(r.get('income_quarterly',{})),len(r['filings']),r['errors'],flush=True)
 return r
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:records=list(ex.map(one,TICKERS))

# Read primary documents and preserve the table/fact evidence separately from research conclusions.
def document(url,name):
 rec={'url':url,'retrieved_at':datetime.now(timezone.utc).isoformat(),'status':'unavailable'}
 try:
  resp=get(url,sec='sec.gov' in urlparse(url).netloc);rec['url_final']=resp.url
  rec['sha256']=hashlib.sha256(resp.content).hexdigest();rec['content_type']=resp.headers.get('Content-Type')
  if 'pdf' in rec['content_type'].lower():
   (OUT/(name+'.pdf')).parent.mkdir(parents=True,exist_ok=True);(OUT/(name+'.pdf')).write_bytes(resp.content)
   rec['status']='downloaded_pdf';return rec
  soup=BeautifulSoup(resp.content,'lxml');rec['title']=soup.title.get_text(' ',strip=True) if soup.title else ''
  try:tables=pd.read_html(io.StringIO(str(soup)));rec['tables']=[{'columns':[str(c) for c in df.columns],'rows':df.fillna('').astype(str).values.tolist()} for df in tables]
  except ValueError:rec['tables']=[]
  rec['links']=[{'text':a.get_text(' ',strip=True)[:160],'url':urljoin(resp.url,a.get('href'))} for a in soup.find_all('a',href=True) if re.search(r'(202[456]|10-[kq]|20-f|quarter|annual|financial|presentation|sec.fil)',a.get_text(' ',strip=True)+' '+a.get('href'),re.I)]
  # Full text is an internal research artifact, not published dashboard content.
  for n in soup(['script','style','nav','footer']):n.decompose()
  rec['text']=soup.get_text(' ',strip=True);rec['status']='retrieved'
  # Entity-level inline XBRL facts; reject segment/member contexts.
  contexts={}
  for c in soup.find_all(lambda n:n.name and n.name.lower().endswith('context')):
   if c.find(lambda n:n.name and n.name.lower().endswith(('explicitmember','typedmember'))):continue
   def val(suffix):
    n=c.find(lambda n:n.name and n.name.lower().endswith(suffix));return n.get_text(strip=True) if n else None
   contexts[c.get('id')]={'start':val('startdate'),'end':val('enddate') or val('instant')}
  facts=[]
  for n in soup.find_all(lambda n:n.name and n.name.lower().endswith('nonfraction')):
   k=n.get('name','');cx=contexts.get(n.get('contextref'))
   if not cx or not cx['end'] or cx['end']<'2023-01-01':continue
   if not re.search(r'Revenue|SalesRevenue|GrossProfit|OperatingIncome|NetIncome|ProfitLoss|OperatingActiv|AcquireProperty|CapitalExpend|Depreciation|Diluted|CommonStockShares|TotalDebt|CashAndCash|StockholdersEquity|ShareBased',k,re.I):continue
   try:
    text=n.get_text(strip=True).replace(',','').replace('$','').replace('(','-').replace(')','');v=0. if text in ['—','-','–'] else float(text)
    v*=10**int(n.get('scale',0));v*=-1 if n.get('sign')=='-' else 1
    facts.append({'tag':k,**cx,'value':v,'unit':n.get('unitref'),'context':n.get('contextref')})
   except (ValueError,TypeError):pass
  rec['inline_facts']=facts
 except Exception as e:rec['error']=type(e).__name__+': '+str(e)[:250]
 save(name+'.json',rec);return rec

for r in records:
 ticker=r['ticker'];urls=[]
 for s in PREVIOUS[ticker]['metadata'].get('sources',[]):
  u=s.get('locator','')
  if u.startswith('https://') and not any(h in u for h in ['finance.yahoo.com','stockanalysis.com','github.com']):urls.append(u)
 for f in r['filings']:
  form=f.get('type',f.get('form',''));date=f.get('date','')
  if form in ['10-K','10-Q','20-F','40-F']:
   u=f.get('edgarUrl') or f.get('url')
   if u:urls.append(u)
 urls=list(dict.fromkeys(urls))[:7]
 documents=[]
 for j,u in enumerate(urls):documents.append(document(u,f'{ticker}/primary_{j}'))
 r['primary_documents']=[{k:v for k,v in x.items() if k not in ['text','tables','inline_facts','links']} for x in documents]
 # Public standardized historical tables are supplemental evidence, never relabeled as issuer filings.
 for suffix in ['financials/?p=quarterly','financials/balance-sheet/?p=quarterly','financials/cash-flow-statement/?p=quarterly']:
  doc=document(f'https://stockanalysis.com/stocks/{ticker.lower()}/{suffix}',f'{ticker}/history_'+suffix.split('/')[1].split('?')[0])
 print('PRIMARY',ticker,[(x['status'],len(x.get('inline_facts',[])),len(x.get('tables',[]))) for x in documents],flush=True)
 save(f'{ticker}/vendor.json',r)

# One direct SEC API availability probe; do not repeat rate-limited/blocked requests for every name.
try:
 sec=get('https://data.sec.gov/api/xbrl/companyfacts/CIK0001551182.json',sec=True).json();save('ETN/sec_companyfacts.json',sec);sec_available=True
except Exception as e:sec_available=False;save('sec_access.json',{'available':False,'error':str(e),'substitute':'Issuer releases/filing links plus separately labeled standardized historical tables'})
if sec_available:
 for r in records:
  urls=[f.get('edgarUrl',f.get('url','')) for f in r.get('filings',[])]
  matches=[re.search(r'/data/(\d+)/',u) for u in urls];ids=[m.group(1) for m in matches if m]
  if not ids:continue
  cik=int(ids[0]);time.sleep(.25)
  try:
   sub=get(f'https://data.sec.gov/submissions/CIK{cik:010d}.json',sec=True).json()
   if r['ticker'] not in sub.get('tickers',[]):raise ValueError('CIK/ticker mismatch')
   save(f'{r["ticker"]}/sec_submissions.json',sub)
   save(f'{r["ticker"]}/sec_companyfacts.json',get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json',sec=True).json())
  except Exception as e:print('SEC_ERROR',r['ticker'],str(e))
summary={'cutoff':CUTOFF,'market_session':SESSION,'stocks':len(records),'prices_exact':sum(r.get('technical',{}).get('price_date')==SESSION for r in records),'sec_api_available':sec_available,'retrieved_at':datetime.now(timezone.utc).isoformat(),'calculator_sha256':hashlib.sha256((APP/'research_scoring.py').read_bytes()).hexdigest()}
save('summary.json',summary);save('collection.json',{'metadata':summary,'benchmarks':bench,'stocks':records})
print(json.dumps(summary),flush=True)
