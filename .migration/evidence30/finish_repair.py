"""Temporary deterministic recovery. Corrupt trailing transfer data is never executed."""
import base64,hashlib,lzma,subprocess
from pathlib import Path
APP=Path('multi-bagger-dashboard')
packed=base64.b64decode(''.join(Path(f'.migration/evidence30/part{i}.b64').read_text().strip() for i in range(3)),validate=True)
raw=lzma.LZMADecompressor().decompress(packed)[:107992]
assert hashlib.sha256(raw).hexdigest()=='ad5fa2775e806a74ddc28bb75166af2dbf60b6d2809a199fc9a2d9d03bff8cb6'
paths={line[6:] for line in raw.decode().splitlines() if line.startswith('+++ b/')}
assert len(paths)==9 and all(p.startswith('multi-bagger-dashboard/') and '..' not in Path(p).parts for p in paths)
Path('/tmp/mb30-complete.patch').write_bytes(raw)
subprocess.run(['git','apply','--check','/tmp/mb30-complete.patch'],check=True)
subprocess.run(['git','apply','/tmp/mb30-complete.patch'],check=True)

def edits(name,replacements):
 p=APP/name;s=p.read_text()
 for old,new in replacements:
  if old not in s:raise ValueError(name+' missing expected source anchor: '+old[:70])
  s=s.replace(old,new)
 p.write_text(s)

edits('evidence_tools/evidence_audit_builder.py',[
 ("full=all(p['status']=='complete' for p in passes.values()) and r['mb_input_weight_coverage']==1", "input_ready=all(p['status']=='complete' for p in passes.values()) and r['mb_input_weight_coverage']==1 and not note.get('missing')\n  full=False # Bounded input checks cannot certify the original broader six-pass workflow.\n  assurance={'full_six_pass_complete':False,'model_return_validated':False,'scope':'Filed-document, financial-input and calculation audit; not exhaustive six-pass investment diligence','remaining':['Complete quarter-level segment/KPI and guidance-history reconciliation for the original research scope.','Exhaustive current index/ETF and peer-competition review is not complete.','Source-level analyst-grade justification and the full contradiction matrix require additional review.']}\n  warn('full_research_scope', 'The broader six-pass research programme remains incomplete. A passed input audit is not a fully verified MB score.', 'notice')"),
 ("confidence='lower' if ncritical else 'medium' if not full else 'higher_within_stated_scope'", "confidence='lower' if ncritical else 'medium'"),
 ("eligible=(full and ncritical==0)", "eligible=(input_ready and ncritical==0)"),
 ("'status':'reviewed_within_scope' if full else 'provisional_with_explicit_gaps','verified_mb_score':r['research_mb_score'] if full else None", "'status':'reviewed_within_scope' if input_ready else 'provisional_with_explicit_gaps','verified_mb_score':None,'input_audited_mb_score':r['research_mb_score'] if input_ready else None,'research_assurance':assurance"),
 ("'baseline_status':'reviewed_within_scope' if full else 'provisional_with_explicit_gaps'", "'baseline_status':'reviewed_within_scope' if input_ready else 'provisional_with_explicit_gaps'"),
 ("'status','baseline_status','input_dependency_sha256','verified_mb_score','evidence_check_coverage_pct'", "'status','baseline_status','input_dependency_sha256','verified_mb_score','input_audited_mb_score','research_assurance','evidence_check_coverage_pct'"),
 ("'research_review_required':not full", "'research_review_required':True"),
 ("if not full:stock['action']+=' · provisional'", "if not input_ready:stock['action']+=' · provisional'\n  m['input_audit_reviewed_at']=now\n  m['key_catalyst']=note['catalyst']"),
 ("rec['full_research_reviewed_at']=now if audits[t]['status']=='reviewed_within_scope' else None", "rec['full_research_reviewed_at']=None;rec['input_audit_reviewed_at']=now if audits[t]['status']=='reviewed_within_scope' else None"),
 ("'full_six_pass_complete':all(a['status']=='reviewed_within_scope' for a in audits.values())", "'full_six_pass_complete':False"),
 ("'verified_within_scope_count':sum(a['verified_mb_score'] is not None for a in audits.values())", "'verified_within_scope_count':0,'input_audited_count':sum(a['input_audited_mb_score'] is not None for a in audits.values()),'full_six_pass_complete':False"),
 ("'verified':audits[s['ticker']]['verified_mb_score']", "'verified':None,'input_audited':audits[s['ticker']]['input_audited_mb_score']"),
 ("x['changes']['notes']=['Source-backed evidence repair, not a market-price move.'", "x['record_limitations']=['All 30 receive a reproducible screening scorecard, not a verified six-pass investment score.','Input-audit checklist completion is separate from broader six-pass research completion; the latter is not yet certified.','Standardized historical observations and any missing values are disclosed at cell level; rows do not imply eight primary-verified quarters.','TAM, moat and execution remain source-informed analyst judgments totaling 40% of the model.','FY+1 periods differ by issuer; the forward-gross-profit calculation is a constant-margin scenario, not an actual forecast.','Incomplete MB and E&V input weights are shown with scores. Missing values are not zero.','Preferred entry ranges carried from the old archive are not newly validated buy bands.','All market measurements use the September 4 completed regular session, not a new Sunday trading session.','Action means daily research attention, not BUY or portfolio allocation. Automatic swaps and broker orders remain disabled.']\n x['metadata']['assurance_status']='Input audit only; full six-pass research incomplete'\n x['changes']['notes']=['Source-backed evidence repair, not a market-price move.'")])

