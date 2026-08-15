# 2024 S&P 500 Top-5 Momentum SMA Filter Comparison

Rules common to both runs:

- Universe: current S&P 500 constituents.
- Rank by 126-trading-day adjusted-close momentum.
- Hold at most five 20% slots.
- Generate signals after the close.
- Execute exits and entries at the next trading day's open.

| Variant | Return | CAGR | Max DD | Sharpe | Buys | Sells | Final Holdings |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Baseline | 3.98% | 3.99% | -37.34% | 0.29 | 116 | 111 | APP, PLTR, AXON, TSLA, UAL |
| SMA20 Filter | 0.77% | 0.77% | -34.12% | 0.19 | 272 | 267 | PLTR, TSLA, UAL, CIEN, TPR |
| SMA50 Filter | 12.33% | 12.38% | -29.58% | 0.52 | 170 | 165 | APP, PLTR, AXON, TSLA, UAL |
| SMA100 Filter | 1.94% | 1.95% | -37.23% | 0.23 | 141 | 136 | APP, PLTR, AXON, TSLA, UAL |
| SMA200 Filter | 3.98% | 3.99% | -37.34% | 0.29 | 116 | 111 | APP, PLTR, AXON, TSLA, UAL |

## Takeaway

SMA50 was the best of these simple filters in 2024. It improved return from 3.98% to 12.33%, reduced max drawdown from -37.34% to -29.58%, and improved Sharpe from 0.29 to 0.52.

SMA20 was too reactive and more than doubled turnover. SMA100 underperformed baseline. SMA200 was effectively identical to baseline in this year because the selected high-momentum names were already above their SMA200 when it mattered.
