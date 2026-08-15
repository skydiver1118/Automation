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

- Historical universe symbols considered: `816`
- Historical membership file coverage used: `2005-10-28` to `2025-08-23`
- Symbols with usable Yahoo adjusted daily OHLCV: `647`
- Signals generated: `16916`
- Trades executed: `192`

## Performance Summary

| Segment | Total Return % | CAGR % | Max Drawdown % | Sharpe | Trades | Win Rate % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Strategy IS 2010-01-01 to 2020-01-01 | 172.14 | 10.54 | -22.72 | 0.739 | 112 | 50.89 |
| S&P 500 IS 2010-01-01 to 2020-01-01 | 185.16 | 11.06 | -19.78 | 0.785 | 0 | nan |
| Strategy OOS 2020-01-01 to 2026-05-30 | 19.29 | 2.79 | -34.99 | 0.249 | 80 | 50.0 |
| S&P 500 OOS 2020-01-01 to 2026-05-30 | 132.67 | 14.1 | -33.92 | 0.747 | 0 | nan |

## Exit Reason Counts

- `time_stop`: 118
- `stop`: 72
- `target`: 2

## Last 20 Trades

| Symbol | EntryDate | ExitDate | EntryPrice | ExitPrice | ReturnPct | ExitReason | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADSK | 2024-09-30 | 2024-12-23 | 275.68 | 297.49 | 7.91 | time_stop | 87.22 |
| PODD | 2024-11-11 | 2025-02-07 | 275.52 | 283.08 | 2.74 | time_stop | 75.71 |
| DIS | 2025-02-05 | 2025-03-06 | 116.81 | 105.0 | -10.11 | stop | 80.63 |
| JBL | 2024-12-18 | 2025-03-18 | 138.81 | 135.3782 | -2.47 | time_stop | 82.86 |
| PAYC | 2025-02-24 | 2025-04-04 | 215.2 | 194.66 | -9.54 | stop | 80.81 |
| HCA | 2025-07-01 | 2025-07-22 | 386.74 | 349.07 | -9.74 | stop | 79.11 |
| DG | 2025-05-19 | 2025-08-13 | 94.97 | 114.0642 | 20.11 | time_stop | 65.88 |
| DLR | 2025-07-22 | 2025-08-21 | 174.99 | 160.11 | -8.5 | stop | 86.93 |
| EXPE | 2025-06-09 | 2025-09-03 | 175.4 | 211.2778 | 20.45 | time_stop | 71.35 |
| NKE | 2025-08-25 | 2025-09-12 | 78.55 | 71.22 | -9.33 | stop | 83.57 |
| META | 2025-08-13 | 2025-10-06 | 782.91 | 689.58 | -11.92 | stop | 85.65 |
| MLM | 2025-10-06 | 2025-11-06 | 635.73 | 598.47 | -5.86 | stop | 88.38 |
| USB | 2025-09-04 | 2025-11-26 | 47.58 | 47.9858 | 0.85 | time_stop | 82.88 |
| BKR | 2025-09-16 | 2025-12-09 | 46.76 | 47.3524 | 1.27 | time_stop | 82.44 |
| A | 2025-11-26 | 2025-12-09 | 152.05 | 139.67 | -8.14 | stop | 81.89 |
| TMO | 2026-01-05 | 2026-02-05 | 601.27 | 553.98 | -7.87 | stop | 84.77 |
| CSX | 2025-12-10 | 2026-03-09 | 36.82 | 40.4759 | 9.93 | time_stop | 79.74 |
| PHM | 2026-02-17 | 2026-03-19 | 143.35 | 115.8 | -19.22 | stop | 80.7 |
| BG | 2026-01-12 | 2026-03-27 | 98.95 | 129.56 | 30.93 | target | 90.48 |
| EMN | 2026-05-04 | 2026-05-19 | 77.77 | 69.91 | -10.11 | stop | 84.02 |
