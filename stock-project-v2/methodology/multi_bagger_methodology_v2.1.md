# Multi Bagger Methodology v2.1 — Pass Scores and Persistence

## Purpose

This specification separates the investment outputs shown on the Multi Bagger dashboard from the evidence and domain assessments produced during the six-pass research process. The dated JSON snapshot is the system of record. CSV and Markdown files are derived artifacts.

## Headline outputs

The following dashboard values remain distinct from the six pass records:

- **Multi Bagger Score (0–100):** long-term 5–10x asymmetry and business-quality assessment. The standing factor weights are TAM 15, revenue/backlog/ARR trajectory 15, unit economics/profitability/FCF 10, balance sheet/runway 10, dilution/capital allocation 10, moat 15, management execution 10, and valuation/starting market cap 15.
- **Expectation & Valuation Score (0–100):** forward expectations, estimate revisions, revenue timing, valuation, and market-implied hurdle assessment.
- **Weekly Technical Analysis Score (0–100):** timing overlay. Its components are trend and 20/50/200-DMA alignment 30%, RSI/MACD/ADX momentum 20%, volume/accumulation/relative strength 20%, support/resistance and risk/reward 20%, and near-term catalyst/price confirmation 10%.

The headline scores are not computed by averaging Passes 1–6. Any future aggregation formula requires a new methodology version.

## Six-pass records

Each pass stores an assessment score, completion percentage, status, confidence, source IDs, findings, and missing fields.

| Pass | Stored assessment |
|---|---|
| 1. Primary-source inventory | Quality and sufficiency of primary-source coverage, including current SEC filings and company disclosures. |
| 2. Financial reconstruction | Revenue trajectory, margins, earnings/FCF, balance sheet, dilution, segment mix, and KPI quality. |
| 3. Forward expectations | Guidance, consensus/revisions, backlog/ARR/contracts, revenue timing, market-implied expectations, and valuation. |
| 4. Risk/moat/sector review | Competition, technology, customer concentration, financing, regulatory/geopolitical risk, sector trend, and index/ETF exposure. |
| 5. Technical review | Weekly Technical Analysis Score. When present, this score must equal the stock-level `weekly_technical_score`. |
| 6. Adversarial audit | Thesis resilience after searching for contradictory evidence and reconciling discrepancies among filings, company claims, estimates, and prior dashboard records. |

`completion_pct` measures evidence coverage and process completion; it is not an investment score. Missing evidence must never be converted to a score of zero.

## Pass status semantics

- `complete`: score is present and `completion_pct` is 100.
- `partial`: work is usable but incomplete; missing fields must be disclosed when material.
- `incomplete`: score is null and missing fields are listed.
- `not_applicable`: score is null because the pass does not apply.
- `legacy_not_captured`: a prior dashboard did not preserve that pass score or structured record.
- `legacy_score_only`: a prior dashboard preserved the final score but not the underlying components or completion evidence.

Production refreshes should invoke the storage command with `--require-complete`. Legacy imports are permitted without this flag and remain visibly distinguishable from fully auditable records.

## Storage contract

```text
data/multi_bagger/
├── pass_scores/
│   ├── YYYY-MM-DD.json
│   ├── YYYY-MM-DD-r2.json       # explicit same-date correction, when needed
│   └── latest.json
├── history/
│   └── pass_score_history.csv
├── evidence/
│   ├── YYYY-MM-DD.json
│   └── YYYY-MM-DD-r2.json
└── schemas/
    ├── pass_scores.schema.json
    └── evidence_manifest.schema.json

reports/multi_bagger/
├── YYYY-MM-DD.md
└── YYYY-MM-DD-r2.md
```

Rules:

1. A dated JSON snapshot is immutable. An identical replay is idempotent; conflicting content is rejected.
2. A same-date correction uses `snapshot_revision: 2` or higher and records the corrected field, prior value, corrected value, and reason.
3. `latest.json` points to the newest run date and revision. Backfilling an older snapshot does not move the pointer backward.
4. `pass_score_history.csv` has one row per `(snapshot_id, ticker)` and is derived from the dated JSON files.
5. Every pass `source_id` must resolve to the matching evidence manifest.
6. Event date, market-session date, generation timestamp, recording timestamp, and methodology version are separate fields.
7. Market capitalization is stored as integer U.S. dollars plus the human-readable dashboard value.
8. The action, thesis status, entry-zone status, corrections, Top-20 additions/removals, and index/ETF changes are persisted with each run.

## Commands

Persist a regular six-pass refresh:

```bash
python stock-project-v2/scripts/store_multibagger_pass_scores.py \
  path/to/pass_scores.json \
  --evidence path/to/evidence.json \
  --project-root stock-project-v2 \
  --require-complete
```

Validate without writing:

```bash
python stock-project-v2/scripts/store_multibagger_pass_scores.py \
  path/to/pass_scores.json \
  --evidence path/to/evidence.json \
  --project-root stock-project-v2 \
  --require-complete \
  --dry-run
```

Verify the complete repository history:

```bash
python stock-project-v2/scripts/store_multibagger_pass_scores.py \
  --project-root stock-project-v2 \
  --verify-repository
```

The repository verifier reconciles all dated snapshots against the CSV, verifies evidence references, checks generated reports, and confirms that `latest.json` matches the newest dated snapshot.
