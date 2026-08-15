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
- Signals generated: `6212`
- Trades executed: `105`

## Performance Summary

| Segment | Total Return % | CAGR % | Max Drawdown % | Sharpe | Trades | Win Rate % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Strategy IS 2010-01-01 to 2020-01-01 | 68.84 | 5.38 | -18.14 | 0.484 | 62 | 56.45 |
| S&P 500 IS 2010-01-01 to 2020-01-01 | 185.16 | 11.06 | -19.78 | 0.785 | 0 | nan |
| Strategy OOS 2020-01-01 to 2026-05-30 | 55.05 | 7.09 | -15.73 | 0.614 | 43 | 48.84 |
| S&P 500 OOS 2020-01-01 to 2026-05-30 | 132.67 | 14.1 | -33.92 | 0.747 | 0 | nan |

## Exit Reason Counts

- `time_stop`: 69
- `stop`: 35
- `target`: 1

## Last 20 Trades

| Symbol | EntryDate | ExitDate | EntryPrice | ExitPrice | ReturnPct | ExitReason | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HCA | 2023-04-11 | 2023-07-06 | 266.25 | 288.2506 | 8.26 | time_stop | 83.76 |
| MCO | 2023-07-25 | 2023-08-16 | 352.63 | 323.59 | -8.24 | stop | 79.7 |
| FDX | 2023-07-11 | 2023-10-03 | 239.01 | 246.8898 | 3.3 | time_stop | 78.56 |
| TTWO | 2023-07-11 | 2023-10-03 | 149.04 | 137.56 | -7.7 | time_stop | 77.71 |
| NRG | 2023-11-01 | 2024-01-29 | 40.49 | 52.1698 | 28.85 | time_stop | 81.21 |
| GPN | 2024-02-14 | 2024-04-04 | 134.42 | 123.13 | -8.4 | stop | 83.1 |
| JCI | 2024-05-20 | 2024-08-14 | 67.7 | 67.097 | -0.89 | time_stop | 75.99 |
| EXR | 2024-06-18 | 2024-09-12 | 146.6 | 164.2537 | 12.04 | time_stop | 79.0 |
| PNC | 2024-07-15 | 2024-10-07 | 158.28 | 171.6182 | 8.43 | time_stop | 82.04 |
| DIS | 2025-02-05 | 2025-03-06 | 116.81 | 105.0 | -10.11 | stop | 80.63 |
| JBL | 2024-12-18 | 2025-03-18 | 138.81 | 135.3783 | -2.47 | time_stop | 82.86 |
| PAYC | 2025-02-24 | 2025-04-04 | 215.2 | 194.66 | -9.54 | stop | 80.81 |
| DG | 2025-05-20 | 2025-08-14 | 94.97 | 112.9904 | 18.97 | time_stop | 65.88 |
| AMZN | 2025-09-10 | 2025-10-17 | 236.53 | 211.42 | -10.62 | stop | 83.25 |
| CDNS | 2025-07-29 | 2025-10-21 | 335.16 | 333.45 | -0.51 | time_stop | 86.92 |
| HUBB | 2025-10-28 | 2025-11-20 | 449.12 | 404.63 | -9.91 | stop | 82.58 |
| INCY | 2025-10-27 | 2026-01-22 | 92.86 | 105.06 | 13.14 | time_stop | 77.73 |
| HST | 2025-11-10 | 2026-02-05 | 17.61 | 18.7996 | 6.76 | time_stop | 79.82 |
| TMO | 2026-01-05 | 2026-02-05 | 601.27 | 553.98 | -7.87 | stop | 84.77 |
| VRTX | 2026-03-10 | 2026-03-19 | 503.88 | 450.67 | -10.56 | stop | 70.8 |
