# Annual S&P 500 Top-5 Momentum Backtests

Rules: rank after each close by 126-trading-day adjusted-close momentum, SMA filter: SMA50 (top_n), execute exits/entries at the next trading day's open, hold at most five 20% slots.

| Year | Actual Trading Period | Return | Max DD | Sharpe | Buys | Sells | Final Holdings |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 2020 | 2020-01-02 to 2020-12-31 | -15.37% | -24.97% | -0.30 | 153 | 148 | TSLA, TPR, FCX, BLDR, FSLR |
| 2021 | 2021-01-04 to 2021-12-31 | 0.71% | -20.73% | 0.17 | 142 | 137 | BLDR, ON, DDOG, ANET, TSLA |
| 2022 | 2022-01-03 to 2022-12-30 | 17.55% | -18.57% | 0.69 | 135 | 133 | SMCI, ROST |
| 2023 | 2023-01-03 to 2023-12-29 | 70.20% | -15.13% | 1.89 | 120 | 115 | VRT, COIN, CVNA, CRWD, WSM |
| 2024 | 2024-01-02 to 2024-12-31 | 13.66% | -26.88% | 0.56 | 125 | 120 | APP, PLTR, AXON, TSLA, UAL |
| 2025 | 2025-01-02 to 2025-12-31 | 11.81% | -27.90% | 0.50 | 127 | 122 | WDC, SNDK, LITE, SATS, CIEN |

Each row is a standalone full-year backtest that starts fresh at the beginning of that year.
This uses current S&P 500 constituents, not point-in-time index membership, so long-horizon results may contain survivorship bias.
