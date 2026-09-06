# Multi Bagger Final 25

Published independently at `https://skydiver1118.github.io/Automation/multi-bagger/`.
Stock Project V2 remains at `/Automation/stock-project-v2/`; neither its universe nor scoring is changed.

## Final membership

`final_list.json` is the authoritative **25-member** registry. The five approved additions are KTOS, AVAV, HUBB, VST and ETN. All previous 20 members remain. No future refresh may silently truncate to 20 or overwrite this registry without an explicit membership change.

## Score integrity

The displayed September 6 run uses **MB25_RESEARCH_V1_20260906**, the same common research calibration for all 25. `research_scoring.py` is the only calculator for those research outputs. Its inputs, analyst grades, methodology, source links and arithmetic checks are versioned under `research/2026-09-06/`.

This publishes research results; it does **not** certify an official investment scoring model. Archived official MB/E&V mappings could not be reproduced. Official fields and P(5x) are deliberately null in the new snapshot; separately named research fields are displayed. Old September 3 and September 4 scores remain intact and are accessible through the history selector. Cross-calibration score/rank deltas are null, not zero. E&V with 70% coverage is valuation-only. POET has 70% MB input-weight coverage. Six-pass partial work is not marked complete.

## Information shown

Ticker then closing price, market capitalization, sector and sector-trend judgment, three research scores, coverage/confidence, preferred entry status, action and thesis. Ticker details include financial bridges, next-fiscal-year expectations, share changes, moving averages/RSI/MACD/ADX/ATR/volume/returns, technical reference levels, factor scores, sensitivity, ETF weights and benchmark index associations, prior archive and source links.

ETF exposure was checked in IVV, IWB, IWM, IJH and ITA using primary September 3 holdings files. It is not an exhaustive direct index roster. New stocks have no invented fundamental entry zones or P(5x) estimates. Legacy preferred ranges are identified as not revalued.

## Time and refresh semantics

Research/market data: September 4 closing session; collection completed September 6 at 09:22 Eastern. The saved watchlist-recording time and actual dashboard-build time are separate and display date, hour, minute and EDT/EST. This explicit user-requested Sunday membership rebuild is not a scheduled closed-market research refresh. No holiday email was sent.

`build_site.py` validates and rebuilds the site from saved evidence; it does not falsely label that operation a fresh full SEC study. New research refreshes must supply current source evidence, the complete final-list universe and one verified scoring calibration. The publication gate rejects a stale 20-stock payload or inconsistent research scores. The current frozen calibration is intentionally fail-closed; a future research calibration needs a versioned input/validator update, not an unlabelled mix of methods.

## Archive and deployment

Canonical snapshot/history remains in `stock-project-v2/data/multi_bagger/` for backward compatibility, isolated from Stock V2 score data. `2026-09-06.json` is a new `research_rerun` snapshot: 25 rows added to the prior 40-row archive. The research-score CSV has separately named columns so historical official numbers cannot be mistaken for the new calibration.

Publish workflow stages only `/multi-bagger/`, uses `keep_files: true`, and shares the existing Pages concurrency group. It never runs the Stock V2 ranking generator.

Validation: `python -m unittest discover -s multi-bagger-dashboard -p 'test_*.py' -v`; build: `python multi-bagger-dashboard/build_site.py`.
