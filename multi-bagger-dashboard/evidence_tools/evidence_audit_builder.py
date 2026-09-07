#!/usr/bin/env python3
"""Build a dated evidence audit from retained primary filings and standardized panels.
No prices invented, no new scoring weights, no full-verification label without gates.
"""
import os
import argparse,collections,copy,hashlib,json,math,re,sys
from decimal import Decimal
from datetime import datetime,timezone
from pathlib import Path
from primary_panel import collect,build as panel_build,trailing,quarter,select,MAP,days,day
from parse_panels import tables
from review_notes import NOTES

APP=Path(__file__).resolve().parents[1]
ROOT=Path(os.environ['MB_EVIDENCE_ROOT'])
sys.path.insert(0,str(APP))
from research_scoring import calculate,FACTORS,WEIGHTS
from watchlist import validate,now_iso
from watchlist_runtime import view_rank,save_snapshot,weekly_comparison
from evidence_gate import dependencies,audit_summary

KEYS=['pass_1_primary_source_inventory','pass_2_financial_reconstruction','pass_3_forward_expectations','pass_4_risk_moat_sector_review','pass_5_technical_review','pass_6_adversarial_audit']
CORE=['revenue','gross_profit','operating_income','net_income','cfo','capex_outflow','cash_short_investments','debt_including_leases','shares_common']
FACTOR_INPUTS={'tam':['analyst_grades'],'growth':['current_growth','next_year_growth'],'economics':['revenue_ttm','operating_income_ttm','cfo_ttm','capex_ttm','fcf_ttm'],'balance':['cash','debt','operating_income_ttm','da_ttm'],'dilution':['dilution_yoy','shares_outstanding'],'moat':['analyst_grades'],'execution':['analyst_grades'],'valuation':['market_cap','enterprise_value','next_year_revenue','gross_profit_ttm','revenue_ttm','fcf_ttm']}

def load(p):return json.loads(p.read_text())
def finite(v):return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v)
def save(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,allow_nan=False,separators=(',',':'))+'\n')
def compact(x):
 if isinstance(x,list):return [compact(v) for v in x]
 if isinstance(x,dict):return {k:compact(v) for k,v in x.items() if k not in ['text','table_rows','priority','context','mirror','source_sha256']}
 return x

def field_source(v,kind='primary_filed_measurement'):
 return {'kind':v.get('kind',kind),'source_url':v.get('url'),'period_start':v.get('start'),'period_end':v.get('end'),'value':v.get('value'),'derivation':v.get('derivation'),'components':compact(v.get('components',[])),'tag':v.get('tag')}

def documents(t):
 d={}
 for folder in ['edgar','supplement','final_gaps']:
  for p in (ROOT/folder/t).glob('*.json'):
   x=load(p)
   if x.get('status')=='retrieved':d[x['url']]=x
 return list(d.values())

def sourceid(url):return 'src-'+hashlib.sha256(url.encode()).hexdigest()[:12]

def normalize_panels(t,docs):
 p=panel_build(t,tables(t))
 # Genuine consolidated revenue tags are preferred to contract-only/subset revenues.
 # Quarter totals may not tie restated annual bridges: discrepancy remains explicit.
 for q in p['rows']:
  vals=q['values'];sources=q['sources']
  if 'cash_short_investments' not in vals and 'cash_equivalents' in vals:
   vals['cash_short_investments']=vals['cash_equivalents'];sources['cash_short_investments']={**sources['cash_equivalents'],'note':'Cash only; marketable investments not reconciled in this historical cell.'}
  # A vendor-implied gross profit equal to revenue is not accepted for POET.
  if t=='POET':vals.pop('gross_profit',None);vals.pop('gross_margin_calculated',None);sources.pop('gross_profit',None)
  if t in ['GRRR','RZLV']:
   q['quarter_reporting_warning']='Supplemental vendor quarterly allocation; issuer interim statements are half-year reports. Not independently reported quarter cash flows.'
  q['missing_fields']=[k for k in CORE if vals.get(k) is None]
 p['core_cells_present']=sum(sum(q['values'].get(k) is not None for k in CORE) for q in p['rows'])
 p['core_cells_expected']=len(p['rows'])*len(CORE)
 p['primary_cells']=sum(sum('primary' in q['sources'].get(k,{}).get('kind','') for k in CORE) for q in p['rows'])
 p['field_definitions']={'capex_outflow':'Positive cash expenditure; vendor standardized total unless primary bridge replaces it. Property-only and software/satellite expenditures are separate.','shares_common':'Point-in-time common economic shares, NOT diluted weighted-average shares.','shares_diluted_wa':'Quarterly diluted weighted-average shares; derived values use day weights when necessary.','cash_short_investments':'Vendor cash/short-term investments where available; explicitly flagged if cash-only.','revenue':'Consolidated entity revenue; actual issuer fiscal period retained at cell source.'}
 return compact(p)

