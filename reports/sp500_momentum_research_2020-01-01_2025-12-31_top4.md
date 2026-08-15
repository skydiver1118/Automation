# S&P 500 Momentum Research Grid

Benchmark: SPMO total return = 202.49%.

| Rank | Variant | Return | Excess vs SPMO | CAGR | Max DD | Sharpe | Buys | Final Holdings |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 126 skip21 | 251.60% | 49.10% | 23.33% | -38.64% | 0.74 | 721 | SATS, SNDK, LITE, WDC |
| 2 | 126 raw baseline | 160.05% | -42.45% | 17.28% | -43.45% | 0.60 | 642 | SNDK, SATS, LITE, CIEN |
| 3 | 252 skip21 | 119.72% | -82.77% | 14.03% | -43.74% | 0.54 | 486 | WDC, LITE, HOOD, STX |
| 4 | 126 skip21 + SMA50 topN | 111.71% | -90.78% | 13.33% | -32.71% | 0.58 | 695 | SNDK, SATS, LITE, WDC |
| 5 | 126 raw + SMA50 topN | 106.95% | -95.55% | 12.90% | -41.21% | 0.53 | 662 | SNDK, LITE, SATS, CIEN |
| 6 | 126 raw + SMA100 topN | 76.28% | -126.22% | 9.92% | -45.39% | 0.44 | 651 | SNDK, SATS, LITE, CIEN |
| 7 | 126 raw + SPY SMA200 | 69.47% | -133.03% | 9.20% | -37.23% | 0.43 | 577 | SNDK, SATS, LITE, CIEN |
| 8 | 126 raw + SMA50 topN + SPY SMA200 | 61.07% | -141.43% | 8.27% | -39.35% | 0.41 | 593 | SNDK, LITE, SATS, CIEN |
| 9 | 126 risk-adjusted + SMA50 topN | 29.82% | -172.67% | 4.45% | -29.91% | 0.30 | 857 | WDC, SNDK, LITE, CIEN |
| 10 | 252 risk-adjusted skip21 | 24.24% | -178.25% | 3.69% | -52.71% | 0.27 | 715 | WDC, STX, NEM, LITE |
| 11 | 126 risk-adjusted | 0.20% | -202.29% | 0.03% | -40.24% | 0.15 | 873 | WDC, SNDK, LITE, CIEN |
| 12 | 252 skip21 + SMA50 topN | -5.05% | -207.54% | -0.86% | -35.76% | 0.10 | 480 | WDC, LITE, STX |
| 13 | 252 risk-adjusted skip21 + SMA50 topN + SPY SMA200 | -39.28% | -241.77% | -7.98% | -48.61% | -0.27 | 556 | WDC, STX, NEM, LITE |
| 14 | 252 risk-adjusted skip21 + SMA50 topN | -45.05% | -247.54% | -9.50% | -53.84% | -0.32 | 664 | WDC, STX, NEM, LITE |

Research ideas tested: SPMO-like 12-1 momentum, volatility-adjusted momentum, SMA50/SMA100 top-N gates, and a SPY SMA200 market regime filter.
Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.
