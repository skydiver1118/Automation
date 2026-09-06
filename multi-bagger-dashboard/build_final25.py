#!/usr/bin/env python3
"""Publish the user-approved 25-member list using an explicitly labelled research run.
No broker operations. Existing dated snapshots and Stock V2 files are never rewritten.
All calculations use the frozen same-session research evidence, not Sunday quotes.
"""
from __future__ import annotations
import copy, csv, hashlib, importlib.util, io, json, sys
from datetime import datetime, timezone
from pathlib import Path
from research_scoring import compute_all, FACTORS, WEIGHTS

APP=Path(__file__).resolve().parent
ROOT=APP.parent
PROJECT=ROOT/'stock-project-v2'
STUDY=APP/'research/2026-09-06'
PASS=['pass_1_primary_source_inventory','pass_2_financial_reconstruction','pass_3_forward_expectations','pass_4_risk_moat_sector_review','pass_5_technical_review','pass_6_adversarial_audit']


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def money(v):return '—' if v is None else f'${v:,.2f}'
def load(path):return json.loads(path.read_text())

# These are qualitative research judgments, not live economic indicators.
SECTOR={
 'IREN':('AI cloud / infrastructure','Bullish','AI compute demand and power access; capital intensity and capacity delivery risks.'),
 'APLD':('AI cloud / infrastructure','Bullish','Contracted AI/HPC demand; financing, customer concentration and construction risk.'),
 'NBIS':('AI cloud / infrastructure','Bullish','AI capacity expansion; large funding requirements and hyperscaler competition.'),
 'WULF':('AI cloud / infrastructure','Bullish','Power-backed computing leases; tenant concentration and buildout execution.'),
 'AMPX':('Advanced batteries','Bullish','Aviation and defense qualification; production ramp and unit-economics risk.'),
 'BKSY':('Space / defense intelligence','Bullish','Intelligence demand and constellation upgrades; capex and funding risk.'),
 'RKLB':('Space / defense','Bullish','Launch and space-systems demand; new vehicle execution and capital spending.'),
 'KTOS':('Defense / unmanned systems','Bullish','Uncrewed systems and propulsion demand; funded-order conversion, cash burn and dilution.'),
 'AVAV':('Defense / counter-drone','Bullish','Counter-drone and autonomous systems demand; acquisition integration and dilution.'),
 'HUBB':('Grid / electrification','Bullish','Grid replacement and electrification; acquisition debt and integration.'),
 'ETN':('Electrical / electrification','Bullish','AI electrical equipment and electrification; starting valuation and acquisition leverage.'),
 'VST':('Power generation','Bullish','Data-center electricity demand and scarce generation; hedging, commodity and leverage risks.'),
 'FIGR':('Digital lending / fintech','Neutral','Loan marketplace digitization; acquisition, credit and finance-accounting comparability.'),
 'ZETA':('Marketing software / AI','Bullish','AI-enabled marketing and first-party data; acquisition and competition risks.'),
 'TSSI':('AI infrastructure integration','Bullish','Rack integration demand; procurement mix, concentration and cash conversion.'),
 'RZLV':('Commerce software / AI','Neutral','Agentic commerce opportunity; organic validation, financing and going-concern risks.'),
 'CRMD':('Infection prevention / therapeutics','Neutral','Product commercialization; reimbursement and acquired-product concentration.'),
 'EVLV':('Security screening','Neutral','Recurring screening subscriptions; competitive and execution credibility risks.'),
 'RR':('Service robotics','Neutral','Automation demand; early revenue, unproven unit economics and dilution.'),
 'GRRR':('AI / security infrastructure','Neutral','Project demand; financing timing, concentration and collections.'),
 'AXTI':('Optical semiconductor materials','Bullish','AI optical interconnect demand; export-permit, China and cyclical exposure.'),
 'SOUN':('Voice / agentic AI','Bullish','Enterprise voice AI; post-LivePerson integration and capital structure reconciliation.'),
 'POET':('Optical interconnects','Bullish','AI optical integration; early commercialization and missing financial coverage.'),
 'SERV':('Autonomous delivery robotics','Neutral','Automation potential; issuer revenue cut, platform dependence and negative unit economics.'),
 'SSII':('Surgical robotics','Neutral','Robotic surgery adoption; funding, small scale and pending regulatory decisions.')}