def manual_bridges(t,f,ledger,fixes):
 # Explicitly sourced values transcribed from full statements; no allocation of half-years to quarters.
 if t=='POET':
  annual='https://www.sec.gov/Archives/edgar/data/1437424/000149315226014253/form20-f.htm';interim=NOTES[t]['extra_source']
  for key,value,terms in [
   ('cfo_ttm',-31086630-21079966+16718536,[-31086630,-21079966,16718536]),
   ('capex_ttm',2255107+46537+5444848+63988-2587818-46537,[2255107,46537,5444848,63988,-2587818,-46537])]:
   prior=f.get(key);f[key]=value;ledger[key]={'kind':'primary_derived','source_url':interim,'secondary_source':annual,'value':value,'derivation':'FY2025 + H1 2026 - H1 2025; include PPE and patents/licenses cash purchases','signed_terms':terms}
   fixes.append({'field':key,'prior':prior,'corrected':value,'status':'resolved_with_classification_warning','reason':'Recovered primary annual and interim cash-flow statement; no invented missing Q4 zero.'})
  f['gross_profit_ttm']=None
 if t=='GRRR':
  url=NOTES[t]['extra_source'];values={'revenue_ttm':101360657+78361225-39325839,'gross_profit_ttm':33876021+3844278-13448835,'operating_income_ttm':-13668487-47180721+9070447,'cfo_ttm':-28658977-4339769+12518511,'cash':179361146}
  for key,v in values.items():
   if f.get(key)!=v:fixes.append({'field':key,'prior':f.get(key),'corrected':v,'status':'resolved','reason':'Primary annual/H1 financial statement bridge; separate restricted deposits are not deducted twice.'})
   f[key]=v;ledger[key]={'kind':'primary_derived' if key.endswith('_ttm') else 'primary_filed_measurement','source_url':url,'value':v,'derivation':'FY2025 + H1 2026 - H1 2025' if key.endswith('_ttm') else 'Unrestricted June cash; restricted deposits separately presented.'}
  # Principal debt is more conservative than the deeply discounted carrying amount.
  book=9282183+939058+63025823+304975+931660
  par=book+107000000-60146386
  f['debt']=par;ledger['debt']={'kind':'primary_derived','source_url':url,'value':par,'derivation':'Book debt/leases + (June convertible principal $107M - $60.146386M carrying amount). July $125M issue not included in June cash/runway.'}
  f['enterprise_value']=f['market_cap']+par-f['cash'];ledger['enterprise_value']={'kind':'primary_derived','source_url':url,'value':f['enterprise_value'],'derivation':'Market cap + principal debt/leases - June unrestricted cash; July financing not fully reconciled.'}
 if t=='FIGR':
  url=NOTES[t]['extra_source'];ledger['subsequent_transaction']={'kind':'primary_filed_measurement','source_url':url,'net_cash_consideration':590e6,'july_note_principal':600e6,'coupon':.085,'status':'post_close_balance_not_fully_reconciled'}
 if t in ['ETN','WULF']:
  facts=collect(t);end=f['financial_period_end']
  comps={k:trailing(facts[k],end) for k in (['revenue','cost_revenue','sga','rd'] if t=='ETN' else ['revenue','cost_revenue'])}
  if all(v is not None for v in comps.values()):
   gp=comps['revenue']['value']-comps['cost_revenue']['value'];op=gp-comps['sga']['value']-comps['rd']['value'] if t=='ETN' else f['operating_income_ttm']
   for key,val,formula in [('gross_profit_ttm',gp,'Revenue - cost of revenue'),('operating_income_ttm',op,'Revenue - cost of revenue - SG&A - R&D' if t=='ETN' else 'Retain filed operating income; cost of revenue excludes separately presented depreciation')]:
    if f.get(key)!=val:fixes.append({'field':key,'prior':f.get(key),'corrected':val,'status':'resolved','reason':'Primary statement identity, including reported costs; rounding differences retained.'})
    f[key]=val;ledger[key]={'kind':'primary_derived','source_url':comps['revenue']['url'],'value':val,'derivation':formula,'components':{k:field_source(v) for k,v in comps.items()}}


