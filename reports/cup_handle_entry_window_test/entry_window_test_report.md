# Cup-And-Handle Entry Window Test

This is technical strategy research, not investment advice.

## Setup

- Candidate pool: top 10 weekly candidates by score, after `TargetReturnPct > 30%`.
- Entry stock filter: `Close > SMA50` and stock 63-day return greater than S&P 500 63-day return.
- Entry market filter: `S&P 500 close > SMA100`.
- Exit: `ATR14 3.5x initial stop`, no measured target, 60-trading-day time stop.
- Portfolio: maximum 3 concurrent stocks.
- Test variable: breakout entry window from 3 to 10 trading days after trade-start date.

## Benchmarks

| Segment | S&P 500 Return % | CAGR % | Max DD % | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| IS | 185.16 | 11.06 | -19.78 | 0.785 |
| OOS | 132.67 | 14.1 | -33.92 | 0.747 |

## Selection

- Best by IS return: `6` trading days.
- Best IS return: `233.49%`; OOS return for that same window: `43.32%`.
- Best by OOS return: `3` trading days with OOS `134.36%`.

## Results

| EntryWindowTradingDays | Signals | IS_TotalReturnPct | IS_CagrPct | IS_MaxDrawdownPct | IS_Sharpe | IS_Trades | IS_WinRatePct | OOS_TotalReturnPct | OOS_CagrPct | OOS_MaxDrawdownPct | OOS_Sharpe | OOS_Trades | OOS_WinRatePct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3.0 | 6492.0 | 193.57 | 11.39 | -18.48 | 0.83 | 105.0 | 51.43 | 134.36 | 14.22 | -15.92 | 0.937 | 72.0 | 51.39 |
| 4.0 | 6492.0 | 169.8 | 10.45 | -21.73 | 0.737 | 111.0 | 46.85 | 41.98 | 5.63 | -26.4 | 0.435 | 78.0 | 43.59 |
| 5.0 | 6482.0 | 193.48 | 11.38 | -23.63 | 0.789 | 115.0 | 48.7 | 43.65 | 5.82 | -25.95 | 0.443 | 80.0 | 42.5 |
| 6.0 | 6482.0 | 233.49 | 12.82 | -20.35 | 0.89 | 115.0 | 52.17 | 43.32 | 5.78 | -31.82 | 0.445 | 78.0 | 43.59 |
| 7.0 | 6482.0 | 231.5 | 12.75 | -20.58 | 0.878 | 115.0 | 52.17 | 62.66 | 7.89 | -29.25 | 0.57 | 79.0 | 46.84 |
| 8.0 | 6482.0 | 181.83 | 10.93 | -17.25 | 0.778 | 115.0 | 53.04 | 97.57 | 11.22 | -24.06 | 0.751 | 78.0 | 48.72 |
| 9.0 | 6482.0 | 198.53 | 11.57 | -21.06 | 0.802 | 115.0 | 52.17 | 129.98 | 13.89 | -21.2 | 0.891 | 76.0 | 51.32 |
| 10.0 | 6473.0 | 140.55 | 9.19 | -25.12 | 0.648 | 113.0 | 50.44 | 117.15 | 12.87 | -17.75 | 0.849 | 76.0 | 51.32 |
