from pathlib import Path
APP=Path('multi-bagger-dashboard')
p=APP/'v22_pipeline.py';s=p.read_text()
old="        if not r.get('price_date'):\n            reasons.append('Market-data date is missing.')"
new="""        if not r.get('price_date'):
            reasons.append('Market-data date is missing.')
        else:
            try:
                age = (as_of - date.fromisoformat(r['price_date'])).days
                if age < 0 or age > 4:
                    reasons.append('Quote date is outside the permitted four-calendar-day freshness window; a new scenario score is withheld.')
            except (ValueError, TypeError):
                reasons.append('Quote date cannot be verified.')"""
assert old in s;s=s.replace(old,new)
old="'calibration_status': data['calibration']['status']}"
new="""'calibration_status': data['calibration']['status'],
            'last_refresh_attempt': json.loads((app/'monitoring/last_attempt.json').read_text()) if (app/'monitoring/last_attempt.json').exists() else None}"""
assert old in s;s=s.replace(old,new);p.write_text(s)
p=APP/'v22/app.js';s=p.read_text();old="+' · Scenario evaluation: '+d.evaluation_date_utc+' UTC';"
new="""+' · Scenario evaluation: '+d.evaluation_date_utc+' UTC';
 const attempt=build?.v22?.last_refresh_attempt;
 if($('history').value==='latest'&&attempt?.status==='failed_preserved_last_good')$('freshness').textContent+=' · MARKET REFRESH FAILED '+when(attempt.at)+': '+(attempt.error||'Source data unavailable')+'. Last good measurements retained.';"""
assert old in s;s=s.replace(old,new);p.write_text(s)
p=APP/'test_v22_integration.py';s=p.read_text();anchor='    def test_expiration_and_draft_withhold(self):';assert anchor in s
s=s.replace(anchor,"""    def test_stale_quotes_do_not_get_scenario_scores(self):
        d,a,c=fixture();d['stocks'][0]['metadata']['research']['price_date']='2026-09-01'
        r=self.compute(d,a,c)['stocks'][0]
        self.assertIsNone(r['shadow_feasibility_score'])
        self.assertTrue(any('freshness window' in reason for reason in r['critical_reasons']))
"""+anchor);p.write_text(s)
p=APP/'v22/README.md';s=p.read_text().replace('All available stock prices retain their actual\nmarket dates.', 'All available stock prices retain their actual\nmarket dates. A failed market catch-up retains the last good snapshot and shows\nan explicit failure/date warning; quotes beyond four calendar days cannot\nproduce a new scenario score.')
p.write_text(s)
print('Added conservative stale-quote gate and explicit failed-refresh banner without changing the frozen quality engine.')
import runpy
runpy.run_path('.migration/v22/fix_candidate_audit.py',run_name='__main__')
