# Nasdaq-100 Top-1 Skip-Momentum Annual Reset vs SPMO, SMH, VGT

Strategy rules: each year starts at 1.0 equity with no carried holding. At each month start, rank the current Nasdaq-100 universe by Close[t-21 trading days] / Close[t-126 trading days] - 1 using only data available after the prior trading day's close, buy the top-ranked stock at the next open, and hold until the next monthly open. Latest partial year is valued through the latest available close.

Drawdown: strategy drawdown is measured from daily held-position equity inside each year. Benchmark returns use adjusted first open to latest/last close, and benchmark drawdowns use adjusted daily close equity inside the same year window.

| Period | Strategy Return | Strategy Max DD | Decisions | Exec Trades | Final Holding | SPMO Return | SPMO Max DD | SMH Return | SMH Max DD | VGT Return | VGT Max DD |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2020 | 129.76% | -60.63% | 12 | 13 | TSLA | 27.16% | -30.95% | 52.96% | -33.62% | 44.74% | -31.84% |
| 2021 | 31.65% | -64.61% | 12 | 9 | TSLA | 22.21% | -10.67% | 40.76% | -15.58% | 29.87% | -10.82% |
| 2022 | -14.27% | -37.65% | 12 | 21 | DXCM | -10.56% | -22.74% | -34.07% | -45.14% | -29.78% | -34.50% |
| 2023 | 84.73% | -32.37% | 12 | 19 | PDD | 17.43% | -8.63% | 70.32% | -14.42% | 51.26% | -12.87% |
| 2024 | -33.61% | -47.95% | 12 | 9 | APP | 46.73% | -13.16% | 41.13% | -24.82% | 31.02% | -15.23% |
| 2025 | 86.39% | -57.00% | 12 | 7 | SNDK | 25.54% | -20.13% | 47.74% | -32.65% | 20.76% | -27.13% |
| 2026 YTD | 476.06% | -25.85% | 5 | 1 | SNDK | 19.65% | -10.98% | 50.79% | -14.93% | 19.10% | -13.65% |

| Compounded Annual-Reset Return | Strategy | SPMO | SMH | VGT |
| --- | ---: | ---: | ---: | ---: |
| 2020 to date | 3314.96% | 259.69% | 660.18% | 276.23% |

Validation notes:
- No-lookahead checks were OK for every strategy row.
- This still uses the current Nasdaq-100 constituent file for historical years, so survivorship/index-membership bias remains.
- Results exclude slippage, spreads, commissions, taxes, and market-impact costs.
