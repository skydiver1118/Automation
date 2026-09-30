"""v2.2 mathematical/evidence/preservation tests use synthetic data, not live constants."""
import copy
import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from feasibility_v22 import scenario, enterprise_scenario, reverse_requirements, scenario_set
from v22_pipeline import archive, build_payload, canonical, financial_basis, METHODOLOGY

APP = Path(__file__).resolve().parent
TODAY = date(2026, 9, 29)

def fixture():
    row = {'ticker':'TEST','metadata': {'tier':'candidate','tier_rank':1,
        'research_reviewed_at':'2026-09-28T20:00:00Z',
        'score_eligibility':{'scoreable':True}, 'audit':{'warnings':[]},
        'research':{'market_cap':100.,'price':10.,'price_date':'2026-09-28',
            'revenue_ttm':100.,'financial_period_end':'2026-06-30','mb_input_weight_coverage':1.,
            'factor_coverage':{'growth':1.},'factor_scores':{'growth':50.},
            'research_mb_score':55.,'research_ev_score':50.}}}
    data = {'stocks':[row],'recorded_at':'2026-09-29T12:00:00Z', 'market_session_date':'2026-09-28',
            'methodology_version':'unchanged-v1','metadata':{'monitoring_id':'synthetic'}}
    fields={'revenue_cagr':0.,'net_margin':.5,'terminal_pe':10.,'dilution_5y':.2}
    rec={'review_status':'reviewed','reviewed_at':'2026-09-29T00:00:00Z','valid_through':'2026-10-10',
        'financial_basis_sha256':financial_basis(row),'model':'equity_pe',
        'model_rationale':'Synthetic unit-test case, not real company research.',
        'funding_assessment':'Synthetic explicit 20% dilution assumption.',
        'sources':{'S':{'url':'https://example.com/fixture','as_of':'2026-09-28'}}, 'scenarios':{}}
    for name,margin in [('bear',.3),('base',.5),('bull',.7)]:
        rec['scenarios'][name]={'label':'Synthetic '+name,'inputs':fields|{'net_margin':margin},
            'assumption_evidence':{k:{'rationale':'Synthetic assumption for arithmetic testing.','source_ids':['S']} for k in fields}}
    definitions={'methodology':METHODOLOGY,'status':'shadow_only','records':{'TEST':rec}}
    calibration={'status':'blocked_not_calibrated','production_adoption_allowed':False}
    return data,definitions,calibration

