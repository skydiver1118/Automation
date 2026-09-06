#!/usr/bin/env python3
"""Read-only supplementary filed documents. Explicit CDN mirror provenance retained."""
import ast,concurrent.futures,hashlib,json,re,time
from datetime import datetime,timezone
from pathlib import Path
import requests
from bs4 import BeautifulSoup
OLD=Path('mb30_edgar');NEW=Path('mb30_supplement');NEW.mkdir(exist_ok=True)
VENDOR=Path('mb30_evidence')
known={x['retrieval_url'] for x in json.loads((OLD/'inventory.json').read_text())}
jobs=[]
# Extra quarters omitted by prior five-quarter cap. No dates invented.
for p in VENDOR.glob('*/vendor.json'):
 x=json.loads(p.read_text())
 for f in x.get('filings',[]):
  if f.get('type') not in ['10-Q','10-K','20-F'] or not '2024-07-01'<=f.get('date','')<='2026-09-06':continue
  u=f.get('exhibits',{}).get(f['type'])
  if not u or u in known:continue
  if not u.startswith('https://cdn.yahoofinance.com/prod/sec-filings/'):continue
  parts=u.split('/prod/sec-filings/')[1].split('/')
  jobs.append({'ticker':p.parent.name,'filed':f['date'],'form':f['type'],'url':'https://www.sec.gov/Archives/edgar/data/'+str(int(parts[0]))+'/'+parts[1]+'/'+parts[2],'retrieval_url':u})
# Exact documents independently located on EDGAR/issuer sites that vendor inventory omitted.
EXTRA=[
('ZETA','2026-02-25','10-K','1851003/000119312526068598/zeta-20251231.htm'),
('KTOS','2026-08-04','10-Q','1069258/000106925826000077/ktos-20260628.htm'),
('KTOS','2026-02-26','10-K','1069258/000106925826000013/ktos-20251228.htm'),
('BKSY','2026-08-06','10-Q','1753539/000175353926000124/bksy-20260630.htm'),
('WULF','2026-08-10','10-Q','1083301/000108330126000166/wulf-20260630.htm'),
('SOUN','2026-02-26','10-K','1840856/000184085626000006/soun-20251231.htm'),
('SOUN','2026-09-04','8-K','1840856/000121390026097712/ea0304691-8k_sound.htm'),
('FIGR','2026-09-01','8-K','2064124/000149315226040931/form8-k.htm'),
('QBTS','2026-08-06','10-Q','1907982/000190798226000129/qbts-20260630.htm'),
('EOSE','2026-08-06','10-Q','1805077/000162828026052906/eose-20260630.htm'),
('POET','2026-08-13','6-K','1437424/000149315226037615/ex99-1.htm'),
('POET','2026-03-31','20-F','1437424/000149315226014253/form20-f.htm'),
('POET','2026-09-04','6-K','1437424/000117184326005894/exh_991.htm'),
('RZLV','2026-09-01','6-K','1920294/000119312526378541/rzlv-ex99_1.htm'),
('GRRR','2026-08-24','6-K','1903145/000143774926028827/ex_974013.htm')]
for t,d,f,p in EXTRA:
 cik,acc,file=p.split('/');jobs.append({'ticker':t,'filed':d,'filed_date_precision':'reported_date_to_verify_against_header','form':f,'url':'https://www.sec.gov/Archives/edgar/data/'+p,'retrieval_url':'https://cdn.yahoofinance.com/prod/sec-filings/'+cik.zfill(10)+'/'+acc+'/'+file})
# Broader numeric fields for the annual and most recent interim, including expenses and capex subcomponents.
for t in [p.name for p in OLD.iterdir() if p.is_dir()]:
 ds=[json.loads(p.read_text()) for p in (OLD/t).glob('*.json')]
 for form in ['10-K','20-F','10-Q']:
  matches=sorted([x for x in ds if x['form']==form],key=lambda x:x['filed'],reverse=True)
  if matches:
   d=matches[0];jobs.append({k:d[k] for k in ['ticker','filed','form','url','retrieval_url']})
jobs=list({x['retrieval_url']:x for x in jobs}.values())

def work(r):
 r=dict(r);r['retrieved_at']=datetime.now(timezone.utc).isoformat()
 try:
  resp=requests.get(r['retrieval_url'],headers={'User-Agent':'Mozilla/5.0'},timeout=15);resp.raise_for_status()
  r['sha256']=hashlib.sha256(resp.content).hexdigest();s=BeautifulSoup(resp.content,'lxml');contexts={};units={}
  for c in s.find_all(lambda n:n.name and n.name.lower().endswith('context')):
   if c.find(lambda n:n.name and n.name.lower().endswith(('explicitmember','typedmember'))):continue
   def v(k):
    n=c.find(lambda n:n.name and n.name.lower().endswith(k));return n.get_text(strip=True) if n else None
   contexts[c.get('id')]={'start':v('startdate'),'end':v('enddate') or v('instant')}
  for u in s.find_all(lambda n:n.name and n.name.lower().endswith('unit')):units[u.get('id')]=u.get_text(' ',strip=True)
  facts=[]
  for n in s.find_all(lambda n:n.name and n.name.lower().endswith('nonfraction')):
   cx=contexts.get(n.get('contextref'));tag=n.get('name','')
   if not cx or not cx['end'] or cx['end']<'2023-01-01':continue
   try:
    v=n.get_text(strip=True).replace(',','').replace('$','').replace('(','-').replace(')','');v=0. if v in ['—','-','–'] else float(v)
    v*=10**int(n.get('scale',0));v*=-1 if n.get('sign')=='-' else 1
    facts.append({'tag':tag,**cx,'value':v,'unit':units.get(n.get('unitref'),n.get('unitref')),'context':n.get('contextref')})
   except (ValueError,TypeError):pass
  r['facts']=facts
  # Table rows preserve context in financial exhibits without inline XBRL; not a scored observation.
  r['table_rows']=[[c.get_text(' ',strip=True) for c in tr.find_all(['td','th'],recursive=False)] for tr in s.find_all('tr')]
  for n in s(['script','style']):n.decompose()
  r['text']=s.get_text(' ',strip=True);r['status']='retrieved'
 except Exception as e:r.update(status='unavailable',error=str(e)[:200])
 p=NEW/r['ticker'];p.mkdir(exist_ok=True)
 (p/(r['filed']+'-'+r['form']+'-'+hashlib.sha256(r['url'].encode()).hexdigest()[:8]+'.json')).write_text(json.dumps(r,separators=(',',':')))
 print(r['ticker'],r['form'],r['status'],len(r.get('facts',[])),flush=True)
 return {k:v for k,v in r.items() if k not in ['text','facts','table_rows']}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:res=list(ex.map(work,jobs))
(NEW/'inventory.json').write_text(json.dumps(res,indent=2))
print(json.dumps({'documents':len(res),'retrieved':sum(x['status']=='retrieved' for x in res)}))
