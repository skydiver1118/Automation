#!/usr/bin/env python3
"""Read-only primary-document ledger. A downloaded document is not a completed review."""
from __future__ import annotations
import argparse, concurrent.futures, hashlib, json, re, time
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup

TAGS={'RevenueFromContractWithCustomerExcludingAssessedTax','RevenueFromContractWithCustomerIncludingAssessedTax','Revenues','SalesRevenueNet','SalesRevenueGoodsNet','SalesRevenueServicesNet','OperatingRevenue','Revenue','GrossProfit','OperatingIncomeLoss','ProfitLossFromOperatingActivities','NetIncomeLoss','NetIncomeLossAvailableToCommonStockholdersBasic','ProfitLoss','NetCashProvidedByUsedInOperatingActivities','CashFlowsFromUsedInOperatingActivities','PaymentsToAcquirePropertyPlantAndEquipment','PurchaseOfPropertyPlantAndEquipment','PaymentsToDevelopSoftware','PaymentsToAcquireProductiveAssets','PaymentsToAcquireOtherPropertyPlantAndEquipment','CashAndCashEquivalentsAtCarryingValue','CashAndCashEquivalents','ShortTermInvestments','MarketableSecuritiesCurrent','LongTermInvestments','AvailableForSaleSecuritiesDebtSecuritiesCurrent','AvailableForSaleSecuritiesDebtSecuritiesNoncurrent','LongTermDebtCurrent','LongTermDebtNoncurrent','ShortTermBorrowings','LongTermDebt','LongTermDebtAndCapitalLeaseObligations','LongTermDebtAndFinanceLeaseObligationsCurrent','LongTermDebtAndFinanceLeaseObligationsNoncurrent','StockholdersEquity','Equity','Assets','Liabilities','WeightedAverageNumberOfDilutedSharesOutstanding','WeightedAverageNumberOfSharesOutstandingBasic','CommonStockSharesOutstanding','EntityCommonStockSharesOutstanding','ShareBasedCompensation','SharebasedPaymentArrangementNoncashExpense','DepreciationDepletionAndAmortization','DepreciationDepletionAndAmortizationPropertyPlantAndEquipment','DepreciationAmortizationAndAccretionNet','IncomeTaxExpenseBenefit','InterestExpense','CostOfRevenue','CostOfGoodsAndServicesSold','ResearchAndDevelopmentExpense','RestrictedCashAndCashEquivalentsCurrent','RestrictedCashAndCashEquivalentsNoncurrent'}
LOWTAGS={x.lower() for x in TAGS}
def text(el):return el.get_text(' ',strip=True) if el else None
def parse(html):
    soup=BeautifulSoup(html,'lxml');contexts={};units={}
    def tagname(tag):return str(tag.name).split(':')[-1].lower()
    for c in soup.find_all(lambda t:tagname(t)=='context'):
        def get(k):return text(c.find(lambda t:tagname(t)==k))
        contexts[c.get('id')]={'start':get('startdate'),'end':get('enddate') or get('instant'),'instant':get('instant') is not None,'dimensions':bool(c.find(lambda t:tagname(t) in ['explicitmember','typedmember']))}
    for u in soup.find_all(lambda t:tagname(t)=='unit'):units[u.get('id')]=text(u)
    facts=[]
    for f in soup.find_all(lambda t:tagname(t)=='nonfraction'):
        name=f.get('name','');short=name.split(':')[-1];ctx=contexts.get(f.get('contextref'))
        if not ctx or ctx['dimensions'] or not ctx.get('end') or ctx['end']<'2023-06-01':continue
        if short.lower() not in LOWTAGS:continue
        raw=text(f);v=re.sub(r'[^0-9.\-]','',raw or '')
        if not v:continue
        try:
            value=float(v)*10**int(f.get('scale',0))
            if f.get('sign')=='-' or '(' in raw:value=-abs(value)
        except (ValueError,OverflowError):continue
        facts.append({'tag':name,'start':ctx['start'],'end':ctx['end'],'instant':ctx['instant'],'value':value,'unit':units.get(f.get('unitref')),'decimals':f.get('decimals'),'context':f.get('contextref')})
    paragraphs=[]
    for p in soup.find_all(['p']):
        v=text(p)
        if v and 100<len(v)<1800 and re.search(r'customer concentration|substantial doubt|going concern|material weakness|restricted cash|subsequent event|major customer|revenue recognition|competitive|competition|export control|related party|related-party',v,re.I):
            if v not in paragraphs:paragraphs.append(v)
    return {'facts':facts,'risk_excerpts':paragraphs[:25],'context_count':len(contexts)}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--evidence',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();base=Path(a.evidence);out=Path(a.output);out.mkdir(exist_ok=True)
    jobs=[]
    for p in sorted(base.glob('*/vendor.json')):
        t=p.parent.name;filings=json.loads(p.read_text()).get('sec_filings',[]);reg=[x for x in filings if x['date']<='2026-09-06' and x['date']>='2024-01-01']
        annual=[x for x in reg if x['type'] in ['10-K','20-F','40-F']][:2]
        quarters=[x for x in reg if x['type']=='10-Q'][:4]
        if not quarters:quarters=[x for x in reg if x['type']=='6-K'][:3]
        # Latest post-quarter material filings are archived for reconciliation, never presumed immaterial.
        material=[x for x in reg if x['type'] in ['8-K','6-K'] and x['date']>='2026-08-01'][:3]
        selected={x['edgarUrl']:x for x in annual+quarters+material}
        for f in selected.values():
            ex=f.get('exhibits',{});keys=[f['type']]
            if f['type'] in ['6-K','8-K']:keys+=list(k for k in ex if k.startswith('EX-99'))[:2]
            for key in keys:
                url=ex.get(key)
                if url and not url.lower().endswith('.pdf'):jobs.append((t,f['date'],f['type'],key,url))
    def fetch(job):
        t,date,form,key,url=job;rec={'ticker':t,'filed':date,'form':form,'document':key,'mirror_url':url,'status':'unavailable','retrieved_at':datetime.now(timezone.utc).isoformat()}
        parts=urlparse(url).path.split('/')
        if 'sec-filings' in parts:
            i=parts.index('sec-filings');rec['sec_url']='https://www.sec.gov/Archives/edgar/data/'+str(int(parts[i+1]))+'/'+parts[i+2]+'/'+parts[-1]
        try:
            res=requests.get(url,headers={'User-Agent':'Mozilla/5.0 (compatible; FinancialEvidenceReview)'},timeout=20);res.raise_for_status()
            rec.update(parse(res.text));rec['sha256']=hashlib.sha256(res.content).hexdigest();rec['status']='retrieved';rec['bytes']=len(res.content)
            directory=out/t;directory.mkdir(exist_ok=True);name=date+'-'+form+'-'+key+'-'+hashlib.sha256(url.encode()).hexdigest()[:8]
            (directory/(name+'.html')).write_bytes(res.content)
            (directory/(name+'.json')).write_text(json.dumps(rec,ensure_ascii=False))
        except Exception as e:rec['error']=type(e).__name__+': '+str(e)[:150]
        print(json.dumps({k:v for k,v in rec.items() if k not in ['facts','risk_excerpts']}),flush=True)
        return rec
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(fetch,jobs))
    (out/'ledger.json').write_text(json.dumps({'generated_at':datetime.now(timezone.utc).isoformat(),'cutoff':'2026-09-06','source_note':'Filed documents served by the public Yahoo SEC-document mirror, identified by accession and original SEC URL. Mirror retrieval is not independent issuer authentication or exhaustive filing coverage.','documents':results},ensure_ascii=False))
    print('DOCUMENTS',len(results),'RETRIEVED',sum(x['status']=='retrieved' for x in results),flush=True)
if __name__=='__main__':main()
