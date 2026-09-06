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
def verify():
    reg=load(APP/'final_list.json');latest=load(BASE/'pass_scores/latest.json')
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
    for token in ['<title>Multi Bagger Final 25 Dashboard</title>','<th>Ticker</th><th>Price</th><th>Market cap</th>','./data/pass_scores/latest.json','./data/history/snapshots.json']:
        if token not in html:raise ValueError('Required UI feature missing: '+token)
    script=re.findall(r'<script>(.*?)</script>',html,re.S)
    if len(script)!=1:raise ValueError('Expected one inline application script')
    receipt={'members':25,'additions':sorted(new),'removals':[],'history':hist,'research_values_reconciled':25,'unverified_official_scores_withheld':True,'market_session_date':latest['market_session_date'],'research_data_collected_at':latest['generated_at'],'watchlist_recorded_at':latest['recorded_at'],'snapshot_sha256':digest(BASE/'pass_scores/latest.json'),'legacy_snapshots_sha256':{p.name:digest(p) for p in (BASE/'pass_scores').glob('2026-09-0[34].json')},'scoring_code_sha256':digest(APP/'research_scoring.py'),'full_six_pass_complete':False}
    return latest,receipt,script[0]

def build(dest):
    dest=dest.resolve()
    if dest==ROOT or dest==APP or dest==PROJECT or dest in [BASE.resolve()]:raise ValueError('Refusing destructive staging directory')
    latest,receipt,script=verify()
    if dest.exists():shutil.rmtree(dest)
    dest.mkdir(parents=True)
    shutil.copy(APP/'index.html',dest/'index.html');shutil.copy(APP/'final_list.json',dest/'final_list.json')
    shutil.copytree(BASE,dest/'data')
    shutil.copytree(PROJECT/'reports/multi_bagger',dest/'reports')
    shutil.copytree(APP/'research/2026-09-06',dest/'research')
    shutil.copy(APP/'research_scoring.py',dest/'research/research_scoring.py')
    snaps=[]
    for p in sorted((BASE/'pass_scores').glob('*.json')):
        if p.name=='latest.json':continue
        x=load(p);snaps.append({'id':p.stem,'count':x['universe_size'],'methodology':x['methodology_version'],'market_session_date':x['market_session_date']})
    (dest/'data/history/snapshots.json').write_text(json.dumps({'snapshots':snaps},indent=2)+'\n')
    prices={'market_session_date':latest['market_session_date'],'generated_at':latest['generated_at'],'price_basis':latest['price_basis'],'coverage':{'requested':25,'available':25,'missing':[]},'prices':{s['ticker']:{'price_usd':s['metadata']['research']['price'],'as_of':s['metadata']['research']['price_date'],'currency':'USD','source':'September 6 research collection; Yahoo Finance daily closing price','status':'ok'} for s in latest['stocks']}}
    (dest/'data/prices').mkdir(exist_ok=True);(dest/'data/prices/latest.json').write_text(json.dumps(prices,indent=2)+'\n')
    built=datetime.now(timezone.utc).replace(microsecond=0).isoformat();receipt['built_at']=built
    (dest/'build.json').write_text(json.dumps(receipt,indent=2)+'\n');(dest/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n');(dest/'.nojekyll').touch()
    (dest/'app.syntax-check.js').write_text(script)
    return receipt

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=ROOT/'.multi-bagger-pages');args=ap.parse_args();print(json.dumps(build(args.output),indent=2))
