#!/usr/bin/env python3
"""Read-only production adapter plus separate immutable v2.2 shadow artifacts.

Never changes monitoring scores, membership, histories or the frozen v1 engine.
No network calls and no automatic estimates of long-term scenario assumptions.
"""
from __future__ import annotations
import argparse
import copy
import csv
import hashlib
import itertools
import json
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse
from critical_data_policy import assess
from feasibility_v22 import METHODOLOGY, VERSION, _finite, reverse_requirements, scenario_set

SCENARIOS = ('bear', 'base', 'bull')
PE_FIELDS = ('revenue_cagr', 'net_margin', 'terminal_pe', 'dilution_5y')
EV_FIELDS = ('revenue_cagr', 'ebitda_margin', 'terminal_ev_ebitda', 'dilution_5y',
             'net_debt_5y', 'preferred_claims_5y', 'minority_claims_5y', 'other_claims_5y')

def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False,
                       allow_nan=False)+'\n').encode('utf-8')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def financial_basis(stock):
    m = stock.get('metadata', {}); r = m.get('research', {})
    return sha(canonical({k: r.get(k) for k in ('revenue_ttm', 'financial_period_end',
        'cash', 'debt', 'ev_bridge_residual', 'dilution_basis')} |
        {'research_reviewed_at': m.get('research_reviewed_at')}))

def text(value):
    return isinstance(value, str) and bool(value.strip())

def _definition_errors(definition, stock, as_of):
    errors = []
    if not isinstance(definition, dict) or not definition:
        return ['Reviewed bear/base/bull growth, margins, terminal multiples, dilution and funding assumptions are missing.']
    if definition.get('review_status') != 'reviewed':
        errors.append('Scenario inputs have not been reviewed; draft assumptions cannot be scored.')
    for field in ('reviewed_at', 'valid_through', 'model_rationale', 'funding_assessment'):
        if not text(definition.get(field)):
            errors.append('Missing scenario evidence: '+field)
    try:
        reviewed = datetime.fromisoformat(definition['reviewed_at'].replace('Z', '+00:00'))
        if reviewed.tzinfo is None or reviewed.date() > as_of:
            errors.append('Invalid/future scenario review date.')
        if date.fromisoformat(definition['valid_through']) < as_of:
            errors.append('Scenario review expired; refresh the assumptions.')
    except (KeyError, TypeError, ValueError):
        errors.append('Valid review and expiration dates are required.')
    if definition.get('financial_basis_sha256') != financial_basis(stock):
        errors.append('Scenario financial dependency changed or was not bound to the reviewed inputs.')
    model = definition.get('model')
    if model not in ('equity_pe', 'enterprise_ebitda'):
        errors.append('Unsupported sector model; a documented operating-company model cannot substitute for project or finance valuation.')
    sources = definition.get('sources') or {}
    if not isinstance(sources, dict):
        return errors + ['Scenario sources must be a source-ID mapping.']
    if not isinstance(definition.get('scenarios'), dict):
        return errors + ['Bear/base/bull scenario records are missing.']
    for sid, src in sources.items():
        if not isinstance(src, dict) or urlparse(str(src.get('url', ''))).scheme != 'https' or not text(src.get('as_of')):
            errors.append('Scenario source lacks HTTPS locator/as-of date: '+str(sid))
        else:
            try:
                sourced = date.fromisoformat(src['as_of'])
                if sourced > as_of: errors.append('Scenario source date is in the future: '+str(sid))
            except (ValueError, TypeError):
                errors.append('Scenario source has an invalid as-of date: '+str(sid))
    for name in SCENARIOS:
        case = definition.get('scenarios', {}).get(name, {})
        if not isinstance(case, dict):
            errors.append(name+': invalid scenario record'); continue
        inputs = case.get('inputs', {})
        evidence = case.get('assumption_evidence', {})
        if not isinstance(inputs, dict) or not isinstance(evidence, dict):
            errors.append(name+': invalid input/evidence mapping'); continue
        for field in PE_FIELDS if model == 'equity_pe' else EV_FIELDS:
            if not _finite(inputs.get(field)):
                errors.append(f'{name}: required assumption missing/invalid: {field}')
            rationale = evidence.get(field, {})
            if not isinstance(rationale, dict):
                errors.append(name+': invalid assumption rationale: '+field); continue
            refs = rationale.get('source_ids') or []
            if not text(rationale.get('rationale')) or not isinstance(refs, list) or not refs or any(not isinstance(ref, str) or ref not in sources for ref in refs):
                errors.append(f'{name}: sourced rationale missing for {field}')
        if not text(case.get('label')):
            errors.append(name+': scenario interpretation missing')
    return errors

