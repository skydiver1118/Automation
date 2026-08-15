# Cup-And-Handle Rotation Strategy Backtest

This is technical strategy research, not investment advice.

## Strategy Rules

- Point-in-time S&P 500 membership comes from the public `hanshof/sp500_constituents` historical constituents file.
- Dates after the membership file's latest row use the last available constituent snapshot.
- Weekly cup-and-handle patterns are scanned after each completed week.
- Weekly signal volume gate: handle average volume must be <= 1.05x cup average volume.
- Candidates must score above the configured threshold and have target return greater than 30%, where target return is `target / breakout - 1`.
- Portfolio can hold up to three concurrent stocks.
- Buy uses a breakout stop: enter if the stock trades at or above the breakout level within the next three trading days.
- Entry volume condition: `enabled`, breakout-day volume >= 1.40x prior 50-day average.
- If no breakout fill occurs within three trading days, the candidate expires and the tester rotates to another qualified candidate.
- Exit at measured target, stop out at handle low, or use a 60-trading-day time stop so capital is not trapped indefinitely.
- If stop and target are both touched on the same day, the stop is assumed first.

## Data Audit

- Historical universe symbols considered: `816`
- Historical membership file coverage used: `2005-10-28` to `2025-08-23`
- Symbols with usable Yahoo adjusted daily OHLCV: `510`
- Signals generated: `13753`
- Trades executed: `142`

## Performance Summary

| Segment | Total Return % | CAGR % | Max Drawdown % | Sharpe | Trades | Win Rate % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Strategy IS 2010-01-01 to 2020-01-01 | 262.33 | 13.76 | -17.42 | 0.905 | 80 | 52.5 |
| S&P 500 IS 2010-01-01 to 2020-01-01 | 185.16 | 11.06 | -19.78 | 0.785 | 0 | nan |
| Strategy OOS 2020-01-01 to 2026-05-30 | 173.94 | 17.04 | -16.49 | 1.008 | 62 | 53.23 |
| S&P 500 OOS 2020-01-01 to 2026-05-30 | 132.67 | 14.1 | -33.92 | 0.747 | 0 | nan |

## Exit Reason Counts

- `time_stop`: 71
- `stop`: 56
- `target`: 15

## Last 20 Trades

| Symbol | EntryDate | ExitDate | EntryPrice | ExitPrice | ReturnPct | ExitReason | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PODD | 2024-06-24 | 2024-07-08 | 204.74 | 193.74 | -5.37 | stop | 72.26 |
| JCI | 2024-05-20 | 2024-08-14 | 66.55 | 67.097 | 0.82 | time_stop | 86.47 |
| NEM | 2024-07-11 | 2024-10-03 | 43.27 | 51.7776 | 19.66 | time_stop | 81.81 |
| GILD | 2024-09-12 | 2024-12-05 | 77.51 | 89.5841 | 15.58 | time_stop | 74.2 |
| HPE | 2025-01-06 | 2025-01-28 | 21.33 | 20.44 | -4.17 | stop | 72.82 |
| EXPE | 2024-11-06 | 2025-02-04 | 164.57 | 166.4059 | 1.12 | time_stop | 81.76 |
| DAL | 2024-11-06 | 2025-02-04 | 58.17 | 67.8756 | 16.68 | time_stop | 81.26 |
| HSY | 2025-03-07 | 2025-03-17 | 177.4 | 163.25 | -7.98 | stop | 63.87 |
| CVS | 2025-02-12 | 2025-05-08 | 55.82 | 65.456 | 17.26 | time_stop | 74.83 |
| LUV | 2025-07-10 | 2025-07-30 | 33.99 | 30.29 | -10.89 | stop | 82.81 |
| DXCM | 2025-07-30 | 2025-08-01 | 89.96 | 79.4 | -11.74 | stop | 87.65 |
| META | 2025-07-31 | 2025-10-06 | 746.15 | 690.03 | -7.52 | stop | 82.69 |
| INCY | 2025-08-13 | 2025-11-05 | 81.82 | 105.7 | 29.19 | time_stop | 86.61 |
| IQV | 2025-10-01 | 2025-12-24 | 196.22 | 226.02 | 15.19 | time_stop | 75.08 |
| HOLX | 2025-10-20 | 2026-01-14 | 70.9 | 75.16 | 6.01 | time_stop | 77.29 |
| WAT | 2025-11-24 | 2026-02-09 | 391.79 | 350.65 | -10.5 | stop | 80.64 |
| DOW | 2026-02-03 | 2026-03-19 | 28.46 | 37.94 | 33.31 | target | 83.61 |
| DOW | 2026-03-31 | 2026-04-17 | 40.64 | 35.19 | -13.41 | stop | 62.41 |
| MRNA | 2026-03-04 | 2026-05-28 | 54.94 | 47.57 | -13.41 | time_stop | 66.59 |
| HPE | 2026-05-13 | 2026-05-29 | 31.64 | 41.56 | 31.35 | target | 74.48 |
