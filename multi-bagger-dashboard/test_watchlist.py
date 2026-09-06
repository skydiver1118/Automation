"""Membership, calendar, provenance and no-auto-swap regression tests."""
import copy
import hashlib
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch
import pandas as pd
from watchlist import load, validate, members, intake, approved_swap, public_registry, REGISTRY, APP
from watchlist_runtime import market_gate, seed, DATA, BASE, view_rank, weekly_comparison, save_snapshot
from build_site import verify

class WatchlistTests(unittest.TestCase):
    def setUp(self):
        self.live=load(REGISTRY);self.current=load(DATA/'latest.json')
        first=sorted((DATA/'runs').glob('*membership_migration.json'))[0]
        self.initial=load(first);self.initial_reg=self.initial['metadata']['registry']
        self.r=copy.deepcopy(self.initial_reg);self.s=copy.deepcopy(self.initial)
    def test_action_10_and_candidates_20(self):
        self.assertEqual(len(members(self.initial_reg,'action')),10)
        self.assertEqual(len(members(self.initial_reg,'candidate')),20)
        self.assertEqual(len(set(members(self.initial_reg))),30)
    def test_exact_initial_action_members(self):
        self.assertEqual(members(self.initial_reg,'action'),['ETN','ZETA','HUBB','VST','FIGR','CRMD','AXTI','KTOS','EVLV','RKLB'])
    def test_all_original_members_retained(self):
        old=load(APP/'research/2026-09-06/final25_registry.json')
        self.assertTrue(set(old['members'])<=set(members(self.r)))
    def test_photo_back_pocket_and_no_photo_biotech(self):
        self.assertTrue({'RGTI','QBTS','OKLO','SMR','EOSE'}<=set(members(self.r,'candidate')))
        self.assertFalse({'INO','CAPR','GOSS','SLS'}&set(members(self.r)))
    def test_intake_candidate_only_no_score(self):
        r=intake(self.r,'TEST','Testing future intake','2026-09-06T18:00:00+00:00')
        self.assertEqual(len(members(r,'action')),10);self.assertIn('TEST',members(r,'candidate'))
        x=view_rank(self.s,r);s=next(v for v in x['stocks'] if v['ticker']=='TEST')
        self.assertIsNone(s['multi_bagger_score']);self.assertFalse(s['metadata']['research'])
    def test_duplicates_rejected(self):
        with self.assertRaises(ValueError):intake(self.r,'ETN','Already exists')
    def test_no_11th_action(self):
        r=copy.deepcopy(self.r);next(v for v in r['stocks'] if v['tier']=='candidate')['tier']='action'
        with self.assertRaises(ValueError):validate(r)
    def test_unapproved_swap_rejected(self):
        with self.assertRaises(ValueError):approved_swap(self.r,'RGTI','ETN','','No approval')
    def test_approved_swap_keeps_count(self):
        r=approved_swap(self.r,'RGTI','ETN','test-only','Unit test; not persisted')
        self.assertEqual(len(members(r,'action')),10);self.assertIn('ETN',members(r,'candidate'))
    def test_scores_never_change_membership(self):
        x=copy.deepcopy(self.s);next(v for v in x['stocks'] if v['ticker']=='RGTI')['metadata']['research']['research_mb_score']=99
        y=view_rank(x,self.r);self.assertEqual(next(v for v in y['stocks'] if v['ticker']=='RGTI')['metadata']['tier'],'candidate')
    def test_holiday_and_sunday_skip_silent(self):
        for at in ['2026-09-06T12:00:00+00:00','2026-09-07T12:00:00+00:00']:
            g=market_gate(datetime.fromisoformat(at),'daily');self.assertFalse(g['run']);self.assertFalse(g['notify'])
    def test_trading_day_uses_prior_complete_close(self):
        g=market_gate(datetime.fromisoformat('2026-09-08T12:00:00+00:00'),'daily')
        self.assertTrue(g['run']);self.assertEqual(g['market_session_date'],'2026-09-04')
    def test_early_close_day_runs(self):
        g=market_gate(datetime.fromisoformat('2026-11-27T13:00:00+00:00'),'daily')
        self.assertTrue(g['run']);self.assertTrue(g['early_close']);self.assertEqual(g['market_session_date'],'2026-11-25')
    def test_weekly_holiday_uses_last_complete_session_and_no_email(self):
        g=market_gate(datetime.fromisoformat('2026-07-04T13:00:00+00:00'),'weekly')
        self.assertTrue(g['run']);self.assertFalse(g['notify']);self.assertEqual(g['market_session_date'],'2026-07-02')
    def test_dst_handles_eastern_date(self):
        g=market_gate(datetime.fromisoformat('2026-01-06T13:00:00+00:00'),'daily')
        self.assertTrue(g['run']);self.assertEqual(g['date'],'2026-01-06')
    def test_unexpected_closure_override(self):
        with patch('watchlist_runtime.load',return_value={'full_day_closures':{'2026-09-08':'test closure'}}):
            g=market_gate(datetime.fromisoformat('2026-09-08T12:00:00+00:00'),'daily')
        self.assertFalse(g['run']);self.assertFalse(g['notify'])
    def test_calendar_failure_fails_closed(self):
        with patch('watchlist_runtime.xcals.get_calendar',side_effect=RuntimeError('calendar unavailable')):
            with self.assertRaises(RuntimeError):market_gate(datetime.fromisoformat('2026-09-08T12:00:00+00:00'),'daily')
    def test_weekly_math_not_full_research(self):
        r=weekly_comparison(self.initial,self.initial_reg,None,'2026-09-04')
        self.assertEqual(len(r['proposals']),20)
        self.assertFalse(any(p['status']=='recommendation_pending_approval' for p in r['proposals']))
        self.assertFalse(r['automatic_swaps'])
    def test_stale_candidate_cannot_qualify(self):
        s=copy.deepcopy(self.s);c=next(v for v in s['stocks'] if v['ticker']=='RGTI');c['metadata']['research']['research_mb_score']=99
        r=weekly_comparison(s,self.r,None,'2026-09-11')
        p=next(v for v in r['proposals'] if v['candidate']=='RGTI');self.assertIn('Price dates not aligned',p['blockers'])
    def test_snapshot_immutable_and_latest_reconciles(self):
        with tempfile.TemporaryDirectory() as d,patch('watchlist_runtime.DATA',Path(tempfile.mkdtemp())):
            ts='2026-09-06T18:00:00+00:00';save_snapshot(self.s,'test',ts)
            changed=copy.deepcopy(self.s);changed['universe_size']=999
            with self.assertRaises(ValueError):save_snapshot(changed,'test',ts)
    def test_current_data_and_source_reconciliation(self):
        x,r,_=verify();self.assertEqual(r['members'],len(members(self.live)));self.assertEqual(r['research_values_reconciled'],sum(bool(s['metadata'].get('research',{}).get('analyst_grades')) for s in x['stocks']))
        for s in x['stocks']:
            self.assertIn('research_reviewed_at',s['metadata'])
            if s['metadata'].get('research',{}).get('price_date'):self.assertLessEqual(s['metadata']['research']['price_date'],x['run_date'])
    def test_old_snapshots_intact(self):
        expected={'2026-09-03.json':'70e71eb9fa15b42860d9f692816bce1416558a17d4ffd9c6f65c4a5ad0929751',
          '2026-09-04.json':'1bf8bb14f56fd87eb10ea9afa59c131b474a10dac5725947b323775a4ad1a947'}
        for f,h in expected.items():self.assertEqual(hashlib.sha256((BASE/'pass_scores'/f).read_bytes()).hexdigest(),h)
    def test_single_registry_no_competing_final_list(self):
        self.assertFalse((APP/'final_list.json').exists());self.assertEqual(public_registry(self.r)['members'],members(self.r))

if __name__=='__main__':unittest.main()
