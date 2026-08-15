# Annual S&P 500 Top-5 Momentum Backtests

Rules: rank after each close by 126-trading-day adjusted-close momentum, SMA filter: none, execute exits/entries at the next trading day's open, hold at most five 20% slots.

| Year | Actual Trading Period | Return | Max DD | Sharpe | Buys | Sells | Final Holdings |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 2020 | 2020-01-02 to 2020-12-31 | 27.90% | -35.81% | 0.77 | 82 | 80 | TSLA, MRNA |
| 2021 | 2021-01-04 to 2021-12-31 | 11.87% | -31.30% | 0.48 | 78 | 76 | AMD, DDOG |
| 2022 | 2022-01-03 to 2022-12-30 | -15.66% | -37.48% | -0.22 | 54 | 52 | FSLR, SMCI |
| 2023 | 2023-01-03 to 2023-12-29 | 110.06% | -31.08% | 1.75 | 65 | 63 | VRT, COIN |
| 2024 | 2024-01-02 to 2024-12-31 | 2.30% | -42.08% | 0.29 | 59 | 57 | PLTR, APP |
| 2025 | 2025-01-02 to 2025-12-31 | 78.81% | -30.51% | 1.32 | 47 | 45 | SNDK, LITE |

Each row is a standalone full-year backtest that starts fresh at the beginning of that year.
This uses current S&P 500 constituents, not point-in-time index membership, so long-horizon results may contain survivorship bias.
