"""Keep historical migration expectations separate from live-data invariants.

The September 7 policy migration deliberately retained the September 4 close.
That is a property of its immutable snapshot, NOT a constraint on future refreshes.
Live membership is approved separately; changing prices must not force swaps.
"""
import copy
import json
import math
import unittest
from datetime import datetime
from pathlib import Path
from critical_data_policy import assess, headline_mb, rank_key

APP = Path(__file__).resolve().parent
POLICY_FIXTURE = APP / 'monitoring/runs/2026-09-07T155915Z-critical_data_rerank.json'
EXPECTED_UNSCORED = {'FIGR','RKLB','GRRR','QBTS','SOUN','POET','OKLO','APLD','SMR','EOSE','RZLV','SERV'}
EXPECTED_ACTION = ['ETN','ZETA','HUBB','CRMD','VST','AXTI','KTOS','AVAV','EVLV','BKSY']

class CriticalDataPolicyTests(unittest.TestCase):
    """Unchanged policy promises tested against the dated policy snapshot."""
    def setUp(self):
        self.x = json.loads(POLICY_FIXTURE.read_text())
        self.rows = {s['ticker']:s for s in self.x['stocks']}

    def test_expected_critical_data_holds(self):
        got = {t for t,s in self.rows.items() if s['metadata']['score_eligibility']['status']=='missing_critical_data'}
        self.assertEqual(got, EXPECTED_UNSCORED)
        for t in got:
            r = self.rows[t]['metadata']['research']; q = self.rows[t]['metadata']['score_eligibility']
            self.assertFalse(q['scoreable']); self.assertTrue(q['critical_reasons'])
            self.assertIsNone(r['research_mb_score']); self.assertIsNone(r['research_ev_score'])
            self.assertIsNone(self.rows[t]['metadata']['tier_rank'])
            self.assertEqual(self.rows[t]['data_confidence'], 'missing_critical_data')

    def test_scoreable_warning_examples_remain_scored(self):
        for t in ['VST','IREN','NBIS','TSSI','RR']:
            self.assertTrue(self.rows[t]['metadata']['score_eligibility']['scoreable'], t)
            self.assertIsNotNone(self.rows[t]['metadata']['research']['research_mb_score'])
        self.assertIn('historical_cells_missing', [w['code'] for w in self.rows['VST']['metadata']['audit']['warnings']])
        self.assertIn('quarter_bridge_mismatch', [w['code'] for w in self.rows['IREN']['metadata']['audit']['warnings']])

    def test_capital_claim_gap_blocks_eose(self):
        q = self.rows['EOSE']['metadata']['score_eligibility']
        self.assertFalse(q['scoreable'])
        self.assertTrue(any('financing claims' in x.lower() for x in q['critical_reasons']))

    def test_action10_is_top10_scoreable_at_authorized_migration(self):
        action = sorted([s for s in self.x['stocks'] if s['metadata']['tier']=='action'], key=lambda s:s['metadata']['tier_rank'])
        self.assertEqual([s['ticker'] for s in action], EXPECTED_ACTION)
        self.assertTrue(all(s['metadata']['score_eligibility']['scoreable'] for s in action))
        scoreable = sorted([s for s in self.x['stocks'] if s['metadata']['score_eligibility']['scoreable']], key=rank_key)
        self.assertEqual([s['ticker'] for s in scoreable[:10]], EXPECTED_ACTION)

    def test_market_data_not_refreshed_on_labor_day_policy_run(self):
        p = self.x['metadata']['critical_data_policy']
        self.assertFalse(p['market_refresh_performed'])
        self.assertEqual(self.x['market_session_date'], '2026-09-04')
        self.assertEqual(p['market_gate']['date'], '2026-09-07')
        self.assertFalse(p['market_gate']['run'])

    def test_no_hidden_current_rank_for_unscored(self):
        for s in self.x['stocks']:
            if not s['metadata']['score_eligibility']['scoreable']:
                self.assertIsNone(s['metadata']['tier_rank'])

