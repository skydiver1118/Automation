# Independent Nasdaq-100 Top-1 Monthly Skip-Momentum Validation

Rules replicated: current Nasdaq-100 price file, top 1 stock, monthly rebalance, score = Close[t-21 trading days] / Close[t-126 trading days] - 1, signal after the prior month-end close, execute at the next trading day open.

No-lookahead guard: every row requires the signal close, skipped score close, and lookback close to be dated before the trade open. Completed months are measured open-to-open; the final partial month is valued from entry open to the latest available close.

- Window: 2025-01-01 through 2026-05-15
- Rows: 17
- Actions: BUY 1, SWITCH 3, HOLD 13
- Total return: 1005.28%
- Final equity: 11.052753x
- Reconciliation difference: 0.000000000000
- No-lookahead checks: OK
- PDF decision sequence match: YES

| Month | Signal | Trade | Selected | Action | Score Close | Lookback Close | Return | Equity |
| --- | --- | --- | --- | --- | --- | --- | ---: | ---: |
| 2025-01 | 2024-12-31 | 2025-01-02 | APP | BUY | 2024-11-29 | 2024-07-02 | 6.78% | 1.067813 |
| 2025-02 | 2025-01-31 | 2025-02-03 | APP | HOLD | 2024-12-30 | 2024-07-31 | -0.93% | 1.057935 |
| 2025-03 | 2025-02-28 | 2025-03-03 | APP | HOLD | 2025-01-29 | 2024-08-27 | -24.56% | 0.798103 |
| 2025-04 | 2025-03-31 | 2025-04-01 | APP | HOLD | 2025-02-28 | 2024-09-26 | 6.73% | 0.851809 |
| 2025-05 | 2025-04-30 | 2025-05-01 | PLTR | SWITCH | 2025-03-31 | 2024-10-25 | 9.49% | 0.932669 |
| 2025-06 | 2025-05-30 | 2025-06-02 | PLTR | HOLD | 2025-04-30 | 2024-11-25 | 2.92% | 0.959882 |
| 2025-07 | 2025-06-30 | 2025-07-01 | PLTR | HOLD | 2025-05-29 | 2024-12-24 | 14.62% | 1.100242 |
| 2025-08 | 2025-07-31 | 2025-08-01 | PLTR | HOLD | 2025-07-01 | 2025-01-29 | -2.48% | 1.072922 |
| 2025-09 | 2025-08-29 | 2025-09-02 | PLTR | HOLD | 2025-07-31 | 2025-02-28 | 19.92% | 1.286655 |
| 2025-10 | 2025-09-30 | 2025-10-01 | WDC | SWITCH | 2025-08-29 | 2025-03-31 | 28.68% | 1.655624 |
| 2025-11 | 2025-10-31 | 2025-11-03 | SNDK | SWITCH | 2025-10-02 | 2025-05-02 | 0.47% | 1.663398 |
| 2025-12 | 2025-11-28 | 2025-12-01 | SNDK | HOLD | 2025-10-29 | 2025-05-30 | 15.35% | 1.918671 |
| 2026-01 | 2025-12-31 | 2026-01-02 | SNDK | HOLD | 2025-12-01 | 2025-07-02 | 140.97% | 4.623420 |
| 2026-02 | 2026-01-30 | 2026-02-02 | SNDK | HOLD | 2025-12-30 | 2025-07-31 | 5.07% | 4.857688 |
| 2026-03 | 2026-02-27 | 2026-03-02 | SNDK | HOLD | 2026-01-28 | 2025-08-27 | 5.44% | 5.121873 |
| 2026-04 | 2026-03-31 | 2026-04-01 | SNDK | HOLD | 2026-03-02 | 2025-09-29 | 62.35% | 8.315575 |
| 2026-05 | 2026-04-30 | 2026-05-01 | SNDK | HOLD | 2026-03-31 | 2025-10-28 | 32.92% | 11.052753 |

Caveat: this validates the price-timing logic and reproduced PDF numbers, but it still uses the current Nasdaq-100 constituent list for historical dates. A stricter investment-grade test needs point-in-time index membership and independent corporate-action verification.
