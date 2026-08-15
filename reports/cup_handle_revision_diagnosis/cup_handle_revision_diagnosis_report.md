# Cup-And-Handle OOS Diagnosis And Revised 3-Stock Rule

This is technical strategy research, not investment advice.

## Diagnosis

- The original 3-stock IS winner did not mainly fail during the 2022 bear market; it underperformed most in bull years.
- Original OOS annual underperformance was largest in 2021, 2023, 2024, and 2025.
- Stop exits had poor expectancy, while time-stop exits were usually profitable. Tightening stops alone was not the fix.
- The stronger fix was entry quality: require stock relative strength versus S&P 500 and use a faster market filter.

## Revised Rule

- Entry stock filter: `Close > SMA50` and 63-day stock return greater than S&P 500 63-day return.
- Entry market filter: `S&P 500 close > SMA100`.
- Exit: `ATR14 3.5x initial stop`, no measured target, 60-trading-day time stop.
- Portfolio: maximum 3 concurrent stocks.

## Summary

| Segment | Revised Strategy Return % | S&P 500 Return % | Strategy Max DD % | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| IS | 193.57 | 185.16 | -18.48 | 0.83 |
| OOS | 134.36 | 132.67 | -15.92 | 0.937 |

## Original OOS Annual Return/Drawdown

| Year | StrategyReturnPct | SP500ReturnPct | ExcessPct | StrategyMaxDDPct | SP500MaxDDPct |
| --- | --- | --- | --- | --- | --- |
| 2020.0 | 14.14 | 15.29 | -1.16 | -10.06 | -33.92 |
| 2021.0 | 7.53 | 28.79 | -21.27 | -17.17 | -5.21 |
| 2022.0 | -9.71 | -19.95 | 10.24 | -9.77 | -25.43 |
| 2023.0 | 14.09 | 24.73 | -10.64 | -7.24 | -10.28 |
| 2024.0 | 12.7 | 24.01 | -11.31 | -8.88 | -8.49 |
| 2025.0 | 0.18 | 16.65 | -16.47 | -14.85 | -18.9 |
| 2026.0 | 10.97 | 10.52 | 0.45 | -6.96 | -9.1 |

## Revised OOS Annual Return/Drawdown

| Year | StrategyReturnPct | SP500ReturnPct | ExcessPct | StrategyMaxDDPct | SP500MaxDDPct |
| --- | --- | --- | --- | --- | --- |
| 2020.0 | 22.35 | 15.29 | 7.05 | -7.86 | -33.92 |
| 2021.0 | 29.87 | 28.79 | 1.08 | -15.09 | -5.21 |
| 2022.0 | -2.89 | -19.95 | 17.06 | -11.69 | -25.43 |
| 2023.0 | 13.38 | 24.73 | -11.35 | -9.22 | -10.28 |
| 2024.0 | 19.26 | 24.01 | -4.75 | -5.33 | -8.49 |
| 2025.0 | 0.54 | 16.65 | -16.11 | -11.01 | -18.9 |
| 2026.0 | 16.04 | 10.52 | 5.52 | -6.85 | -9.1 |

## Original OOS Trade By Year

| Year | Trades | AvgReturnPct | MedianReturnPct | WinRatePct | Stops | AtrStops | Targets | TimeStops |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020.0 | 8.0 | 5.18 | 1.68 | 62.5 | 2.0 | 0.0 | 0.0 | 6.0 |
| 2021.0 | 15.0 | 0.29 | -6.15 | 40.0 | 8.0 | 0.0 | 0.0 | 7.0 |
| 2022.0 | 3.0 | -2.6 | -11.53 | 33.33 | 2.0 | 0.0 | 0.0 | 1.0 |
| 2023.0 | 12.0 | 5.91 | 9.5 | 66.67 | 3.0 | 0.0 | 0.0 | 9.0 |
| 2024.0 | 11.0 | 1.46 | 2.51 | 54.55 | 4.0 | 0.0 | 0.0 | 7.0 |
| 2025.0 | 10.0 | 0.47 | -8.53 | 40.0 | 6.0 | 0.0 | 1.0 | 3.0 |
| 2026.0 | 4.0 | 7.15 | 6.3 | 50.0 | 2.0 | 0.0 | 1.0 | 1.0 |

## Revised OOS Trade By Year

| Year | Trades | AvgReturnPct | MedianReturnPct | WinRatePct | Stops | AtrStops | Targets | TimeStops |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2020.0 | 9.0 | 7.47 | 1.1 | 66.67 | 2.0 | 0.0 | 0.0 | 7.0 |
| 2021.0 | 14.0 | 5.95 | 2.88 | 57.14 | 6.0 | 0.0 | 0.0 | 8.0 |
| 2022.0 | 9.0 | -0.37 | -5.47 | 44.44 | 4.0 | 0.0 | 0.0 | 5.0 |
| 2023.0 | 11.0 | 5.97 | 8.26 | 63.64 | 1.0 | 0.0 | 0.0 | 10.0 |
| 2024.0 | 12.0 | 2.23 | 0.14 | 50.0 | 4.0 | 0.0 | 0.0 | 8.0 |
| 2025.0 | 12.0 | -0.46 | -7.08 | 25.0 | 9.0 | 0.0 | 0.0 | 3.0 |
| 2026.0 | 5.0 | 10.19 | 9.2 | 60.0 | 2.0 | 0.0 | 0.0 | 3.0 |

## Original OOS Exit Summary

| ExitReason | Trades | AvgReturnPct | MedianReturnPct | WinRatePct |
| --- | --- | --- | --- | --- |
| stop | 27 | -9.84 | -9.4 | 0.0 |
| target | 2 | 33.02 | 33.02 | 100.0 |
| time_stop | 34 | 10.53 | 11.06 | 88.24 |

## Revised OOS Exit Summary

| ExitReason | Trades | AvgReturnPct | MedianReturnPct | WinRatePct |
| --- | --- | --- | --- | --- |
| stop | 28 | -7.61 | -7.08 | 0.0 |
| time_stop | 44 | 11.32 | 11.55 | 84.09 |

## Original OOS Exposure By Year

| Year | AvgExposurePct | MedianExposurePct | AvgOpenPositions | Days |
| --- | --- | --- | --- | --- |
| 2020.0 | 54.05 | 66.39 | 1.59 | 253.0 |
| 2021.0 | 72.77 | 68.88 | 2.2 | 252.0 |
| 2022.0 | 17.29 | 0.0 | 0.49 | 251.0 |
| 2023.0 | 65.05 | 86.84 | 1.94 | 250.0 |
| 2024.0 | 80.5 | 92.97 | 2.45 | 252.0 |
| 2025.0 | 55.84 | 65.91 | 1.67 | 250.0 |
| 2026.0 | 59.95 | 66.76 | 1.79 | 102.0 |

## Revised OOS Exposure By Year

| Year | AvgExposurePct | MedianExposurePct | AvgOpenPositions | Days |
| --- | --- | --- | --- | --- |
| 2020.0 | 59.25 | 66.65 | 1.75 | 253.0 |
| 2021.0 | 70.46 | 67.64 | 2.11 | 252.0 |
| 2022.0 | 47.51 | 66.2 | 1.39 | 251.0 |
| 2023.0 | 77.35 | 99.93 | 2.32 | 250.0 |
| 2024.0 | 76.94 | 68.66 | 2.31 | 252.0 |
| 2025.0 | 57.48 | 66.28 | 1.72 | 250.0 |
| 2026.0 | 66.97 | 100.0 | 2.04 | 102.0 |
