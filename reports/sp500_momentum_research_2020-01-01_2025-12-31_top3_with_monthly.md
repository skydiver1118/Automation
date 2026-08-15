# S&P 500 Momentum Research Grid

Benchmark: SPMO total return = 202.49%.

| Rank | Variant | Return | Excess vs SPMO | CAGR | Max DD | Sharpe | Buys | Final Holdings |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 126 skip21 | 317.08% | 114.59% | 26.89% | -41.78% | 0.78 | 598 | SNDK, LITE, SATS |
| 2 | 126 raw baseline | 234.07% | 31.58% | 22.28% | -44.88% | 0.68 | 465 | SNDK, LITE, SATS |
| 3 | 252 skip21 | 206.09% | 3.60% | 20.51% | -36.66% | 0.66 | 351 | WDC, LITE, STX |
| 4 | 126 skip21 monthly | 180.81% | -21.68% | 18.79% | -47.57% | 0.63 | 110 | SATS, SNDK, LITE |
| 5 | 126 raw + SMA50 topN | 170.76% | -31.73% | 18.07% | -44.87% | 0.63 | 499 | SNDK, LITE, SATS |
| 6 | 126 skip21 + SMA50 topN | 138.26% | -64.23% | 15.58% | -41.36% | 0.62 | 577 | SNDK, LITE, SATS |
| 7 | 126 raw + SMA100 topN | 121.89% | -80.61% | 14.22% | -45.02% | 0.53 | 484 | SNDK, LITE, SATS |
| 8 | 126 raw + SMA50 topN + SPY SMA200 | 73.06% | -129.44% | 9.58% | -44.87% | 0.44 | 457 | SNDK, LITE, SATS |
| 9 | 126 raw + SPY SMA200 | 65.97% | -136.52% | 8.82% | -44.88% | 0.41 | 438 | SNDK, LITE, SATS |
| 10 | 252 risk-adjusted skip21 | 40.32% | -162.17% | 5.81% | -45.83% | 0.34 | 520 | WDC, STX, LITE |
| 11 | 126 risk-adjusted + SMA50 topN | 19.76% | -182.73% | 3.05% | -35.73% | 0.26 | 702 | SNDK, LITE, CIEN |
| 12 | 252 skip21 + SMA50 topN | 16.32% | -186.17% | 2.55% | -31.25% | 0.23 | 331 | WDC, LITE, STX |
| 13 | 126 risk-adjusted | -19.49% | -221.98% | -3.55% | -51.55% | 0.06 | 717 | SNDK, LITE, CIEN |
| 14 | 252 risk-adjusted skip21 + SMA50 topN + SPY SMA200 | -33.56% | -236.06% | -6.59% | -45.91% | -0.16 | 401 | WDC, STX, LITE |
| 15 | 252 risk-adjusted skip21 + SMA50 topN | -33.72% | -236.21% | -6.63% | -47.74% | -0.13 | 487 | WDC, STX, LITE |

Research ideas tested: SPMO-like 12-1 momentum, volatility-adjusted momentum, SMA50/SMA100 top-N gates, and a SPY SMA200 market regime filter.
Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.
