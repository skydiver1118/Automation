"""Evidence status for displayed scores; a calculator result is never a research sign-off.

The original numerical calculator remains frozen. This module separates an audited
input set from its later price/estimate overlays and invalidates sign-off on new gaps.
"""
from __future__ import annotations
import copy
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from critical_data_policy import apply as apply_score_policy

APP = Path(__file__).resolve().parent
CORE_DEPENDENCIES = ('revenue_ttm','gross_profit_ttm','operating_income_ttm',
 'cfo_ttm','capex_ttm','fcf_ttm','cash','debt','da_ttm','current_growth',
 'dilution_yoy','analyst_grades','financial_period_end')


def dependencies(result: dict) -> str:
    payload={k:result.get(k) for k in CORE_DEPENDENCIES}
    return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()


def evidence_status(stock: dict, reasons: list[str] | None = None) -> dict:
    """Update a current snapshot only. Never alter the dated source audit or old runs."""
    m=stock.setdefault('metadata',{});r=m.setdefault('research',{})
    a=m.get('audit')
    if not a:
        r['full_research_validation_complete']=False
        if r.get('research_mb_score') is not None:
            stock['data_confidence']='unreviewed';r['confidence']='unreviewed'
        return stock
    a=copy.deepcopy(a);m['audit']=a
    reasons=list(dict.fromkeys(reasons or []))
    live_reasons=list(reasons)
    if m.get('refresh_status')=='stale_refresh_failed':
        live_reasons.append('Latest market refresh failed; retained values keep their original dates.')
    if a.get('input_dependency_sha256') and dependencies(r)!=a['input_dependency_sha256']:
        live_reasons.append('An audited financial/analyst dependency changed; new evidence review is required.')
    if r.get('mb_input_weight_coverage',0)<1:
        reasons.append('Some MB input weight is missing; a fully populated headline is not available.')
    if a.get('baseline_status',a.get('status'))!='reviewed_within_scope':
        reasons.append('Original source audit has unresolved checklist or comparability gaps.')
    dynamic=[]
    for reason in dict.fromkeys(live_reasons):
        dynamic.append({'code':'live_review_required','severity':'warning','message':reason,'field':None})
    a['warnings']=[v for v in a.get('warnings',[]) if v.get('code')!='live_review_required']+dynamic
    blocking=bool(reasons or live_reasons) or any(v.get('severity')=='critical' for v in a['warnings'])
    a['baseline_status']=a.get('baseline_status',a.get('status'))
    a['status']='provisional_with_explicit_gaps' if blocking else 'reviewed_within_scope'
    a['input_audited_mb_score']=None if blocking else r.get('research_mb_score')
    a['verified_mb_score']=None
    a.setdefault('research_assurance',{})['full_six_pass_complete']=False
    a['score_values_as_of']=r.get('price_date')
    r['full_research_validation_complete']=False
    confidence='lower' if any(w.get('severity')=='critical' for w in a['warnings']) else 'medium'
    r['confidence']=confidence;stock['data_confidence']=confidence
    m['research_review_required']=True # Full research cannot be signed off by a market-data update.
    if dynamic:
        # Preserve original audit checkpoints and expose a distinct live invalidation.
        for key in ['pass_1_primary_source_inventory','pass_3_forward_expectations','pass_6_adversarial_audit']:
            p=stock.get('passes',{}).get(key)
            if not p:continue
            p.setdefault('metadata',{}).setdefault('original_audit_status',p['status'])
            p['metadata']['live_warning']=True
            p['status']='partial'
            p['missing_fields']=list(dict.fromkeys(p.get('missing_fields',[])+[v['message'] for v in dynamic]))
    a['completed_passes']=sum(p.get('status')=='complete' for p in stock.get('passes',{}).values())
    return apply_score_policy(stock)


def audit_summary(snapshot: dict) -> dict:
    rows=snapshot.get('stocks',[])
    return {'stock_count':len(rows),
      'scorecards_with_audit':sum(bool(s.get('metadata',{}).get('audit')) for s in rows),
      'eight_factor_scorecards':sum(len(s.get('metadata',{}).get('research',{}).get('factor_scores',{}))==8 for s in rows),
      'full_numeric_input_coverage':sum(s.get('metadata',{}).get('research',{}).get('mb_input_weight_coverage')==1 for s in rows),
      'reviewed_within_scope':sum(s.get('metadata',{}).get('audit',{}).get('input_audited_mb_score') is not None for s in rows),
      'input_audited':sum(s.get('metadata',{}).get('audit',{}).get('input_audited_mb_score') is not None for s in rows),
      'full_research_verified':sum(s.get('metadata',{}).get('audit',{}).get('verified_mb_score') is not None for s in rows),
      'provisional':sum(s.get('metadata',{}).get('audit',{}).get('input_audited_mb_score') is None for s in rows),
      'critical_hold':sum(any(w.get('severity')=='critical' for w in s.get('metadata',{}).get('audit',{}).get('warnings',[])) for s in rows),
      'scoreable':sum(s.get('metadata',{}).get('score_eligibility',{}).get('scoreable') is True for s in rows),
      'critical_data_unscored':sum(s.get('metadata',{}).get('score_eligibility',{}).get('status')=='missing_critical_data' for s in rows),
      'full_six_pass_complete':all(s.get('metadata',{}).get('research',{}).get('full_research_validation_complete') is True for s in rows)}


def verify_audit(stock: dict, root: Path = APP) -> None:
    """Validate source lineage, score arithmetic, and the positive claim of sign-off."""
    m=stock['metadata'];a=m.get('audit')
    if not a:return
    rel=m.get('audit_file','').removeprefix('./')
    p=(root/rel).resolve()
    if not p.is_relative_to((root/'evidence_audit').resolve()):raise ValueError('Audit path outside evidence directory')
    doc=json.loads(p.read_text())
    if doc['ticker']!=stock['ticker']:raise ValueError('Audit issuer mismatch')
    if len(doc['factors'])!=8 or len(doc['passes'])!=6:raise ValueError('Incomplete scorecard structure')
    if len(doc['financial_history']['rows'])!=8:raise ValueError('Expected eight dated financial-history rows')
    ids={s['id'] for s in doc['sources']}
    for factor in doc['factors']:
        if set(factor['source_ids'])-ids:raise ValueError('Factor source ID is unresolved')
    # The dated audit equals its own research snapshot, not every later market-overlay score.
    contributions=sum(v['weighted_contribution'] or 0 for v in doc['factors'])
    if abs(contributions-doc['screening_mb_score'])>1e-8:raise ValueError('Audit factor contributions do not sum')
    if a.get('verified_mb_score') is not None or m['research'].get('full_research_validation_complete'):
        raise ValueError('Full research verification is not supported by this bounded input-audit version')
    q=m.get('score_eligibility',{})
    if q.get('status')=='missing_critical_data':
        if m['research'].get('research_mb_score') is not None or m['research'].get('research_ev_score') is not None:
            raise ValueError('Critical-data stock must have current headline investment scores withheld')
    if a.get('input_audited_mb_score') is not None:
        r=m['research']
        if r.get('mb_input_weight_coverage')!=1 or any(p['status']!='complete' for p in stock['passes'].values()):
            raise ValueError('Unsupported fully reviewed headline score')
        if any(w['severity']=='critical' for w in a['warnings']):raise ValueError('Critical warning cannot coexist with sign-off')
        if abs(a['input_audited_mb_score']-r['research_mb_score'])>1e-8:raise ValueError('Current audited score mismatch')
