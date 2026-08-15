# S&P 500 Yearly Idea Grid vs SPMO

Each period is reset independently. Returns execute stock sleeves at next-day open using signals known after the prior close.

| Rank | Variant | Wins vs SPMO | Compounded Reset Return | Worst Excess | 2024 Return | 2024 Excess | 2026 YTD Return | 2026 YTD Excess |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | Top2 skip21 monthly | 5/7 | 640.54% | -35.17% | 43.63% | -3.55% | 98.12% | 74.50% |
| 2 | Top2 skip21 weekly | 4/7 | 761.41% | -30.77% | 18.12% | -29.06% | 90.47% | 66.85% |
| 3 | Top2 skip21 daily | 4/7 | 620.47% | -44.88% | 2.30% | -44.88% | 55.35% | 31.73% |
| 4 | Top4 skip21 daily | 4/7 | 477.89% | -32.18% | 14.99% | -32.18% | 61.20% | 37.58% |
| 5 | Top2 raw daily | 4/7 | 197.77% | -63.63% | 36.63% | -10.55% | 74.09% | 50.47% |
| 6 | Top3 skip21 daily | 3/7 | 623.65% | -32.77% | 14.40% | -32.77% | 70.30% | 46.68% |
| 7 | Top2 skip21 SMA200 | 3/7 | 544.72% | -44.88% | 2.30% | -44.88% | 55.35% | 31.73% |
| 8 | Top2 skip21 SMA50 | 3/7 | 302.97% | -46.53% | 0.65% | -46.53% | 50.51% | 26.89% |
| 9 | 50% SPMO + 50% Top2 | 3/7 | 157.05% | -45.13% | 2.05% | -45.13% | 34.28% | 10.66% |
| 10 | 75% SPMO + 25% Top2 | 2/7 | 37.54% | -46.80% | 0.37% | -46.80% | 22.91% | -0.72% |
| 11 | Top20 risk-adj inv-vol monthly | 2/7 | 23.14% | -48.73% | -1.55% | -48.73% | 29.10% | 5.48% |
| 12 | Top100 risk-adj inv-vol monthly | 1/7 | 7.48% | -47.21% | -0.03% | -47.21% | 9.58% | -14.04% |
| 13 | Top50 risk-adj inv-vol monthly | 1/7 | -2.81% | -48.18% | -1.00% | -48.18% | 14.06% | -9.56% |
| 14 | Top100 risk-adj inv-vol quarterly | 0/7 | 4.28% | -47.59% | -0.41% | -47.59% | 8.28% | -15.34% |
| 15 | 90% SPMO + 10% Top2 | 0/7 | -8.78% | -48.28% | -1.10% | -48.28% | 15.95% | -7.67% |

Research notes: SPMO-like broad risk-adjusted/inverse-volatility portfolios improved 2024 robustness but did not beat SPMO in every year. Concentrated top-2 variants keep the strongest compounded return but fail individual years like 2021, 2022 and 2024.
Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.
