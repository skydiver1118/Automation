# Top-2 Skip21 Monthly Open-to-Open Validation

Rules: signal after the last close of each month, rank by 126-trading-day momentum excluding the most recent 21 trading days, buy the top 2 equal-weight at the next open, and hold open-to-open until the next rebalance.

| Period | Strategy | Max DD | Trades | SPMO Close | SPMO O2O | Excess vs SPMO Close | Excess vs SPMO O2O | Final Holdings |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 2020 | 112.23% | -54.42% | 26 | 27.08% | 26.65% | 85.15% | 85.58% | TSLA, FDX |
| 2021 | 60.59% | -24.49% | 22 | 24.22% | 22.43% | 36.37% | 38.16% | TSLA, DDOG |
| 2022 | 23.41% | -27.83% | 22 | -10.45% | -10.80% | 33.85% | 34.20% | FSLR, DXCM |
| 2023 | 115.90% | -35.91% | 26 | 19.47% | 17.84% | 96.43% | 98.06% | VRT, CVNA |
| 2024 | 193.93% | -36.96% | 22 | 47.18% | 47.84% | 146.75% | 146.09% | APP, CVNA |
| 2025 | 123.71% | -52.49% | 16 | 25.87% | 26.75% | 97.84% | 96.96% | SNDK, SATS |
| 2026 YTD | 279.68% | -25.62% | 6 | 20.86% | 20.31% | 258.83% | 259.37% | SNDK, LITE |

| Compounded Reset Return | Strategy | SPMO Close | SPMO O2O |
| --- | ---: | ---: | ---: |
| 2020-2026 YTD | 22569.75% | 278.10% | 267.44% |

Validation notes:
- No same-day lookahead: month-end close signals are used for the next trading day's open.
- Returns are open-to-open for the strategy. SPMO is shown both as adjusted close buy-and-hold and open-to-open for comparison.
- Major remaining flaw: this uses the current S&P 500 constituent list for past years, so survivorship/index-membership bias remains.
