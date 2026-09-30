"""Company-review release tests use its immutable source snapshot, never freeze live dates.

These test numerical/provenance safeguards, not the accuracy of five-year forecasts.
"""
import copy
import json
import unittest
from datetime import date
from decimal import Decimal, localcontext
from pathlib import Path
from v22_pipeline import build_payload, financial_basis, canonical
from v22_review_bridge import observed_state, resolve, validate_funding
from test_v22_integration import fixture

APP=Path(__file__).resolve().parent
RELEASE_SOURCE=APP/'monitoring/runs/2026-09-30T013246Z-weekly.json'

class ReviewResolutionTests(unittest.TestCase):
    def example(self):
        d,a,c=fixture();s=d['stocks'][0];s['metadata']['review_queue']=['New source review required']
        s['metadata']['event_scan']={'new_filings':[{'form':'8-K','date':'2026-09-28','url':'https://example.com/old'}]}
        r=a['records']['TEST'];r['review_resolution']={
            'observed_state_sha256':observed_state(s,financial_basis(s)),
            'conclusion':'Synthetic event checked for test only.', 'source_ids':['S'],
            'financial_overrides':{}, 'override_rationale':'', 'override_source_ids':[]}
        return d,a,c

    def compute(self,d,a,c):return build_payload(d,a,c,as_of=date(2026,9,29))['stocks'][0]

    def test_exact_review_clears_only_the_captured_queue(self):
        d,a,c=self.example();before=canonical(d)
        r=self.compute(d,a,c)
        self.assertIsNotNone(r['scenarios']);self.assertEqual(before,canonical(d))
        self.assertFalse(r['full_research_certified']);self.assertIsNone(r['v22_rank'])

    def test_new_filing_invalidates_even_if_queue_message_unchanged(self):
        d,a,c=self.example();d['stocks'][0]['metadata']['event_scan']['new_filings'].append({'url':'https://example.com/new'})
        self.assertIsNone(self.compute(d,a,c)['scenarios'])

    def test_changed_shares_and_financials_invalidate(self):
        for k,v in [('shares_outstanding',11),('revenue_ttm',101),('cash',3)]:
            d,a,c=self.example();d['stocks'][0]['metadata']['research'][k]=v
            with self.subTest(field=k):self.assertIsNone(self.compute(d,a,c)['scenarios'])

    def test_price_change_recalculates_without_approving_new_financial_data(self):
        d,a,c=self.example();old=self.compute(d,a,c)
        d['stocks'][0]['metadata']['research'].update(price=20,market_cap=200)
        new=self.compute(d,a,c);self.assertIsNotNone(new['scenarios'])
        self.assertAlmostEqual(old['supportable_5y_multiple_base']/2,new['supportable_5y_multiple_base'])

    def test_current_capital_claim_hold_cannot_be_overridden(self):
        d,a,c=self.example();s=d['stocks'][0]
        s['metadata']['audit']['warnings']=[{'severity':'critical','code':'material_unresolved','message':'Missing capital claims'}]
        self.assertIsNone(self.compute(d,a,c)['scenarios'])

    def test_financial_correction_requires_sources_and_preserves_original(self):
        d,a,c=self.example();before=copy.deepcopy(d);rr=a['records']['TEST']['review_resolution']
        rr.update(financial_overrides={'economic_shares':12,'revenue_ttm':110,'financial_period_end':'2026-08-01'},override_rationale='Synthetic primary-file reconciliation.',override_source_ids=['S'])
        r=self.compute(d,a,c)
        self.assertEqual(d,before);self.assertEqual(r['reference_market_cap'],120)
        self.assertEqual(r['revenue_ttm'],110);self.assertEqual(r['financial_period_end'],'2026-08-01')
        rr['override_source_ids']=[];self.assertIsNone(self.compute(d,a,c)['scenarios'])

    def test_invalid_or_unpermitted_overrides_fail_closed(self):
        for field,value in [('economic_shares',0),('cash',-1),('financial_period_end','bad'),('research_mb_score',95)]:
            d,a,c=self.example();rr=a['records']['TEST']['review_resolution']
            rr.update(financial_overrides={field:value},override_rationale='Synthetic.',override_source_ids=['S'])
            with self.subTest(field=field):self.assertIsNone(self.compute(d,a,c)['scenarios'])

    def test_funding_budget_cannot_hide_missing_or_double_charged_debt(self):
        rec={'scenarios':{'base':{'inputs':{'net_debt_5y':30},'funding_bridge':dict(starting_net_debt=10,capex_5y=50,cfo_5y=20,new_common_cash_5y=15,other_funding_uses_5y=5,terminal_net_debt=30)}}}
        self.assertEqual(validate_funding(rec),[])
        rec['scenarios']['base']['inputs']['net_debt_5y']=40
        self.assertTrue(validate_funding(rec))
        del rec['scenarios']['base']['funding_bridge']['cfo_5y'];self.assertTrue(validate_funding(rec))

    def test_malformed_funding_is_withheld_not_an_exception(self):
        for cases in ([],{'base':'bad'},{'base':{'funding_bridge':[]}}):
            self.assertTrue(validate_funding({'scenarios':cases}))

class CompanyReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads(RELEASE_SOURCE.read_text())
        cls.assumptions=json.loads((APP/'v22/research/scenario_release_2026-09-29.json').read_text())
        cls.calibration=json.loads((APP/'v22/calibration.json').read_text())
        cls.result=build_payload(cls.data,cls.assumptions,cls.calibration,as_of=date(2026,9,30),source_bytes=RELEASE_SOURCE.read_bytes())
        cls.rows={r['ticker']:r for r in cls.result['stocks']}

    def test_initial_release_has_all_company_dispositions(self):
        self.assertEqual(set(self.assumptions['company_reviews']),{s['ticker'] for s in self.data['stocks']})
        self.assertEqual(self.result['counts']['company_reviews'],32)
        self.assertEqual(self.result['counts']['reviewed_scenario_sets'],16)
        self.assertEqual(self.result['counts']['missing_critical_scenario_data'],16)

    def test_each_assumption_has_reviewed_sources_and_rationale(self):
        for ticker,r in self.assumptions['records'].items():
            for name,s in r['scenarios'].items():
                for k in s['inputs']:
                    e=s['assumption_evidence'][k]
                    self.assertTrue(e['rationale']);self.assertTrue(e['source_ids'])
                    self.assertTrue(all(id in r['sources'] for id in e['source_ids']))
            self.assertEqual(validate_funding(r),[],ticker)

    def test_newly_identified_perimeter_gaps_do_not_get_scenarios(self):
        for t in ('ETN','NBIS','FIGR','MU','LITE'):
            self.assertIsNone(self.rows[t]['scenarios'],t)
            self.assertIsNone(self.rows[t]['shadow_feasibility_score'],t)
            self.assertTrue(self.rows[t]['critical_reasons'],t)

    def test_all_48_cases_match_independent_decimal_arithmetic(self):
        with localcontext() as ctx:
            ctx.prec=40
            for row in self.result['stocks']:
                if not row['scenarios']:continue
                r=row['scenario_assumptions']
                for name,out in row['scenarios'].items():
                    p=r['scenarios'][name]['inputs'];d=lambda x:Decimal(str(x))
                    revenue=d(row['revenue_ttm'])*(1+d(p['revenue_cagr']))**5
                    if r['model']=='equity_pe':equity=revenue*d(p['net_margin'])*d(p['terminal_pe'])
                    else:equity=revenue*d(p['ebitda_margin'])*d(p['terminal_ev_ebitda'])-sum(d(p[k]) for k in ('net_debt_5y','preferred_claims_5y','minority_claims_5y','other_claims_5y'))
                    multiple=max(Decimal(0),equity)/(d(row['reference_market_cap'])*(1+d(p['dilution_5y'])))
                    self.assertAlmostEqual(float(multiple),out['supportable_5y_multiple'],places=10,msg=row['ticker']+name)
                    self.assertAlmostEqual(float(revenue),r['scenarios'][name]['revenue_year5_usd'],delta=max(1.,float(revenue)*1e-12))

    def test_review_corrections_not_written_back_to_v1(self):
        original={s['ticker']:s['metadata']['research'] for s in self.data['stocks']}
        self.assertEqual(self.rows['AVAV']['revenue_ttm'],2002659000)
        self.assertEqual(self.rows['AVAV']['financial_period_end'],'2026-08-01')
        self.assertAlmostEqual(self.rows['RGTI']['reference_market_cap'],341508685*original['RGTI']['price'])
        self.assertEqual(json.loads(RELEASE_SOURCE.read_text()),self.data)

    def test_stress_and_uncalibrated_status_are_explicit(self):
        for r in self.result['stocks']:
            self.assertIsNone(r['v22_final_score']);self.assertIsNone(r['v22_rank']);self.assertIsNone(r['probability_5x'])
            self.assertFalse(r['full_research_certified'])
            if r['scenarios']:
                self.assertLessEqual(r['stressed_base']['supportable_5y_multiple'],r['supportable_5y_multiple_base']+1e-12)
                self.assertIn('not a full',r['stressed_base']['rule'])

if __name__=='__main__':unittest.main()
