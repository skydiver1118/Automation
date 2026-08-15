# Nasdaq-100 Top-2 Skip21 Monthly Open-to-Open vs QQQ

Rules: current Nasdaq-100 universe, signal after the last close of each month, rank by 126-trading-day momentum excluding the most recent 21 trading days, buy the top 2 equal-weight at the next open, and hold open-to-open until the next rebalance. Each year/YTD period resets independently.

| Period | Strategy | Max DD | Trades | QQQ Close | QQQ O2O | Excess vs QQQ Close | Excess vs QQQ O2O | Final Holdings |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2020 | 148.61% | -39.54% | 26 | 45.97% | 46.76% | 102.64% | 101.85% | TSLA, QCOM |
| 2021 | 38.94% | -50.12% | 18 | 29.24% | 27.44% | 9.70% | 11.50% | TSLA, DDOG |
| 2022 | -14.29% | -39.88% | 28 | -33.22% | -33.45% | 18.93% | 19.16% | DXCM, ALNY |
| 2023 | 90.50% | -25.98% | 22 | 55.91% | 54.15% | 34.60% | 36.36% | PDD, APP |
| 2024 | 44.89% | -38.09% | 20 | 27.74% | 28.12% | 17.15% | 16.76% | APP, PLTR |
| 2025 | 145.92% | -52.49% | 18 | 21.01% | 21.10% | 124.91% | 124.83% | SNDK, WDC |
| 2026 YTD | 235.72% | -25.62% | 6 | 15.77% | 14.67% | 219.95% | 221.06% | SNDK, WDC |

| Compounded Reset Return | Strategy | QQQ Close | QQQ O2O |
| --- | ---: | ---: | ---: |
| 2020-2026 YTD | 6647.15% | 251.51% | 241.34% |

Validation notes:
- No same-day lookahead: month-end close signals are used for the next trading day's open.
- Major remaining flaw: this uses the current Nasdaq-100 constituent list for past years, so survivorship/index-membership bias remains.
