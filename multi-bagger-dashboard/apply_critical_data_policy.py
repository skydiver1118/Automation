#!/usr/bin/env python3
"""Apply critical-data score eligibility to the current 30-stock dashboard.

Research-policy operation only: no market-data download, no notification, no broker call.
The latest completed market session remains unchanged. User explicitly authorized rerank.
"""
from __future__ import annotations
import copy,json
from datetime import datetime,timezone
from pathlib import Path
from critical_data_policy import apply,headline_mb,finite,rank_key
from watchlist import REGISTRY,load,save as save_registry,approved_swap,validate,members
from watchlist_runtime import DATA,view_rank,save_snapshot,market_gate,ET

APP=Path(__file__).resolve().parent
APPROVAL='Conversation 2026-09-07: If any missing data are critical and needed, label stock missing critical data and not score it. Refresh again and rerank.'


def main():
    latest=load(DATA/'latest.json');reg=load(REGISTRY);validate(reg)
    if len(latest['stocks'])!=30:raise ValueError('Expected current 30-stock universe')
    # This policy refresh must not pretend a new holiday price session occurred.
    now=datetime.now(timezone.utc)
    gate=market_gate(now,'daily')
    if gate['run']:
        raise ValueError('This migration is intended for the 2026-09-07 closed-session research refresh only')
    if gate['date']!='2026-09-07' or latest['market_session_date']!='2026-09-04':
        raise ValueError(f'Unexpected calendar/session state {gate} / {latest["market_session_date"]}')
    before={s['ticker']:copy.deepcopy(s) for s in latest['stocks']}
    latest['stocks']=[apply(s) for s in latest['stocks']]
    scored=[s for s in latest['stocks'] if finite(headline_mb(s))]
    scored.sort(key=lambda s:(-headline_mb(s),s['ticker']))
    top10=[s['ticker'] for s in scored[:10]]
    if len(top10)!=10:raise ValueError('Fewer than 10 scoreable stocks; Action10 cannot be populated')
    current=set(members(reg,'action'));target=set(top10)
    promote=sorted(target-current,key=top10.index);demote=sorted(current-target,key=lambda t:next((i for i,s in enumerate(scored) if s['ticker']==t),999))
    if len(promote)!=len(demote):raise ValueError('Action swap cardinality mismatch')
    for p,d in zip(promote,demote):
        reg=approved_swap(reg,p,d,APPROVAL,'Critical-data gating: only stocks with all score-critical inputs may enter the ranked Action10; rerank scoreable stocks by unchanged MB screening score.')
    reg['initial_selection_basis']='Action10 contains the 10 highest current MB screening scores among stocks that pass MB_CRITICAL_DATA_GATE_V1. Missing critical data is unscored, not reweighted.'
    reg['promotion_policy']['min_input_coverage']=1.0
    reg['promotion_policy']['requires_no_critical_score_data_gaps']=True
    rows={s['ticker']:s for s in latest['stocks']}
    for rec in reg['stocks']:
        if rec['tier']=='archived':continue
        s=rows[rec['ticker']];q=s['metadata']['score_eligibility']
        rec['score_eligibility']=q['status']
        if q['scoreable']:
            rec['promotion_blocker']=s['metadata'].get('promotion_blocker') or rec['promotion_blocker']
            if rec['tier']=='action' and rec['ticker']=='VST':
                rec['promotion_blocker']='No score-critical data gap. Eight historical display cells remain unavailable but all current MB factor inputs are populated; retain the visible noncritical warning.'
        else:
            rec['promotion_blocker']='Missing critical data — no MB/E&V headline score: '+'; '.join(q['critical_reasons'])
        rec['priority']='daily' if rec['tier']=='action' else 'weekly'
    reg['updated_at']=datetime.now(timezone.utc).replace(microsecond=0).isoformat();validate(reg);save_registry(reg)
    # Reattach changed registry, rank scored names only, then enforce no-score presentation.
    latest=view_rank(latest,reg)
    for s in latest['stocks']:
        q=s['metadata']['score_eligibility']
        if not q['scoreable']:
            s['metadata']['tier_rank']=None
    latest['metadata']['critical_data_policy']={
        'version':'MB_CRITICAL_DATA_GATE_V1','applied_at':reg['updated_at'],'market_refresh_performed':False,
        'market_gate':gate,'market_session_retained':'2026-09-04','scoreable_count':sum(s['metadata']['score_eligibility']['scoreable'] for s in latest['stocks']),
        'unscored_critical_count':sum(not s['metadata']['score_eligibility']['scoreable'] for s in latest['stocks']),
        'action_selection':'Top 10 MB scores among scoreable stocks only','approval_ref':APPROVAL}
    latest['metadata']['ranking_basis']='Scoreable names are ranked by unchanged MB screening score within tier. Stocks missing required critical data are unscored and have no rank.'
    latest['metadata']['audit_summary']['critical_data_unscored']=latest['metadata']['critical_data_policy']['unscored_critical_count']
    latest['metadata']['audit_summary']['scoreable']=latest['metadata']['critical_data_policy']['scoreable_count']
    latest.setdefault('changes',{}).setdefault('notes',[])
    latest['changes']['notes'] += [
        'September 7 is a full-day U.S. market holiday; no new price/technical session was created. September 4 close retained.',
        'New critical-data policy: missing required MB factor inputs or material score-driving capital/model-perimeter data results in no MB/E&V headline score and no rank.',
        'Noncritical history/source warnings remain visible but do not automatically erase a fully populated current MB screening score.',
        'Action10 reranked among scoreable names only; this is research attention, not a trade instruction.'
    ]
    latest['changes']['critical_data_unscored']=sorted(s['ticker'] for s in latest['stocks'] if not s['metadata']['score_eligibility']['scoreable'])
    latest['changes']['action_promotions']=promote;latest['changes']['action_demotions']=demote
    latest['record_limitations']=list(dict.fromkeys(latest.get('record_limitations',[])+[
        'A stock with missing critical score data is explicitly unscored. Diagnostic calculator outputs from prior immutable audits are not used for current ranking.',
        'Historical-cell gaps that do not remove a current required MB factor remain warnings; they are not converted to zero.',
        'Full six-pass research remains distinct from score eligibility and is not certified by this rerank.'
    ]))
    # No current rank/delta should imply a hidden score for critical-data stocks.
    for s in latest['stocks']:
        q=s['metadata']['score_eligibility'];r=s['metadata']['research']
        if not q['scoreable']:
            assert r['research_mb_score'] is None and r['research_ev_score'] is None and s['metadata']['tier_rank'] is None
        else:assert finite(r['research_mb_score'])
    out=save_snapshot(latest,'critical_data_rerank')
    summary={'market_refresh':False,'market_session':out['market_session_date'],'action':members(reg,'action'),
      'candidate':members(reg,'candidate'),'promoted':promote,'demoted':demote,
      'scoreable':[s['ticker'] for s in sorted(out['stocks'],key=rank_key) if s['metadata']['score_eligibility']['scoreable']],
      'unscored':[(s['ticker'],s['metadata']['score_eligibility']['critical_reasons']) for s in out['stocks'] if not s['metadata']['score_eligibility']['scoreable']]}
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
