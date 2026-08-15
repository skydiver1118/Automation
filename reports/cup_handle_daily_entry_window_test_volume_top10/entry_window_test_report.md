# Cup-And-Handle Entry Window Test

This is technical strategy research, not investment advice.

## Setup

- Candidate pool: top 10 weekly candidates by score, after `TargetReturnPct > 30%`.
- Entry stock filter: `Close > SMA50` and stock 63-day return greater than S&P 500 63-day return.
- Entry market filter: `S&P 500 close > SMA100`.
- Exit: `ATR14 3.5x initial stop`, no measured target, 60-trading-day time stop.
- Portfolio: maximum 3 concurrent stocks.
- Entry volume condition: `enabled`, breakout-day volume >= 1.40x prior 50-day average.
- Test variable: breakout entry window from 3 to 10 trading days after trade-start date.

## Benchmarks

| Segment | S&P 500 Return % | CAGR % | Max DD % | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| IS | 185.16 | 11.06 | -19.78 | 0.785 |
| OOS | 132.67 | 14.1 | -33.92 | 0.747 |

## Selection

- Best by IS return: `9` trading days.
- Best IS return: `462.02%`; OOS return for that same window: `233.81%`.
- Best by OOS return: `7` trading days with OOS `263.74%`.

## Results

| EntryWindowTradingDays | Signals | IS_TotalReturnPct | IS_CagrPct | IS_MaxDrawdownPct | IS_Sharpe | IS_Trades | IS_WinRatePct | OOS_TotalReturnPct | OOS_CagrPct | OOS_MaxDrawdownPct | OOS_Sharpe | OOS_Trades | OOS_WinRatePct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3.0 | 13739.0 | 185.62 | 11.08 | -21.5 | 0.724 | 68.0 | 55.88 | 137.6 | 14.47 | -17.87 | 0.904 | 48.0 | 52.08 |
| 4.0 | 13729.0 | 210.27 | 12.0 | -26.36 | 0.753 | 77.0 | 54.55 | 105.21 | 11.88 | -16.49 | 0.77 | 47.0 | 53.19 |
| 5.0 | 13719.0 | 355.54 | 16.39 | -31.9 | 0.922 | 75.0 | 60.0 | 129.44 | 13.85 | -18.1 | 0.87 | 49.0 | 53.06 |
| 6.0 | 13709.0 | 285.32 | 14.46 | -31.45 | 0.84 | 78.0 | 58.97 | 162.13 | 16.24 | -19.87 | 0.972 | 47.0 | 55.32 |
| 7.0 | 13709.0 | 391.64 | 17.29 | -27.94 | 0.977 | 75.0 | 62.67 | 263.74 | 22.34 | -16.34 | 1.212 | 48.0 | 64.58 |
| 8.0 | 13709.0 | 343.13 | 16.07 | -27.94 | 0.935 | 76.0 | 61.84 | 234.44 | 20.75 | -20.85 | 1.173 | 51.0 | 58.82 |
| 9.0 | 13701.0 | 462.02 | 18.87 | -18.73 | 1.027 | 79.0 | 63.29 | 233.81 | 20.71 | -17.96 | 1.127 | 49.0 | 57.14 |
| 10.0 | 13691.0 | 388.49 | 17.21 | -18.56 | 0.934 | 79.0 | 63.29 | 221.91 | 20.03 | -18.66 | 1.069 | 48.0 | 56.25 |
