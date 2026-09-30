from pathlib import Path
from datetime import date
import json,sys,csv,hashlib
APP=Path(__file__).resolve().parents[2];sys.path.insert(0,str(APP))
from v22_pipeline import build_payload,canonical
source=APP/'monitoring/runs/2026-09-30T013246Z-weekly.json'
a=json.loads((APP/'v22/assumptions.json').read_text());c=json.loads((APP/'v22/calibration.json').read_text())
r=build_payload(json.loads(source.read_text()),a,c,as_of=date(2026,9,30),source_bytes=source.read_bytes())
# Reproducible dated review; live sidecar is separately built from monitoring/latest.json.
def cash(x):
 if x is None:return '—'
 return ('$'+f'{x/1e9:,.3f}'+'B') if abs(x)>=1e9 else '$'+f'{x/1e6:,.2f}'+'M'
def percent(x):return f'{x*100:.1f}%'
lines=['# Multi Bagger v2.2 — company scenario review','',
'**Information cutoff: September 29, 2026. Quotes: September 29 regular-session close. Company source review: September 29, 11:09 p.m. EDT (September 30, 03:09 UTC).**','',
'**32 company dispositions; 16 populated bear/base/bull scenario sets; 16 remain unscored because of critical inputs or model-perimeter gaps.** All existing members are retained. Action10/Candidates22 and the frozen business-screen calculator are unchanged.','',
'## How to read the results','',
'These are source-informed analyst hypotheses, not issuer forecasts, independent research certification, confidence intervals or calibrated probabilities. A 1.5× multiple means a hypothetical terminal share price 50% above the starting price, excluding dividends. The associated feasibility number is only a monotonic diagnostic of the base scenario. It is not a combined investment score and cannot automatically change list membership. No final v2.2 rank or P(5×) is claimed.','',
'Missing critical information is not set to zero. Company sources anchor reasoning but do not prove future margins, growth, multiples, dilution or capital access. Year-five revenue endpoints are converted to equivalent CAGR; this is not a claim that a transitioning company grows smoothly each year. Bear/bull are not the worst/best possible outcomes. Terminal P/E is applied after common-equity interest, tax, recurring stock compensation and non-common distributions; enterprise models subtract debt and non-common claims once. No dividends or spin-off value are silently counted.','',
'## Populated cases — no production reranking','',
'| Stock | Current list | Price | Reference cap | Bear × | Base × | Bull × | Stressed base × |',
'|---|---|---:|---:|---:|---:|---:|---:|']
for s in r['stocks']:
 if s['scenarios']:
  m=[s['scenarios'][n]['supportable_5y_multiple'] for n in ['bear','base','bull']]
  lines.append(f"| {s['ticker']} | {s['tier']} | ${s['price']:,.2f} | {cash(s['reference_market_cap'])} | {m[0]:.2f} | {m[1]:.2f} | {m[2]:.2f} | {s['stressed_base']['supportable_5y_multiple']:.2f} |")
lines+=['','The conservative stress reduces base revenue CAGR and normalized margin by 5 percentage points each, terminal valuation multiple by 20%, and adds 10 percentage points of cumulative dilution. It holds terminal debt unchanged; it is a transparent model-sensitivity test, not a complete stressed cash-flow projection. No parameters were optimized against subsequent stock returns.','',
'No base scenario reaches 5×. This is a result of the stated assumptions and starting prices, not proof that fivefold outcomes are impossible. CRMD and IREN reach 5× only in their demanding bull scenarios. Their tail upside does not establish the probability, risk-adjusted attractiveness or best entry timing.','',
'## Unscored — critical information and next decision','',
'| Stock | Reason | Next evidence |','|---|---|---|']
for s in r['stocks']:
 if not s['scenarios']:
  rv=s.get('company_review') or {}
  gaps=rv.get('critical_gaps') or s['critical_reasons']
  lines.append('| '+s['ticker']+' | '+'; '.join(gaps).replace('|','/')+' | '+rv.get('next_review_trigger','Research required').replace('|','/')+' |')