def build_payload(snapshot, definitions, calibration, *, source_bytes=None, as_of=None):
    """All current members get a row; missing evidence NEVER becomes a score."""
    source_bytes = source_bytes if source_bytes is not None else canonical(snapshot)
    as_of = as_of or datetime.now(timezone.utc).date()
    if definitions.get('methodology') != METHODOLOGY or definitions.get('status') != 'shadow_only':
        raise ValueError('Unexpected scenario registry methodology/status')
    if calibration.get('status') != 'blocked_not_calibrated' or calibration.get('production_adoption_allowed') is not False:
        raise ValueError('A config flag cannot authorize production adoption; use a reviewed calibration release')
    seen = set(); rows = []
    for stock in snapshot['stocks']:
        ticker = stock['ticker']
        if ticker in seen:
            raise ValueError('Duplicate ticker: '+ticker)
        seen.add(ticker)
        m = stock.get('metadata', {}); r = m.get('research', {}); q = assess(stock)
        cap = r.get('market_cap')
        if not _finite(cap) or cap <= 0:
            cap = None
        revenue = r.get('revenue_ttm')
        if not _finite(revenue) or revenue <= 0:
            revenue = None
        definition = definitions.get('records', {}).get(ticker)
        reasons = list(q['critical_reasons'])
        if cap is None:
            reasons.append('Current economic market capitalization is missing.')
        if revenue is None:
            reasons.append('Positive, comparable trailing revenue is missing for this operating-company scenario.')
        if not r.get('price_date'):
            reasons.append('Market-data date is missing.')
        else:
            try:
                age = (as_of - date.fromisoformat(r['price_date'])).days
                if age < 0 or age > 4:
                    reasons.append('Quote date is outside the permitted four-calendar-day freshness window; a new scenario score is withheld.')
            except (ValueError, TypeError):
                reasons.append('Quote date cannot be verified.')
        if m.get('refresh_status') == 'stale_refresh_failed':
            reasons.append('Latest market refresh failed; old prices cannot establish a current scenario score.')
        reasons.extend(m.get('review_queue') or [])
        reasons.extend(_definition_errors(definition, stock, as_of))
        warnings = [w.get('message', '') for w in m.get('audit', {}).get('warnings', []) if w.get('message')]
        if m.get('research_review_required'):
            warnings.append('Broader research remains incomplete; neither numerical coverage nor a scenario calculation certifies six passes.')
        # Estimates and technical data keep their original timestamps; no freshness manufactured.
        out = {'ticker': ticker, 'tier': m.get('tier', 'candidate'), 'list_rank': m.get('tier_rank'),
            'price': r.get('price'), 'price_date': r.get('price_date'),
            'reference_market_cap': cap, 'market_cap_basis': r.get('market_cap_basis', 'Saved market-vendor reference; see source audit'),
            'market_source': r.get('market_source'), 'primary_source': r.get('primary_source'),
            'financial_period_end': r.get('financial_period_end'), 'financial_reviewed_at': m.get('research_reviewed_at'),
            'revenue_ttm': revenue, 'financial_basis_sha256': financial_basis(stock),
            'mb_quality_score_v1': r.get('research_mb_score') if q['scoreable'] else None,
            'quality_score_status': q['status'], 'technical_score': r.get('technical_score'),
            'required_5x_market_cap_no_dilution': cap*5 if cap else None,
            'incremental_equity_required_no_dilution': cap*4 if cap else None,
            'required_5x_market_cap_dilution_adjusted': None,
            'supportable_terminal_equity_value_base': None, 'supportable_5y_multiple_base': None,
            'feasibility_gap_base': None, 'shadow_feasibility_score': None,
            'v22_final_score': None, 'probability_5x': None, 'v22_rank': None,
            'status': 'missing_critical_data', 'critical_reasons': [],
            'warnings': list(dict.fromkeys(warnings)), 'scenarios': None,
            'scenario_assumptions': copy.deepcopy(definition), 'reverse_sensitivities': [],
            'production_rank_effect': False, 'full_research_certified': False}
        if not reasons:
            try:
                result = scenario_set(market_cap=cap, revenue_ttm=revenue,
                    model=definition['model'], **{n: definition['scenarios'][n]['inputs'] for n in SCENARIOS})
                base = result['scenarios']['base']
                out.update(status='shadow_uncalibrated', scenarios=result['scenarios'],
                    shadow_feasibility_score=result['shadow_score'],
                    required_5x_market_cap_dilution_adjusted=base['required_5x_market_cap_dilution_adjusted'],
                    supportable_terminal_equity_value_base=base['terminal_equity_value_5y'],
                    supportable_5y_multiple_base=base['supportable_5y_multiple'], feasibility_gap_base=base['feasibility_gap'])
            except (ValueError, TypeError, OverflowError) as exc:
                reasons.append('Invalid/inconsistent scenario: '+str(exc))
        out['critical_reasons'] = list(dict.fromkeys(reasons))
        # Reverse hurdles are conditional arithmetic, not an analyst forecast or score.
        if cap is not None:
            for dilution, margin, pe in itertools.product((0., .2, .5), (.1, .2, .3), (15., 20., 30.)):
                out['reverse_sensitivities'].append(reverse_requirements(market_cap=cap, revenue_ttm=revenue,
                    dilution_5y=dilution, net_margin=margin, terminal_pe=pe))
        rows.append(out)
    definition_hash = sha(canonical(definitions)); source_hash = sha(source_bytes)
    engine_hash = sha(Path(__file__).with_name('feasibility_v22.py').read_bytes())
    code_hash = sha(Path(__file__).read_bytes())
    run_id = sha(canonical([source_hash, definition_hash, sha(canonical(calibration)), engine_hash, code_hash, str(as_of)]))[:24]
    return {'schema_version': VERSION, 'methodology': METHODOLOGY, 'mode': 'shadow_only',
        'run_id': run_id, 'evaluation_date_utc': str(as_of),
        'source_snapshot_id': snapshot.get('metadata', {}).get('monitoring_id'),
        'source_snapshot_sha256': source_hash, 'source_recorded_at': snapshot.get('recorded_at'),
        'source_market_session_date': snapshot.get('market_session_date'),
        'assumptions_sha256': definition_hash, 'engine_sha256': engine_hash, 'adapter_sha256': code_hash,
        'production_methodology': snapshot.get('methodology_version'),
        'production_rank_effect': False, 'probability_5x': None, 'final_v22_score': None,
        'calibration': calibration, 'counts': {'members': len(rows),
            'action': sum(r['tier']=='action' for r in rows), 'candidate': sum(r['tier']=='candidate' for r in rows),
            'capitalization_hurdles': sum(r['reference_market_cap'] is not None for r in rows),
            'reviewed_scenario_sets': sum(r['status']=='shadow_uncalibrated' for r in rows),
            'missing_critical_scenario_data': sum(r['status']=='missing_critical_data' for r in rows)},
        'limitations': [
            'v1 quality score, scenario feasibility and technical timing are separate measures. No new blended score is invented.',
            'A 5x stock-price outcome requires 5x current equity value only with unchanged economic shares; dilution raises the hurdle.',
            'P/E values common equity after interest and tax; the enterprise route deducts net debt and non-common claims exactly once.',
            'Reverse sensitivities are hypothetical requirements, not company forecasts, probabilities, targets or certified valuations.',
            'Scenario math excludes dividends and is not the delisting-adjusted total-return measure required by the historical calibration gate.',
            'Forecast inputs require dated source-linked rationales and explicit funding/dilution assumptions. Missing is never zero.',
            'Each stock retains its true data date; daily Action data must not be mistaken for a newly reviewed Candidate record.'], 'stocks': rows}

