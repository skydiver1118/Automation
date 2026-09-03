# Multi-Bagger Skill — Production Contract

## Scope

Use this workflow whenever a ticker is analyzed for the Multi Bagger dashboard or compared with an existing Multi Bagger ranking.

## Required research passes

1. **Primary-source inventory** — latest 10-K/20-F, 10-Q/6-K, material 8-K, earnings release, investor presentation, and recent company disclosures.
2. **Financial reconstruction** — at least eight quarters of revenue/growth, margins, earnings/FCF, balance sheet, share count/dilution, segment mix, and relevant KPIs.
3. **Forward expectations** — guidance history, consensus/revisions, backlog/ARR/contracts, revenue timing, market-implied expectations, and valuation.
4. **Risk / moat / sector** — competition, technology, customer concentration, financing, regulatory/geopolitical risks, sector trend, and index/ETF membership.
5. **Technical review** — price trend, 20/50/200-DMA, RSI, MACD, ADX, volume/relative strength, support/resistance, and entry zones.
6. **Contradiction / adversarial audit** — actively search for evidence that could invalidate or materially weaken the thesis and reconcile discrepancies among filings, company claims, consensus, and prior dashboard records.

## Single-source-of-truth scoring rule

The research workflow does **not** create its own headline score. After the six passes, eligible inputs must be processed by the active production Multi Bagger methodology. The active version is currently `multi-bagger-v2.1`.

Only scores persisted by the production pipeline under the active methodology version may be labeled as official `MB Score`, `E&V Score`, `P(5x)`, or `Weekly Technical Score`.

If the production scorer or a required input is unavailable, report the ticker as **UNSCORED** and identify the missing dependency. Never estimate or hand-create a substitute numerical MB score.

## Comparability rule

Stocks may be ranked directly against one another only when their official records use the same methodology version. If versions differ, either re-score them under the current production version or show them separately.

## Required output for a scored ticker

- ticker and snapshot date
- methodology version
- MB Score
- E&V Score
- P(5x)
- Weekly Technical Score
- confidence/evidence quality
- action
- entry zone
- six-pass completion/evidence status
- adversarial-audit conclusion

## Authority chain

```text
Six-pass research
  -> production methodology
  -> canonical dated JSON
  -> append-only history
  -> dashboard/report/chat presentation
```

The canonical dated JSON is the system of record. Dashboard, ChatGPT, Codex, and other consumers must display that record rather than independently recomputing headline scores.