class CurrentCriticalDataInvariantTests(unittest.TestCase):
    """Date-independent safety checks still run on every refreshed latest snapshot."""
    def setUp(self):
        self.x = json.loads((APP / 'monitoring/latest.json').read_text())
        self.registry = json.loads((APP / 'watchlist_registry.json').read_text())

    def test_current_critical_inputs_still_withhold_scores_and_ranks(self):
        for s in self.x['stocks']:
            m = s['metadata']; r = m.get('research', {}); q = assess(s)
            self.assertEqual(q['scoreable'], m['score_eligibility']['scoreable'], s['ticker'])
            if not q['scoreable']:
                self.assertIsNone(r.get('research_mb_score'), s['ticker'])
                self.assertIsNone(r.get('research_ev_score'), s['ticker'])
                self.assertIsNone(m.get('tier_rank'), s['ticker'])
                self.assertTrue(q['critical_reasons'], s['ticker'])
            else:
                self.assertTrue(math.isfinite(headline_mb(s)), s['ticker'])
                self.assertGreaterEqual(r['mb_input_weight_coverage'], 1-1e-12)

    def test_current_tier_ranks_sorted_without_automatic_membership_changes(self):
        expected = {r['ticker']:r['tier'] for r in self.registry['stocks'] if r['tier'] in ['action','candidate']}
        self.assertEqual({s['ticker']:s['metadata']['tier'] for s in self.x['stocks']}, expected)
        for tier in ['action', 'candidate']:
            rows = [s for s in self.x['stocks'] if s['metadata']['tier']==tier]
            scored = [s for s in rows if headline_mb(s) is not None]
            self.assertEqual([s['ticker'] for s in scored], [s['ticker'] for s in sorted(scored,key=rank_key)])
            self.assertEqual([s['metadata']['tier_rank'] for s in scored], list(range(1,len(scored)+1)))
        self.assertFalse(self.registry['automatic_swaps'])
        self.assertFalse(self.x['metadata']['full_six_pass_complete'])

    def test_successful_current_measurements_use_the_run_session(self):
        target = self.x['market_session_date']
        for s in self.x['stocks']:
            m = s['metadata']
            if m.get('refresh_status')=='market_and_estimates_refreshed' and m.get('last_market_refresh_at')==self.x.get('generated_at'):
                self.assertEqual(m['research']['price_date'], target, s['ticker'])
                self.assertEqual(m['technical']['price_date'], target, s['ticker'])

    def test_calendar_advances_after_labor_day_and_preserves_holiday_guard(self):
        from watchlist_runtime import market_gate
        for timestamp, mode, target in [
            ('2026-09-08T08:00:00-04:00','daily','2026-09-04'),
            ('2026-09-09T08:00:00-04:00','daily','2026-09-08'),
            ('2026-09-10T08:00:00-04:00','daily','2026-09-09'),
            ('2026-09-11T08:00:00-04:00','daily','2026-09-10'),
            ('2026-09-11T18:00:00-04:00','daily','2026-09-11'),
            ('2026-09-12T09:00:00-04:00','weekly','2026-09-11'),
        ]:
            with self.subTest(timestamp=timestamp):
                gate = market_gate(datetime.fromisoformat(timestamp), mode)
                self.assertTrue(gate['run'])
                self.assertEqual(gate['market_session_date'], target)
        holiday = market_gate(datetime.fromisoformat('2026-09-07T08:00:00-04:00'), 'daily')
        self.assertFalse(holiday['run']); self.assertFalse(holiday['notify'])

    def test_future_measurement_does_not_rewrite_historical_policy(self):
        from watchlist_runtime import view_rank
        before = POLICY_FIXTURE.read_bytes()
        sample = copy.deepcopy(self.x)
        sample['market_session_date'] = '2026-09-11'
        for s in sample['stocks']:
            if s['metadata']['score_eligibility']['scoreable']:
                s['metadata']['research']['price_date'] = '2026-09-11'
        result = view_rank(sample, self.registry)
        self.assertEqual(result['market_session_date'], '2026-09-11')
        self.assertEqual(POLICY_FIXTURE.read_bytes(), before)
        self.assertEqual(json.loads(before)['market_session_date'], '2026-09-04')

if __name__ == '__main__':
    unittest.main()
