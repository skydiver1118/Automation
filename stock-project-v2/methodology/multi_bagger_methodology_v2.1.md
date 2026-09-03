# Multi Bagger Methodology v2.1 — Pass Scores and Persistence

## Purpose

This specification separates the investment outputs shown on the Multi Bagger dashboard from the evidence and domain assessments produced during the six-pass research process. The dated JSON snapshot is the system of record. CSV and Markdown files are derived artifacts.

## Single source of truth

The Multi-Bagger Skill is the required six-pass research workflow. `multi-bagger-v2.1` is the only official production scoring methodology until a formally versioned successor replaces it.

Rules:

1. There is exactly one official Multi Bagger Score for a ticker and snapshot: the score persisted by the production Multi Bagger scoring pipeline under the active `methodology_version`.
2. ChatGPT, Codex, notebooks, reports, and dashboard code must not invent, estimate, rescale, or publish an independent score labeled `Multi Bagger Score`, `MB Score`, `Expectation & Valuation Score`, `P(5x)`, or `Weekly Technical Score`.
3. A research analysis may contain qualitative assessments and pass findings before scoring, but these are explicitly non-official until processed by the active production methodology.
4. Every official score record must carry the active `methodology_version` and be persisted to the canonical dated JSON snapshot. The dashboard reads that canonical record; it does not recompute or override headline scores in the browser.
5. Cross-stock ranking is apples-to-apples only when the compared records use the same `methodology_version`. A methodology-version mismatch must be disclosed and must not be represented as a directly comparable ranking.
6. If a required production scorer, factor input, or evidence field is unavailable, the correct output is `unscored`/null with the missing requirement identified. Missing data must never be replaced by an ad-hoc numerical score.
7. A methodology upgrade must receive a new explicit version (for example `multi-bagger-v2.2`) and become the new authority in one central production configuration. Historical snapshots retain their original methodology version and are never silently rewritten.
8. The six-pass workflow and the headline scoring engine are separate layers: research creates auditable evidence; the production methodology turns eligible factor inputs into official scores.
9. Before a newly analyzed ticker is compared with the live Top-20, the production pipeline should validate its score record and, where practical, reproduce/validate at least one existing same-version benchmark record.
10. Any legacy dashboard headline score whose underlying factor worksheet was not captured remains valid as a historical legacy observation, but it must not be reverse-engineered into missing factor inputs or used to claim that a newly hand-scored ticker is directly comparable.

Operational flow:

```text
Multi-Bagger Skill (Passes 1–6)
        ↓
auditable factor/evidence inputs
        ↓
active production methodology (currently multi-bagger-v2.1)
        ↓
canonical dated JSON snapshot
        ↓
append-only history + dashboard + reports
```

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
