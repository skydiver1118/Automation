# Multi Bagger — Action 10 + Candidate Bench

Published path remains `/Automation/multi-bagger/`. Stock Project V2's universe,
engine, dashboard and workflow are separate and are not changed by these jobs.

## September 6 source-evidence repair

Current Action10 is selected only from stocks passing all stated input-audit checklists,
with 100% MB numerical input-weight coverage and no critical unresolved warning:
**ETN, ZETA, HUBB, CRMD, AXTI, KTOS, AVAV, EVLV, BKSY, AMPX**.
AVAV/BKSY/AMPX replace FIGR/VST/RKLB for daily attention. All 30 are retained.
This one-time reassignment was explicitly authorized by the user. Later automated
refreshes still cannot change membership, and all future intake remains Candidate-first.

The `evidence_audit/2026-09-06/` archive now supplies 30 eight-factor scorecards,
eight dated financial periods per stock (missing/vendor-allocated observations flagged),
245 retrieved filed-document references, explicit input derivations, sources, corrections,
forecast panels, risk/catalyst records, and six checklist records per stock.
**13/30 pass the stated input-audit checks; 22/30 have full MB numerical input weight.**
All 30 have computed screening scores; 17 retain explicit input/comparability gaps. The
`input_audited_mb_score` field identifies 13 bounded input audits. The separate
`verified_mb_score` remains null for all 30, and full six-pass completion remains false.
Complete segment/KPI and guidance-history reconciliation, exhaustive index/ETF and peer
review, and the complete analyst-evidence/contradiction matrix remain outstanding.
Input-check completion is not a calibrated return forecast or full research certification.

The eight-factor calculator and absolute score mappings are unchanged. The six stages
are research checklists, not six numerical grades. UI status cells show checks passed,
source detail, dates, and outstanding items. Every historical financial cell distinguishes
filed, derived, standardized-vendor, or missing evidence. The full historical panel is
not represented as independently primary-verified when vendor observations remain.

`evidence_gate.py` derives confidence from evidence state, NOT ticker-specific defaults,
and withdraws a prior sign-off when new filings, changed financial dependencies,
unavailable consensus or stale prices require review. Daily prices/estimates may
recalculate a screen but never rewrite or redate the immutable source audit.
The dated audit and live overlay remain separate; missing information never becomes zero.

On mobile, the six-pass matrix becomes readable two-column checklist cards. Ticker
views include the eight-quarter table, score contribution math, TTM bridge, consensus
panel, primary-document inventory, counter-thesis and warnings. Current CSV/report
exports carry the evidence status and missingness warnings, not just an unlabeled score.

Reconstruction tooling is in `evidence_tools/`. Run the dated builder only with the
retained source archives in directories `new30`, `edgar`, `supplement`, `final_gaps`
under the `MB_EVIDENCE_ROOT` environment path. It refuses to overwrite a dated audit.
Subsequent repairs require a new version/date rather than silently editing this archive.
The published numeric evidence and the monitoring snapshot retain enough input
information to independently reproduce the eight-factor score without vendor access.

The original implementation notes below describe the pre-audit initial membership;
they are preserved as history, not a second current membership source.

## Original user-approved membership (historical initial state)

`watchlist_registry.json` is the sole membership source of truth. Initially:

- Action10, selected by the previous common-calibration research ranking:
  ETN, ZETA, HUBB, VST, FIGR, CRMD, AXTI, KTOS, EVLV, RKLB.
- Candidates20: remaining 15 former Final25 names, plus RGTI, QBTS, OKLO, SMR, EOSE.
- No former member was deleted. The four photo biotech candidates are excluded.
- Every future stock MUST enter Candidates first. No score/rank can promote it automatically.
- Action is a daily-research attention tier, NOT a BUY signal or a portfolio allocation.
- FIGR and other provisional-data flags remain visible. Initial selection is an explicit
  membership migration, not a claim that every member satisfies all future promotion gates.

The old `final_list.json` is archived at `research/2026-09-06/final25_registry.json`.
A public compatibility `final_list.json` is generated at build time from the registry;
it is never an input or a competing membership file.

## Cadence

`multi-bagger-refresh.yml` schedules Action refresh at 08:00 America/New_York on
weekdays and the Candidate/common-date comparison at 09:00 Saturday in that timezone.
GitHub schedules are best effort and may be delayed; display actual completion time.

Daily: refresh price, cap bridge, estimates and technical calculations for Action only;
scan SEC filing metadata for all names, without relabeling weekly candidate scores as daily.
Weekly: refresh both tiers with a common completed regular-session price cutoff;
produce a promotion/demotion queue. Neither job edits registry membership.

