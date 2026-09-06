#!/usr/bin/env python3
"""Canonical membership. Intake is Candidate-only; research ranks never move members."""
from __future__ import annotations
import argparse
import copy
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

APP = Path(__file__).resolve().parent
REGISTRY = APP / 'watchlist_registry.json'
TIERS = {'action', 'candidate', 'archived'}

def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding='utf-8'))

def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def validate(reg: dict) -> None:
    if reg.get('schema_version') != '2.0':
        raise ValueError('Unsupported registry schema')
    if reg.get('action_limit') != 10 or reg.get('intake_default') != 'candidate':
        raise ValueError('Action cap 10 and Candidate-first intake are mandatory')
    if reg.get('automatic_swaps') is not False:
        raise ValueError('Automatic membership swaps are not authorized')
    seen = set()
    for row in reg['stocks']:
        t = row['ticker']
        if not re.fullmatch(r'[A-Z0-9.\-]{1,15}', t) or t in seen:
            raise ValueError(f'Invalid/duplicate ticker {t}')
        seen.add(t)
        if row['tier'] not in TIERS or not row.get('membership_since'):
            raise ValueError(f'Invalid membership for {t}')
        if not row.get('promotion_blocker') or not row.get('next_review_trigger'):
            raise ValueError(f'Candidate/review rationale missing: {t}')
    if sum(s['tier'] == 'action' for s in reg['stocks']) > reg['action_limit']:
        raise ValueError('Action list exceeds 10')

def members(reg: dict, tier: str | None = None) -> list[str]:
    validate(reg)
    return [s['ticker'] for s in reg['stocks'] if (s['tier'] == tier if tier else s['tier'] != 'archived')]

def intake(reg: dict, ticker: str, reason: str, timestamp: str | None = None) -> dict:
    """No tier argument: new symbols can never bypass Candidate intake."""
    out = copy.deepcopy(reg)
    validate(out)
    t = ticker.strip().upper()
    if any(s['ticker'] == t for s in out['stocks']):
        raise ValueError(f'{t} already exists; intake cannot promote or duplicate it')
    if not reason.strip():
        raise ValueError('Research rationale is required')
    ts = timestamp or now_iso()
    out['stocks'].append({'ticker': t, 'tier': 'candidate', 'membership_since': ts,
        'origin': 'candidate_intake', 'intake_reason': reason.strip(),
        'promotion_blocker': 'Unreviewed intake: complete sourced research and common-date comparison.',
        'next_review_trigger': 'Next weekly candidate review', 'priority': 'unreviewed',
        'model_scope': 'unreviewed', 'full_research_reviewed_at': None})
    out['events'].append({'at': ts, 'ticker': t, 'from': None, 'to': 'candidate', 'reason': reason.strip()})
    out['updated_at'] = ts
    validate(out)
    return out

def approved_swap(reg: dict, promote: str, demote: str, approval_ref: str, reason: str) -> dict:
    """A deliberate recorded approval is required. Schedulers never call this function."""
    if not approval_ref.strip() or not reason.strip():
        raise ValueError('Explicit approval reference and reason required')
    out = copy.deepcopy(reg); validate(out)
    rows = {s['ticker']: s for s in out['stocks']}
    if promote not in rows or demote not in rows:
        raise ValueError('Both symbols must exist; intake first')
    if rows[promote]['tier'] != 'candidate' or rows[demote]['tier'] != 'action':
        raise ValueError('Swap must be Candidate -> Action and Action -> Candidate')
    ts = now_iso()
    for t, frm, to in [(promote, 'candidate', 'action'), (demote, 'action', 'candidate')]:
        rows[t]['tier'] = to; rows[t]['membership_since'] = ts
        out['events'].append({'at': ts, 'ticker': t, 'from': frm, 'to': to,
            'reason': reason, 'approval_ref': approval_ref})
    out['updated_at'] = ts; validate(out)
    return out

def save(reg: dict, path: Path = REGISTRY) -> None:
    validate(reg)
    path.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def public_registry(reg: dict) -> dict:
    """Compatibility final_list.json is derived at publish time, never an input."""
    return {'schema_version':'2.0', 'name':'Multi Bagger Action 10 + Candidates',
        'source':'watchlist_registry.json', 'members':members(reg),
        'action':members(reg,'action'), 'candidates':members(reg,'candidate'),
        'intake_default':'candidate', 'automatic_swaps':False,
        'updated_at':reg['updated_at'], 'separate_from_stock_project_v2':True}

if __name__ == '__main__':
    ap=argparse.ArgumentParser(description=__doc__); sub=ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('validate')
    p=sub.add_parser('add'); p.add_argument('ticker'); p.add_argument('--reason',required=True)
    p=sub.add_parser('swap'); p.add_argument('--promote',required=True); p.add_argument('--demote',required=True)
    p.add_argument('--approval-ref',required=True); p.add_argument('--reason',required=True)
    a=ap.parse_args(); r=load(REGISTRY)
    if a.cmd=='add': save(intake(r,a.ticker,a.reason))
    elif a.cmd=='swap': save(approved_swap(r,a.promote.upper(),a.demote.upper(),a.approval_ref,a.reason))
    else: validate(r)
    if a.cmd in ['add','swap']:
        from watchlist_runtime import DATA, view_rank, save_snapshot
        if (DATA/'latest.json').exists():save_snapshot(view_rank(load(DATA/'latest.json'),load(REGISTRY)),'membership_change')
    print(json.dumps(public_registry(load(REGISTRY)), indent=2))