class V22MathTests(unittest.TestCase):
    def test_fivefold_equity_hurdle_increases_with_dilution(self):
        r=scenario(market_cap=100,revenue_ttm=100,revenue_cagr=0,net_margin=.5,terminal_pe=10,dilution_5y=.2)
        self.assertEqual(r['required_5x_market_cap'],500)
        self.assertEqual(r['required_5x_market_cap_dilution_adjusted'],600)
        self.assertEqual(r['terminal_equity_value_5y'],500)
        self.assertAlmostEqual(r['supportable_5y_multiple'],5/1.2)
    def test_pe_cannot_subtract_debt_twice(self):
        with self.assertRaises(ValueError):scenario(market_cap=100,revenue_ttm=100,revenue_cagr=0,net_margin=.5,terminal_pe=10,net_debt_5y=20)
    def test_enterprise_claims_exactly_once(self):
        r=enterprise_scenario(market_cap=100,revenue_ttm=100,revenue_cagr=0,ebitda_margin=.5,terminal_ev_ebitda=10,dilution_5y=.2,net_debt_5y=50,preferred_claims_5y=20,minority_claims_5y=10,other_claims_5y=0)
        self.assertEqual(r['terminal_equity_value_5y'],420)
        self.assertAlmostEqual(r['supportable_5y_multiple'],3.5)
    def test_reverse_matches_forward(self):
        r=reverse_requirements(market_cap=100,revenue_ttm=50,dilution_5y=.2,net_margin=.2,terminal_pe=20)
        x=scenario(market_cap=100,revenue_ttm=50,revenue_cagr=r['required_revenue_cagr'],net_margin=.2,terminal_pe=20,dilution_5y=.2)
        self.assertAlmostEqual(x['supportable_5y_multiple'],5)
    def test_reverse_missing_revenue_is_not_zero(self):
        r=reverse_requirements(market_cap=100,revenue_ttm=None,dilution_5y=0,net_margin=.2,terminal_pe=20)
        self.assertIsNone(r['required_revenue_cagr']);self.assertEqual(r['required_terminal_equity'],500)
    def test_bad_inputs_fail_closed(self):
        args=dict(market_cap=100,revenue_ttm=100,revenue_cagr=0,net_margin=.2,terminal_pe=20,dilution_5y=0)
        for k,v in [('market_cap',0),('revenue_ttm',None),('net_margin',2),('dilution_5y',-1),('revenue_cagr',-1.5),('terminal_pe',True),('net_margin',float('nan'))]:
            with self.subTest(field=k),self.assertRaises(ValueError):scenario(**(args|{k:v}))
    def test_overflow_rejected(self):
        with self.assertRaises(ValueError):
            reverse_requirements(market_cap=1e308,revenue_ttm=100,dilution_5y=.5,net_margin=.2,terminal_pe=20)
    def test_no_dividend_probability_claim(self):
        r=scenario(market_cap=100,revenue_ttm=100,revenue_cagr=0,net_margin=.5,terminal_pe=10)
        self.assertEqual(r['shadow_feasibility_score'],85)
        self.assertIsNone(r['calibrated_probability_5x']);self.assertIsNone(r['final_multibagger_score'])
        self.assertIn('excluding_dividends',r['return_basis'])

