import os
import json,re,ast,datetime
from pathlib import Path
ROOT=Path(os.environ['MB_EVIDENCE_ROOT'])/'new30'
MAPPING={
'Revenue Revenue Growth':'revenue','Gross Profit Gross Profit Growth':'gross_profit','Operating Income Operating Income Growth':'operating_income','Net Income Net Income Growth':'net_income','Earnings Per Share EPS Growth':'eps_diluted',
'Revenue Growth':'revenue_growth_yoy','Gross Margin':'gross_margin','Operating Margin':'operating_margin','Profit Margin':'net_margin','FCF Margin':'fcf_margin',
'Operating Cash Flow':'cfo','Capital Expenditures':'capex_signed','Free Cash Flow':'fcf_vendor','Depreciation & Amortization':'da','Stock-Based Compensation':'sbc',
'Cash & Equivalents':'cash_equivalents','Cash & Short-Term Investments':'cash_short_investments','Restricted Cash':'restricted_cash','Total Debt':'debt_including_leases','Long-Term Investments':'long_investments','Receivables':'receivables','Goodwill':'goodwill','Total Assets':'assets',"Shareholders' Equity":'equity','Total Common Shares Outstanding':'shares_common','Filing Date Shares Outstanding':'shares_filing',
'Order Backlog':'backlog'}

def parse_num(s,m):
 s=s.strip().replace(',','')
 if not s or s in ['-','—','N/A','n/a','Upgrade','0/0']:return None
 try:
  if s.endswith('%'):return float(s[:-1])/100
  return float(s)*(1 if m=='eps_diluted' else 1e6)
 except:return None

def tables(t):
 panels={};segments={}
 for name in ['history_.json','history_cash-flow-statement.json','history_balance-sheet.json']:
  x=json.loads((ROOT/t/name).read_text())
  for tb in x.get('tables',[]):
   labels=[]
   for h in tb['columns'][1:]:
    h=ast.literal_eval(h)
    label=h[0];mm=re.search(r'([A-Z][a-z]{2} \d{1,2}, \d{4})',h[1]);date=datetime.datetime.strptime(mm.group(),'%b %d, %Y').date().isoformat() if mm else None
    labels.append((label,date))
   for row in tb['rows']:
    metric=MAPPING.get(row[0])
    if metric:
     for (lab,date),v in zip(labels,row[1:]):
      if not date or date>'2026-09-06':continue
      p=panels.setdefault(date,{'period_end':date,'fiscal_period':lab,'values':{},'sources':{}})
      value=parse_num(v,metric)
      if value is not None:
       p['values'][metric]=value;p['sources'][metric]={'url':x['url'],'row':row[0],'kind':'standardized_vendor_table','source_sha256':x['sha256'],'retrieved_at':x['retrieved_at']}
    elif name=='history_.json' and (' Growth' in row[0]) and not any(a in row[0] for a in ['Revenue Growth','Net Cash','Cash Flow','EPS','Per Share','Dividend','Cash &','Total Debt']):
     if any('Q' in l[0] for l in labels):
      vals=[{'period_end':date,'value':parse_num(v,'segment_revenue')} for (lab,date),v in zip(labels,row[1:])][:8]
      segments[row[0].split(' Growth')[0]]=vals
 out=sorted(panels.values(),key=lambda v:v['period_end'],reverse=True)[:8]
 for row in out:
  v=row['values']
  if 'cfo' in v and 'capex_signed' in v:
   v['capex_outflow']=-v['capex_signed'];v['fcf_calculated']=v['cfo']+v['capex_signed']
   row['sources']['capex_outflow']={**row['sources'].get('capex_signed',{}),'kind':'derived_from_standardized_vendor','derivation':'Negate cash-flow capex sign to show a positive outflow; missing capex is not zero.'}
   row['sources']['fcf_calculated']={'kind':'derived_from_standardized_vendor','url':row['sources'].get('cfo',{}).get('url'),'derivation':'CFO minus productive capex','components':[row['sources'].get('cfo',{}),row['sources'].get('capex_outflow',{})]}
  if v.get('revenue'):
   for k,target in [('gross_profit','gross_margin_calculated'),('operating_income','operating_margin_calculated'),('fcf_calculated','fcf_margin_calculated')]:
    if v.get(k) is not None:v[target]=v[k]/v['revenue']
 return {'ticker':t,'quarter_target':8,'unit':'USD; shares in units; ratios decimal','rows':out,'segment_history':segments,'caveat':'Supplemental standardized historical statements. Primary-source cross-check and definition reconciliation are recorded separately. Dash is missing, never assumed zero.'}

if __name__=='__main__':
 out={p.parent.name:tables(p.parent.name) for p in ROOT.glob('*/vendor.json')}
 Path('/mnt/data/mb_repair/panels.json').write_text(json.dumps(out,indent=2))
 print('Ticker,quarters,core_cells,revenue8,operating8,cfo8,capex8,shares8')
 for t,p in sorted(out.items()):
  metrics=['revenue','gross_profit','operating_income','net_income','cfo','capex_outflow','cash_short_investments','debt_including_leases','shares_common']
  counts={k:sum(r['values'].get(k) is not None for r in p['rows']) for k in metrics}
  print(t,len(p['rows']),sum(counts.values()),counts)
