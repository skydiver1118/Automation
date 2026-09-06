# Multi Bagger — Action 10 + Candidate Bench

Published path remains `/Automation/multi-bagger/`. Stock Project V2's universe,
engine, dashboard and workflow are separate and are not changed by these jobs.

## User-approved membership

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