class V22AdapterTests(unittest.TestCase):
    def compute(self,d=None,a=None,c=None):
        f=fixture();return build_payload(d or f[0],a or f[1],c or f[2],as_of=TODAY)
    def test_reviewed_scenarios_produce_only_shadow(self):
        p=self.compute();r=p['stocks'][0]
        self.assertEqual(r['status'],'shadow_uncalibrated');self.assertIsNotNone(r['shadow_feasibility_score'])
        for k in ('v22_final_score','probability_5x','v22_rank'):self.assertIsNone(r[k])
        self.assertFalse(p['production_rank_effect'])
    def test_missing_scenarios_withhold_score_but_keep_hurdle(self):
        d,a,c=fixture();a['records']={};r=self.compute(d,a,c)['stocks'][0]
        self.assertIsNone(r['shadow_feasibility_score']);self.assertTrue(r['critical_reasons'])
        self.assertEqual(r['required_5x_market_cap_no_dilution'],500);self.assertEqual(len(r['reverse_sensitivities']),27)
    def test_critical_v1_hold_is_not_bypassed(self):
        d,a,c=fixture();d['stocks'][0]['metadata']['audit']['warnings']=[{'severity':'critical','code':'material_unresolved','message':'Unreconciled financing'}]
        r=self.compute(d,a,c)['stocks'][0];self.assertIsNone(r['shadow_feasibility_score']);self.assertIsNone(r['mb_quality_score_v1'])
    def test_omitted_dilution_is_not_zero(self):
        d,a,c=fixture();del a['records']['TEST']['scenarios']['base']['inputs']['dilution_5y']
        r=self.compute(d,a,c)['stocks'][0];self.assertIsNone(r['shadow_feasibility_score'])
    def test_unsourced_assumption_withholds_score(self):
        d,a,c=fixture();a['records']['TEST']['scenarios']['base']['assumption_evidence']['terminal_pe']['source_ids']=[]
        self.assertIsNone(self.compute(d,a,c)['stocks'][0]['shadow_feasibility_score'])
    def test_changed_financial_dependency_withholds(self):
        d,a,c=fixture();d['stocks'][0]['metadata']['research']['revenue_ttm']=101
        self.assertIsNone(self.compute(d,a,c)['stocks'][0]['shadow_feasibility_score'])
    def test_stale_quotes_do_not_get_scenario_scores(self):
        d,a,c=fixture();d['stocks'][0]['metadata']['research']['price_date']='2026-09-01'
        r=self.compute(d,a,c)['stocks'][0]
        self.assertIsNone(r['shadow_feasibility_score'])
        self.assertTrue(any('freshness window' in reason for reason in r['critical_reasons']))
    def test_expiration_and_draft_withhold(self):
        for field,value in [('valid_through','2026-08-01'),('review_status','draft')]:
            d,a,c=fixture();a['records']['TEST'][field]=value
            self.assertIsNone(self.compute(d,a,c)['stocks'][0]['shadow_feasibility_score'])
    def test_new_unreviewed_members_are_included_unscored(self):
        d,a,c=fixture();d['stocks'].append({'ticker':'NEW','metadata':{'tier':'candidate','research':{}}})
        r=self.compute(d,a,c)['stocks'][1];self.assertIsNone(r['reference_market_cap']);self.assertIsNone(r['shadow_feasibility_score']);self.assertTrue(r['critical_reasons'])
    def test_no_mutation_or_cross_list_reordering(self):
        d,a,c=fixture();before=copy.deepcopy([d,a,c]);self.compute(d,a,c);self.assertEqual([d,a,c],before)
    def test_duplicate_rejected(self):
        d,a,c=fixture();d['stocks'].append(copy.deepcopy(d['stocks'][0]))
        with self.assertRaises(ValueError):self.compute(d,a,c)
    def test_malformed_evidence_and_future_sources_fail_closed(self):
        for field,value in [('sources',[]),('sources',{'S':{'url':'https://example.com/test','as_of':'2099-01-01'}}),('scenarios',[]),('scenarios',{'base':'not a record'})]:
            d,a,c=fixture();a['records']['TEST'][field]=value
            self.assertIsNone(self.compute(d,a,c)['stocks'][0]['shadow_feasibility_score'])
    def test_config_cannot_turn_on_production(self):
        d,a,c=fixture();c['production_adoption_allowed']=True
        with self.assertRaises(ValueError):self.compute(d,a,c)
    def test_actual_universe_respects_existing_nulls(self):
        d=json.loads((APP/'monitoring/latest.json').read_text());before=canonical(d)
        a=json.loads((APP/'v22/assumptions.json').read_text());c=json.loads((APP/'v22/calibration.json').read_text())
        p=build_payload(d,a,c,as_of=TODAY)
        self.assertEqual(len(p['stocks']),len(d['stocks']));self.assertEqual(canonical(d),before)
        for original,row in zip(d['stocks'],p['stocks']):
            self.assertEqual(original['ticker'],row['ticker'])
            if not original['metadata'].get('score_eligibility',{}).get('scoreable'):
                self.assertIsNone(row['mb_quality_score_v1']);self.assertIsNone(row['shadow_feasibility_score'])
    def test_archive_is_idempotent_immutable_and_separate(self):
        with tempfile.TemporaryDirectory() as folder:
            app=Path(folder);(app/'v22').mkdir();(app/'monitoring').mkdir()
            d,a,c=fixture();raw=canonical(d);(app/'monitoring/latest.json').write_bytes(raw)
            (app/'v22/assumptions.json').write_bytes(canonical(a));(app/'v22/calibration.json').write_bytes(canonical(c))
            one=archive(app);two=archive(app);self.assertEqual(one,two)
            self.assertEqual((app/'monitoring/latest.json').read_bytes(),raw)
            paths=list((app/'monitoring/v22/runs').glob('*.json'));self.assertEqual(len(paths),1)
            paths[0].write_text('{}')
            with self.assertRaises(ValueError):archive(app)
