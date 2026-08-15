# S&P 500 Top-5 Momentum: 63 vs 126 Days, Baseline vs SMA50 Top-N

Rules common to all tests:

- Annual reset for each calendar year from 2020 through 2025.
- Rank S&P 500 stocks after each close by adjusted-close momentum.
- Execute exits and entries at the next trading day's open.
- Hold at most five 20% portfolio slots; unused slots stay in cash.

SMA50 revised method:

- First rank all stocks and take the raw top 5.
- Then only buy or hold raw top-5 names that are above SMA50.
- Do not fill open slots from ranks 6+.

| Year | 126 Baseline | 126 SMA50 Revised | 63 Baseline | 63 SMA50 Revised |
| ---: | ---: | ---: | ---: | ---: |
| 2020 | -12.27% | -15.37% | -40.81% | -34.98% |
| 2021 | 12.83% | 0.71% | 19.85% | 21.70% |
| 2022 | 4.85% | 17.55% | -21.62% | -13.92% |
| 2023 | 85.96% | 70.20% | 60.60% | 61.25% |
| 2024 | 3.98% | 13.66% | -5.80% | -5.75% |
| 2025 | 43.50% | 11.81% | 16.11% | 15.22% |

| Variant | Average Annual Return | Compounded Reset-Year Return | Worst Yearly Max DD |
| --- | ---: | ---: | ---: |
| 126 Baseline | 23.14% | 188.00% | -37.34% |
| 126 SMA50 Revised | 16.43% | 116.70% | -27.90% |
| 63 Baseline | 4.72% | -2.34% | -48.20% |
| 63 SMA50 Revised | 7.25% | 19.28% | -43.09% |

Takeaways:

- Best return profile in this reset-year test: 126-day baseline.
- Best drawdown profile: 126-day SMA50 revised.
- SMA50 revised improves the 63-day version, but the 63-day momentum window remains weaker than both 126-day versions.
- On 126-day momentum, SMA50 revised improves 2022 and 2024, but gives back too much in 2021, 2023, and 2025.

Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.
