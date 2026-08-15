# 2026 Monthly S&P 500 Top-5 Momentum Backtests

Rules: rank after each close by 126-trading-day adjusted-close momentum, execute exits/entries at the next trading day's open, hold at most five 20% slots.

| Month | Requested Period | Actual Trading Period | Return | Max DD | Sharpe | Buys | Sells | Final Holdings |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 2026-01 | 2026-01-01 to 2026-01-31 | 2026-01-02 to 2026-01-30 | 5.12% | -9.83% | 1.23 | 8 | 3 | SNDK, LITE, SATS, WDC, MU |
| 2026-02 | 2026-02-01 to 2026-02-28 | 2026-02-02 to 2026-02-27 | 5.35% | -7.48% | 2.07 | 12 | 7 | SNDK, LITE, CIEN, MU, WDC |
| 2026-03 | 2026-03-01 to 2026-03-31 | 2026-03-02 to 2026-03-31 | 3.39% | -19.15% | 0.88 | 8 | 3 | SNDK, LITE, CIEN, WDC, COHR |
| 2026-04 | 2026-04-01 to 2026-04-30 | 2026-04-01 to 2026-04-30 | 13.21% | -3.48% | 3.54 | 11 | 6 | SNDK, LITE, CIEN, WDC, STX |
| 2026-05 | 2026-05-01 to 2026-05-31 | 2026-05-01 to 2026-05-12 | 5.80% | -2.46% | 5.10 | 7 | 2 | SNDK, LITE, WDC, MU, INTC |

Note: CAGR is intentionally omitted from this table because one-month annualization is noisy and easy to overread.
This uses current S&P 500 constituents, which is fine for a 2026 smoke test but not a point-in-time constituent backtest.
