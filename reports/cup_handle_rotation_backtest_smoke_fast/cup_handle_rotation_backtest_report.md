# Cup-And-Handle Rotation Strategy Backtest

This is technical strategy research, not investment advice.

## Strategy Rules

- Point-in-time S&P 500 membership comes from the public `hanshof/sp500_constituents` historical constituents file.
- Dates after the membership file's latest row use the last available constituent snapshot.
- Weekly cup-and-handle patterns are scanned after each completed week.
- Candidates must score above the configured threshold and have target return greater than 30%, where target return is `target / breakout - 1`.
- Portfolio can hold up to three concurrent stocks.
- Buy uses a breakout stop: enter if the stock trades at or above the breakout level within the next three trading days.
- If no breakout fill occurs within three trading days, the candidate expires and the tester rotates to another qualified candidate.
- Exit at measured target, stop out at handle low, or use a 60-trading-day time stop so capital is not trapped indefinitely.
- If stop and target are both touched on the same day, the stop is assumed first.

## Data Audit

- Historical universe symbols considered: `20`
- Historical membership file coverage used: `2005-10-28` to `2025-08-23`
- Symbols with usable Yahoo adjusted daily OHLCV: `14`
- Signals generated: `391`
- Trades executed: `29`

## Performance Summary

| Segment | Total Return % | CAGR % | Max Drawdown % | Sharpe | Trades | Win Rate % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Strategy IS 2010-01-01 to 2020-01-01 | 14.22 | 1.34 | -12.42 | 0.322 | 16 | 37.5 |
| S&P 500 IS 2010-01-01 to 2020-01-01 | 185.16 | 11.06 | -19.78 | 0.785 | 0 | nan |
| Strategy OOS 2020-01-01 to 2026-05-30 | -10.28 | -1.68 | -16.3 | -0.347 | 13 | 30.77 |
| S&P 500 OOS 2020-01-01 to 2026-05-30 | 132.67 | 14.1 | -33.92 | 0.747 | 0 | nan |

## Exit Reason Counts

- `stop`: 15
- `time_stop`: 14

## Last 20 Trades

| Symbol | EntryDate | ExitDate | EntryPrice | ExitPrice | ReturnPct | ExitReason | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADM | 2016-07-18 | 2016-10-10 | 32.85 | 32.4279 | -1.28 | time_stop | 75.24 |
| ADI | 2016-10-05 | 2016-12-29 | 54.41 | 61.8824 | 13.73 | time_stop | 86.0 |
| AAL | 2016-10-11 | 2017-01-05 | 38.09 | 44.345 | 16.42 | time_stop | 70.22 |
| ADM | 2016-11-08 | 2017-02-03 | 35.88 | 33.2062 | -7.45 | time_stop | 57.32 |
| AAP | 2018-03-13 | 2018-04-19 | 104.38 | 90.75 | -13.06 | stop | 74.59 |
| AAP | 2018-05-22 | 2018-08-15 | 107.06 | 138.4025 | 29.28 | time_stop | 65.76 |
| AAPL | 2019-09-09 | 2019-12-02 | 51.49 | 63.6182 | 23.55 | time_stop | 66.26 |
| ABBV | 2020-02-10 | 2020-03-12 | 72.29 | 62.52 | -13.52 | stop | 77.92 |
| ABBV | 2020-07-01 | 2020-09-08 | 78.4 | 71.63 | -8.64 | stop | 66.33 |
| ADM | 2020-07-28 | 2020-10-20 | 36.26 | 43.3221 | 19.48 | time_stop | 70.2 |
| A | 2022-12-13 | 2023-01-06 | 153.41 | 140.73 | -8.27 | stop | 82.91 |
| ADI | 2023-04-03 | 2023-04-27 | 187.83 | 168.95 | -10.05 | stop | 66.23 |
| AAPL | 2023-07-19 | 2023-08-04 | 191.79 | 182.67 | -4.76 | stop | 63.14 |
| ACN | 2023-08-29 | 2023-09-28 | 310.64 | 288.71 | -7.06 | stop | 78.49 |
| A | 2024-03-04 | 2024-05-28 | 138.6 | 145.9176 | 5.28 | time_stop | 66.62 |
| ADM | 2025-10-15 | 2025-11-04 | 62.95 | 56.88 | -9.64 | stop | 71.43 |
| ADI | 2025-08-26 | 2025-11-18 | 254.5 | 228.6043 | -10.18 | time_stop | 67.21 |
| A | 2025-10-01 | 2025-12-24 | 130.21 | 137.7589 | 5.8 | time_stop | 67.22 |
| AAPL | 2025-11-25 | 2026-01-06 | 276.54 | 263.9 | -4.57 | stop | 58.36 |
| ADM | 2026-01-12 | 2026-04-08 | 61.55 | 71.2502 | 15.76 | time_stop | 77.72 |