edits('evidence_gate.py',[
 ("a['verified_mb_score']=None if blocking else r.get('research_mb_score')", "a['input_audited_mb_score']=None if blocking else r.get('research_mb_score')\n    a['verified_mb_score']=None\n    a.setdefault('research_assurance',{})['full_six_pass_complete']=False"),
 ("r['full_research_validation_complete']=not blocking", "r['full_research_validation_complete']=False"),
 ("confidence='lower' if any(w.get('severity')=='critical' for w in a['warnings']) else ('medium' if blocking else 'higher_within_stated_scope')", "confidence='lower' if any(w.get('severity')=='critical' for w in a['warnings']) else 'medium'"),
 ("m['research_review_required']=blocking", "m['research_review_required']=True # Full research cannot be signed off by a market-data update."),
 ("'reviewed_within_scope':sum(s.get('metadata',{}).get('audit',{}).get('verified_mb_score') is not None for s in rows)", "'reviewed_within_scope':sum(s.get('metadata',{}).get('audit',{}).get('input_audited_mb_score') is not None for s in rows),\n      'input_audited':sum(s.get('metadata',{}).get('audit',{}).get('input_audited_mb_score') is not None for s in rows),\n      'full_research_verified':sum(s.get('metadata',{}).get('audit',{}).get('verified_mb_score') is not None for s in rows)"),
 ("'provisional':sum(s.get('metadata',{}).get('audit',{}).get('verified_mb_score') is None for s in rows)", "'provisional':sum(s.get('metadata',{}).get('audit',{}).get('input_audited_mb_score') is None for s in rows)"),
 ("if a.get('verified_mb_score') is not None:\n        r=m['research']", "if a.get('verified_mb_score') is not None or m['research'].get('full_research_validation_complete'):\n        raise ValueError('Full research verification is not supported by this bounded input-audit version')\n    if a.get('input_audited_mb_score') is not None:\n        r=m['research']"),
 ("if m.get('research_review_required') or r.get('mb_input_weight_coverage')!=1", "if r.get('mb_input_weight_coverage')!=1"),
 ("if abs(a['verified_mb_score']-r['research_mb_score'])>1e-8", "if abs(a['input_audited_mb_score']-r['research_mb_score'])>1e-8")])

