# S&P 500 Momentum Research Grid

Benchmark: SPMO total return = 202.49%.

| Rank | Variant | Return | Excess vs SPMO | CAGR | Max DD | Sharpe | Buys | Final Holdings |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 126 raw + SMA50 topN | 451.63% | 249.13% | 32.95% | -63.58% | 0.77 | 174 | SNDK |
| 2 | 126 raw + SPY SMA200 | 410.99% | 208.50% | 31.27% | -60.74% | 0.76 | 159 | SNDK |
| 3 | 126 raw baseline | 395.88% | 193.39% | 30.61% | -67.67% | 0.74 | 170 | SNDK |
| 4 | 126 raw + SMA50 topN + SPY SMA200 | 369.14% | 166.65% | 29.41% | -63.54% | 0.74 | 162 | SNDK |
| 5 | 126 skip21 | 355.85% | 153.36% | 28.79% | -57.23% | 0.72 | 212 | SNDK |
| 6 | 252 skip21 | 249.41% | 46.92% | 23.20% | -49.12% | 0.65 | 138 | LITE |
| 7 | 126 skip21 + SMA50 topN | 219.63% | 17.14% | 21.39% | -67.85% | 0.63 | 189 | SNDK |
| 8 | 126 raw + SMA100 topN | 212.67% | 10.17% | 20.94% | -66.91% | 0.62 | 175 | SNDK |
| 9 | 252 risk-adjusted skip21 | 48.66% | -153.83% | 6.84% | -66.02% | 0.38 | 179 | WDC |
| 10 | 252 skip21 + SMA50 topN | 26.44% | -176.05% | 3.99% | -50.73% | 0.31 | 129 | LITE |
| 11 | 252 risk-adjusted skip21 + SMA50 topN | 15.53% | -186.96% | 2.44% | -54.46% | 0.26 | 169 | WDC |
| 12 | 252 risk-adjusted skip21 + SMA50 topN + SPY SMA200 | -17.99% | -220.48% | -3.25% | -65.10% | 0.10 | 133 | WDC |
| 13 | 126 risk-adjusted + SMA50 topN | -83.48% | -285.97% | -25.94% | -89.24% | -0.35 | 299 | SNDK |
| 14 | 126 risk-adjusted | -89.97% | -292.46% | -31.85% | -93.59% | -0.50 | 305 | SNDK |

Research ideas tested: SPMO-like 12-1 momentum, volatility-adjusted momentum, SMA50/SMA100 top-N gates, and a SPY SMA200 market regime filter.
Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.
