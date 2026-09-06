#!/usr/bin/env python3
"""Validate and stage only the Multi Bagger website. Never run or modify Stock V2."""
from __future__ import annotations
import argparse, csv, hashlib, importlib.util, json, re, shutil
from datetime import datetime, timezone
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker
from research_scoring import compute_all

APP=Path(__file__).resolve().parent
ROOT=APP.parent
PROJECT=ROOT/'stock-project-v2'
BASE=PROJECT/'data/multi_bagger'

def load(p):return json.loads(p.read_text())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_legacy():
    reg=load(APP/'research/2026-09-06/final25_registry.json');latest=load(BASE/'pass_scores/latest.json')
    expected=set(reg['members']);got={s['ticker'] for s in latest['stocks']}
    if len(expected)!=25 or expected!=got or len(latest['stocks'])!=25:raise ValueError('Final-25 registry mismatch; never truncate to the former Top20')
    new=set(reg['additions']);prior=load(BASE/'pass_scores/2026-09-04.json')
    if new!={'KTOS','AVAV','HUBB','VST','ETN'} or got-new!={s['ticker'] for s in prior['stocks']}:raise ValueError('Membership change differs from user approval')
    schema=load(BASE/'schemas/pass_scores.schema.json');v=Draft202012Validator(schema,format_checker=FormatChecker())
    for p in (BASE/'pass_scores').glob('*.json'):v.validate(load(p))
    spec=importlib.util.spec_from_file_location('store',PROJECT/'scripts/store_multibagger_pass_scores.py');store=importlib.util.module_from_spec(spec);spec.loader.exec_module(store)
    hist=store.verify_repository(PROJECT)
    inputs=load(APP/'research/2026-09-06/inputs.json');calc={r['ticker']:r for r in compute_all(inputs)}
    if latest['metadata']['display_mode']!='common_calibration_research':raise ValueError('Unexpected display calibration')
    for s in latest['stocks']:
        r=s['metadata']['research'];c=calc[s['ticker']]
        if not s['metadata']['final_member']:raise ValueError('Member missing final-list flag')
        if r['price_date']!=latest['market_session_date']:raise ValueError('Price/session mismatch')
        if any(s[k] is not None for k in ['multi_bagger_score','expectation_valuation_score','probability_5x_pct']):raise ValueError('Unverified official scores/probabilities must not be fabricated')
        if any(s[k] is not None for k in ['rank_delta','multi_bagger_score_delta','expectation_valuation_score_delta','weekly_technical_score_delta']):raise ValueError('Do not manufacture cross-calibration deltas')
        for k in ['research_mb_score','research_ev_score','technical_score']:
            if r[k] is None and c[k] is None:continue
            if r[k] is None or c[k] is None or abs(r[k]-c[k])>1e-10:raise ValueError('Stored research values fail calculation reconciliation')
        if s['weekly_technical_score']!=round(c['technical_score']):raise ValueError('Rounded P5 agreement failed')
    html=(APP/'index.html').read_text()
    for token in ['<title>Multi Bagger Action 10 + Candidates Dashboard</title>','<th>Ticker</th><th>Price</th><th>Market cap</th>','./data/pass_scores/latest.json','./data/history/snapshots.json']:
        if token not in html:raise ValueError('Required UI feature missing: '+token)
    script=re.findall(r'<script>(.*?)</script>',html,re.S)
    if len(script)!=1:raise ValueError('Expected one inline application script')
    receipt={'members':25,'additions':sorted(new),'removals':[],'history':hist,'research_values_reconciled':25,'unverified_official_scores_withheld':True,'market_session_date':latest['market_session_date'],'research_data_collected_at':latest['generated_at'],'watchlist_recorded_at':latest['recorded_at'],'snapshot_sha256':digest(BASE/'pass_scores/latest.json'),'legacy_snapshots_sha256':{p.name:digest(p) for p in (BASE/'pass_scores').glob('2026-09-0[34].json')},'scoring_code_sha256':digest(APP/'research_scoring.py'),'full_six_pass_complete':False}
    return latest,receipt,script[0]

