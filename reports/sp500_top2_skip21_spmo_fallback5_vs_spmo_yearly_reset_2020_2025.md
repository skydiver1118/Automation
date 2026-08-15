# Top-2 Skip-Month Momentum With 5% SPMO Fallback vs SPMO

Strategy:

- S&P 500 universe.
- Rank stocks by 126-trading-day momentum excluding the most recent 21 trading days.
- Base sleeve holds top 2 equal-weight stocks.
- Track the base sleeve's model drawdown.
- If model drawdown reaches 5%, use SPMO as the active sleeve.
- Return to the stock sleeve when model drawdown recovers above the 5% trigger.
- Reset each calendar year.

| Year | Strategy Return | SPMO Return | Excess | Strategy Max DD | Fallback Days |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 2020 | 61.84% | 27.08% | 34.76% | -19.18% | 177 |
| 2021 | 61.64% | 24.22% | 37.43% | -9.64% | 186 |
| 2022 | -19.50% | -10.45% | -9.05% | -19.94% | 242 |
| 2023 | 346.75% | 19.47% | 327.28% | -6.62% | 146 |
| 2024 | 44.50% | 47.18% | -2.68% | -12.78% | 213 |
| 2025 | 189.80% | 25.87% | 163.94% | -11.34% | 128 |

| Compounded Reset-Year Return | Strategy | SPMO | Excess |
| --- | ---: | ---: | ---: |
| 2020-2025 | 3839.78% | 212.86% | 3626.93% |

Takeaway: the 5% SPMO fallback beats SPMO in 4 of 6 reset years and nearly matches it in 2024, but still underperforms in 2022. It greatly reduces the concentrated stock sleeve drawdowns in most years.

Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.
