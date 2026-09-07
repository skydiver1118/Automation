import os
import json,datetime,collections,math,copy
from pathlib import Path
ROOT=Path(os.environ['MB_EVIDENCE_ROOT'])
MAP={
'revenue':['Revenues','RevenueFromContractWithCustomerExcludingAssessedTax','RevenueFromContractWithCustomerIncludingAssessedTax','SalesRevenueNet','Revenue','RevenueNet'],
'cost_revenue':['CostOfRevenue','CostOfGoodsAndServicesSold','CostOfGoodsSold','CostOfSales'],
'gross_profit':['GrossProfit'],
'operating_income':['OperatingIncomeLoss','ProfitLossFromOperatingActivities'],
'net_income':['NetIncomeLoss','ProfitLoss'],
'cfo':['NetCashProvidedByUsedInOperatingActivities','CashFlowsFromUsedInOperatingActivities'],
'capex_property':['PaymentsToAcquirePropertyPlantAndEquipment','PurchaseOfPropertyPlantAndEquipment','PaymentsToAcquireProductiveAssets','PaymentsToAcquireOtherPropertyPlantAndEquipment','PaymentsToAcquirePropertyPlantAndEquipmentNet'],
'da':['DepreciationDepletionAndAmortization','DepreciationDepletionAndAmortizationPropertyPlantAndEquipment','DepreciationAmortizationAndAccretionNet','DepreciationAndAmortization','AdjustmentsForDepreciationDepletionAndAmortisation'],
'shares_diluted_wa':['WeightedAverageNumberOfDilutedSharesOutstanding','AdjustedWeightedAverageShares'],
'shares_basic_wa':['WeightedAverageNumberOfSharesOutstandingBasic','WeightedAverageShares'],
'sbc':['ShareBasedCompensation','SharebasedPaymentArrangementNoncashExpense','AdjustmentsForSharebasedPayments'],
'cash_equivalents':['CashAndCashEquivalentsAtCarryingValue','CashAndCashEquivalents'],
'shares_common':['CommonStockSharesOutstanding','EntityCommonStockSharesOutstanding'],
'equity':['StockholdersEquity','Equity'],
'backlog':['RevenueRemainingPerformanceObligation'], 'sga':['SellingGeneralAndAdministrativeExpense'], 'rd':['ResearchAndDevelopmentExpense'], 'capex_software':['PaymentsForSoftware','PaymentsToAcquireSoftware','PaymentsToDevelopSoftware','ExpendituresForInternalUseSoftware'], 'capex_satellite':['SatelliteProcurementWorkInProcess']}

def day(d):return datetime.date.fromisoformat(d)
def days(a,b):return (day(b)-day(a)).days+1

def collect(t):
 out=collections.defaultdict(list)
 for p in list((ROOT/'edgar'/t).glob('*.json')) + list((ROOT/'supplement'/t).glob('*.json')) + list((ROOT/'final_gaps'/t).glob('*.json')):
  d=json.loads(p.read_text())
  for f in d.get('facts',[]):
   tag=f['tag'].split(':')[-1]
   for m,tags in MAP.items():
    if tag in tags:
     if m.startswith('shares') and 'share' not in (f.get('unit') or '').lower():continue
     if not m.startswith('shares') and not any(u in (f.get('unit') or '').lower() for u in ['usd','iso4217']):continue
     out[m].append({**f,'priority':tags.index(tag),'url':d['url'],'mirror':d['retrieval_url'],'filed':d['filed'],'source_sha256':d['sha256'],'kind':'primary_filing_mirror','retrieved_at':d['retrieved_at']})
 return out