def _atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix+'.tmp')
    tmp.write_bytes(data); tmp.replace(path)

def archive(app, snapshot=None):
    app = Path(app); raw = (app/'monitoring/latest.json').read_bytes()
    snapshot = json.loads(raw) if snapshot is None else snapshot
    if json.loads(raw) != snapshot:
        raise ValueError('Cannot archive v2.2 against an uncommitted/latest-mismatched snapshot')
    payload = build_payload(snapshot, json.loads((app/'v22/assumptions.json').read_text()),
        json.loads((app/'v22/calibration.json').read_text()), source_bytes=raw)
    root = app/'monitoring/v22'; path = root/'runs'/(payload['run_id']+'.json')
    if path.exists():
        if json.loads(path.read_text()) != payload:
            raise ValueError('Conflicting immutable v2.2 run')
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('xb') as handle:
            handle.write(canonical(payload))
    _atomic(root/'latest.json', canonical(payload))
    history = []
    for p in sorted((root/'runs').glob('*.json')):
        x = json.loads(p.read_text())
        history.append({k:x[k] for k in ('run_id','evaluation_date_utc','source_snapshot_id','source_market_session_date','counts')})
    _atomic(root/'history.json', canonical({'runs': sorted(history,key=lambda x:(x['evaluation_date_utc'],x['source_snapshot_id'] or '',x['run_id']))}))
    return payload

