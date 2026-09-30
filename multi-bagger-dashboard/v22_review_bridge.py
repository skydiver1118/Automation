"""Source-reviewed v2.2 input/event overlay; never changes the v1 record.

The review signature excludes price and includes financial inputs, economic shares
and exact outstanding filing triggers. A historical resolution cannot approve a
new filing or a changed share count. Overrides require explicit source rationales.
"""
from __future__ import annotations
import copy,hashlib,json,math

def _sha(x):
    return hashlib.sha256((json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False)+'\n').encode()).hexdigest()

def observed_state(stock, financial_hash):
    m=stock.get('metadata',{});r=m.get('research',{})
    return _sha({'financial_basis_sha256':financial_hash,'economic_shares':r.get('shares_outstanding'),
                 'review_queue':m.get('review_queue') or [],'event_filings':m.get('event_scan',{}).get('new_filings',[])})

def finite(x):
    return isinstance(x,(int,float)) and not isinstance(x,bool) and math.isfinite(x)

def resolve(stock, definition, financial_hash):
    """Return independent scenario inputs and queue gaps, preserving all legacy data."""
    m=stock.get('metadata',{});r=copy.deepcopy(m.get('research',{}))
    queue=list(m.get('review_queue') or [])
    rec=(definition or {}).get('review_resolution')
    if rec is None:
        return r,queue,[],None
    errors=[];sources=(definition or {}).get('sources',{})
    if not isinstance(rec,dict):return r,queue+['Invalid source-review resolution.'],[],None
    if rec.get('observed_state_sha256')!=observed_state(stock,financial_hash):
        return r,queue+['Reviewed financial/share/filing state changed; scenario resolution needs a new source review.'],[],None
    refs=rec.get('source_ids',[])
    if not rec.get('conclusion') or not isinstance(refs,list) or not refs or any(k not in sources for k in refs):
        errors.append('A reviewed filing trigger requires a conclusion and valid source references.')
    changes=rec.get('financial_overrides',{})
    allowed={'revenue_ttm','financial_period_end','cash','debt','economic_shares'}
    if not isinstance(changes,dict) or any(k not in allowed for k in changes):
        errors.append('Unsupported scenario financial override.');changes={}
    if changes:
        rr=rec.get('override_source_ids',[])
        if not rec.get('override_rationale') or not isinstance(rr,list) or not rr or any(k not in sources for k in rr):
            errors.append('Financial correction requires primary sources and a written reconciliation.')
        for k,v in changes.items():
            if k=='financial_period_end':
                from datetime import date
                try:date.fromisoformat(v)
                except (TypeError,ValueError):errors.append('Invalid corrected financial period.')
            elif not finite(v) or v<0 or (k in ('economic_shares','revenue_ttm') and v==0):
                errors.append('Invalid corrected financial input: '+k)
    if errors:return r,queue+errors,[],None
    r.update({k:v for k,v in changes.items() if k!='economic_shares'})
    if 'economic_shares' in changes:
        if not finite(r.get('price')) or r['price']<=0:
            return r,['A corrected capitalization requires a valid share price.'],[],None
        r['market_cap']=changes['economic_shares']*r['price']
        r['shares_outstanding']=changes['economic_shares']
        r['market_cap_basis']='Dated disclosed-event-adjusted economic shares × saved close; source reconciliation in v2.2 review. Not a real-time fully diluted certification.'
    notes=[]
    if changes:notes.append('v2.2 input correction only: '+rec['override_rationale']+' Legacy quality-score inputs are not silently rewritten.')
    if queue:notes.append('Captured filing/period triggers were reviewed specifically for these scenarios; this is not full six-pass certification. Future trigger changes block reuse.')
    return r,[],notes,copy.deepcopy(rec)

def validate_funding(definition):
    """Check cash identity if the analyst supplied an enterprise funding budget."""
    errors=[]
    if definition is None:return errors
    if not isinstance(definition,dict):return ['Invalid scenario definition for funding review.']
    cases=definition.get('scenarios',{})
    if not isinstance(cases,dict):return ['Invalid scenario records for funding review.']
    for name,case in cases.items():
        if not isinstance(case,dict):
            errors.append(str(name)+': invalid funding scenario.');continue
        b=case.get('funding_bridge')
        if b is None:continue
        fields=('starting_net_debt','capex_5y','cfo_5y','new_common_cash_5y','other_funding_uses_5y','terminal_net_debt')
        if not isinstance(b,dict) or not all(finite(b.get(k)) for k in fields):
            errors.append(name+': incomplete five-year funding bridge.');continue
        if any(b[k]<0 for k in ('capex_5y','new_common_cash_5y','other_funding_uses_5y')):
            errors.append(name+': funding sources/uses signs are invalid.')
        implied=b['starting_net_debt']+b['capex_5y']+b['other_funding_uses_5y']-b['cfo_5y']-b['new_common_cash_5y']
        supplied=case.get('inputs',{}).get('net_debt_5y')
        if not finite(supplied) or not math.isclose(implied,supplied,rel_tol=1e-10,abs_tol=.01) or not math.isclose(implied,b['terminal_net_debt'],rel_tol=1e-10,abs_tol=.01):
            errors.append(name+': terminal debt does not reconcile to the funding budget.')
    return errors