def verify():
    from watchlist import validate, members
    from watchlist_runtime import view_rank, snapshot_id
    legacy,receipt,script=verify_legacy()
    registry=load(APP/'watchlist_registry.json');validate(registry)
    latest=load(APP/'monitoring/latest.json')
    seen=[s['ticker'] for s in latest['stocks']]
    if len(seen)!=len(set(seen)) or set(seen)!=set(members(registry)):
        raise ValueError('Monitoring/registry mismatch. Intake must be Candidate-first and archived.')
    rows={s['ticker']:s for s in latest['stocks']}
    for member in registry['stocks']:
        if member['tier']=='archived':continue
        if rows[member['ticker']]['metadata']['tier']!=member['tier']:
            raise ValueError('Tier mismatch; no implicit rank-based promotions')
    immutable=APP/'monitoring/runs'/f'{snapshot_id(latest)}.json'
    if load(immutable)!=latest:raise ValueError('Latest monitoring pointer differs from immutable run')
    from research_scoring import calculate
    for s in latest['stocks']:
        m=s['metadata'];r=m.get('research',{})
        if s['multi_bagger_score'] is not None or s['probability_5x_pct'] is not None:
            raise ValueError('Research monitoring must not manufacture official scores')
        if r.get('analyst_grades'):
            import copy
            calculated=calculate(copy.deepcopy(r),{'technical':m['technical']},m['benchmarks'])
            for k in ['research_mb_score','research_ev_score','technical_score']:
                if r.get(k) is None and calculated[k] is None:continue
                if r.get(k) is None or calculated[k] is None or abs(r[k]-calculated[k])>1e-8:
                    raise ValueError(f'{s["ticker"]}: monitoring calculation mismatch {k}')
        if 'membership' not in m:raise ValueError('Membership provenance missing')
    receipt.update({'legacy_history':receipt.pop('history'),'members':len(seen),
        'action_count':len(members(registry,'action')),'candidate_count':len(members(registry,'candidate')),
        'candidate_first':True,'automatic_swaps':False,'monitoring_id':snapshot_id(latest),
        'registry_sha256':digest(APP/'watchlist_registry.json'),
        'monitoring_sha256':digest(APP/'monitoring/latest.json'),
        'snapshot_sha256':digest(APP/'monitoring/latest.json'),
        'monitoring_history_count':len(list((APP/'monitoring/runs').glob('*.json'))),
        'market_session_date':latest['market_session_date'],'refresh_kind':latest['metadata']['refresh_kind'],'watchlist_recorded_at':latest['recorded_at'],
        'additions':['RGTI','QBTS','OKLO','SMR','EOSE'],'action_members':members(registry,'action'),'candidate_members':members(registry,'candidate'),
        'research_values_reconciled':sum(bool(s['metadata'].get('research',{}).get('analyst_grades')) for s in latest['stocks'])})
    return latest,receipt,script


