# S&P 500 Momentum Research Grid

Benchmark: SPMO total return = 202.49%.

| Rank | Variant | Return | Excess vs SPMO | CAGR | Max DD | Sharpe | Buys | Final Holdings |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 126 skip21 | 347.25% | 144.76% | 28.38% | -45.59% | 0.77 | 379 | SNDK, LITE |
| 2 | 252 skip21 | 150.96% | -51.54% | 16.59% | -46.26% | 0.56 | 231 | WDC, LITE |
| 3 | 126 skip21 + SMA50 topN | 110.09% | -92.40% | 13.18% | -47.92% | 0.52 | 368 | SNDK, LITE |
| 4 | 252 risk-adjusted skip21 | 95.36% | -107.13% | 11.82% | -43.33% | 0.48 | 347 | WDC, STX |
| 5 | 126 raw baseline | 60.29% | -142.20% | 8.19% | -60.48% | 0.41 | 320 | SNDK, LITE |
| 6 | 126 raw + SMA50 topN | 48.52% | -153.98% | 6.82% | -55.27% | 0.37 | 335 | SNDK, LITE |
| 7 | 126 raw + SPY SMA200 | 38.24% | -164.25% | 5.55% | -50.55% | 0.35 | 282 | SNDK, LITE |
| 8 | 126 raw + SMA50 topN + SPY SMA200 | 31.39% | -171.10% | 4.66% | -51.33% | 0.32 | 294 | SNDK, LITE |
| 9 | 252 risk-adjusted skip21 + SMA50 topN | 13.99% | -188.50% | 2.21% | -31.40% | 0.23 | 312 | WDC, STX |
| 10 | 126 raw + SMA100 topN | 10.88% | -191.62% | 1.74% | -58.34% | 0.28 | 327 | SNDK, LITE |
| 11 | 252 risk-adjusted skip21 + SMA50 topN + SPY SMA200 | 0.60% | -201.89% | 0.10% | -36.40% | 0.15 | 240 | WDC, STX |
| 12 | 126 risk-adjusted + SMA50 topN | -1.70% | -204.19% | -0.29% | -54.80% | 0.18 | 506 | SNDK, LITE |
| 13 | 252 skip21 + SMA50 topN | -7.27% | -209.77% | -1.25% | -44.62% | 0.14 | 235 | WDC, LITE |
| 14 | 126 risk-adjusted | -12.77% | -215.27% | -2.25% | -62.16% | 0.14 | 515 | SNDK, LITE |

Research ideas tested: SPMO-like 12-1 momentum, volatility-adjusted momentum, SMA50/SMA100 top-N gates, and a SPY SMA200 market regime filter.
Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.
