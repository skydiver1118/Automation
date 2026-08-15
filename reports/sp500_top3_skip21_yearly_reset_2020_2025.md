# Annual S&P 500 Top-5 Momentum Backtests

Rules: rank after each close by 126-trading-day adjusted-close momentum, SMA filter: none, execute exits/entries at the next trading day's open, hold at most five 20% slots.

| Year | Actual Trading Period | Return | Max DD | Sharpe | Buys | Sells | Final Holdings |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 2020 | 2020-01-02 to 2020-12-31 | 22.59% | -28.14% | 0.72 | 112 | 109 | TSLA, TPR, MRNA |
| 2021 | 2021-01-04 to 2021-12-31 | 2.49% | -32.19% | 0.24 | 123 | 120 | AMD, DDOG, TSLA |
| 2022 | 2022-01-03 to 2022-12-30 | -14.05% | -36.19% | -0.21 | 91 | 88 | FSLR, AXON, SMCI |
| 2023 | 2023-01-03 to 2023-12-29 | 86.79% | -25.13% | 1.77 | 94 | 91 | VRT, COIN, WSM |
| 2024 | 2024-01-02 to 2024-12-31 | 14.40% | -38.63% | 0.53 | 100 | 97 | PLTR, APP, TPL |
| 2025 | 2025-01-02 to 2025-12-31 | 84.13% | -34.23% | 1.42 | 89 | 86 | SNDK, LITE, SATS |

Each row is a standalone full-year backtest that starts fresh at the beginning of that year.
This uses current S&P 500 constituents, not point-in-time index membership, so long-horizon results may contain survivorship bias.
