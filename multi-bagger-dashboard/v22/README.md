# Multi Bagger v2.2 — integrated 5× feasibility shadow layer

**Status: Shadow / uncalibrated. Production ranking is NOT migrated.**

This implements the approved September 24 v2.2 specification in
`stock-project-v2/methodology/multi_bagger_methodology_v2.2.md` without replacing
`MB25_RESEARCH_V1_20260906`, changing its calculator, assigning probabilities,
or changing Action/Candidate membership. The visible v1 quality value is the
existing research score, never an independently certified score.

## What is live

The Action dashboard links to `./v22/`. Every current member, including new,
unreviewed Candidates, has a row. All available stock prices retain their actual
market dates. A failed market catch-up retains the last good snapshot and shows
an explicit failure/date warning; quotes beyond four calendar days cannot
produce a new scenario score. A page build is not a quote refresh or a new research review.

The page displays reference market cap, required no-dilution 5× equity value,
quality score (v1), reviewed scenario feasibility where available, detailed
missing-data reasons, reverse-valuation sensitivities, and calibration status.
The final v2.2 score, P(5×), and v2.2 rank stay null. No list re-normalization or
arbitrary large-cap exclusion is introduced.

**Initial scenario coverage:** No approved company-specific, source-linked
bear/base/bull records were found in the repository. `assumptions.json` starts
with no reviewed records. It does not turn one-year consensus into five-year
growth, treat incomplete capital claims as zero, or reuse a chat illustration
as an approved valuation. Therefore a numerical feasibility score remains
withheld for each company until its required scenario evidence is supplied.
The reverse-valuation view is useful immediately without pretending that a
hypothetical requirement is a forecast.

## Math and a correction to the original prototype

Horizon is five years. Cumulative dilution `d` is fractional economic-share
change, so `d=0.20` means 20% more shares, NOT 20% every year.

- No-dilution 5× market-cap hurdle: `5 * current_cap`.
- Actual future equity needed for a 5× share-price outcome:
  `5 * current_cap * (1 + d)`.
- Required incremental future equity: that amount minus current cap.
- Equity-P/E scenario: `revenue5 * normalized_common_net_margin * terminal_PE`.
- Enterprise scenario: `revenue5 * normalized_EBITDA_margin * EV_EBITDA`,
  minus net debt, preferred, minority and other non-common claims.
- Per-share supportable multiple: future common equity divided by
  `current_cap * (1+d)`.
- Feasibility gap: supportable multiple / 5; a gap of 1 means the scenario
  reaches 5×, not that the outcome is certain.

The prototype incorrectly permitted subtracting net debt from a P/E-derived
**equity** value. v2.2.1 rejects nonzero debt on that route; the separately
identified enterprise route deducts capital claims once. It also distinguishes
actual future company equity from its current-share-equivalent value. The
original no-dilution output key is retained for compatibility and labelled.

The original diagnostic mapping is unchanged: multiples 1/1.5/2/3/4/5/7 map to
0/15/30/50/70/85/100 with clipped linear interpolation. **85 does not mean an 85%
probability of 5×.** Inputs that overflow or imply invalid growth, margin,
capitalization, dilution or inconsistent bear/base/bull outcomes are rejected.

## Scenario evidence contract

Each record under `assumptions.json.records.TICKER` requires:

- `review_status: reviewed`, timezone-aware `reviewed_at`, dated `valid_through`.
- `model: equity_pe` or `enterprise_ebitda`, plus `model_rationale` and
  `funding_assessment`; a development-stage reactor or finance company cannot
  be passed through the ordinary operating model just to generate a score.
- `financial_basis_sha256` matching the fingerprint shown in the stock detail.
  Changes to reviewed revenue, period, cash/debt/claims/dilution basis or review
  date invalidate old assumptions. Market-price changes alone do not do so.
- `sources`: source-ID objects containing a HTTPS `url` and `as_of` date.
- `scenarios.bear/base/bull`, each with a label, explicit numeric `inputs`, and
  `assumption_evidence` for **every** required field. Evidence includes a written
  rationale and valid `source_ids`. A source supports the judgment; it does not
  make the assumption a reported fact.

Equity inputs: revenue CAGR, common net margin, terminal P/E, cumulative dilution.
Enterprise inputs: revenue CAGR, EBITDA margin, terminal EV/EBITDA, dilution,
terminal net debt, preferred, minority and other claims. Documented zeros are
allowed; omitted claims and dilution are not silently set to zero.

Existing critical-data holds and new source-review triggers continue to block
scenario scoring even with an otherwise complete scenario record. Expired,
draft, mismatched or unsupported-model records remain unscored with reasons.

## Reverse requirements are NOT analyst scenarios

The detail panel provides 27 precomputed combinations: cumulative dilution of
0/20/50%, common net margins of 10/20/30%, and terminal P/E of 15/20/30×. These
are explicitly hypothetical sensitivities, not company-specific bear/base/bull
estimates. They show the equity, annual net income, revenue and five-year CAGR
needed to achieve a 5× share-price outcome. Missing trailing revenue means no
CAGR; missing market capitalization means no reverse bridge. Technical scores
remain separate. Neither view produces a buy entry or trades.

## Persistence and refresh

`v22_pipeline.py` creates a separate immutable sidecar under
`monitoring/v22/runs/<content-key>.json`, plus latest and history pointers.
The key binds the actual monitoring bytes, assumptions, calibration record,
engine, adapter and evaluation date. Repeating identical inputs is idempotent;
a conflicting overwrite fails. Each sidecar records its source run and hashes.

`build_site.py` automatically builds this sidecar on existing daily, weekly,
Candidate-intake and code-publication paths. The existing monitoring commit
step persists it on data refreshes. Only `/multi-bagger/v22/` and its navigation
link are added to the website. Stock Project V2 and other sibling sites remain
separate. Old monitoring and original 20/25-stock histories are not rewritten.

## Validation, safety and remaining work

Python tests exercise arithmetic, dilution, double-count prevention, zero versus
missing, sensitivity, source dependencies, invalid inputs, Critical Data holds,
calendar-independent fixtures, preservation, archive idempotency and dynamic
membership. Browser tests cover desktop/mobile, filters, detail/reverse
sensitivity, historical sidecars, data-fetch failure and deployment hashes.
The public verifier checks the actual v2.2 artifact, not a timestamp alone.

**Calibration is still blocked.** The known SEC cohort collector failed; no
point-in-time, survivorship-safe, delisting-adjusted out-of-sample calibration
has passed. A configuration flag cannot enable production scores: the adapter
rejects it and always emits null for final v2.2 score/P(5×)/rank. Scenario math
uses terminal share-price multiples excluding dividends; calibration requires
verified total returns. There is no claim these are interchangeable.

## Rendering design

One lightweight table with mobile cards; no streaming graph or external chart
library. At 32 members, at most one detail dialog is open. Small JSON is loaded
once; filters work locally, and reverse sensitivities select Python-computed
values rather than duplicating valuation formulas in JavaScript. Fetches use
no-store plus cache-busting. A failed reload preserves the last loaded display
with an explicit error, never calls it fresh, and never changes investment
state. A source/build hash mismatch blocks the new display. Keyboard controls,
44px touch targets, dark mode and visible source dates are supported.