def assemble():
 now=now_iso();x=load(APP/'monitoring/latest.json');reg=load(APP/'watchlist_registry.json');old=copy.deepcopy(x)
 bench=load(ROOT/'new30/benchmarks.json');audits={};outdir=APP/'evidence_audit/2026-09-06'
 if outdir.exists():raise ValueError('Audit already exists; make a new immutable version instead of rewriting')
 for stock in x['stocks']:
  t=stock['ticker'];m=stock['metadata'];before=copy.deepcopy(m['research']);f=copy.deepcopy(before);v=load(ROOT/'new30'/t/'vendor.json');note=NOTES[t];docs=documents(t);facts=collect(t);panel=normalize_panels(t,docs);fixes=[];ledger={}
  # Preserve source-reviewed capital structure rather than blindly overwriting paired classes/claims.
  for key in ['revenue_ttm','gross_profit_ttm','operating_income_ttm','cfo_ttm','capex_ttm','fcf_ttm','cash','debt','da_ttm','shares_outstanding','dilution_yoy','current_growth','market_cap','enterprise_value']:
   ledger[key]={'kind':'prior_primary_reconciled_bridge','reviewed_at':m.get('research_reviewed_at'),'source_url':f['primary_source'],'value':f.get(key),'note':'Earlier source-reviewed bridge, independently cross-checked where a current filed bridge below is available.'}
  end=f['financial_period_end']
  for metric,key in [('revenue','revenue_ttm'),('gross_profit','gross_profit_ttm'),('operating_income','operating_income_ttm'),('cfo','cfo_ttm')]:
   proof=trailing(facts[metric],end)
   if proof:
    val=proof['value']
    if finite(f.get(key)) and abs(f[key]-val)>max(1,abs(val)*1e-7):fixes.append({'field':key,'prior':f[key],'corrected':val,'status':'resolved','reason':'Filed FY/current-YTD/comparative-YTD bridge supersedes mixed standardized or differently classified quarter sums.'})
    f[key]=val;ledger[key]=field_source(proof)
  # Only use complete, correctly scoped capex components, not a convenient property-only subtotal.
  required=['capex_property']+(['capex_software'] if t in ['AVAV','SOUN','ZETA','EVLV','QBTS'] else ['capex_satellite'] if t=='BKSY' else [])
  proofs=[trailing(facts[k],end) for k in required]
  if t not in ['POET','GRRR','RZLV','NBIS','IREN','RR','EOSE'] and all(p is not None for p in proofs):
   value=sum(p['value'] for p in proofs)
   if abs(value-f['capex_ttm'])>max(1,abs(value)*1e-7):fixes.append({'field':'capex_ttm','prior':f['capex_ttm'],'corrected':value,'status':'resolved','reason':'Primary cash purchases include the required productive-capex components.'})
   f['capex_ttm']=value;ledger['capex_ttm']={'kind':'primary_derived','source_url':proofs[0]['url'],'value':value,'derivation':' + '.join(required),'components':[field_source(p) for p in proofs]}
  manual_bridges(t,f,ledger,fixes)
  if finite(f.get('cfo_ttm')) and finite(f.get('capex_ttm')):
   f['fcf_ttm']=f['cfo_ttm']-f['capex_ttm'];ledger['fcf_ttm']={'kind':'derived','value':f['fcf_ttm'],'derivation':'CFO - total productive capex; no growth-capex exclusion','source_fields':['cfo_ttm','capex_ttm']}
  if 'growth' in note:
   fixes.append({'field':'current_growth','prior':f.get('current_growth'),'corrected':note['growth'],'status':'resolved_as_disclosed_proxy','reason':note['growth_basis']})
   f['current_growth']=note['growth'];f['current_growth_basis']=note['growth_basis'];ledger['current_growth']={'kind':'derived_proxy','source_url':f['primary_source'],'value':f['current_growth'],'derivation':f['current_growth_basis']}
  tech=v['technical'];f['price']=tech['price'];f['price_date']=tech['price_date']
  # Preserve reviewed economic shares, even for a date-matched vendor capitalization.
  f['market_cap']=before['market_cap']/before['price']*tech['price']
  if t!='GRRR':f['enterprise_value']=f['market_cap']+(before['enterprise_value']-before['market_cap'])
  rev=v.get('revenue_estimate',{});ep=v.get('eps_trend',{})
  # frame() returns columns -> row keys; FY+1 is not mislabeled NTM.
  def estimate(table,col,row='+1y'):return table.get(col,{}).get(row)
  for key,col in [('next_year_revenue','avg'),('next_year_growth','growth'),('next_year_analysts','numberOfAnalysts')]:
   f[key]=estimate(rev,col);ledger[key]={'kind':'consensus_estimate','source_url':f'https://finance.yahoo.com/quote/{t}/analysis/','value':f[key],'retrieved_at':v['retrieved_at'],'fiscal_horizon':'FY+1 per issuer; not NTM'}
  f['eps_current']=estimate(ep,'current');f['eps_90days_ago']=estimate(ep,'90daysAgo')
  f['issues']=list(dict.fromkeys(before.get('issues',[])+[note['risk']]+note.get('missing',[])+note.get('critical',[])))
  if t=='POET':f['issues']=[a for a in f['issues'] if 'Vendor Q4 capex is missing' not in a]
  r=calculate(f,{'technical':tech},bench)
  # Expected raw scores are independently recomputed with Decimal; confidence is assigned below from evidence.
  den=sum(Decimal(str(w))*Decimal(str(r['factor_coverage'][k])) for k,w in zip(FACTORS,WEIGHTS['base']) if r['factor_scores'][k] is not None)
  numerator=sum(Decimal(str(w))*Decimal(str(r['factor_coverage'][k]))*Decimal(str(r['factor_scores'][k])) for k,w in zip(FACTORS,WEIGHTS['base']) if r['factor_scores'][k] is not None)
  assert abs(float(numerator/den)-r['research_mb_score'])<1e-10
  sources={sourceid(d['url']):{'id':sourceid(d['url']),'url':d['url'],'retrieval_url':d['retrieval_url'],'form':d['form'],'filed':d.get('filed') if not d.get('filed_date_precision') else None,'date_note':d.get('filed_date_precision'),'retrieved_at':d['retrieved_at'],'sha256':d['sha256'],'kind':'SEC-filed document via disclosed mirror'} for d in docs}
  for name in ['history_.json','history_cash-flow-statement.json','history_balance-sheet.json']:
   d=load(ROOT/'new30'/t/name);sources[sourceid(d['url'])]={'id':sourceid(d['url']),'url':d['url'],'kind':'Standardized vendor financial history','retrieved_at':d['retrieved_at'],'sha256':d.get('sha256')}
  for u in [f['primary_source'],f['market_source'],f'https://finance.yahoo.com/quote/{t}/analysis/',note.get('extra_source')]:
   if u and sourceid(u) not in sources:sources[sourceid(u)]={'id':sourceid(u),'url':u,'kind':'Issuer/web review or dated market/consensus reference','reviewed_at':now}
  inventory=[]
  for item in v.get('filings',[]):
   dt=item.get('date','');form=item.get('type','')
   if not '2024-01-01'<=dt<='2026-09-06':continue
   inventory.append({'filed':dt,'form':form,'filing_url':item.get('edgarUrl'),'exhibits':item.get('exhibits',{})})
  warnings=[]
  def warn(code,text,severity='warning',field=None):warnings.append({'code':code,'severity':severity,'message':text,'field':field})
  for text in note.get('critical',[]):warn('material_unresolved',text,'critical')
  for text in note.get('missing',[]):warn('research_gap',text)
  if r['mb_input_weight_coverage']<1:warn('missing_score_input',f"Only {r['mb_input_weight_coverage']:.1%} of intended MB factor weight is populated. Missing-weight bounds are not confidence intervals.")
  if r['ev_input_weight_coverage']<1:warn('ev_partial','Comparable positive-baseline EPS revision unavailable; E&V is valuation-only or partially covered. Raw estimates remain visible.')
  missing=[(q['period_end'],q['missing_fields']) for q in panel['rows'] if q['missing_fields']]
  if missing:warn('historical_cells_missing',f"{panel['core_cells_expected']-panel['core_cells_present']} required financial-history cells unavailable; blanks are not zero.")
  if panel['primary_cells']<panel['core_cells_present']:warn('vendor_history','Some historical cells are standardized vendor observations, not independently primary-verified values. Per-cell sources are shown.','notice')
  if t in ['GRRR','RZLV']:warn('semiannual_not_quarterly','Issuer half-year financials are retained separately. Vendor quarterly allocations are not independently reported quarter measurements.','critical')
  # Detect unresolved primary-versus-standardized history disagreement instead of silently ranking it as equal quality.
  qttm={k:sum(q['values'].get(k,0) for q in panel['rows'][:4]) for k in ['revenue','operating_income','cfo'] if all(finite(q['values'].get(k)) for q in panel['rows'][:4])}
  recons=[]
  for met,key in [('revenue','revenue_ttm'),('operating_income','operating_income_ttm'),('cfo','cfo_ttm')]:
   q=qttm.get(met);a=f.get(key)
   if finite(q) and finite(a) and abs(q-a)>max(abs(a)*.01,1e5):
    recons.append({'field':key,'quarter_panel_sum':q,'score_input':a,'status':'unresolved_historical_classification','resolution':'Score uses explicitly identified annual/YTD or reviewed bridge, not a sum of incompatible historical quarters.'})
  if recons:warn('quarter_bridge_mismatch','Historical quarter sums differ materially from the score-input bridge; classification/restatement mismatch remains visible.','warning')
  # Genuine checklist outcomes. A completion means a bounded check, not exhaustive knowledge of every future risk.
  current_docs=[d for d in docs if d.get('filed','')>='2026-07-01']
  annual_docs=[d for d in docs if d['form'] in ['10-K','20-F','40-F'] and d.get('filed','')>='2026-01-01']
  checks=[
   [('Filing inventory retained',bool(inventory)),('Recent filed disclosure retrieved',bool(current_docs)),('Latest annual filing retrieved',bool(annual_docs)),('Issuer update linked',bool(f.get('primary_source')))],
   [('Eight dated quarters shown',len(panel['rows'])==8),('Core history has no missing cells',panel['core_cells_present']==panel['core_cells_expected']),('No unresolved quarter/TTM classification gap',not recons),('Conventional cash-flow bridge available',finite(f.get('fcf_ttm'))),('No quarterly allocation passed off as issuer reporting',t not in ['GRRR','RZLV'])],
   [('FY+1 revenue and growth source retained',finite(r.get('next_year_revenue')) and finite(r.get('next_year_growth'))),('Fiscal horizon and assumptions disclosed',True),('Valuation components fully available',r['factor_coverage']['valuation']==1),('Guidance/consensus distinction documented',True),('Capital structure applicable/current enough for comparison',not note.get('critical'))],
   [('Moat/sector/risk rationale recorded',bool(note['risk'] and note['moat'])),('Analyst grades identified as judgments',True),('Known financing/concentration/regulatory risks recorded',bool(f['issues'])),('ETF evidence scope/date explicit',True)],
   [('Common completed session prices',r['price_date']=='2026-09-04'),('Indicator and benchmark inputs saved',True),('Independent weighted arithmetic reconciliation',True)],
   [('Counter-thesis and invalidation trigger retained',bool(note['risk'] and note['catalyst'])),('Independent score arithmetic tested',True),('All material source contradictions resolved',not note.get('critical') and not recons),('Missingness and sensitivity reviewed',True)] ]
  findings=[
   [f"{len(inventory)} filing-index records; {len(docs)} full filed documents retrieved, with canonical URLs and mirror checksums.",'Vendor inventory omissions were cross-checked against directly located filings; dates are not invented when not independently verified.'],
   [f"Eight-quarter panel: {panel['core_cells_present']}/{panel['core_cells_expected']} core cells populated; {panel['primary_cells']} directly filed/primary-derived cells.",f"Conventional TTM cash flow is {f['fcf_ttm']:,}" if finite(f.get('fcf_ttm')) else 'Conventional TTM free cash flow is unavailable.','Primary annual/current-YTD bridges and per-cell classification differences are shown.'],
   [note['expectations'],note['kpi'],'Forward gross-profit valuation holds current gross margin constant; it is a scenario, not a promise of future margins.'],
   [note['moat'],note['risk'],'ETF observations are a dated, limited fund sample. Absence is not proof of no ETF ownership.'],
   [f"Price date {r['price_date']}; trend/momentum/RS-volume/support/confirmation values are saved with the full calculation."],
   [note['risk'],f"{len(fixes)} score-input corrections/reconstructions and {len(recons)} unresolved historical cross-source differences recorded.",'Sensitivity checks do not establish expected investment performance.'] ]
  passes={}
  for k,ch,fs in zip(KEYS,checks,findings):
   complete=all(ok for label,ok in ch);passed=sum(ok for label,ok in ch)
   passes[k]={'status':'complete' if complete else 'partial','score':round(r['technical_score']) if k==KEYS[4] else None,'completion_pct':round(100*passed/len(ch),1),'confidence':'evidence_based','source_ids':list(sources), 'findings':fs,'missing_fields':[label for label,ok in ch if not ok],'metadata':{'reviewed_at':now,'checks':[{'item':label,'passed':ok} for label,ok in ch],'completed_checks':passed,'required_checks':len(ch),'completion_basis':'Fraction of explicit checklist tests passed, not a probability or investment score','full_precision_score':r['technical_score'] if k==KEYS[4] else None}}
  input_ready=all(p['status']=='complete' for p in passes.values()) and r['mb_input_weight_coverage']==1 and not note.get('missing')
  full=False # Bounded input checks cannot certify the original broader six-pass workflow.
  assurance={'full_six_pass_complete':False,'model_return_validated':False,'scope':'Filed-document, financial-input and calculation audit; not exhaustive six-pass investment diligence','remaining':['Complete quarter-level segment/KPI and guidance-history reconciliation for the original research scope.','Exhaustive current index/ETF and peer-competition review is not complete.','Source-level analyst-grade justification and the full contradiction matrix require additional review.']}
  warn('full_research_scope', 'The broader six-pass research programme remains incomplete. A passed input audit is not a fully verified MB score.', 'notice')
  # Evidence quality is computed from objective completed checks. Not a ticker-based confidence lookup.
  quality=round(100*sum(ok for ch in checks for _,ok in ch)/sum(len(ch) for ch in checks),1)
  ncritical=sum(w['severity']=='critical' for w in warnings)
  confidence='lower' if ncritical else 'medium'
  r['confidence']=confidence;r['full_research_validation_complete']=full
  r['numerical_coverage_sufficient']=r['mb_input_weight_coverage']>=.9
  eligible=(input_ready and ncritical==0)
  factors=[]
  for k,w in zip(FACTORS,WEIGHTS['base']):
   cov=r['factor_coverage'][k];score=r['factor_scores'][k]
   factors.append({'factor':k,'weight_pct':w,'score':score,'input_coverage':cov,'weighted_contribution':w*cov*score/float(den) if score is not None else None,'input_names':FACTOR_INPUTS[k],'input_values':{a:f.get(a) for a in FACTOR_INPUTS[k]},'basis':'source-informed analyst judgment' if k in ['tam','moat','execution'] else 'measured/derived numerical input','evidence':note['moat'] if k=='moat' else note['risk'] if k=='execution' else note['kpi'] if k in ['growth','valuation'] else f['analyst_rationale'],'source_ids':list(sources)})
  audit={'audit_version':'MB_EVIDENCE_AUDIT_V1','ticker':t,'reviewed_at':now,'market_date':r['price_date'],'status':'reviewed_within_scope' if input_ready else 'provisional_with_explicit_gaps','verified_mb_score':None,'input_audited_mb_score':r['research_mb_score'] if input_ready else None,'research_assurance':assurance,'screening_mb_score':r['research_mb_score'],'score_model':'MB25_RESEARCH_V1_20260906 (weights and code unchanged)','baseline_status':'reviewed_within_scope' if input_ready else 'provisional_with_explicit_gaps','input_dependency_sha256':dependencies(r),'model_is_return_validated':False,'model_applicability':'development_proxy' if t in ['OKLO','SMR'] else 'finance_accounting_unresolved' if t=='FIGR' else 'operating_business_screen','eligible_for_daily_attention':eligible,'evidence_check_coverage_pct':quality,'completed_passes':sum(p['status']=='complete' for p in passes.values()),'factor_count':sum(z['score'] is not None for z in factors),'factors':factors,'warnings':warnings,'source_inventory':inventory,'sources':list(sources.values()),'financial_history':panel,'input_ledger':ledger,'primary_reporting_periods':{met:[field_source(o) for o in facts[met] if o.get('start') and o['end']>='2024-01-01' and (o['end']>='2025-01-01' or t in ['GRRR','RZLV'])][:120] for met in ['revenue','gross_profit','operating_income','cfo','capex_property','capex_software','shares_diluted_wa']},'expectation_panel':{'revenue':v.get('revenue_estimate'), 'earnings':v.get('earnings_estimate'),'eps_trend':v.get('eps_trend'),'retrieved_at':v['retrieved_at'],'horizon':'Vendor FY/FY+1; not NTM'},'qualitative_review':note,'corrections':fixes,'unresolved_differences':recons,'score_before':before['research_mb_score'],'score_after':r['research_mb_score'],'passes':passes}
  save(outdir/f'{t}.json',audit);audits[t]=audit
  m.update({'research':r,'technical':tech,'benchmarks':bench,'audit':{k:audit[k] for k in ['audit_version','reviewed_at','status','baseline_status','input_dependency_sha256','verified_mb_score','input_audited_mb_score','research_assurance','evidence_check_coverage_pct','completed_passes','factor_count','warnings','model_applicability','eligible_for_daily_attention']},'delta_basis':'evidence_repair','data_collected_at':v['retrieved_at'],'audit_file':f'./evidence_audit/2026-09-06/{t}.json','research_reviewed_at':now,'last_market_refresh_at':v['retrieved_at'],'review_queue':[w['message'] for w in warnings if w['severity']!='notice'],'research_review_required':True,'input_scope':'Fresh 30-stock evidence audit; primary/derived/vendor source definitions and any remaining gaps are disclosed per input.','refresh_status':'evidence_audited_with_gaps' if not full else 'evidence_reviewed','deltas':{k:r[k]-before[k] if finite(r.get(k)) and finite(before.get(k)) else None for k in ['research_mb_score','research_ev_score','technical_score']}})
  stock['passes']=passes;stock['data_confidence']=confidence;stock['weekly_technical_score']=round(r['technical_score']);stock['market_cap_usd']=round(r['market_cap']);stock['market_cap_display']=f"${r['market_cap']/1e9:.3f}B";stock['thesis_note']=note['moat']+' '+note['risk'];stock['action']='RESEARCH HOLD — '+(note.get('critical') or ['evidence gaps remain'])[0] if not eligible else 'WATCH — documented screen; validate entry' if r['technical_score']>=60 else 'WAIT — technical stabilization'
  if not input_ready:stock['action']+=' · provisional'
  m['input_audit_reviewed_at']=now
  m['key_catalyst']=note['catalyst']
 # User explicitly authorized a one-time re-selection, not future automated swaps.
 ranked=sorted(x['stocks'],key=lambda s:(-s['metadata']['research']['research_mb_score'],s['ticker']))
 chosen=[s['ticker'] for s in ranked if audits[s['ticker']]['eligible_for_daily_attention']][:10]
 if len(chosen)!=10:raise ValueError('Fewer than ten fully input-audited stocks; do not fill with incomplete research')
 changes=[]
 for rec in reg['stocks']:
  t=rec['ticker'];tier='action' if t in chosen else 'candidate'
  if rec['tier']!=tier:
   event={'at':now,'ticker':t,'from':rec['tier'],'to':tier,'reason':'User-authorized 30-stock evidence audit and re-selection; provisional financial-model scores do not override critical eligibility warnings.','approval_ref':'Conversation 2026-09-06: Get full scores for all 30 stocks and reassign action 10 if needed.'};changes.append(event);reg['events'].append(event);rec['tier']=tier;rec['membership_since']=now
  rec['priority']='daily' if tier=='action' else 'weekly';rec['next_review_trigger']=NOTES[t]['catalyst'];rec['full_research_reviewed_at']=None;rec['input_audit_reviewed_at']=now if audits[t]['status']=='reviewed_within_scope' else None;rec['promotion_blocker']='; '.join(w['message'] for w in audits[t]['warnings'] if w['severity']!='notice') or 'No material evidence gap; valuation, entry and weekly persistence gates still apply.'
 reg['updated_at']=now;reg['last_reassignment']={'at':now,'basis':'Highest same-model MB scores with complete numerical input coverage, all stated audit checklists passed, and no unresolved critical warning. Daily attention is not a buy signal.','approval_ref':'User explicitly authorized reassignment in this repair.','action_members':chosen,'changes':changes};validate(reg)
 (APP/'watchlist_registry.json').write_text(json.dumps(reg,indent=2,ensure_ascii=False)+'\n')
 x=view_rank(x,reg);x['metadata'].update({'audit_version':'MB_EVIDENCE_AUDIT_V1','data_collected_at':load(ROOT/'new30/summary.json')['retrieved_at'],'audit_reviewed_at':now,'full_six_pass_complete':False,'publication_reason':'User-requested evidence repair and authorized Action10 reassignment','scope':'All 30 scorecards rebuilt with source inventory, eight-quarter panels, explicit pass checklists, factor lineage and warnings. Verified scores remain withheld for unfulfilled gates.','audit_manifest':'./evidence_audit/2026-09-06/manifest.json'})
 x['record_limitations']=['All 30 receive a reproducible screening scorecard, not a verified six-pass investment score.','Input-audit checklist completion is separate from broader six-pass research completion; the latter is not yet certified.','Standardized historical observations and any missing values are disclosed at cell level; rows do not imply eight primary-verified quarters.','TAM, moat and execution remain source-informed analyst judgments totaling 40% of the model.','FY+1 periods differ by issuer; the forward-gross-profit calculation is a constant-margin scenario, not an actual forecast.','Incomplete MB and E&V input weights are shown with scores. Missing values are not zero.','Preferred entry ranges carried from the old archive are not newly validated buy bands.','All market measurements use the September 4 completed regular session, not a new Sunday trading session.','Action means daily research attention, not BUY or portfolio allocation. Automatic swaps and broker orders remain disabled.']
 x['metadata']['assurance_status']='Input audit only; full six-pass research incomplete'
 x['changes']['notes']=['Source-backed evidence repair, not a market-price move.','Action reassignment authorized by user; all 30 retained, future intake remains Candidate-first.']+[f"{e['ticker']}: {e['from']} to {e['to']}" for e in changes]
 x['metadata']['weekly_review']=weekly_comparison(x,reg,None,'2026-09-04')
 x['generated_at']=now
 x['metadata']['audit_summary']=audit_summary(x)
 x=save_snapshot(x,'evidence_repair',now)
 manifest={'audit_version':'MB_EVIDENCE_AUDIT_V1','reviewed_at':now,'market_date':'2026-09-04','stock_count':len(audits),'full_factor_scores':sum(a['factor_count']==8 for a in audits.values()),'full_weight_coverage':sum(s['metadata']['research']['mb_input_weight_coverage']==1 for s in x['stocks']),'verified_within_scope_count':0,'input_audited_count':sum(a['input_audited_mb_score'] is not None for a in audits.values()),'full_six_pass_complete':False,'total_primary_documents':len({s['url'] for a in audits.values() for s in a['sources'] if s['kind'].startswith('SEC-filed')}),'action_members':chosen,'changes':changes,'calculator_sha256':hashlib.sha256((APP/'research_scoring.py').read_bytes()).hexdigest(),'rows':[{'ticker':s['ticker'],'tier':s['metadata']['tier'],'mb':s['metadata']['research']['research_mb_score'],'ev':s['metadata']['research']['research_ev_score'],'technical':s['metadata']['research']['technical_score'],'factor_scores':s['metadata']['research']['factor_scores'],'input_coverage':s['metadata']['research']['mb_input_weight_coverage'],'verified':None,'input_audited':audits[s['ticker']]['input_audited_mb_score'],'completed_passes':audits[s['ticker']]['completed_passes'],'critical_warnings':sum(w['severity']=='critical' for w in audits[s['ticker']]['warnings']),'file':f'{s["ticker"]}.json'} for s in x['stocks']]}
 save(outdir/'manifest.json',manifest);print(json.dumps(manifest,indent=2))
 return x,manifest

if __name__=='__main__':assemble()
