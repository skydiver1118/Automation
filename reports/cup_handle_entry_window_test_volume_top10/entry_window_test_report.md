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

- Best by IS return: `8` trading days.
- Best IS return: `284.44%`; OOS return for that same window: `98.21%`.
- Best by OOS return: `9` trading days with OOS `102.21%`.

## Results

| EntryWindowTradingDays | Signals | IS_TotalReturnPct | IS_CagrPct | IS_MaxDrawdownPct | IS_Sharpe | IS_Trades | IS_WinRatePct | OOS_TotalReturnPct | OOS_CagrPct | OOS_MaxDrawdownPct | OOS_Sharpe | OOS_Trades | OOS_WinRatePct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3.0 | 6212.0 | 86.75 | 6.45 | -16.41 | 0.621 | 56.0 | 57.14 | 57.93 | 7.4 | -12.57 | 0.695 | 37.0 | 45.95 |
| 4.0 | 6212.0 | 131.03 | 8.75 | -19.73 | 0.719 | 70.0 | 57.14 | 61.14 | 7.73 | -17.8 | 0.676 | 42.0 | 47.62 |
| 5.0 | 6203.0 | 152.73 | 9.73 | -16.65 | 0.789 | 72.0 | 58.33 | 97.46 | 11.21 | -16.82 | 0.877 | 47.0 | 53.19 |
| 6.0 | 6203.0 | 241.24 | 13.08 | -16.65 | 1.032 | 72.0 | 61.11 | 84.53 | 10.04 | -21.33 | 0.775 | 49.0 | 51.02 |
| 7.0 | 6203.0 | 256.61 | 13.58 | -19.77 | 1.051 | 74.0 | 62.16 | 87.04 | 10.27 | -21.38 | 0.796 | 50.0 | 52.0 |
| 8.0 | 6203.0 | 284.44 | 14.43 | -18.47 | 1.159 | 71.0 | 64.79 | 98.21 | 11.27 | -18.44 | 0.859 | 51.0 | 49.02 |
| 9.0 | 6203.0 | 230.22 | 12.71 | -18.13 | 1.05 | 72.0 | 58.33 | 102.21 | 11.62 | -16.08 | 0.831 | 55.0 | 49.09 |
| 10.0 | 6196.0 | 192.81 | 11.36 | -17.63 | 0.921 | 71.0 | 59.15 | 97.19 | 11.19 | -17.98 | 0.868 | 49.0 | 48.98 |
