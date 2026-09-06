#!/usr/bin/env python3
"""Read-only evidence collection. Retrieved sources never imply completed research."""
from __future__ import annotations
import argparse, csv, hashlib, io, json, math, re, time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
import numpy as np
import pandas as pd
import requests
import yfinance as yf
from bs4 import BeautifulSoup

APP=Path(__file__).resolve().parent
TYPES=['income-statement','balance-sheet','cash-flow-statement']
CUTOFF='2026-09-06';MARKET='2026-09-04'
def clean(v):
    if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [clean(x) for x in v]
    if isinstance(v,np.integer):return int(v)
    if isinstance(v,(float,np.floating)):return float(v) if math.isfinite(v) else None
    if isinstance(v,(pd.Timestamp,datetime)):return v.isoformat()
    return v

def save(p,x):p.write_text(json.dumps(clean(x),ensure_ascii=False,allow_nan=False,default=str))
def frame(d):return {} if d is None or d.empty else {str(c):{str(k):clean(v) for k,v in d[c].items()} for c in d}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='evidence30');a=ap.parse_args();out=Path(a.output);out.mkdir(exist_ok=True)
    snapshot=json.loads((APP/'monitoring/latest.json').read_text());tickers=[s['ticker'] for s in snapshot['stocks']]
    assert len(tickers)==len(set(tickers))==30
    session=requests.Session();session.headers.update({'User-Agent':'Mozilla/5.0 (compatible; InvestmentResearch/1.0)'})
    manifest=[]
    for stock in snapshot['stocks']:
        ticker=stock['ticker'];d=out/ticker;d.mkdir(exist_ok=True);record={'ticker':ticker,'retrieved_at':datetime.now(timezone.utc).isoformat(),'market_date':MARKET,'pages':[],'errors':[]}
        for kind in TYPES:
            url=f'https://stockanalysis.com/stocks/{ticker.lower()}/financials/{kind}/?p=quarterly'
            p={'kind':kind,'url':url,'retrieved_at':datetime.now(timezone.utc).isoformat(),'status':'unavailable'}
            try:
                response=session.get(url,timeout=25);response.raise_for_status();text=response.text;soup=BeautifulSoup(text,'html.parser')
                p['sha256']=hashlib.sha256(response.content).hexdigest();p['title']=soup.title.get_text(' ',strip=True) if soup.title else ''
                p['tables']=[[[c.get_text(' ',strip=True) for c in row.find_all(['th','td'],recursive=False)][:14] for row in tb.find_all('tr')] for tb in soup.find_all('table')]
                p['source_notes']=[x for x in soup.stripped_strings if any(k in x.lower() for k in ['millions','thousands','financials in','last updated','data source','standardized'])][:18]
                p['filings']=[{'form':x.get_text(' ',strip=True),'url':urljoin(url,x.get('href',''))} for x in soup.find_all('a',href=True) if 'sec.gov/Archives' in x['href'] or x.get_text(' ',strip=True) in ['10-K','10-Q','20-F','6-K']]
                p['status']='retrieved' if p['tables'] else 'no_tables'
                # Temporary raw bytes are kept only in the audit artifact, not production history.
                (d/(kind+'.html')).write_text(text)
            except Exception as e:p['error']=f'{type(e).__name__}: {e}'[:250]
            save(d/(kind+'.json'),p);record['pages'].append({k:v for k,v in p.items() if k!='tables'});time.sleep(.5)
        sources=stock['metadata'].get('sources',[]);primary=stock['metadata']['research'].get('primary_source')
        urls=list(dict.fromkeys([primary]+[x.get('locator') for x in sources if x.get('source_kind') in ['issuer_results_or_filing','issuer results / filing']]))
        for i,url in enumerate(u for u in urls if u and u.startswith('https://')):
            p={'kind':'primary_release_or_filing','url':url,'retrieved_at':datetime.now(timezone.utc).isoformat(),'status':'unavailable'}
            try:
                response=session.get(url,timeout=25);response.raise_for_status();text=response.text;soup=BeautifulSoup(text,'html.parser')
                for x in soup(['script','style','nav','header','footer']):x.decompose()
                p['sha256']=hashlib.sha256(response.content).hexdigest();p['status']='retrieved';p['text']=soup.get_text(' ',strip=True)
                p['links']=[{'title':x.get_text(' ',strip=True),'url':urljoin(url,x['href'])} for x in soup.find_all('a',href=True) if any(k in (x['href']+' '+x.get_text()).lower() for k in ['10-q','10-k','20-f','6-k','sec-filings','sec.gov','quarter','annual-report','2026'])][:80]
                (d/f'primary{i}.html').write_text(text)
            except Exception as e:p['error']=f'{type(e).__name__}: {e}'[:250]
            save(d/f'primary{i}.json',p);record['pages'].append({k:v for k,v in p.items() if k not in ['text','links']});time.sleep(.3)
        vendor=yf.Ticker(ticker);v={'ticker':ticker,'retrieved_at':datetime.now(timezone.utc).isoformat(),'errors':{}}
        for name,fn in [('info',vendor.get_info),('sec_filings',vendor.get_sec_filings),('revenue_estimate',vendor.get_revenue_estimate),('earnings_estimate',vendor.get_earnings_estimate),('eps_trend',vendor.get_eps_trend),('income_quarterly',lambda:vendor.get_income_stmt(freq='quarterly')),('balance_quarterly',lambda:vendor.get_balance_sheet(freq='quarterly')),('cashflow_quarterly',lambda:vendor.get_cashflow(freq='quarterly'))]:
            try:
                value=fn();v[name]=frame(value) if isinstance(value,pd.DataFrame) else value
            except Exception as e:v['errors'][name]=f'{type(e).__name__}: {e}'[:250]
        save(d/'vendor.json',v)
        save(d/'manifest.json',record);manifest.append(record)
        print(json.dumps({'ticker':ticker,'statements':[p['status'] for p in record['pages'][:3]],'primary':[p['status'] for p in record['pages'][3:]],'vendor_errors':list(v['errors'])}),flush=True)
    # Independent current-session technical evidence via the existing monitoring implementation.
    raw=yf.download(tickers+['QQQ','SMH'],start='2024-01-01',end='2026-09-05',auto_adjust=False,group_by='ticker',progress=False,threads=True)
    for t in tickers+['QQQ','SMH']:
        try:raw[t].dropna(subset=['Close']).to_csv(out/(t+'_daily.csv'))
        except Exception as e:print('PRICE_ERROR',t,str(e),flush=True)
    funds={'IVV':('239726','ishares-core-s-p-500-etf','S&P 500'),'IWB':('239707','ishares-russell-1000-etf','Russell 1000'),'IWM':('239710','ishares-russell-2000-etf','Russell 2000'),'IJH':('239763','ishares-core-s-p-mid-cap-etf','S&P MidCap 400'),'ITA':('239502','ishares-u-s-aerospace-defense-etf','U.S. aerospace and defense')};holdings=[]
    for symbol,(pid,slug,index) in funds.items():
        url=f'https://www.ishares.com/us/products/{pid}/{slug}/latest-holdings.csv';rec={'fund':symbol,'url':url,'benchmark':index,'retrieved_at':datetime.now(timezone.utc).isoformat(),'status':'unavailable','holdings':[]}
        try:
            res=session.get(url,timeout=25);res.raise_for_status();text=res.content.decode('utf-8-sig');lines=text.splitlines();h=next(i for i,l in enumerate(lines) if l.startswith(('Ticker,','"Ticker",')))
            rec['as_of_header']=' | '.join(l for l in lines[:h] if 'as of' in l.lower());rec['sha256']=hashlib.sha256(res.content).hexdigest()
            for row in csv.DictReader(io.StringIO('\n'.join(lines[h:]))):
                if row.get('Ticker') in tickers:rec['holdings'].append({'ticker':row['Ticker'],'weight_pct':row.get('Weight (%)'),'name':row.get('Name')})
            rec['status']='retrieved'
        except Exception as e:rec['error']=str(e)[:250]
        holdings.append(rec)
    save(out/'etf_evidence.json',holdings);save(out/'manifest.json',{'as_of':CUTOFF,'market_date':MARKET,'generated_at':datetime.now(timezone.utc).isoformat(),'stocks':manifest,'note':'Source retrieval and tables are not verification. A source-linked review must accept individual claims and reconcile accounting before releasing verified scores.'})
    print('DONE',len(manifest),flush=True)
if __name__=='__main__':main()