def select(obs, end, duration=None,instant=False):
 good=[]
 for o in obs:
  if abs((day(o['end'])-day(end)).days)>5:continue
  if instant and o.get('start'):continue
  if not instant:
   if not o.get('start'):continue
   if duration and not duration[0]<=days(o['start'],o['end'])<=duration[1]:continue
  good.append(o)
 if not good:return None
 # Priority among tags and latest available filing for restatements; exact date wins.
 good.sort(key=lambda o:(o['priority'],abs((day(o['end'])-day(end)).days),-int(o['filed'].replace('-',''))))
 x=copy.deepcopy(good[0]);dups=[o for o in good if o['priority']==x['priority'] and o['filed']==x['filed'] and o.get('start')==x.get('start') and o['end']==x['end']]
 vals={o['value'] for o in dups}
 if len(vals)>1:
  counts=collections.Counter(o['value'] for o in dups);common=counts.most_common()
  if len(common)>1 and common[0][1]>common[1][1]:
   x=copy.deepcopy(next(o for o in dups if o['value']==common[0][0]));x['rounding_variants']=sorted(vals)
  else:
   x['ambiguous_values']=sorted(vals);return None
 return x

def quarter(obs,end,weighted=False):
    candidates=[]
    direct=select(obs,end,(65,110))
    if direct:candidates.append(direct)
    # Allow Q4=FY-9M, Q3=9M-H1, Q2=H1-Q1, Q1=H1-Q2.
    for total in obs:
        if not total.get('start') or not 150<=days(total['start'],total['end'])<=385:continue
        for part in obs:
            if part.get('tag')!=total.get('tag') or part.get('unit')!=total.get('unit') or not part.get('start'):continue
            n=days(total['start'],total['end']);n0=days(part['start'],part['end'])
            if not 65<=n-n0<=110:continue
            if total['start']==part['start'] and part['end']<total['end']:
                a=(day(part['end'])+datetime.timedelta(days=1)).isoformat();b=total['end']
            elif total['end']==part['end'] and part['start']>total['start']:
                a=total['start'];b=(day(part['start'])-datetime.timedelta(days=1)).isoformat()
            else:continue
            if abs((day(b)-day(end)).days)>5:continue
            value=(total['value']*n-part['value']*n0)/(n-n0) if weighted else total['value']-part['value']
            candidates.append({'tag':total['tag'],'start':a,'end':b,'value':value,'unit':total['unit'],'url':total['url'],'mirror':total['mirror'],'priority':total['priority'],'filed':max(total['filed'],part['filed']),'selection_filed':min(total['filed'],part['filed']),'source_sha256':total['source_sha256'],'retrieved_at':total['retrieved_at'],'kind':'primary_derived','derivation':'day-weighted average from disjoint period difference' if weighted else 'Filed larger period minus contained disjoint remainder','components':[total,part]})
    if not candidates:return None
    candidates.sort(key=lambda o:(o['priority'],-int(o.get('selection_filed',o['filed']).replace('-','')),o['kind']!='primary_filing_mirror'))
    return candidates[0]

def trailing(obs,end):
    # A fiscal-year flow or FY + current YTD - previous same-length YTD.
    direct=select(obs,end,(350,385))
    if direct:return direct
    available=[o for o in obs if o.get('start') and abs((day(o['end'])-day(end)).days)<=5 and 65<=days(o['start'],o['end'])<=300]
    available.sort(key=lambda o:(o['priority'],-days(o['start'],o['end']),-int(o['filed'].replace('-',''))))
    current=select(obs,end,(days(available[0]['start'],available[0]['end']),days(available[0]['start'],available[0]['end']))) if available else None
    if not current:return None
    years=[o for o in obs if o.get('start') and 350<=days(o['start'],o['end'])<=385 and 0<days(o['end'],current['start'])<=8]
    if not years:return None
    years.sort(key=lambda o:(o['priority'],-int(o['filed'].replace('-',''))));annual=select(obs,years[0]['end'],(350,385))
    if not annual:return None
    prior=[o for o in obs if o.get('start') and abs(days(o['start'],o['end'])-days(current['start'],current['end']))<=7 and 350<=days(o['end'],current['end'])<=378 and abs(days(o['start'],annual['start']))<=7 and o['tag']==current['tag']]
    if not prior:return None
    prior.sort(key=lambda o:(o['priority'],-int(o['filed'].replace('-',''))));pr=prior[0]
    return {'tag':current['tag'],'value':annual['value']+current['value']-pr['value'],'end':end,'start':(day(pr['end'])+datetime.timedelta(days=1)).isoformat(),'kind':'primary_derived','derivation':'FY + current YTD - prior comparable YTD (no overlap)','components':[annual,current,pr],'url':current['url'],'unit':current['unit'],'retrieved_at':current['retrieved_at'],'filed':current['filed']}

