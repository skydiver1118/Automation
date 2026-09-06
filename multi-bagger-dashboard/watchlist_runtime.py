#!/usr/bin/env python3
"""Daily Action / weekly Candidate monitoring with immutable snapshots.

Uses the unchanged research calculator. Market data and estimates can be refreshed
mechanically; reviewed statements and analyst grades retain their true review date.
New filings/financial periods create research holds, never fabricated six-pass reviews.
"""
from __future__ import annotations
import argparse
import copy
import csv
import hashlib
import io
import json
import math
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo
import numpy as np
import pandas as pd
import exchange_calendars as xcals
from research_scoring import calculate, technical as technical_score
from watchlist import APP, REGISTRY, load, members, now_iso, validate

DATA = APP / 'monitoring'
BASE = APP.parent / 'stock-project-v2/data/multi_bagger'
ET = ZoneInfo('America/New_York')
METHOD = 'MB25_RESEARCH_V1_20260906'
PASS_KEYS = ['pass_1_primary_source_inventory','pass_2_financial_reconstruction',
 'pass_3_forward_expectations','pass_4_risk_moat_sector_review','pass_5_technical_review','pass_6_adversarial_audit']

def clean(x):
    if isinstance(x, dict): return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x, (list,tuple)): return [clean(v) for v in x]
    if isinstance(x, (np.integer,)): return int(x)
    if isinstance(x, (float,np.floating)): return float(x) if math.isfinite(x) else None
    if isinstance(x, (datetime,pd.Timestamp)): return x.isoformat()
    if x is pd.NA: return None
    return x

