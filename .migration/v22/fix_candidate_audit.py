from pathlib import Path
APP=Path('multi-bagger-dashboard')
p=APP/'evidence_gate.py';s=p.read_text()
s=s.replace("'scorecards_with_audit':sum(bool(s.get('metadata',{}).get('audit')) for s in rows)","'scorecards_with_audit':sum(bool(s.get('metadata',{}).get('audit')) and bool(s.get('metadata',{}).get('audit_file')) for s in rows)")
old="""    m=stock['metadata'];a=m.get('audit')
    if not a:return
    rel=m.get('audit_file','').removeprefix('./')
"""
new="""    m=stock['metadata'];a=m.get('audit');r=m.get('research',{})
    if r.get('full_research_validation_complete') or (a or {}).get('verified_mb_score') is not None:
        raise ValueError('Full research verification is not supported by this bounded input-audit version')
    if not a:return
    rel=m.get('audit_file','')
    if not rel:
        # A price-only Candidate receives a policy/warning envelope after its first
        # technical refresh. That envelope is not a source audit. Permit only an
        # explicitly unscored, unranked, unreviewed Candidate; never waive source
        # lineage for an investment score or relax path containment.
        q=m.get('score_eligibility',{})
        claims=[r.get('research_mb_score'),r.get('research_ev_score'),
                a.get('input_audited_mb_score'),a.get('headline_mb_score'),a.get('headline_ev_score'),
                q.get('headline_mb_score'),q.get('headline_ev_score'),
                stock.get('multi_bagger_score'),stock.get('expectation_valuation_score'),
                stock.get('probability_5x_pct')]
        empty_candidate=(m.get('tier')=='candidate' and not r.get('analyst_grades')
            and not r.get('factor_scores') and r.get('mb_input_weight_coverage') is None
            and m.get('tier_rank') is None and q.get('scoreable') is False
            and q.get('status')=='missing_critical_data' and bool(q.get('critical_reasons'))
            and a.get('status')!='reviewed_within_scope' and a.get('baseline_status')!='reviewed_within_scope'
            and all(v is None for v in claims))
        if not empty_candidate:raise ValueError('Missing source audit file cannot support investment scores or a reviewed claim')
        return
    if not isinstance(rel,str):raise ValueError('Audit path must be a relative string')
    rel=rel.removeprefix('./')
"""
assert old in s;s=s.replace(old,new);p.write_text(s)
(APP/'test_candidate_audit_envelope.py').write_text('''"""A technical-only Candidate must remain unscored without claiming a source audit."""
import tempfile
import unittest
from pathlib import Path
from critical_data_policy import apply
from evidence_gate import audit_summary, verify_audit
from watchlist_runtime import empty_stock

def candidate():
    s=empty_stock('NEWCO')
    s['metadata'].update({'tier':'candidate','tier_rank':None,
        'research':{'price':10.0,'price_date':'2026-09-29','technical_score':50.0}})
    return apply(s)

class CandidateAuditEnvelopeTests(unittest.TestCase):
    def test_technical_only_policy_envelope_is_not_an_audit(self):
        s=candidate()
        with tempfile.TemporaryDirectory() as d:verify_audit(s,Path(d))
        self.assertEqual(audit_summary({'stocks':[s]})['scorecards_with_audit'],0)
        self.assertIsNone(s['metadata']['research']['research_mb_score'])
        self.assertFalse(s['metadata']['score_eligibility']['scoreable'])

    def test_a_missing_file_cannot_support_an_investment_score(self):
        for field in ['research_mb_score','research_ev_score','full_research_validation_complete']:
            s=candidate();s['metadata']['research'][field]=50
            with self.subTest(field=field),self.assertRaises(ValueError):verify_audit(s)
        for field in ['input_audited_mb_score','verified_mb_score','headline_mb_score']:
            s=candidate();s['metadata']['audit'][field]=50
            with self.subTest(field=field),self.assertRaises(ValueError):verify_audit(s)
        s=candidate();s['metadata']['tier_rank']=1
        with self.assertRaises(ValueError):verify_audit(s)
        s=candidate();s['metadata']['audit']['status']='reviewed_within_scope'
        with self.assertRaises(ValueError):verify_audit(s)
        s=candidate();s['metadata']['tier']='action'
        with self.assertRaises(ValueError):verify_audit(s)

    def test_outside_path_is_still_rejected_for_unreviewed_candidate(self):
        for path in ['../outside.json','./evidence_audit/../../outside.json','/tmp/outside.json']:
            s=candidate();s['metadata']['audit_file']=path
            with tempfile.TemporaryDirectory() as d,self.subTest(path=path),self.assertRaisesRegex(ValueError,'outside evidence'):
                verify_audit(s,Path(d))

    def test_claimed_source_file_cannot_silently_disappear(self):
        s=candidate();s['metadata']['audit_file']='./evidence_audit/missing.json'
        with tempfile.TemporaryDirectory() as d,self.assertRaises(FileNotFoundError):verify_audit(s,Path(d))

if __name__=='__main__':unittest.main()
''')
print('Preserved source-path containment; technical-only Candidate policy envelopes remain unscored and are not counted as audits.')
