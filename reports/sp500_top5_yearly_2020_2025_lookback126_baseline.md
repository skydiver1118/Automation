# Annual S&P 500 Top-5 Momentum Backtests

Rules: rank after each close by 126-trading-day adjusted-close momentum, SMA filter: none, execute exits/entries at the next trading day's open, hold at most five 20% slots.

| Year | Actual Trading Period | Return | Max DD | Sharpe | Buys | Sells | Final Holdings |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 2020 | 2020-01-02 to 2020-12-31 | -12.27% | -23.80% | -0.18 | 153 | 148 | TSLA, TPR, FCX, BLDR, FSLR |
| 2021 | 2021-01-04 to 2021-12-31 | 12.83% | -18.36% | 0.54 | 137 | 132 | DDOG, BLDR, ON, ANET, TSLA |
| 2022 | 2022-01-03 to 2022-12-30 | 4.85% | -28.91% | 0.31 | 139 | 134 | FSLR, AXON, SMCI, ROST, NFLX |
| 2023 | 2023-01-03 to 2023-12-29 | 85.96% | -18.49% | 1.94 | 106 | 101 | VRT, COIN, CVNA, CRWD, WSM |
| 2024 | 2024-01-02 to 2024-12-31 | 3.98% | -37.34% | 0.29 | 116 | 111 | APP, PLTR, AXON, TSLA, UAL |
| 2025 | 2025-01-02 to 2025-12-31 | 43.50% | -31.89% | 1.04 | 115 | 110 | SATS, WDC, SNDK, LITE, CIEN |

Each row is a standalone full-year backtest that starts fresh at the beginning of that year.
This uses current S&P 500 constituents, not point-in-time index membership, so long-horizon results may contain survivorship bias.
