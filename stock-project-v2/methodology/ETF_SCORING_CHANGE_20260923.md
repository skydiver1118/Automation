# Leveraged-ETF scoring change — 2026-09-23

User-requested methodology change: set `etf_scoring.leveraged_long_term_penalty`
from 15 to 0 for all leveraged ETFs. The production configuration remains the
single source of truth. Scoring version: `2.3-no-leverage-penalty`.

ETF Long-Term Score is now 45% relative strength + 30% technical + 25% trend/risk,
without a fixed leverage deduction. The short-term formula is unchanged. The
ETF composite score continues to use the recalculated long-term score at its
existing 35% weight; its other weights are unchanged.

SOXL remains identified as a 3x leveraged ETF. This scoring change does not
remove leverage/compounding warnings, imply reduced investment risk, or bypass
the options dashboard's BUY/STRONG BUY ownership gate or execution checks.
The option dashboard must consume the recomputed Stock V2 canonical ratings;
it must not add 15 locally or force any security to SELL.

Recompute the full configured universe using the latest completed session,
materialize decisions, rebuild the canonical layer, and publish Stock V2 before
refreshing the options dashboard. Existing fingerprint invalidation and
same-session history revision archiving remain enabled. Historical snapshots
from earlier sessions are not retroactively restated by this change.

Regression tests in `tests/test_normalization.py` verify a zero production
penalty, retained SOXL leverage metadata, equal scores for ETFs with identical
market inputs, and unchanged non-leveraged ETF/stock scores on fixed inputs.