def export_site(app, dest, snapshot):
    """Persist the derived v2.2 history, then publish its isolated artifact directory."""
    import shutil
    app = Path(app); dest = Path(dest)
    data = archive(app, snapshot)
    output = dest/'v22'; output.mkdir(parents=True, exist_ok=True)
    for name in ('index.html', 'app.js', 'style.css', 'assumptions.json', 'calibration.json', 'README.md'):
        shutil.copy(app/'v22'/name, output/name)
    shutil.copytree(app/'monitoring/v22', output, dirs_exist_ok=True)
    shutil.copy(app/'feasibility_v22.py', output/'feasibility_v22.py')
    fields = ('ticker','tier','list_rank','price','price_date','reference_market_cap','mb_quality_score_v1',
        'required_5x_market_cap_no_dilution','required_5x_market_cap_dilution_adjusted',
        'supportable_terminal_equity_value_base','supportable_5y_multiple_base','feasibility_gap_base',
        'shadow_feasibility_score','v22_final_score','probability_5x','status','critical_reasons')
    with (output/'current.csv').open('w',newline='') as h:
        writer = csv.DictWriter(h, fieldnames=fields); writer.writeheader()
        for row in data['stocks']:
            record = {k:row.get(k) for k in fields}
            record['critical_reasons'] = '; '.join(row['critical_reasons'])
            writer.writerow(record)
    return {'version': VERSION, 'methodology': METHODOLOGY, 'mode': 'shadow_only',
            'artifact': './v22/latest.json', 'artifact_sha256': sha((output/'latest.json').read_bytes()),
            'source_snapshot_sha256': data['source_snapshot_sha256'], 'run_id': data['run_id'],
            'counts': data['counts'], 'production_rank_effect': False,
            'calibration_status': data['calibration']['status'],
            'last_refresh_attempt': json.loads((app/'monitoring/last_attempt.json').read_text()) if (app/'monitoring/last_attempt.json').exists() else None}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    print(json.dumps(archive(args.app)['counts'], indent=2))
