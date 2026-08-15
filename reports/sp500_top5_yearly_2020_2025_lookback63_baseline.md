# Annual S&P 500 Top-5 Momentum Backtests

Rules: rank after each close by 63-trading-day adjusted-close momentum, SMA filter: none, execute exits/entries at the next trading day's open, hold at most five 20% slots.

| Year | Actual Trading Period | Return | Max DD | Sharpe | Buys | Sells | Final Holdings |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 2020 | 2020-01-02 to 2020-12-31 | -40.81% | -48.20% | -1.25 | 214 | 209 | TRGP, COHR, TPR, OXY, PLTR |
| 2021 | 2021-01-04 to 2021-12-31 | 19.85% | -21.95% | 0.75 | 213 | 208 | ANET, BLDR, CIEN, TER, ON |
| 2022 | 2022-01-03 to 2022-12-30 | -21.62% | -28.72% | -0.57 | 258 | 253 | SMCI, UHS, HAL, MRNA, BA |
| 2023 | 2023-01-03 to 2023-12-29 | 60.60% | -20.69% | 1.55 | 168 | 163 | CRWD, COIN, XYZ, EXPE, AMD |
| 2024 | 2024-01-02 to 2024-12-31 | -5.80% | -28.54% | -0.01 | 205 | 200 | APP, PLTR, TSLA, UAL, HOOD |
| 2025 | 2025-01-02 to 2025-12-31 | 16.11% | -33.82% | 0.60 | 187 | 182 | SNDK, LITE, COHR, ALB, MU |

Each row is a standalone full-year backtest that starts fresh at the beginning of that year.
This uses current S&P 500 constituents, not point-in-time index membership, so long-horizon results may contain survivorship bias.
