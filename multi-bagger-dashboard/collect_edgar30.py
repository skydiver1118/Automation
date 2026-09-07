#!/usr/bin/env python3
"""Read-only collection of SEC-filed documents at disclosed public mirror URLs."""
import concurrent.futures, hashlib, json, re, time
from datetime import datetime, timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup
ROOT=Path('mb30_evidence');OUT=Path('mb30_edgar');OUT.mkdir(exist_ok=True)

def choose(ticker):
 x=json.loads((ROOT/ticker/'vendor.json').read_text());out=[];annual=quarter=0
 for f in sorted(x.get('filings',[]),key=lambda z:z.get('date',''),reverse=True):
  date=f.get('date','');form=f.get('type');ex=f.get('exhibits',{})
  if not '2024-01-01'<=date<='2026-09-06':continue
  if form in ['10-K','20-F','40-F'] and annual<2:
   annual+=1;keys=[form]
  elif form=='10-Q' and quarter<5:
   quarter+=1;keys=[form]
  elif form in ['6-K','8-K'] and date>='2026-08-01':
   keys=[k for k in ex if k.startswith('EX-99')][:2]
  else:continue
  for k in keys:
   u=ex.get(k)
   if u and u.startswith('https://cdn.yahoofinance.com/prod/sec-filings/'):
    parts=u.split('/prod/sec-filings/')[1].split('/');canonical='https://www.sec.gov/Archives/edgar/data/'+str(int(parts[0]))+'/'+parts[1]+'/'+parts[2]
    out.append({'ticker':ticker,'filed':date,'form':form,'exhibit':k,'url':canonical,'retrieval_url':u})
  if len(out)>=12:break
 return out
jobs=[]
for p in ROOT.glob('*/vendor.json'):jobs+=choose(p.parent.name)

def work(rec):
 url=rec['retrieval_url'];r=dict(rec);r['retrieved_at']=datetime.now(timezone.utc).isoformat()
 try:
  response=requests.get(url,headers={'User-Agent':'Mozilla/5.0'},timeout=12);response.raise_for_status()
  r['sha256']=hashlib.sha256(response.content).hexdigest();s=BeautifulSoup(response.content,'lxml')
  contexts={}
  for c in s.find_all(lambda n:n.name and n.name.lower().endswith('context')):
   if c.find(lambda n:n.name and n.name.lower().endswith(('explicitmember','typedmember'))):continue
   def value(k):
    n=c.find(lambda n:n.name and n.name.lower().endswith(k));return n.get_text(strip=True) if n else None
   contexts[c.get('id')]={'start':value('startdate'),'end':value('enddate') or value('instant')}
  units={}
  for u in s.find_all(lambda n:n.name and n.name.lower().endswith('unit')):units[u.get('id')]=u.get_text(' ',strip=True)
  facts=[]
  for n in s.find_all(lambda n:n.name and n.name.lower().endswith('nonfraction')):
   tag=n.get('name','');cx=contexts.get(n.get('contextref'))
   if not cx or not cx['end'] or cx['end']<'2023-01-01':continue
   if not re.search(r'Revenue|SalesRevenue|GrossProfit|OperatingIncome|IncomeLossFromContinuing|NetIncome|ProfitLoss|OperatingActiv|AcquireProperty|CapitalExpend|Depreciation|Diluted|WeightedAverage|CommonStockShares|Debt|CashAndCash|StockholdersEquity|ShareBased|CostOfRevenue|CostOfGoods|CostOfSales',tag,re.I):continue
   try:
    text=n.get_text(strip=True).replace(',','').replace('$','').replace('(','-').replace(')','')
    v=0. if text in ['—','-','–'] else float(text);v*=10**int(n.get('scale',0));v*=-1 if n.get('sign')=='-' else 1
    facts.append({'tag':tag,**cx,'value':v,'unit':units.get(n.get('unitref'),n.get('unitref')),'context':n.get('contextref')})
   except (ValueError,TypeError):pass
  r['facts']=facts
  for n in s(['script','style']):n.decompose()
  r['text']=s.get_text(' ',strip=True)
  r['status']='retrieved'
 except Exception as e:r.update(status='unavailable',error=str(e)[:200])
 p=OUT/r['ticker'];p.mkdir(exist_ok=True);name=r['filed']+'-'+r['form']+'-'+r['exhibit'].replace('.','_')+'-'+hashlib.sha256(url.encode()).hexdigest()[:8]+'.json'
 (p/name).write_text(json.dumps(r,separators=(',',':')))
 print(r['ticker'],r['filed'],r['form'],r['exhibit'],r['status'],len(r.get('facts',[])),flush=True)
 return {k:v for k,v in r.items() if k not in ['text','facts']}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:results=list(ex.map(work,jobs))
(OUT/'inventory.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'documents':len(results),'retrieved':sum(r['status']=='retrieved' for r in results)}))
