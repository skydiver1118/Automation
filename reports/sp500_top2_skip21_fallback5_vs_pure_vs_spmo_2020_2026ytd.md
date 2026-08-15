# Top-2 Skip-Month Momentum: Pure vs 5% SPMO Fallback vs SPMO

Strategy: S&P 500 top 2 by 126-trading-day momentum excluding the most recent 21 trading days. The fallback version uses SPMO whenever the pure stock sleeve's model drawdown is at or below -5%. Each row resets at the period start.

| Period | Pure Strategy | 5% Fallback | SPMO | Fallback - Pure | Pure - SPMO | Fallback - SPMO | Pure Max DD | Fallback Max DD | Fallback Days |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 2020 | 27.90% | 61.84% | 27.08% | 33.94% | 0.83% | 34.76% | -35.81% | -19.18% | 177 |
| 2021 | 11.87% | 61.64% | 24.22% | 49.77% | -12.34% | 37.43% | -31.30% | -9.64% | 186 |
| 2022 | -15.66% | -19.50% | -10.45% | -3.84% | -5.21% | -9.05% | -37.48% | -19.94% | 242 |
| 2023 | 110.06% | 346.75% | 19.47% | 236.68% | 90.59% | 327.28% | -31.08% | -6.62% | 146 |
| 2024 | 2.30% | 44.50% | 47.18% | 42.20% | -44.88% | -2.68% | -42.08% | -12.78% | 213 |
| 2025 | 78.81% | 189.80% | 25.87% | 110.99% | 52.95% | 163.94% | -30.51% | -11.34% | 128 |
| 2026 YTD | 55.35% | 221.71% | 23.62% | 166.36% | 31.73% | 198.09% | -20.39% | -6.28% | 48 |

| Compounded Reset-Period Return | Pure Strategy | 5% Fallback | SPMO |
| --- | ---: | ---: | ---: |
| 2020-2026 YTD | 620.47% | 12574.78% | 286.76% |

Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.