def build(t,sa):
 facts=collect(t);out=copy.deepcopy(sa)
 for q in out['rows']:
  vals=q['values'];end=q['period_end']
  for metric,obs in facts.items():
   f=select(obs,end,instant=True) if metric in ['cash_equivalents','shares_common','equity','backlog'] else quarter(obs,end,metric.startswith('shares_'))
   if f:
    if metric in vals and abs(vals[metric]-f['value'])>max(abs(f['value'])*.005,10000):
     q.setdefault('vendor_differences',[]).append({'field':metric,'vendor':vals[metric],'primary':f['value'],'explanation':'Primary filed entity-level fact takes precedence; standardized vendor definitions may differ.'})
    vals[metric]=f['value'];q['sources'][metric]=f
  rev=vals.get('revenue');cost=vals.get('cost_revenue')
  if rev is not None and cost is not None and 'primary' in q['sources']['revenue']['kind'] and 'primary' in q['sources']['cost_revenue']['kind']:
   vals['gross_profit']=rev-cost;q['sources']['gross_profit']={'kind':'primary_derived','url':q['sources']['revenue']['url'],'derivation':'Filed revenue minus filed cost of revenue; issuer-specific exclusions retained','components':[q['sources']['revenue'],q['sources']['cost_revenue']]}
  # Eaton reports operating-profit components rather than a consolidated operating-income tag.
  if t=='ETN':
   parts={m:quarter(facts[m],end) for m in ['revenue','cost_revenue','sga','rd']}
   if all(v is not None for v in parts.values()):
    vals['operating_income']=parts['revenue']['value']-sum(parts[m]['value'] for m in ['cost_revenue','sga','rd'])
    q['sources']['operating_income']={'kind':'primary_derived','url':parts['revenue']['url'],'value':vals['operating_income'],'derivation':'Filed revenue minus cost of revenue, SG&A and R&D','components':list(parts.values())}
  # A cash capex total is accepted only when every issuer-relevant component is recovered.
  required=['capex_property']+(['capex_software'] if t in ['AVAV','SOUN','ZETA','EVLV','QBTS'] else ['capex_satellite'] if t=='BKSY' else [])
  parts=[quarter(facts[k],end) for k in required]
  if t not in ['EOSE','POET','RR','GRRR','RZLV','NBIS','IREN'] and all(v is not None for v in parts):
   vals['capex_outflow']=sum(v['value'] for v in parts)
   q['sources']['capex_outflow']={'kind':'primary_derived','url':parts[0]['url'],'value':vals['capex_outflow'],'derivation':' + '.join(required),'components':parts}
  # Keep total capex scope separate; property-only not silently substituted for software/satellite capex.
  if vals.get('cfo') is not None and vals.get('capex_outflow') is not None:vals['fcf_calculated']=vals['cfo']-vals['capex_outflow']
  for m,target in [('gross_profit','gross_margin_calculated'),('operating_income','operating_margin_calculated'),('fcf_calculated','fcf_margin_calculated')]:
   if rev and vals.get(m) is not None: vals[target]=vals[m]/rev
 out['primary_metric_counts']={m:sum('primary' in r['sources'].get(m,{}).get('kind','') for r in out['rows']) for m in MAP}
 return out
if __name__=='__main__':
 sa=json.loads((ROOT/'panels.json').read_text());res={t:build(t,p) for t,p in sa.items()};(ROOT/'primary_panels.json').write_text(json.dumps(res,separators=(',',':')))
 print('Ticker primary revenue/op/cfo/PP&E/shares /8')
 for t,p in sorted(res.items()):print(t,[p['primary_metric_counts'][m] for m in ['revenue','operating_income','cfo','capex_property','shares_diluted_wa']], 'TTM', {m:round(sum(r['values'].get(m,0) for r in p['rows'][:4])/1e6,3) if all(m in r['values'] for r in p['rows'][:4]) else None for m in ['revenue','operating_income','cfo']})
