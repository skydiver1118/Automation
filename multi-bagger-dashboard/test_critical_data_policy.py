import json,unittest
from pathlib import Path
from critical_data_policy import assess,headline_mb

APP=Path(__file__).resolve().parent
EXPECTED_UNSCORED={'FIGR','RKLB','GRRR','QBTS','SOUN','POET','OKLO','APLD','SMR','EOSE','RZLV','SERV'}
EXPECTED_ACTION=['ETN','ZETA','HUBB','CRMD','VST','AXTI','KTOS','AVAV','EVLV','BKSY']

class CriticalDataPolicyTests(unittest.TestCase):
 def setUp(self):
  self.x=json.loads((APP/'monitoring/latest.json').read_text())
  self.rows={s['ticker']:s for s in self.x['stocks']}
 def test_expected_critical_data_holds(self):
  got={t for t,s in self.rows.items() if s['metadata']['score_eligibility']['status']=='missing_critical_data'}
  self.assertEqual(got,EXPECTED_UNSCORED)
  for t in got:
   r=self.rows[t]['metadata']['research'];q=self.rows[t]['metadata']['score_eligibility']
   self.assertFalse(q['scoreable']);self.assertTrue(q['critical_reasons'])
   self.assertIsNone(r['research_mb_score']);self.assertIsNone(r['research_ev_score'])
   self.assertIsNone(self.rows[t]['metadata']['tier_rank'])
   self.assertEqual(self.rows[t]['data_confidence'],'missing_critical_data')
 def test_scoreable_warning_examples_remain_scored(self):
  for t in ['VST','IREN','NBIS','TSSI','RR']:
   q=self.rows[t]['metadata']['score_eligibility'];self.assertTrue(q['scoreable'],t)
   self.assertIsNotNone(self.rows[t]['metadata']['research']['research_mb_score'])
  self.assertIn('historical_cells_missing',[w['code'] for w in self.rows['VST']['metadata']['audit']['warnings']])
  self.assertIn('quarter_bridge_mismatch',[w['code'] for w in self.rows['IREN']['metadata']['audit']['warnings']])
 def test_capital_claim_gap_blocks_eose(self):
  q=self.rows['EOSE']['metadata']['score_eligibility']
  self.assertFalse(q['scoreable']);self.assertTrue(any('financing claims' in x.lower() for x in q['critical_reasons']))
 def test_action10_is_top10_scoreable(self):
  action=[s for s in self.x['stocks'] if s['metadata']['tier']=='action']
  action=sorted(action,key=lambda s:s['metadata']['tier_rank'])
  self.assertEqual([s['ticker'] for s in action],EXPECTED_ACTION)
  self.assertTrue(all(s['metadata']['score_eligibility']['scoreable'] for s in action))
  scoreable=sorted([s for s in self.x['stocks'] if s['metadata']['score_eligibility']['scoreable']],key=lambda s:(-headline_mb(s),s['ticker']))
  self.assertEqual([s['ticker'] for s in scoreable[:10]],EXPECTED_ACTION)
 def test_market_data_not_refreshed_on_labor_day_policy_run(self):
  p=self.x['metadata']['critical_data_policy']
  self.assertFalse(p['market_refresh_performed']);self.assertEqual(self.x['market_session_date'],'2026-09-04')
  self.assertEqual(p['market_gate']['date'],'2026-09-07');self.assertFalse(p['market_gate']['run'])
 def test_no_hidden_current_rank_for_unscored(self):
  for s in self.x['stocks']:
   if not s['metadata']['score_eligibility']['scoreable']:
    self.assertIsNone(s['metadata']['tier_rank'])

if __name__=='__main__':unittest.main()
