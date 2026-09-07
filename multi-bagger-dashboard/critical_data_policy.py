"""Critical-data policy for headline Multi Bagger scoring.

A raw calculator can be useful for diagnostics, but a stock is not ranked or given a
headline MB/E&V score when a required score input or a material valuation/capital-
structure input is missing. Non-critical historical/context gaps remain visible without
silently converting them to zero.
"""
from __future__ import annotations
import copy
import math
import re

CRITICAL_WARNING_CODES={"material_unresolved","semiannual_not_quarterly"}
# These are score-driving capital-structure gaps that were previously only warnings.
CRITICAL_RESEARCH_PATTERNS=(
    r"preferred, derivative and subsequent financing claims",
)


def finite(v):
    return isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(float(v))


def _dedupe(values):
    return list(dict.fromkeys(v for v in values if v))


def assess(stock: dict) -> dict:
    """Return current investment-score eligibility without changing the stock."""
    m=stock.get('metadata',{});r=m.get('research',{});a=m.get('audit') or {}
    reasons=[];noncritical=[]
    if not a:
        reasons.append('No source-linked audit is attached to the current stock record.')
    coverage=r.get('mb_input_weight_coverage')
    if not finite(coverage) or coverage < 1-1e-12:
        missing=[]
        for name,value in (r.get('factor_coverage') or {}).items():
            if not finite(value) or value < 1-1e-12:missing.append(name)
        text='Required MB factor input is missing'
        if missing:text+=': '+', '.join(sorted(missing))
        reasons.append(text+'. Missing factor weight is not reweighted into a comparable headline score.')
    for w in a.get('warnings',[]):
        # A prior application of this policy is a presentation consequence, not an
        # independent underlying reason. Ignoring it allows recovery when data is fixed.
        if w.get('code')=='critical_data_missing':continue
        msg=str(w.get('message') or '')
        if w.get('severity')=='critical' or w.get('code') in CRITICAL_WARNING_CODES:
            reasons.append(msg or 'Critical source/reconciliation warning is unresolved.')
        elif w.get('code')=='research_gap' and any(re.search(p,msg,re.I) for p in CRITICAL_RESEARCH_PATTERNS):
            reasons.append(msg)
        elif w.get('severity') in ['warning','notice']:
            noncritical.append(msg)
    # Defensive validation: a factor score may exist even if its underlying coverage is partial.
    for name,value in (r.get('factor_scores') or {}).items():
        if value is None:reasons.append(f'Required MB factor score is unavailable: {name}.')
    reasons=_dedupe(reasons);noncritical=_dedupe(noncritical)
    return {
        'status':'missing_critical_data' if reasons else 'scoreable',
        'scoreable':not reasons,
        'headline_mb_score':r.get('research_mb_score') if not reasons else None,
        'headline_ev_score':r.get('research_ev_score') if not reasons else None,
        'critical_reasons':reasons,
        'noncritical_warnings':noncritical,
        'policy':'MB_CRITICAL_DATA_GATE_V1',
        'rule':'Required MB factor inputs and material capital-structure/model-perimeter data must be present; critical gaps are unscored, not reweighted.',
    }


def apply(stock: dict) -> dict:
    """Apply policy to a current snapshot. Preserve raw diagnostics but withhold headlines."""
    out=copy.deepcopy(stock);m=out.setdefault('metadata',{});r=m.setdefault('research',{})
    # A never-researched Candidate remains structurally empty. The eligibility state is
    # metadata; do not manufacture empty score fields merely to say it is unscored.
    if not m.get('audit') and not r:
        q=assess(out);m['score_eligibility']=q
        out['data_confidence']='unknown'
        out['action']='MISSING CRITICAL DATA — unscored; source-linked research required before ranking'
        m['promotion_blocker']='Missing critical data — unscored: '+'; '.join(q['critical_reasons'])
        return out
    a=m.setdefault('audit',{})
    # Restore a previously withheld diagnostic before reassessment after a new refresh.
    if r.get('research_mb_score') is None and finite(r.get('research_mb_score_diagnostic')):
        r['research_mb_score']=r['research_mb_score_diagnostic']
    if r.get('research_ev_score') is None and finite(r.get('research_ev_score_diagnostic')):
        r['research_ev_score']=r['research_ev_score_diagnostic']
    q=assess(out);m['score_eligibility']=q
    a['score_eligibility']=copy.deepcopy(q)
    a['score_status']=q['status']
    a['headline_mb_score']=q['headline_mb_score'];a['headline_ev_score']=q['headline_ev_score']
    a['warnings']=[w for w in a.get('warnings',[]) if w.get('code')!='critical_data_missing']
    if not q['scoreable']:
        if finite(r.get('research_mb_score')):r['research_mb_score_diagnostic']=r['research_mb_score']
        if finite(r.get('research_ev_score')):r['research_ev_score_diagnostic']=r['research_ev_score']
        r['research_mb_score']=None;r['research_ev_score']=None
        a['input_audited_mb_score']=None
        a['warnings'].append({'code':'critical_data_missing','severity':'critical','message':'Headline investment scores withheld: '+'; '.join(q['critical_reasons']),'field':'research_mb_score'})
        out['data_confidence']='missing_critical_data';r['confidence']='missing_critical_data'
        out['action']='MISSING CRITICAL DATA — unscored; resolve required evidence before ranking'
        m['promotion_blocker']='Missing critical data — unscored: '+'; '.join(q['critical_reasons'])
    else:
        # The score may still be provisional research; scoreable does not mean six-pass verified.
        if out.get('data_confidence')=='missing_critical_data':out['data_confidence']='medium'
        if r.get('confidence')=='missing_critical_data':r['confidence']='medium'
    return out


def headline_mb(stock: dict):
    q=stock.get('metadata',{}).get('score_eligibility') or assess(stock)
    return stock.get('metadata',{}).get('research',{}).get('research_mb_score') if q.get('scoreable') else None


def rank_key(stock: dict):
    score=headline_mb(stock)
    return (0,-float(score),stock.get('ticker','')) if finite(score) else (1,0,stock.get('ticker',''))
