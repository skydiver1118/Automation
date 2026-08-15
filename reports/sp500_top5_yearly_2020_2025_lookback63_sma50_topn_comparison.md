# S&P 500 Top-5 Momentum: 63-Day Baseline vs SMA50 Top-N Gate

Rules common to both tests:

- Annual reset for each calendar year from 2020 through 2025.
- Rank S&P 500 stocks after each close by 63-trading-day adjusted-close momentum.
- Execute exits and entries at the next trading day's open.
- Hold at most five 20% portfolio slots; unused slots stay in cash.

Variant tested:

- Baseline: buy the top 5 ranked stocks with no SMA filter.
- Revised SMA50: first find the raw top 5, then only hold names from that top 5 that are above SMA50. Do not fill open slots from ranks 6+.

| Year | Baseline Return | SMA50 Top-N Return | Delta | Baseline Max DD | SMA50 Top-N Max DD | DD Improvement | Baseline Sharpe | SMA50 Top-N Sharpe | Baseline Buys | SMA50 Top-N Buys |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2020 | -40.81% | -34.98% | 5.83% | -48.20% | -43.09% | 5.10% | -1.25 | -1.02 | 214 | 212 |
| 2021 | 19.85% | 21.70% | 1.85% | -21.95% | -21.95% | 0.00% | 0.75 | 0.80 | 213 | 213 |
| 2022 | -21.62% | -13.92% | 7.70% | -28.72% | -27.49% | 1.23% | -0.57 | -0.38 | 258 | 249 |
| 2023 | 60.60% | 61.25% | 0.66% | -20.69% | -17.45% | 3.23% | 1.55 | 1.68 | 168 | 168 |
| 2024 | -5.80% | -5.75% | 0.05% | -28.54% | -26.37% | 2.16% | -0.01 | -0.02 | 205 | 201 |
| 2025 | 16.11% | 15.22% | -0.89% | -33.82% | -34.02% | -0.20% | 0.60 | 0.59 | 187 | 185 |

| Metric | Baseline | SMA50 Top-N |
| --- | ---: | ---: |
| Average annual return | 4.72% | 7.25% |
| Compounded return across reset-year results | -2.34% | 19.28% |
| Worst yearly max drawdown | -48.20% | -43.09% |

Takeaway: with 63-day momentum, the revised SMA50 gate improves 2020, 2021, 2022, 2023, and slightly improves 2024, but slightly trails in 2025. It helps mainly by leaving cash idle when the raw top-5 names are below trend, rather than replacing them with lower-ranked stocks.

Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.
