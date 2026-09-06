"""Regression tests for approved membership, scoring disclosure and archive preservation."""
import copy, importlib.util, json, unittest
from decimal import Decimal
from pathlib import Path
from research_scoring import compute_all, score, FACTORS, WEIGHTS
from build_site import verify_legacy as verify, load, APP, BASE

class Final25Tests(unittest.TestCase):
 def test_membership_and_snapshot_reconcile(self):
  x,r,_=verify();self.assertEqual(r['members'],25);self.assertEqual(r['history'],{'snapshots':3,'history_rows':65,'stocks_in_latest':25})
 def test_no_legacy_score_rewrite(self):
  p=load(BASE/'pass_scores/2026-09-04.json');self.assertEqual(p['stocks'][0]['multi_bagger_score'],93);self.assertEqual(p['universe_size'],20)
 def test_independent_decimal_calculation(self):
  p=load(APP/'research/2026-09-06/inputs.json')
  for r in compute_all(p):
   n=Decimal(0);d=Decimal(0)
   for k,w in zip(FACTORS,WEIGHTS['base']):
    if r['factor_scores'][k] is not None:
     eff=Decimal(w)*Decimal(str(r['factor_coverage'][k]));n+=eff*Decimal(str(r['factor_scores'][k]));d+=eff
   self.assertLess(abs(float(n/d)-r['research_mb_score']),1e-10)
 def test_order_invariant(self):
  p=load(APP/'research/2026-09-06/inputs.json');a=compute_all(p);p['stocks'].reverse();self.assertEqual(a,compute_all(p))
 def test_missing_and_zero_differ(self):
  self.assertIsNone(score(None,'growth'));self.assertEqual(score(0,'op'),50)
 def test_missing_probabilities_and_deltas(self):
  x=load(BASE/'pass_scores/latest.json')
  for s in x['stocks']:
   self.assertIsNone(s['probability_5x_pct']);self.assertIsNone(s['rank_delta']);self.assertIsNone(s['multi_bagger_score'])
 def test_no_new_entry_targets_fabricated(self):
  x=load(BASE/'pass_scores/latest.json')
  for s in x['stocks']:
   if s['metadata']['new_member']:self.assertIsNone(s['entry_zone']['low']);self.assertEqual(s['entry_zone']['hit_status'],'no_zone')
 def test_etf_scope_and_source_provenance(self):
  m=load(APP/'research/2026-09-06/membership.json');self.assertEqual(len(m['funds']),5)
  for f in m['funds']:self.assertEqual(f['status'],'retrieved');self.assertIn('Sep 03, 2026',f['as_of_header']);self.assertEqual(len(f['source_sha256']),64)
 def test_partial_passes_are_not_claimed_complete(self):
  x=load(BASE/'pass_scores/latest.json')
  for s in x['stocks']:
   self.assertEqual(sum(p['status']=='complete' for p in s['passes'].values()),1)
   self.assertIn('research',s['passes']['pass_5_technical_review']['metadata']['scope'].lower())
 def test_display_and_null_guards(self):
  html=(APP/'index.html').read_text();self.assertIn('MB research',html);self.assertIn("p.score==null",html);self.assertNotIn('Number(v??0)',html);self.assertIn('coverage(s)',html);self.assertIn('America/New_York',html)

if __name__=='__main__':unittest.main()
