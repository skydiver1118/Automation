"""Evidence provenance, numerical correctness, missingness and review-gate regressions."""
import copy,hashlib,json,unittest
from decimal import Decimal
from pathlib import Path
from evidence_gate import evidence_status,verify_audit,audit_summary,dependencies
from watchlist import APP,load,members,validate

class EvidenceAuditTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.x=load(sorted((APP/'monitoring/runs').glob('*evidence_repair.json'))[0]);cls.rows={s['ticker']:s for s in cls.x['stocks']}
  cls.audits={t:load(APP/s['metadata']['audit_file'].removeprefix('./')) for t,s in cls.rows.items() if s['metadata'].get('audit_file')}
 def test_thirty_complete_scorecard_structures(self):
  self.assertEqual(len(self.rows),30);self.assertEqual(len(self.audits),30)
  for t,a in self.audits.items():
   self.assertEqual(len(a['factors']),8);self.assertEqual(len(a['passes']),6);self.assertEqual(len(a['financial_history']['rows']),8)
   self.assertEqual(len({q['period_end'] for q in a['financial_history']['rows']}),8)
 def test_sources_and_audit_paths_reconcile(self):
  for s in self.rows.values():verify_audit(s)
  for a in self.audits.values():self.assertEqual(len(a['sources']),len({v['id'] for v in a['sources']}))
 def test_independent_weighted_points(self):
  for a in self.audits.values():
   den=sum(Decimal(str(f['weight_pct']))*Decimal(str(f['input_coverage'])) for f in a['factors'] if f['score'] is not None)
   total=sum(Decimal(str(f['weight_pct']))*Decimal(str(f['input_coverage']))*Decimal(str(f['score'])) for f in a['factors'] if f['score'] is not None)/den
   self.assertLess(abs(float(total)-a['screening_mb_score']),1e-8)
 def test_same_calculator_unchanged(self):
  self.assertEqual(hashlib.sha256((APP/'research_scoring.py').read_bytes()).hexdigest(),'dbe4e33b5b5002d32a6e3a6114279332a252db6b627d2806fbd38a7ee7dc078a')
 def test_no_fake_numeric_pass_grades(self):
  for a in self.audits.values():
   for key,p in a['passes'].items():
    if 'pass_5' not in key:self.assertIsNone(p['score'])
    self.assertEqual(p['metadata']['completed_checks'],sum(c['passed'] for c in p['metadata']['checks']))
    self.assertEqual(p['status']=='complete',all(c['passed'] for c in p['metadata']['checks']))
 def test_missing_gross_profit_stays_missing(self):
  a=self.audits['POET'];self.assertIsNone(a['verified_mb_score'])
  self.assertTrue(all(q['values'].get('gross_profit') is None for q in a['financial_history']['rows']))
  self.assertTrue(any(w['code']=='historical_cells_missing' for w in a['warnings']))
 def test_full_signoff_withheld_for_every_stock(self):
  for s in self.rows.values():
   self.assertIsNone(s['metadata']['audit']['verified_mb_score'])
   self.assertFalse(s['metadata']['research']['full_research_validation_complete'])
   self.assertTrue(s['metadata']['research_review_required'])
 def test_no_signoff_on_critical_or_missing(self):
  for s in self.rows.values():
   a=s['metadata']['audit'];r=s['metadata']['research']
   if any(w['severity']=='critical' for w in a['warnings']) or r['mb_input_weight_coverage']<1:self.assertIsNone(a['verified_mb_score'])
 def test_dynamic_new_filing_invalidates(self):
  s=copy.deepcopy(self.rows['ETN']);evidence_status(s,['New material filed acquisition requires review'])
  self.assertIsNone(s['metadata']['audit']['verified_mb_score']);self.assertTrue(s['metadata']['research_review_required'])
  self.assertFalse(s['metadata']['research']['full_research_validation_complete'])
 def test_stale_market_invalidates(self):
  s=copy.deepcopy(self.rows['ETN']);s['metadata']['refresh_status']='stale_refresh_failed';evidence_status(s)
  self.assertIsNone(s['metadata']['audit']['verified_mb_score'])
 def test_changed_financial_dependency_invalidates(self):
  s=copy.deepcopy(self.rows['ETN']);s['metadata']['research']['cash']*=2;evidence_status(s)
  self.assertIsNone(s['metadata']['audit']['verified_mb_score'])
 def test_price_overlay_does_not_claim_new_statement_research(self):
  s=copy.deepcopy(self.rows['ETN']);old=s['metadata']['audit']['reviewed_at'];s['metadata']['research']['price']*=1.01
  self.assertEqual(dependencies(s['metadata']['research']),s['metadata']['audit']['input_dependency_sha256']);evidence_status(s)
  self.assertEqual(s['metadata']['audit']['reviewed_at'],old)
 def test_source_files_immutable_on_live_invalidation(self):
  s=copy.deepcopy(self.rows['ETN']);p=APP/s['metadata']['audit_file'].removeprefix('./');before=p.read_bytes();evidence_status(s,['New filing'])
  self.assertEqual(p.read_bytes(),before)
 def test_authorized_reassignment_retains_all_thirty(self):
  r=self.x['metadata']['registry'];validate(r)
  self.assertEqual(set(members(r,'action')),set('ETN ZETA HUBB CRMD AXTI KTOS AVAV EVLV BKSY AMPX'.split()))
  self.assertEqual(len(members(r,'candidate')),20);self.assertIn('FIGR',members(r,'candidate'));self.assertFalse(r['automatic_swaps'])
  self.assertTrue(r['last_reassignment']['approval_ref'])
 def test_critical_finance_cannot_enter_daily_action(self):
  self.assertFalse(self.audits['FIGR']['eligible_for_daily_attention'])
  self.assertIsNone(self.audits['FIGR']['verified_mb_score'])
 def test_cash_capex_scope_regressions(self):
  q=self.rows['QBTS']['metadata']['research'];self.assertAlmostEqual(q['capex_ttm'],8875000,delta=1)
  w=self.rows['WULF']['metadata']['research'];self.assertAlmostEqual(w['gross_profit_ttm'],114416000,delta=1)
 def test_summary_does_not_overstate_completion(self):
  x=audit_summary(self.x);self.assertEqual(x['scorecards_with_audit'],30);self.assertEqual(x['full_numeric_input_coverage'],22)
  self.assertEqual(x['input_audited'],13);self.assertEqual(x['full_research_verified'],0);self.assertFalse(x['full_six_pass_complete'])
 def test_mobile_and_warning_contract(self):
  s=(APP/'index.html').read_text()
  for token in ['passCards','auditBanner','eight-quarter','financial_history','missing-value','Provisional · information gaps','loadEvidence']:self.assertIn(token.lower(),s.lower())
if __name__=='__main__':unittest.main()
