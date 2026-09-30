"""A technical-only Candidate must remain unscored without claiming a source audit."""
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
