# SOXL/TQQQ Cup-And-Handle Test

This is technical strategy research, not investment advice.

## Setup

- Universe: `SOXL, TQQQ`
- Pattern data: weekly OHLCV.
- Execution data: daily OHLCV.
- Candidate filter: `TargetReturnPct > 30%`.
- Breakout fill window: 3 trading days.
- Entry filter: `Close > SMA50`, ETF 63-day return greater than S&P 500 63-day return, and S&P 500 close > SMA100.
- Exit: `ATR14 3.5x initial stop`, no measured target, 60-trading-day time stop.
- Max concurrent positions: 2, because the universe has only two symbols.

## Summary

| Segment | Strategy Return % | S&P 500 Return % | Strategy Max DD % | Sharpe | Trades |
| --- | ---: | ---: | ---: | ---: | ---: |
| IS | 10.21 | 185.16 | -6.21 | 0.323 | 1 |
| OOS | 27.89 | 132.67 | -6.08 | 0.583 | 2 |

## Data Audit

- Signals generated: `28`
- Trades executed: `3`

## OOS Annual Return/Drawdown

| Year | StrategyReturnPct | SP500ReturnPct | ExcessPct | StrategyMaxDDPct | SP500MaxDDPct |
| --- | --- | --- | --- | --- | --- |
| 2020.0 | 0.0 | 15.29 | -15.29 | 0.0 | -33.92 |
| 2021.0 | 0.0 | 28.79 | -28.79 | 0.0 | -5.21 |
| 2022.0 | 0.0 | -19.95 | 19.95 | 0.0 | -25.43 |
| 2023.0 | 26.32 | 24.73 | 1.59 | -5.81 | -10.28 |
| 2024.0 | 1.24 | 24.01 | -22.77 | -6.08 | -8.49 |
| 2025.0 | 0.0 | 16.65 | -16.65 | 0.0 | -18.9 |
| 2026.0 | 0.0 | 10.52 | -10.52 | 0.0 | -9.1 |

## OOS Trade By Year

| Year | Trades | AvgReturnPct | MedianReturnPct | WinRatePct | Stops | AtrStops | Targets | TimeStops |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023.0 | 1.0 | 52.65 | 52.65 | 100.0 | 0.0 | 0.0 | 0.0 | 1.0 |
| 2024.0 | 1.0 | 2.48 | 2.48 | 100.0 | 0.0 | 0.0 | 0.0 | 1.0 |

## OOS Exit Summary

| ExitReason | Trades | AvgReturnPct | MedianReturnPct | WinRatePct |
| --- | --- | --- | --- | --- |
| time_stop | 2 | 27.56 | 27.56 | 100.0 |

## OOS Exposure By Year

| Year | AvgExposurePct | MedianExposurePct | AvgOpenPositions | Days |
| --- | --- | --- | --- | --- |
| 2020.0 | 0.0 | 0.0 | 0.0 | 253.0 |
| 2021.0 | 0.0 | 0.0 | 0.0 | 252.0 |
| 2022.0 | 0.0 | 0.0 | 0.0 | 251.0 |
| 2023.0 | 13.2 | 0.0 | 0.24 | 250.0 |
| 2024.0 | 12.16 | 0.0 | 0.23 | 252.0 |
| 2025.0 | 0.0 | 0.0 | 0.0 | 250.0 |
| 2026.0 | 0.0 | 0.0 | 0.0 | 102.0 |

## Last 20 Trades

| Symbol | EntryDate | ExitDate | EntryPrice | ExitPrice | ReturnPct | ExitReason | Score |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TQQQ | 2013-03-25 | 2013-06-18 | 0.6 | 0.7225 | 20.42 | time_stop | 68.25 |
| TQQQ | 2023-05-01 | 2023-07-26 | 13.73 | 20.9586 | 52.65 | time_stop | 75.97 |
| TQQQ | 2024-01-22 | 2024-04-16 | 26.67 | 27.3305 | 2.48 | time_stop | 66.68 |