def main():
    registry=load(APP/'final_list.json');inputs=load(STUDY/'inputs.json')
    rows=compute_all(inputs);details={r['financial']['ticker']:r for r in inputs['stocks']}
    if set(registry['members'])!={r['ticker'] for r in rows}:raise ValueError('Registry and recalculated research disagree')
    for r in rows:
        for k in ['research_mb_score','research_ev_score','technical_score']:
            a=r[k];b=details[r['ticker']]['expected'][k]
            if not(a is None and b is None) and (a is None or b is None or abs(a-b)>1e-10):raise ValueError(f'Frozen score changed: {r["ticker"]}/{k}')
    base=PROJECT/'data/multi_bagger'; prior=load(base/'pass_scores/2026-09-04.json');old={s['ticker']:s for s in prior['stocks']}
    if set(old)|set(registry['additions'])!=set(registry['members']):raise ValueError('Unexpected member removal/addition')
    archive={str(p):digest(p) for p in base.rglob('*') if p.is_file() and p.name!='latest.json' and '/history/' not in str(p)}
    dated=base/'pass_scores/2026-09-06.json'
    # Reruns keep the saved recording time; immutable conflicts still fail.
    now=load(dated)['recorded_at'] if dated.exists() else datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    membership=load(STUDY/'membership.json'); sources=load(STUDY/'sources.json')
    evidence_sources=[]
    for n,x in enumerate(sources):
        evidence_sources.append({'source_id':f'study-{n}','source_type':x['source_kind'],'title':x['ticker']+' — '+x.get('use','Research evidence'),'source_date':x.get('market_date'),'retrieved_at':x.get('retrieved_at'),'locator':x['locator'],'content_sha256':None,'notes':'Preserved from the September 6 research audit. A source date is not invented where only a cutoff was recorded.'})
    sid_by_t={t:[f'study-{n}' for n,x in enumerate(sources) if x['ticker']==t] for t in registry['members']}
    evidence_sources.append({'source_id':'frozen-study','source_type':'research_calculation','title':'Frozen common-calibration inputs, model and methodology','source_date':'2026-09-06','retrieved_at':inputs['data_collected_at'],'locator':'multi-bagger-dashboard/research/2026-09-06/inputs.json','content_sha256':digest(STUDY/'inputs.json'),'notes':'Scores reproduced with research_scoring.py; official archived scores were not used as inputs.'})
    for f in membership['funds']:
        evidence_sources.append({'source_id':'etf-'+f['fund'],'source_type':'primary_etf_holdings','title':f['fund']+' holdings','source_date':'2026-09-03' if 'Sep 03, 2026' in f.get('as_of_header','') else None,'retrieved_at':f['retrieved_at'],'locator':f['url'],'content_sha256':f.get('source_sha256'),'notes':f.get('as_of_header',f.get('error',''))})
    limitations=[
      'The final watchlist contains all 25 approved names. Membership is not a recommendation to buy.',
      'Displayed MB, E&V and Technical values use MB25_RESEARCH_V1_20260906. They are not reproduced official dashboard scores and are not comparable with the old calibration.',
      'This manual Sunday rebuild uses September 4 regular-session prices and the September 6 research collection; it is not a new trading session or a newly completed full SEC research run.',
      'Full eight-quarter reconstruction and full six-pass archival coverage remain incomplete. Coverage percentages describe model input weight, not research-pass completion.',
      'TAM, moat and execution are explicit analyst judgments (40% of the base weights). No calibrated P(5x) is available.',
      'E&V marked valuation-only omits an unavailable comparable positive-baseline EPS revision. POET has only 70% MB input-weight coverage.',
      'Index associations are corroborated via five primary ETF holdings files dated September 3, not an exhaustive certified index roster. Absence from those funds does not establish absence from all ETFs.',
      'Existing preferred entry zones are carried from the prior archive, not revalued under this calibration. New members have technical reference levels but no invented preferred valuation zone.',
      'FIGR finance accounting, GRRR financing timing, SOUN post-acquisition capitalization, and POET missing inputs limit comparability.']
    snapshot={'schema_version':'1.0.0','methodology_version':inputs['study'],'run_date':'2026-09-06','snapshot_revision':1,'market_session_date':'2026-09-04','run_type':'research_rerun','generated_at':inputs['data_collected_at'],'recorded_at':now,'source_time_precision':'exact','price_basis':'September 4, 2026 regular-session closing prices. Manual membership publication; not live quotes.','universe_size':25,'changes':{'top20_additions':registry['additions'],'top20_removals':[],'index_etf_changes':[],'entry_zone_hits':[],'notes':['Five approved additions; all prior 20 retained.','Research rank and score deltas against the old calibration are intentionally null, not zero.','New ETF evidence was verified from IVV, IWB, IWM, IJH and ITA; this is not a membership-change claim.']},'corrections':[
      {'ticker':'SERV','field':'thesis_note','prior_value':'Revenue growth / deployment narrative','corrected_value':'FY2026 revenue guidance reduced to $9–10M','reason':'The prior narrative did not fully reflect the August 6 issuer guidance cut.'},
      {'ticker':'RZLV','field':'H1_operating_cash_flow','prior_value':'approximately -$96.1M in earlier narrative','corrected_value':-91956000,'reason':'Reconciled to H1 issuer filing; restricted cash is excluded from unrestricted runway.'},
      {'ticker':'SOUN','field':'capitalization_confidence','prior_value':'Pre-transaction comparability assumed','corrected_value':'Provisional pending post-LivePerson reconciliation','reason':'Acquisition closed September 4; capital structure and estimates need a combined-company reconciliation.'}],
      'record_limitations':limitations,'metadata':{'display_mode':'common_calibration_research','score_status':'research_not_official','title':'Multi Bagger Final 25','data_collected_at':inputs['data_collected_at'],'publication_reason':'User-approved expansion from 20 to 25; no removals','full_six_pass_complete':False,'previous_snapshot_id':'2026-09-04','score_delta_comparable':False,'research_inputs_sha256':digest(STUDY/'inputs.json'),'scoring_code_sha256':digest(APP/'research_scoring.py'),'methodology_file':'./research/methodology.md','sources_scope':membership['scope']},'stocks':[]}
    scopes=load(STUDY/'pass_scope.json')
    for r in rows:
        t=r['ticker'];d=details[t];previous=old.get(t);is_new=t in registry['additions'];sec,trend,driver=SECTOR[t];holdings=[]
        for f in membership['funds']:
            for h in f['holdings']:
                if h['ticker']==t:holdings.append({'fund':f['fund'],'weight_pct':h['weight_pct'],'benchmark':f['benchmark'],'as_of':f.get('as_of_header'),'source':f['url']})
        zone=copy.deepcopy(previous['entry_zone']) if previous else {'low':None,'high':None,'display':'Not established','hit_status':'no_zone','qualifier':None}
        if previous:
            zone['qualifier']='Legacy preferred range from '+prior['run_date']+'; not revalued in this research calibration.'
            if zone['low'] is not None and zone['high'] is not None:zone['hit_status']='hit' if zone['low']<=r['price']<=zone['high'] else ('below' if r['price']<zone['low'] else 'above')
        else:zone['qualifier']='No preferred valuation entry was established; technical levels are references only.'
        if zone['hit_status']=='hit':snapshot['changes']['entry_zone_hits'].append(t)
        action=('RESEARCH HOLD — unresolved inputs' if t in ['POET','SOUN','GRRR','FIGR'] else 'AVOID NEW CAPITAL — thesis risk' if t in ['RZLV','SERV'] else 'WAIT — technical stabilization' if r['technical_score']<50 else 'WATCH — entry confirmation required')
        thesis='under_review' if t in ['POET','SOUN','GRRR','FIGR'] else 'weakened' if t in ['RZLV','SERV'] else 'intact_with_caveats'
        conf='low_medium' if r['confidence']=='Lower' else 'medium' if r['confidence']=='Medium' else 'medium_high'
        source_ids=sid_by_t[t]+['frozen-study'];passes={}
        for i,key in enumerate(PASS):
            scope=scopes[i];is_p5=i==4
            passes[key]={'status':'complete' if is_p5 else 'incomplete','score':round(r['technical_score']) if is_p5 else None,'completion_pct':100 if is_p5 else None,'confidence':conf,'source_ids':source_ids+(['etf-'+h['fund'] for h in holdings] if i==3 else []),'findings':[scope['completed']]+([r['analyst_rationale']] if i==3 else r['issues'] if i==5 else []),'missing_fields':[] if is_p5 else [scope['remaining']],'metadata':{'scope':'Completed research-formula calculation, not reproduction of the archived technical engine' if is_p5 else 'Useful partial work; not certified complete; no invented completion percentage','full_precision_score':r['technical_score'] if is_p5 else None}}
        row={'ticker':t,'rank':r['research_rank'],'rank_delta':None,'market_cap_usd':round(r['market_cap']),'market_cap_display':f"${r['market_cap']/1e9:,.3f}B",'multi_bagger_score':None,'multi_bagger_score_delta':None,'expectation_valuation_score':None,'expectation_valuation_score_delta':None,'weekly_technical_score':round(r['technical_score']),'weekly_technical_score_delta':None,'probability_5x_pct':None,'data_confidence':conf,'action':action,'thesis_status':thesis,'thesis_note':r['analyst_rationale'],'entry_zone':zone,'passes':passes,'metadata':{
          'final_member':True,'new_member':is_new,'company':d['company'],'sector':sec,'sector_trend':trend,'sector_trend_basis':'Analyst sector judgment from the sourced September 6 study, not a live sector index signal','sector_drivers_risks':driver,
          'research':r,'technical':d['technical'],'etf_holdings':holdings,'index_associations':[{'index':h['benchmark'],'via':h['fund'],'status':'ETF benchmark corroboration; not certified direct index roster'} for h in holdings if h['fund']!='ITA'],'membership_confidence':'Primary fund holdings verified; complete index/ETF universe not checked' if holdings else 'Not found in the five scanned ETFs; broader ETF/index membership unverified','data_collected_at':inputs['data_collected_at'],'probability_5x_status':'Not estimated: no calibrated model','key_catalyst':'Next earnings / guidance and execution confirmation; September 9 earnings are pending' if t=='AVAV' else 'Next issuer financial / commercial update; see sourced thesis and risk record','technical_references':{'support_20d_low':d['technical']['low20'],'resistance_20d_high':d['technical']['high20'],'ma20':d['technical']['ma20'],'ma50':d['technical']['ma50'],'ma200':d['technical']['ma200'],'label':'Historical chart reference, not a preferred fundamental valuation entry'},
          'prior_archive':{'run_date':prior['run_date'],'market_date':prior['market_session_date'],'rank':previous['rank'],'mb':previous['multi_bagger_score'],'ev':previous['expectation_valuation_score'],'technical':previous['weekly_technical_score'],'action':previous['action'],'confidence':previous['data_confidence'],'thesis_status':previous['thesis_status'],'entry_zone_hit_status':previous['entry_zone']['hit_status'],'score_comparable':False} if previous else None,
          'market_cap_delta_pct':(r['market_cap']/previous['market_cap_usd']-1)*100 if previous and previous['market_cap_usd'] else None,
          'sources':[x for x in sources if x['ticker']==t]}}
        snapshot['stocks'].append(row)
    evidence={'schema_version':'1.0.0','run_date':'2026-09-06','snapshot_revision':1,'sources':evidence_sources,'limitations':limitations}
    spec=importlib.util.spec_from_file_location('store',PROJECT/'scripts/store_multibagger_pass_scores.py');store=importlib.util.module_from_spec(spec);spec.loader.exec_module(store)
    store.persist_snapshot(snapshot,PROJECT,evidence=evidence)
    for p,h in archive.items():
        if digest(Path(p))!=h:raise ValueError('Historical artifact changed: '+p)
    print(store.verify_repository(PROJECT))
    (STUDY/'calculated.json').write_text(json.dumps({'study':inputs['study'],'rows':rows,'inputs_sha256':digest(STUDY/'inputs.json'),'scoring_code_sha256':digest(APP/'research_scoring.py')},separators=(',',':'),allow_nan=False)+'\n')
    fields=['run_date','methodology','rank','ticker','price','market_cap','mb_research','ev_research','technical_research','mb_input_coverage','ev_input_coverage','official_mb','new_member']
    buf=io.StringIO();w=csv.DictWriter(buf,fieldnames=fields);w.writeheader()
    for s in snapshot['stocks']:
        r=s['metadata']['research'];w.writerow(dict(zip(fields,['2026-09-06',inputs['study'],s['rank'],s['ticker'],r['price'],r['market_cap'],r['research_mb_score'],r['research_ev_score'],r['technical_score'],r['mb_input_weight_coverage'],r['ev_input_weight_coverage'],'',s['metadata']['new_member']])))
    (base/'history/research_score_history.csv').write_text(buf.getvalue())
    print('Final 25 membership publication prepared; no existing member removed. Research fields are separately named; official MB/E&V/P(5x) remain null.')

if __name__=='__main__':main()