def build(dest):
    from watchlist import public_registry
    from watchlist_runtime import snapshot_id
    dest=dest.resolve()
    # Restrict stage cleanup to a dedicated, direct child of this repository.
    if dest.parent!=ROOT.resolve() or dest.name not in ['.multi-bagger-pages','.test-mb-pages']:
        raise ValueError('Only dedicated repository staging directories are allowed')
    latest,receipt,script=verify()
    if dest.exists():shutil.rmtree(dest)
    dest.mkdir(parents=True)
    shutil.copy(APP/'index.html',dest/'index.html')
    (dest/'final_list.json').write_text(json.dumps(public_registry(load(APP/'watchlist_registry.json')),indent=2)+'\n')
    shutil.copy(APP/'watchlist_registry.json',dest/'watchlist_registry.json')
    shutil.copytree(BASE,dest/'data')
    shutil.copytree(APP/'monitoring',dest/'monitoring')
    shutil.copytree(PROJECT/'reports/multi_bagger',dest/'reports')
    shutil.copytree(APP/'research/2026-09-06',dest/'research')
    shutil.copy(APP/'research_scoring.py',dest/'research/research_scoring.py')
    shutil.copy(APP/'research/candidate_seed_2026-09-06.json',dest/'research/candidate_seed_2026-09-06.json')
    snaps=[]
    for p in sorted((BASE/'pass_scores').glob('*.json')):
        if p.name=='latest.json':continue
        x=load(p);snaps.append({'id':p.stem,'count':x['universe_size'],'methodology':x['methodology_version'],
            'market_session_date':x['market_session_date'],'path':'./data/pass_scores/'+p.name})
    snaps+=load(APP/'monitoring/history.json')['snapshots']
    (dest/'data/history/snapshots.json').write_text(json.dumps({'snapshots':snaps},indent=2)+'\n')
    prices={'market_session_date':latest['market_session_date'],'price_basis':'Per-stock completed regular session; Action daily, Candidates weekly',
        'prices':{s['ticker']:{'price_usd':s['metadata'].get('research',{}).get('price'),
            'as_of':s['metadata'].get('research',{}).get('price_date'),'currency':'USD'} for s in latest['stocks']}}
    (dest/'data/prices').mkdir(exist_ok=True);(dest/'data/prices/latest.json').write_text(json.dumps(prices,indent=2)+'\n')
    columns=['snapshot','tier','list_rank','ticker','price','price_date','mb_research','ev_research','technical_research','market_refreshed_at','source_reviewed_at','promotion_blocker']
    def csv_rows(x):
        for s in x['stocks']:
            m=s['metadata'];r=m.get('research',{})
            yield dict(zip(columns,[snapshot_id(x),m['tier'],m['tier_rank'],s['ticker'],r.get('price'),r.get('price_date'),r.get('research_mb_score'),r.get('research_ev_score'),r.get('technical_score'),m.get('last_market_refresh_at'),m.get('research_reviewed_at'),m.get('promotion_blocker')]))
    with (dest/'monitoring/current_scores.csv').open('w',newline='') as h:
        w=csv.DictWriter(h,fieldnames=columns);w.writeheader();w.writerows(csv_rows(latest))
    with (dest/'monitoring/history_scores.csv').open('w',newline='') as h:
        w=csv.DictWriter(h,fieldnames=columns);w.writeheader()
        for p in sorted((APP/'monitoring/runs').glob('*.json')):w.writerows(csv_rows(load(p)))
    report=['# Multi Bagger Action 10 + Candidates','',f'Recorded: {latest["recorded_at"]}',
        'Research scores, not calibrated fivefold-return probabilities. Each row preserves its own market and source-review dates.','',
        '| Tier | Rank | Ticker | Price | Market date | MB research | E&V research | Technical |',
        '|---|---:|---|---:|---|---:|---:|---:|']
    for s in latest['stocks']:
        m=s['metadata'];r=m.get('research',{});fmt=lambda v:'—' if v is None else f'{v:.1f}'
        report.append(f'| {m["tier"]} | {m["tier_rank"]} | {s["ticker"]} | {r.get("price","—")} | {r.get("price_date","—")} | {fmt(r.get("research_mb_score"))} | {fmt(r.get("research_ev_score"))} | {fmt(r.get("technical_score"))} |')
    report+=['','## Policy','Candidate-first intake. Action limit 10. Weekly swaps require explicit approval. No automated orders.','',
       '## Limitations']+['- '+v for v in latest['record_limitations']]
    (dest/'monitoring/current_report.md').write_text('\n'.join(report)+'\n')
    built=datetime.now(timezone.utc).replace(microsecond=0).isoformat();receipt['built_at']=built
    for name in ['build.json','verification.json']:(dest/name).write_text(json.dumps(receipt,indent=2)+'\n')
    (dest/'.nojekyll').touch();(dest/'app.syntax-check.js').write_text(script)
    return receipt

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=ROOT/'.multi-bagger-pages');args=ap.parse_args();print(json.dumps(build(args.output),indent=2))