NYSE and Nasdaq calendar agreement is required for daily runs; weekends and full-day
holidays skip data refresh, publishing and digest silently. Known adhoc closures are in
the calendars; newly announced closures can be added to `market_closures.json`.
Calendar/validation failure fails closed. Early-close sessions are trading days.
Completed-session data only: no intraday candles are mixed into an 8am run.
Manual structure changes/rebuilds can publish on weekends without pretending a market
session occurred. No scheduled email is sent for those changes.

## Actual research scope — important

The exact saved `research_scoring.py` remains unchanged, guarded by its registry SHA256.
Both tiers use the same absolute anchors/weights, never separately normalized scores.
Research MB, E&V and technical scores are NOT the older unverified official scores or
calibrated fivefold-return probabilities. Missing inputs remain missing, not zero.

Automation refreshes market and consensus inputs. It does NOT pretend to perform a
new eight-quarter reconstruction, read every new filing, or certify all six passes.
Previously reviewed statements, capital-claims bridge and analyst grades retain their
actual review timestamp. New financial periods, share-count changes, missing estimates
or new material-form SEC inventory create research holds. The dashboard displays those
holds and keeps last known good data if retrieval fails. SEC metadata is an event trigger,
not a substitute for a primary-source filing review. Old statements are not relabeled current.

For paired economic classes, financing, restricted cash and acquisition effects, retain
reviewed financial bridges rather than silently replacing them with generic vendor fields.
If shares change more than 5%, flag review and identify the retained-share estimate.

## Promotion policy

Weekly comparisons require common market dates, >=90% numerical coverage, fully cleared
research for both sides, cleared candidate blocker, comparable valuation coverage,
>=5 MB point advantage for two distinct consecutive weekly reviews, and sensitivity
support under both growth and quality weights. A 28-day post-swap cooldown applies.
At most two non-overlapping swaps can be recommended; none is required. Repeated runs
within one week never count as additional weeks. Rank is within each tier between reviews.

No auto-swaps and no broker orders. `full_research_reviewed_at` and
`promotion_blocker_cleared` are explicit human-review fields, not populated by a market scan.
The existing incomplete research still blocks promotion. Changes can be made only through
a recorded user approval. Watchlist demotion is not a sell instruction.

## Candidate intake

Use the `Add Multi Bagger Candidate` GitHub Actions workflow (ticker + reason), or:

```bash
python multi-bagger-dashboard/watchlist.py add TICKER --reason 'Why it merits research'
```

The command accepts no tier argument. Duplicate tickers fail, and an unknown company
appears with blank MB/E&V until real research is supplied. Intake persists an immutable
membership snapshot. Do not hand-edit a registry without appending the corresponding snapshot;
publish validation rejects registry/snapshot mismatch.

Approved swap only:

```bash
python multi-bagger-dashboard/watchlist.py swap --promote CANDIDATE --demote ACTION \
  --approval-ref 'user-request-or-approved-review-reference' --reason 'Specific evidence'
```

## Storage and display

- `monitoring/latest.json`: last successful monitoring/membership state.
- `monitoring/runs/<timestamp>-<kind>.json`: immutable monitoring snapshots with tier,
  score, source dates, raw model inputs, six-pass gaps and event/review information.
- `monitoring/history.json`: monitoring snapshot manifest.
- `research/candidate_seed_2026-09-06.json`: source-reconciled photo candidate seed.
- Previous 20/25 research snapshots remain immutable in their original `stock-project-v2/data/multi_bagger/` archive.

Builder produces separate current/history CSV and report downloads from monitoring data.
The history selector includes both the new monitoring states and original 20/25 archives.
Every price shows its actual market date. Date/hour/minute/timezone are visible for builds
and runs. Action defaults to 10 rows; Candidates shows the separate bench with blockers
and next-review triggers. Mobile shows the same members as stock cards. No verified setup
can be a valid Today’s Opportunities result: a legacy range hit alone is never BUY.

## Notifications and safety

After successful scheduled DAILY publishing only, a changes-only digest uses existing
`STOCK_EMAIL_TO`, `STOCK_EMAIL_USERNAME`, `STOCK_EMAIL_APP_PASSWORD` repository secrets.
No secrets are committed or logged. Missing mail secrets leave the dashboard as the
notification surface. Weekly results are available in the dashboard and next trading-day digest.
A static site rebuild is not a research refresh. Deployment success and data freshness
are separate facts. Shared Pages write lock and `destination_dir: multi-bagger` preserve
all sibling dashboards.

## Validation

```bash
python -m unittest discover -s multi-bagger-dashboard -p 'test_*.py' -v
python -m unittest discover -s stock-project-v2/tests -p 'test_multibagger_pass_score_storage.py' -v
python multi-bagger-dashboard/build_site.py --output .multi-bagger-pages
node --check .multi-bagger-pages/app.syntax-check.js
```

Tests cover intake, cap, approval, holiday silence, early closes, DST, closure override,
fail-closed behavior, numerical reconciliation, stale-comparison gates and immutable history.
The old `build_final25.py` is blocked from replacing the current membership structure.