edits('index.html',[
 ('a.verified_mb_score','a.input_audited_mb_score'),('a?.verified_mb_score','a?.input_audited_mb_score'),('au(s)?.verified_mb_score','au(s)?.input_audited_mb_score'),
 ('Six-pass evidence checklist','Six-stage input checklist & research gaps'),
 ('Even audited inputs do not validate future returns.','Full six-pass research is not yet certified for any of the 30. “Inputs audited” covers the stated calculation checks only; it does not validate future returns.'),
 ('<th>Complete</th><th>Thesis</th>','<th>Input stages passed</th><th>Thesis</th>'),
 ('<h3>Source-backed score audit</h3>','<h3>Source-backed score audit</h3><p class="notice"><strong>Full research status: incomplete.</strong> The eight-factor score is a reproducible screen, not a certified six-pass result. The gaps below remain relevant even when the listed input checks pass.</p>'),
 ("let n=a.qualitative_review;text+=", "text+='<h3>Remaining broader research requirements</h3><ul>'+ (a.research_assurance?.remaining||[]).map(v=>'<li>'+esc(v)+'</li>').join('')+'</ul>';let n=a.qualitative_review;text+="),
 ('Each cell now shows its actual checklist status','Each cell shows its bounded input-checklist status'),
 ('function openDetail(ticker){let s=','function openDetail(ticker){state.detailTicker=ticker;let s=')])
edits('build_site.py',[
 ("'audited_mb_score','mb_input_coverage'","'input_audited_mb_score','mb_input_coverage'"),
 ("m.get('audit',{}).get('verified_mb_score')","m.get('audit',{}).get('input_audited_mb_score')")])
edits('evidence_tools/parse_panels.py',[
 ("v['capex_outflow']=-v['capex_signed'];v['fcf_calculated']=v['cfo']+v['capex_signed']", "v['capex_outflow']=-v['capex_signed'];v['fcf_calculated']=v['cfo']+v['capex_signed']\n   row['sources']['capex_outflow']={**row['sources'].get('capex_signed',{}),'kind':'derived_from_standardized_vendor','derivation':'Negate cash-flow capex sign to show a positive outflow; missing capex is not zero.'}\n   row['sources']['fcf_calculated']={'kind':'derived_from_standardized_vendor','url':row['sources'].get('cfo',{}).get('url'),'derivation':'CFO minus productive capex','components':[row['sources'].get('cfo',{}),row['sources'].get('capex_outflow',{})]}")])
edits('test_evidence_audit.py',[
 ("self.assertEqual(x['reviewed_within_scope'],14);self.assertFalse(x['full_six_pass_complete'])","self.assertEqual(x['input_audited'],13);self.assertEqual(x['full_research_verified'],0);self.assertFalse(x['full_six_pass_complete'])"),
 ("def test_no_signoff_on_critical_or_missing(self):", "def test_full_signoff_withheld_for_every_stock(self):\n  for s in self.rows.values():\n   self.assertIsNone(s['metadata']['audit']['verified_mb_score'])\n   self.assertFalse(s['metadata']['research']['full_research_validation_complete'])\n   self.assertTrue(s['metadata']['research_review_required'])\n def test_no_signoff_on_critical_or_missing(self):")])
# Documentation must reflect computed counts, not the old unexecuted claims.
edits('README.md',[
 ('**14/30 pass the stated input-audit checks; 22/30 have full MB numerical input weight.**','**13/30 pass the stated input-audit checks; 22/30 have full MB numerical input weight.**'),
 ('All 30 have computed screening scores, but the remaining 16 do not receive the\n`verified_mb_score` display field. That field means audit checks passed within the\ndisclosed scope, NOT a calibrated return forecast or an independently certified research opinion.','All 30 have computed screening scores; 17 retain explicit input/comparability gaps. The\n`input_audited_mb_score` field identifies 13 bounded input audits. The separate\n`verified_mb_score` remains null for all 30, and full six-pass completion remains false.\nComplete segment/KPI and guidance-history reconciliation, exhaustive index/ETF and peer\nreview, and the complete analyst-evidence/contradiction matrix remain outstanding.\nInput-check completion is not a calibrated return forecast or full research certification.')])
print('Recovered 9 complete source files, restored review notes, and applied assurance/UI corrections.')