lines+=['','A hold may mean that this research record has not reconciled publicly available information; it does not accuse an issuer of failing to disclose data. For MU and LITE, current filings were located but the required reviewed quality/capitalization ledger has not been completed. For ETN and NBIS, additional transaction/share-count complications were identified and are not assumed away.','',
'## Company-by-company evidence and assumptions','']
for s in r['stocks']:
 rv=s.get('company_review') or {};defs=s.get('scenario_assumptions')
 lines+=['### '+s['ticker']+' — '+('scenarios populated' if s['scenarios'] else 'missing critical data; unscored'),'',
'**Reported evidence:** '+rv.get('facts','See linked sources.'),'',
'**Growth rationale:** '+rv.get('growth_rationale','No supportable growth model completed.'),'',
'**Normalized economics:** '+rv.get('normalized_economics','See critical gaps.'),'',
'**Financing / dilution:** '+rv.get('funding_assessment','Not reconciled.'),'',
'**Main risk:** '+rv.get('risk','See warnings.'),'',
'**Next review trigger:** '+rv.get('next_review_trigger','Research needed.')+' **Scheduled review:** '+rv.get('next_review_due','Not set')+'.','']
 if s['scenarios']:
  lines+=['| Case | Revenue in year 5 | Equivalent revenue CAGR | Normalized margin | Terminal valuation | Cumulative dilution | Per-share multiple |',
  '|---|---:|---:|---:|---:|---:|---:|']
  for name in ['bear','base','bull']:
   case=defs['scenarios'][name];v=case['inputs'];ev=defs['model']=='enterprise_ebitda';out=s['scenarios'][name]
   lines.append(f"| {name} | {cash(case['revenue_year5_usd'])} | {percent(v['revenue_cagr'])} | {percent(v['ebitda_margin'] if ev else v['net_margin'])} {'EBITDA' if ev else 'common net'} | {v['terminal_ev_ebitda'] if ev else v['terminal_pe']:.1f}× {'EV/EBITDA' if ev else 'P/E'} | {percent(v['dilution_5y'])} | {out['supportable_5y_multiple']:.2f}× |")
  if defs['model']=='enterprise_ebitda':
   lines+=['','**Enterprise funding bridge: conditional forecasts, not committed financing.**','',
   '| Case | Starting net debt | 5Y capex | 5Y CFO | New common cash | Other funding uses | Terminal net debt | Other capital claims |',
   '|---|---:|---:|---:|---:|---:|---:|---:|']
   for name in ['bear','base','bull']:
    case=defs['scenarios'][name];b=case['funding_bridge'];v=case['inputs'];claims=sum(v[k] for k in ('preferred_claims_5y','minority_claims_5y','other_claims_5y'))
    lines.append('| '+name+' | '+' | '.join(cash(b[k]) for k in ('starting_net_debt','capex_5y','cfo_5y','new_common_cash_5y','other_funding_uses_5y','terminal_net_debt'))+' | '+cash(claims)+' |')
  rr=s.get('scenario_financial_resolution') or {}
  if rr.get('financial_overrides'):lines+=['','**v2.2-only correction:** '+rr['override_rationale']+' Historical v1 scores and their input ledger are not rewritten.','']
 else:
  lines+=['**Critical gaps:** '+'; '.join(rv.get('critical_gaps') or s['critical_reasons']), '']
 for sid,src in rv.get('sources',{}).items():
  lines.append('- ['+sid+']('+src['url']+') — '+src['as_of']+'; '+src.get('kind','source'))
 lines+=['']
lines+=['## Historical calibration: explicit unresolved prerequisite','',
'The authorized specification requires a point-in-time security universe, as-filed formation-date fundamentals, failed/delisted securities, verified five-year total returns, and a chronological untouched out-of-sample comparison. Those data are not present in the accessible research archive. Six public access probes were actually executed: SEC ticker/submission/index/financial-data endpoints returned HTTP 403; SHARADAR fundamentals and price requests returned API-key-required errors. The successful current-company collection is not a successful historical-calibration run.','',
'The audited access receipts are in `calibration_access_checks.json`. No licence was purchased and no security setting or credential was changed. All statistical adoption checks remain false. The current 32 survivors are not substituted for a historical point-in-time sample. Software correctness tests and the conservative scenario stress do not establish empirical investment performance.','',
'## Refresh and preservation','',
'Price updates recalculate scenario per-share multiples using the same documented assumptions. New financial periods, economic share counts, or previously unreviewed filing triggers invalidate the scenario resolution. Every assumption set has an expiration date and a financial dependency hash. The exact current review resolves only the recorded source queue, not future disclosures. Existing critical-data holds remain binding. Historical records, Action membership, the business-screen calculator and Stock Project V2 are untouched.','',
'An integrated column in the main Multi Bagger page now shows bear/base/bull results or the critical gap; the detailed v2.2 view supplies assumptions, source links, correction bridges, and financing budgets. A webpage reload never certifies new research.','',
'**Source monitoring SHA256:** `'+r['source_snapshot_sha256']+'`','**Assumptions SHA256:** `'+r['assumptions_sha256']+'`','']
report=APP/'v22/research/company_review_report.md';report.write_text('\n'.join(lines))
(App:=APP/'v22/research/company_review_summary.json').write_bytes(canonical({'information_cutoff':'2026-09-29','source_snapshot_sha256':r['source_snapshot_sha256'],'counts':r['counts'],'production_rank_effect':False,'calibration':'blocked_not_calibrated','source_documents_retrieved':94}))
# Store a frozen release copy for immutable regression tests and reproducibility.
(APP/'v22/research/scenario_release_2026-09-29.json').write_bytes(canonical(a))
print(r['counts'])
print('Report words:',len(report.read_text().split()))
