# 2024 Failure Diagnosis and Adjustment

Strategy diagnosed:

- S&P 500 universe.
- Top 2 by 126-trading-day momentum, excluding the most recent 21 trading days.
- Equal weight, next-day open execution, annual reset.

## Why 2024 Was Bad

SPMO 2024 return: 47.18%.

Original strategy 2024 return: 2.30%.

The main issue was stale concentrated leadership. The skip-21 rule intentionally ignores the most recent trading month, which is useful for avoiding short-term reversal noise in many years, but in 2024 it kept the strategy in fading high-momentum names too long.

Monthly strategy returns:

| Month | Return |
| --- | ---: |
| 2024-01 | 2.04% |
| 2024-02 | 9.56% |
| 2024-03 | -3.82% |
| 2024-04 | -11.75% |
| 2024-05 | -8.96% |
| 2024-06 | 3.51% |
| 2024-07 | -20.23% |
| 2024-08 | 8.25% |
| 2024-09 | 4.13% |
| 2024-10 | 23.91% |
| 2024-11 | 10.14% |
| 2024-12 | -6.77% |

Worst contributors:

| Ticker | Approx Contribution | Days Held |
| --- | ---: | ---: |
| SMCI | -12.76% | 103 |
| VST | -5.91% | 31 |
| MMM | -5.23% | 10 |
| COHR | -1.53% | 5 |
| CRWD | -1.03% | 41 |

Best contributors:

| Ticker | Approx Contribution | Days Held |
| --- | ---: | ---: |
| APP | 10.19% | 38 |
| COIN | 7.71% | 67 |
| SATS | 4.08% | 8 |
| HOOD | 3.72% | 4 |
| PLTR | 3.35% | 34 |

## Stock-Only Adjustments Tested

| Variant | 2024 Return | Excess vs SPMO | Max DD |
| --- | ---: | ---: | ---: |
| Top 2 126 raw momentum | 36.63% | -10.55% | -50.55% |
| Top 4 126 skip21 | 14.99% | -32.18% | -38.64% |
| Top 3 126 skip21 | 14.40% | -32.77% | -38.63% |
| Top 2 126 skip10 | 13.02% | -34.16% | -48.31% |
| Top 2 126 skip42 | 9.78% | -37.39% | -45.41% |
| Top 5 126 skip21 | 5.31% | -41.87% | -37.22% |
| Original top 2 126 skip21 | 2.30% | -44.88% | -42.08% |

None of the stock-only adjustments beat SPMO in 2024.

## Fallback Adjustment Tested

Adjustment: keep running the top-2 skip-month stock model, but when its model equity drawdown exceeds a threshold, use SPMO as the active sleeve instead of the top-2 stocks. This directly addresses the failure mode: the concentrated stock sleeve is weak while broad momentum is still strong.

| Drawdown Trigger | 2024 Return | Excess vs SPMO | 2024 Max DD | Fallback Days | 2020-2025 Compounded Reset Return |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 5% | 44.50% | -2.68% | -12.78% | 213 | 3839.78% |
| 10% | 23.03% | -24.15% | -15.17% | 172 | 1880.36% |
| 15% | 19.75% | -27.43% | -14.36% | 143 | 864.19% |
| 20% | 26.74% | -20.44% | -19.54% | 106 | 1145.59% |
| 25% | 31.90% | -15.28% | -19.54% | 73 | 1184.38% |

Best adjustment so far:

- Top-2 126-day skip-21 momentum stock sleeve.
- If the sleeve's model drawdown exceeds 5%, rotate into SPMO.
- Rotate back to the stock sleeve when the model drawdown recovers above the trigger.

This did not fully beat SPMO in 2024, but it nearly matched it and drastically reduced drawdown. It also preserved strong compounded reset-year performance across 2020-2025.

Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.