def write(path: Path, obj: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    text=json.dumps(clean(obj),ensure_ascii=False,separators=(',',':'),allow_nan=False)+'\n'
    tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(text,encoding='utf-8');tmp.replace(path)

def finite(x): return isinstance(x,(int,float,np.number)) and not isinstance(x,bool) and math.isfinite(float(x))

def market_gate(at: datetime, mode: str) -> dict:
    if at.tzinfo is None: raise ValueError('Timezone-aware time required')
    local=at.astimezone(ET);d=local.date().isoformat()
    overrides=load(APP/'market_closures.json')
    if d in overrides.get('full_day_closures',{}):
        return {'run':False,'notify':False,'reason':'full_day_closure_override','date':d}
    start=(local.date()-timedelta(days=60)).isoformat();end=(local.date()+timedelta(days=15)).isoformat()
    calendars=[xcals.get_calendar(c,start=start,end=end) for c in ['XNYS','XNAS']]
    is_open=all(c.is_session(d) for c in calendars)
    if mode=='daily' and not is_open:
        return {'run':False,'notify':False,'reason':'no_regular_trading_session','date':d}
    now_utc=pd.Timestamp(at).tz_convert('UTC')
    dates=None
    for c in calendars:
        rows=c.schedule[c.schedule['close']<now_utc]
        sessions={str(v.date()) for v in rows.index}
        dates=sessions if dates is None else dates & sessions
    dates=sorted(v for v in dates if v not in overrides.get('full_day_closures',{}))
    if not dates: raise ValueError('No verified completed market session')
    return {'run':True,'notify':bool(mode=='daily' and is_open),'date':d,
        'market_session_date':dates[-1], 'calendar_check':'XNYS + XNAS; known holidays/adhoc closures plus override file',
        'early_close':bool(is_open and (calendars[0].session_close(d)-calendars[0].session_open(d))<pd.Timedelta(hours=6,minutes=30))}

def technical(frame: pd.DataFrame, target: str) -> dict:
    f=frame.loc[pd.to_datetime(frame.index).date<=pd.Timestamp(target).date()].copy().dropna(subset=['Close'])
    if len(f)<200 or str(f.index[-1].date())!=target: raise ValueError('Insufficient/exact-session price data')
    c,h,l,v=f.Close,f.High,f.Low,f.Volume
    a=f['Adj Close'] if 'Adj Close' in f else c
    d=c.diff();up=d.clip(lower=0).ewm(alpha=1/14,adjust=False).mean();down=(-d.clip(upper=0)).ewm(alpha=1/14,adjust=False).mean()
    rsi=100-100/(1+up/down.replace(0,np.nan))
    macd=c.ewm(span=12,adjust=False).mean()-c.ewm(span=26,adjust=False).mean();sig=macd.ewm(span=9,adjust=False).mean()
    tr=pd.concat([h-l,(h-c.shift()).abs(),(l-c.shift()).abs()],axis=1).max(axis=1);atr=tr.ewm(alpha=1/14,adjust=False).mean()
    u=h.diff();dn=-l.diff();pdm=u.where((u>dn)&(u>0),0.);mdm=dn.where((dn>u)&(dn>0),0.)
    pdi=100*pdm.ewm(alpha=1/14,adjust=False).mean()/atr;mdi=100*mdm.ewm(alpha=1/14,adjust=False).mean()/atr
    adx=(100*(pdi-mdi).abs()/(pdi+mdi).replace(0,np.nan)).ewm(alpha=1/14,adjust=False).mean()
    out={'price':float(c.iloc[-1]),'price_date':target,'rsi14':rsi.iloc[-1],'macd':macd.iloc[-1],
      'macd_signal':sig.iloc[-1],'macd_hist':(macd-sig).iloc[-1],'adx14':adx.iloc[-1],
      'plus_di':pdi.iloc[-1],'minus_di':mdi.iloc[-1],'atr14':atr.iloc[-1],
      'volume_ratio20':v.iloc[-1]/v.tail(20).mean(),'high20':h.tail(20).max(),'low20':l.tail(20).min(),
      'high252':h.tail(252).max(),'low252':l.tail(252).min(),'observations':len(f)}
    for n in [20,50,200]:out[f'ma{n}']=c.tail(n).mean()
    for name,n in [('1m',21),('3m',63),('6m',126),('12m',252)]:out['return_'+name]=a.iloc[-1]/a.iloc[-1-n]-1 if len(a)>n else None
    out=clean(out)
    required=['price','rsi14','macd_hist','adx14','plus_di','minus_di','atr14','volume_ratio20','high20','low20','ma20','ma50','ma200','return_1m','return_3m']
    if not all(finite(out[k]) for k in required) or out['atr14']<=0 or out['high20']<=out['low20']:
        raise ValueError('Nonfinite/degenerate technical inputs; do not score')
    return out

def empty_stock(ticker: str) -> dict:
    passes={k:{'status':'incomplete','score':None,'completion_pct':None,'confidence':'unknown',
       'source_ids':[],'findings':['Candidate intake; not researched.'], 'missing_fields':['Sourced assessment required.']} for k in PASS_KEYS}
    return {'ticker':ticker,'rank':0,'rank_delta':None,'market_cap_usd':None,'market_cap_display':'Not verified',
        'multi_bagger_score':None,'multi_bagger_score_delta':None,'expectation_valuation_score':None,
        'expectation_valuation_score_delta':None,'weekly_technical_score':None,'weekly_technical_score_delta':None,
        'probability_5x_pct':None,'data_confidence':'unknown','action':'RESEARCH HOLD — unreviewed candidate',
        'thesis_status':'under_review','thesis_note':'New stock starts in Candidates. No score inferred from its ticker.',
        'entry_zone':{'display':'Not established','low':None,'high':None,'qualifier':'Research required','hit_status':'no_zone'},
        'passes':passes,'metadata':{'research':{},'company':{'name':ticker},'sources':[], 'technical':{}}}

def view_rank(snapshot: dict, registry: dict) -> dict:
    """Ranks are within tier; a daily score is never compared to a stale candidate rank."""
    validate(registry); x=copy.deepcopy(snapshot);src={s['ticker']:s for s in x['stocks']};out=[]
    for tier in ['action','candidate']:
        rows=[]
        for rec in registry['stocks']:
            if rec['tier']!=tier:continue
            s=src.get(rec['ticker'],empty_stock(rec['ticker']));m=s.setdefault('metadata',{})
            m['membership']=copy.deepcopy(rec);m['tier']=tier;m['new_member']=rec['origin']=='photo_back_pocket'
            r=m.get('research',{});m['promotion_blocker']=rec['promotion_blocker']
            m['research_reviewed_at']=m.get('research_reviewed_at') or m.get('data_collected_at')
            rows.append(s)
        rows.sort(key=lambda s:(-(s['metadata'].get('research',{}).get('research_mb_score') if finite(s['metadata'].get('research',{}).get('research_mb_score')) else -1),s['ticker']))
        for i,s in enumerate(rows,1):s['metadata']['tier_rank']=i;s['rank']=len(out)+1;out.append(s)
    x['stocks']=out;x['universe_size']=len(out)
    x.setdefault('metadata',{}).update({'display_mode':'common_calibration_research','watchlist_schema':'action_candidate_v1',
       'registry':copy.deepcopy(registry),'action_count':len(members(registry,'action')),'candidate_count':len(members(registry,'candidate')),
       'ranking_basis':'Within each tier at its own stated market-data date. Cross-list comparisons occur only in the common-date weekly review.'})
    return x

def snapshot_id(x: dict) -> str: return x['metadata']['monitoring_id']

def save_snapshot(snapshot: dict, mode: str, timestamp: str | None=None) -> dict:
    x=copy.deepcopy(snapshot);ts=timestamp or now_iso();tag=ts.replace(':','').replace('+0000','Z').replace('+00:00','Z')
    sid=tag+'-'+mode
    x['metadata'].update({'monitoring_id':sid,'refresh_kind':mode,'recorded_at':ts})
    x['recorded_at']=ts;x['run_date']=ts[:10]
    path=DATA/'runs'/f'{sid}.json'
    if path.exists():
        if load(path)!=x:raise ValueError('Conflicting immutable monitoring snapshot')
    else:write(path,x)
    # Write latest only after the immutable run exists.
    write(DATA/'latest.json',x)
    history=[]
    for p in sorted((DATA/'runs').glob('*.json')):
        v=load(p);history.append({'id':p.stem,'count':v['universe_size'],'methodology':v['methodology_version'],
          'market_session_date':v['market_session_date'],'path':'./monitoring/runs/'+p.name,
          'mode':v['metadata']['refresh_kind']})
    write(DATA/'history.json',{'snapshots':history})
    return x

def seed() -> dict:
    if (DATA/'latest.json').exists():return view_rank(load(DATA/'latest.json'),load(REGISTRY))
    x=copy.deepcopy(load(BASE/'pass_scores/2026-09-06.json')); reg=load(REGISTRY)
    cs=load(APP/'research/candidate_seed_2026-09-06.json')
    for entry in cs['stocks']:
        f=copy.deepcopy(entry['financial']); t=f['ticker']; result=calculate(f,{'technical':entry['technical']},cs['benchmarks'])
        for k,v in entry['expected'].items():
            if (result[k] is None)!=(v is None) or v is not None and abs(result[k]-v)>1e-8:
                raise ValueError(f'Candidate calibration mismatch {t}/{k}')
        s=empty_stock(t);a=entry['assessment'];s.update({'market_cap_usd':round(result['market_cap']),
          'market_cap_display':f"${result['market_cap']/1e9:.3f}B",'data_confidence':'low_medium',
          'weekly_technical_score':round(result['technical_score']),'action':'WATCH — candidate; '+a['next_check'],
          'thesis_status':'intact_with_caveats','thesis_note':a['assessment']+' '+a['bear']})
        s['metadata'].update({'research':result,'company':entry['company'],'technical':entry['technical'],
          'data_collected_at':entry['data_collected_at'],'sector':entry['company']['industry'],
          'sector_trend':'Not newly assessed','sector_drivers_risks':a['bull']+' '+a['bear'],
          'key_catalyst':a['catalyst'],'sources':[{'locator':result['primary_source'],'source_kind':'issuer results / filing','cutoff':'2026-09-06'},
            {'locator':result['market_source'],'source_kind':'market vendor','retrieved_at':entry['data_collected_at']}],
          'etf_holdings':[],'membership_confidence':'ETF evidence remains in the source research; no new holdings scan claimed.'})
        for k in PASS_KEYS:
            s['passes'][k]['findings']=[a['assessment']];s['passes'][k]['missing_fields']=['Complete source-backed pass record still required.']
        s['passes'][PASS_KEYS[4]].update({'status':'complete','score':round(result['technical_score']),'completion_pct':100,
          'confidence':'medium_high','missing_fields':[], 'metadata':{'scope':'Research technical computation, not full six-pass certification.','full_precision_score':result['technical_score']}})
        x['stocks'].append(s)
    for s in x['stocks']:
        m=s['metadata'];r=m['research'];m['benchmarks']=cs['benchmarks'] if s['ticker'] in {v['financial']['ticker'] for v in cs['stocks']} else load(APP/'research/2026-09-06/inputs.json')['benchmarks'];m['last_market_refresh_at']=m['data_collected_at']
        m['research_reviewed_at']=m['data_collected_at'];m['last_weekly_comparison_at']=None
        m['input_scope']='Reviewed September 6 financial/consensus inputs; no new earnings analysis claimed.'
        m['refresh_status']='saved_research_baseline';m['deltas']={}
    x['changes']={'top20_additions':['RGTI','QBTS','OKLO','SMR','EOSE'],'top20_removals':[],
        'index_etf_changes':[],'entry_zone_hits':[], 'notes':[
        'User approved Action10; the highest 10 existing research ranks selected. Other 15 retained as Candidates.',
        'Five non-biotech back-pocket names added to Candidates. No stock deleted.',
        'All future intake is Candidate-first. Weekly reviews only recommend swaps; no automatic promotions.',
        'This is a list-structure rebuild from saved same-session evidence, not a new financial-statement review.']}
    x['metadata'].update({'weekly_review':{'status':'not_yet_run','proposals':[], 'note':'First scheduled common-date comparison will evaluate all 30. Initial scores retain their reviewed source dates.'},
        'scope':'Membership migration with unchanged research calibration; partial six-pass research disclosed.',
        'last_daily_refresh_at':None,'last_weekly_refresh_at':None})
    x['record_limitations'] += ['Action is a daily-attention tier, not BUY. Candidate quotes/scores update weekly; daily candidate event scans do not refresh those scores.',
       'Full research completion is not inferred from numerical coverage or an automated market-data refresh. Unreviewed statements/filings block promotion.',
       'No new entry ranges were invented. Legacy ranges are not newly validated buy bands.']
    return save_snapshot(view_rank(x,reg),'membership_migration')

def weekly_comparison(x: dict, reg: dict, previous: dict | None, target: str) -> dict:
    """Opportunity queue with explicit blockers, fixed pairs, and unique-week streaks."""
    rows=x['stocks'];actions=[s for s in rows if s['metadata']['tier']=='action'];candidates=[s for s in rows if s['metadata']['tier']=='candidate']
    records=[];week=pd.Timestamp(target).isocalendar();week_id=f'{week.year}-W{week.week:02d}'
    prev_map={p['candidate']:p for p in (previous or {}).get('proposals',[])}
    for c in candidates:
        cr=c['metadata'].get('research',{});cv=cr.get('research_mb_score')
        valid_actions=[a for a in actions if finite(a['metadata'].get('research',{}).get('research_mb_score'))]
        a=min(valid_actions,key=lambda s:s['metadata']['research']['research_mb_score']) if valid_actions else None
        ar=a['metadata']['research'] if a else {};gap=cv-ar['research_mb_score'] if a and finite(cv) else None
        blockers=[]
        if c['metadata'].get('research_review_required') or c['metadata'].get('refresh_status')!='market_and_estimates_refreshed':blockers.append('Pending or failed evidence refresh')
        if cr.get('price_date')!=target or ar.get('price_date')!=target:blockers.append('Price dates not aligned')
        if cr.get('mb_input_weight_coverage',0)<.9:blockers.append('Less than 90% numerical input coverage')
        if not c['metadata']['membership'].get('full_research_reviewed_at'):blockers.append('Full sourced research not cleared')
        if not a or not a['metadata']['membership'].get('full_research_reviewed_at'):blockers.append('Incumbent research comparison not cleared')
        if cr.get('comparison_caveat') or c['metadata']['membership'].get('model_scope')=='project_stage_proxy':blockers.append('Model/accounting comparability unresolved')
        if cr.get('ev_input_weight_coverage',0)<.99 or ar.get('ev_input_weight_coverage',0)<.99:blockers.append('E&V components not fully comparable')
        # No one-number valuation threshold replaces the documented thesis blocker.
        if not c['metadata']['membership'].get('promotion_blocker_cleared',False):blockers.append('Documented promotion blocker not cleared')
        sensitive=a and all(finite(cr.get(k)) and cr[k]>ar.get(k,float('inf')) for k in ['growth_weight_score','quality_weight_score'])
        if not sensitive:blockers.append('Advantage not robust under both alternate weights')
        recent_swaps=[e for e in reg.get('events',[]) if e.get('from') in ['candidate','action'] and e.get('ticker') in [c['ticker'],a['ticker'] if a else None] and e.get('to') in ['candidate','action']]
        if any((pd.Timestamp(target).date()-pd.Timestamp(e['at']).date()).days<reg['promotion_policy']['cooldown_days'] for e in recent_swaps):blockers.append('Membership cooldown active')
        qualifies=bool(gap is not None and gap>=reg['promotion_policy']['min_mb_gap'] and not blockers)
        p=prev_map.get(c['ticker'],{});prior_date=(previous or {}).get('market_session_date')
        last_week=pd.Timestamp(prior_date).isocalendar() if prior_date else None
        consecutive=bool(prior_date and 0<(pd.Timestamp(target)-pd.Timestamp(prior_date)).days<=9 and (last_week.year,last_week.week)!=(week.year,week.week))
        streak=(p.get('qualified_weeks',0)+1 if consecutive and p.get('counterpart')==(a or {}).get('ticker') else 1) if qualifies else 0
        if (previous or {}).get('week_id')==week_id:
            streak=(p.get('qualified_weeks',0) or 1) if qualifies else 0
        records.append({'candidate':c['ticker'],'counterpart':a['ticker'] if a else None,'mb_gap':gap,
          'qualified_weeks':streak,'status':'recommendation_pending_approval' if qualifies and streak>=2 else 'keep_candidate',
          'blockers':blockers,'trigger':c['metadata']['membership']['next_review_trigger']})
    records.sort(key=lambda p:-(p['mb_gap'] if p['mb_gap'] is not None else -1e9))
    # At most two non-overlapping swaps can ever be recommended in one report.
    used=set();count=0
    for p in records:
        if p['status']=='recommendation_pending_approval':
            if p['counterpart'] in used or count>=2:p['status']='qualified_waiting_for_slot'
            else: used.add(p['counterpart']);count+=1
    return {'status':'comparison_complete_research_gates_apply','week_id':week_id,'market_session_date':target,
       'compared_at':now_iso(),'proposals':records,'automatic_swaps':False,
       'note':'Same calculator and market date across both tiers; ranking is not permission to buy or swap.'}

def _filings(ticker_object, since: str) -> dict:
    """Vendor SEC filing inventory is a trigger, not a substitute for reading filings."""
    try:
        raw=ticker_object.get_sec_filings()
        if raw is None:raise ValueError('Filing inventory missing')
        rows=raw.get('filings',[]) if isinstance(raw,dict) else raw
        hits=[]
        for r in rows:
            if not isinstance(r,dict):continue
            dt=r.get('date') or r.get('filingDate')
            if not dt and r.get('epochDate'):dt=datetime.fromtimestamp(r['epochDate'],timezone.utc).date().isoformat()
            if dt and str(dt)[:10]>since[:10] and str(r.get('type',r.get('form',''))).upper() in ['10-K','10-Q','8-K','6-K','20-F','40-F','10-Q/A','10-K/A']:
                hits.append({'date':str(dt)[:10],'form':r.get('type',r.get('form')),'url':r.get('edgarUrl',r.get('url'))})
        return {'status':'checked','new_filings':hits,'checked_at':now_iso(),'scope':'SEC filing metadata via market vendor; materiality and full text require review.'}
    except Exception as e:
        return {'status':'unavailable','new_filings':[],'checked_at':now_iso(),'error':type(e).__name__}

def refresh(mode: str, at: datetime | None=None) -> dict:
    at=at or datetime.now(timezone.utc);gate=market_gate(at,mode)
    if not gate['run']:return {'skipped':True,**gate}
    import yfinance as yf
    reg=load(REGISTRY)
    if hashlib.sha256((APP/'research_scoring.py').read_bytes()).hexdigest()!=reg['scoring_code_sha256']:raise ValueError('Calculator changed without a version migration')
    original=load(DATA/'latest.json');x=view_rank(original,reg)
    target=gate['market_session_date'];selected=set(members(reg,'action') if mode=='daily' else members(reg))
    tickers=sorted(selected|{'QQQ','SMH'})
    raw=yf.download(tickers,start=(pd.Timestamp(target)-pd.Timedelta(days=820)).date().isoformat(),
        end=(pd.Timestamp(target)+pd.Timedelta(days=1)).date().isoformat(),auto_adjust=False,group_by='ticker',progress=False,threads=True)
    def frame(t):
        if isinstance(raw.columns,pd.MultiIndex):
            if t in raw.columns.get_level_values(0):return raw[t].dropna(subset=['Close'])
            return raw.xs(t,axis=1,level=1).dropna(subset=['Close'])
        return raw
    bench={t:technical(frame(t),target) for t in ['QQQ','SMH']}
    ts=at.replace(microsecond=0).isoformat();succeeded=[];errors={};material=[]
    for s in x['stocks']:
        t=s['ticker'];m=s['metadata'];yf_t=yf.Ticker(t)
        event=_filings(yf_t,m.get('research_reviewed_at') or '2026-09-06');m['event_scan']=event
        if event['new_filings']:
            m['research_review_required']=True;material.append(t+': new filing requires review')
        if t not in selected:continue # Candidates retain their true weekly score/price date.
        try:
            tech=technical(frame(t),target);old=copy.deepcopy(m.get('research',{}));info=yf_t.get_info()
            if not old.get('analyst_grades'):
                ta,parts=technical_score(tech,bench)
                m['technical']=tech;m['benchmarks']=bench;m['last_market_refresh_at']=ts
                m['research']={**old,'price':tech['price'],'price_date':target,'technical_score':ta,'technical_components':parts}
                s['weekly_technical_score']=round(ta);s['passes'][PASS_KEYS[4]].update({'status':'complete','completion_pct':100,'score':round(ta),'missing_fields':[], 'metadata':{'scope':'Research technical calculation only','full_precision_score':ta}})
                m['refresh_status']='unreviewed_candidate';s['action']='RESEARCH HOLD — candidate intake'
                succeeded.append(t)
                continue
            f=copy.deepcopy(old);review=[]
            if info.get('mostRecentQuarter'):
                reported=datetime.fromtimestamp(info['mostRecentQuarter'],timezone.utc).date().isoformat()
                if reported>str(f.get('financial_period_end') or ''):review.append('New financial period; audited statement bridge not yet updated')
            # Use economic shares implied by vendor market cap/quote; never silently drop paired classes.
            quote=info.get('regularMarketPrice');cap=info.get('marketCap')
            shares=cap/quote if finite(cap) and finite(quote) and quote>0 else None
            if shares is None:raise ValueError('Market capitalization/share bridge unavailable')
            oldshares=old['market_cap']/old['price']
            if abs(shares/oldshares-1)>.05:review.append('More than 5% economic-share change; reconcile financing/splits/classes')
            # Retain reviewed common-equity bridge for flagged share changes, identify estimate clearly.
            use_shares=oldshares if review and abs(shares/oldshares-1)>.05 else shares
            f.update({'price':tech['price'],'price_date':target,'market_cap':use_shares*tech['price']})
            f['enterprise_value']=f['market_cap']+(old['enterprise_value']-old['market_cap'])
            f['market_cap_basis']='Latest price x reviewed economic shares' if use_shares==oldshares else 'Latest close x vendor implied economic shares'
            # Acquisition/debt/restricted-cash claims remain reviewed, not overwritten with generic vendor totals.
            try:
                rev=yf_t.get_revenue_estimate();eps=yf_t.get_eps_trend()
                if '+1y' not in rev.index:raise ValueError('FY+1 consensus unavailable')
                f['next_year_revenue']=float(rev.loc['+1y','avg']);f['next_year_growth']=float(rev.loc['+1y','growth'])
                if not finite(f['next_year_revenue']) or not finite(f['next_year_growth']):raise ValueError('Incomplete consensus')
                f['eps_current']=float(eps.loc['+1y','current']) if '+1y' in eps.index and 'current' in eps else None
                f['eps_90days_ago']=float(eps.loc['+1y','90daysAgo']) if '+1y' in eps.index and '90daysAgo' in eps else None
                m['estimates_refreshed_at']=ts
            except Exception:
                # Withhold unavailable live consensus rather than relabel a stale estimate as new.
                f['next_year_revenue']=None;f['next_year_growth']=None;f['eps_current']=None;f['eps_90days_ago']=None
                review.append('Fresh consensus unavailable; affected components withheld')
            result=calculate(clean(f),{'technical':tech},bench)
            m.update({'research':result,'technical':tech,'benchmarks':bench,'last_market_refresh_at':ts,
                'refresh_status':'market_and_estimates_refreshed','input_scope':'Prices/estimates updated; reviewed statements and analyst grades carried forward with original dates.',
                'research_review_required':bool(review or m.get('research_review_required')),'review_queue':review,
                'deltas':{k:(result[k]-old[k] if finite(result.get(k)) and finite(old.get(k)) else None) for k in ['research_mb_score','research_ev_score','technical_score']}})
            if event['status']!='checked':m['review_queue'].append('Filing inventory unavailable');m['research_review_required']=True
            s['market_cap_usd']=round(result['market_cap']);s['market_cap_display']=f"${result['market_cap']/1e9:.3f}B"
            s['weekly_technical_score']=round(result['technical_score']);p5=s['passes'][PASS_KEYS[4]]
            p5.update({'status':'complete','score':s['weekly_technical_score'],'completion_pct':100,'missing_fields':[]})
            p5['metadata']={'scope':'Completed research technical computation only','full_precision_score':result['technical_score'],'as_of':target}
            z=s['entry_zone']
            if finite(z.get('low')) and finite(z.get('high')):
                z['hit_status']='hit' if z['low']<=tech['price']<=z['high'] else 'above' if tech['price']>z['high'] else 'below'
            if m.get('research_review_required'):s['action']='RESEARCH HOLD — new or unresolved evidence'
            elif z.get('hit_status')=='hit':s['action']='Within entry band — timing remains weak' if result['technical_score']<60 else 'WATCH — in legacy band; validate entry thesis'
            elif result['technical_score']>=60:s['action']='WATCH — improving timing; no verified entry signal'
            else:s['action']='WAIT — technical stabilization'
            if abs(m['deltas'].get('research_mb_score') or 0)>=3 or abs(m['deltas'].get('technical_score') or 0)>=10 or review:material.append(t+': score/evidence change')
            succeeded.append(t)
        except Exception as e:
            # Keep last good measurement and its date, but never call it refreshed.
            m['refresh_status']='stale_refresh_failed';m['refresh_error']=type(e).__name__+': '+str(e)[:200]
            m['research_review_required']=True;errors[t]=m['refresh_error']
    if len(succeeded)<max(1,math.ceil(.8*len(selected))):
        raise RuntimeError('Insufficient refresh coverage; retain last published snapshot. '+json.dumps(errors))
    previous=original['metadata'].get('weekly_review')
    x['metadata'].update({'scope':'Incremental automated monitoring, not a complete new six-pass research certification.',
        'refresh_summary':{'requested':len(selected),'refreshed':len(succeeded),'failed':errors,'candidate_event_scan_only':mode=='daily',
            'market_session_date':target,'last_verified_statement_review_dates_preserved':True},'calendar_gate':gate,
        'material_changes':sorted(set(material)),'scoring_code_sha256':hashlib.sha256((APP/'research_scoring.py').read_bytes()).hexdigest()})
    x['market_session_date']=target;x['generated_at']=ts
    x['metadata']['last_daily_refresh_at' if mode=='daily' else 'last_weekly_refresh_at']=ts
    if mode=='weekly':
        x['metadata']['weekly_review']=weekly_comparison(x,reg,previous,target)
        for s in x['stocks']:s['metadata']['last_weekly_comparison_at']=ts
    x['changes']['top20_additions']=[];x['changes']['top20_removals']=[]
    x['changes']['entry_zone_hits']=[s['ticker'] for s in x['stocks'] if s['metadata']['tier']=='action' and s['entry_zone']['hit_status']=='hit']
    x['metadata']['notify']=bool(gate['notify'] and (material or (previous or {}).get('compared_at','')>(original['metadata'].get('last_daily_refresh_at') or '')))
    x['changes']['notes']=['Daily refresh affects Action members only; candidate scores retain weekly dates.' if mode=='daily' else 'Weekly mathematical comparison refreshed both tiers on the same completed session.',
        'Reviewed financial bridges and analyst grades are not automatically replaced. Material new disclosures enter the review queue. Membership unchanged.']
    write(DATA/'last_attempt.json',{'at':ts,'status':'success_with_disclosed_gaps' if errors else 'success','mode':mode,'errors':errors})
    return save_snapshot(view_rank(x,reg),mode,ts)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--mode',choices=['daily','weekly','seed','rebuild'],required=True);ap.add_argument('--gate-only',action='store_true')
    a=ap.parse_args()
    try:
        if a.mode in ['seed','rebuild']:
            x=seed()
            if a.mode=='rebuild':x=save_snapshot(view_rank(x,load(REGISTRY)),'membership_rebuild')
            print(json.dumps({'members':x['universe_size'],'action':x['metadata']['action_count'],'candidate':x['metadata']['candidate_count']}))
        elif a.gate_only:
            g=market_gate(datetime.now(timezone.utc),a.mode)
            last=load(DATA/'latest.json') if (DATA/'latest.json').exists() else None
            done=(last or {}).get('metadata',{}).get('last_daily_refresh_at' if a.mode=='daily' else 'last_weekly_refresh_at')
            if done and pd.Timestamp(done).tz_convert('America/New_York').date().isoformat()==g['date']:
                g.update({'run':False,'notify':False,'reason':'already_refreshed_today'})
            if os.getenv('GITHUB_OUTPUT'):
                with open(os.environ['GITHUB_OUTPUT'],'a') as h:h.write('run='+str(g['run']).lower()+'\nnotify='+str(g['notify']).lower()+'\n')
            print(json.dumps(g))
        else:
            x=refresh(a.mode);print(json.dumps({'skipped':x.get('skipped',False),'mode':a.mode,'members':x.get('universe_size')}))
    except Exception as exc:
        print(type(exc).__name__+': '+str(exc),file=sys.stderr);sys.exit(1)
