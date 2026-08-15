# SMH Historical Components Daily Cup-And-Handle Backtest

This is technical strategy research, not investment advice.

## Setup

- Holdings source: `data\smh_components\smh_historical_holdings_sec.csv`.
- Universe logic: latest SMH/legacy Semiconductor HOLDRS holdings snapshot whose SEC filing date was public on or before the signal date.
- Pattern timeframe: daily cup-and-handle, scanned every 5 trading days.
- Candidate pool: top 10 by score after `TargetReturnPct > 30%`.
- Entry window: 7 trading days.
- Entry filters: stock close > SMA50, stock 63-day return > SMH 63-day return, and SMH close > SMA100.
- Entry volume: breakout-day volume >= 1.40x prior 50-day average.
- Exit: ATR14 3.5x stop, no target, 60-trading-day time stop.
- Portfolio: max 3 concurrent stocks.

## Data Audit

- Historical SMH tickers in SEC holdings file: `41`
- Price-available tickers including SMH: `32`
- Signals generated: `1507`
- IS trades: `47`
- OOS trades: `30`

## IS/OOS Comparison

| Strategy | IS_ReturnPct | IS_MaxDrawdownPct | IS_Sharpe | IS_Trades | OOS_ReturnPct | OOS_MaxDrawdownPct | OOS_Sharpe | OOS_Trades |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SMH component daily cup/handle | 54.1 | -20.25 | 0.403 | 47 | 230.45 | -21.86 | 0.985 | 30 |
| SMH buy-and-hold | 464.8 | -27.02 | 0.88 |  | 759.25 | -45.3 | 1.102 |  |
| SMH Top2 L252 S0 SMA100 DCA1 | 2249.91 | -22.84 | 1.374 |  | 993.6 | -26.89 | 1.232 |  |

## Annual Return / Drawdown

| Strategy | Year | AnnualReturnPct | MaxDrawdownPct | Trades |
| --- | --- | --- | --- | --- |
| CupHandle IS | 2010 | -6.16 | -17.05 | 5 |
| CupHandle IS | 2011 | 4.92 | -9.52 | 4 |
| CupHandle IS | 2012 | 0.76 | -11.28 | 6 |
| CupHandle IS | 2013 | -3.11 | -8.22 | 4 |
| CupHandle IS | 2014 | -1.85 | -6.96 | 3 |
| CupHandle IS | 2015 | 30.37 | -12.05 | 6 |
| CupHandle IS | 2016 | 2.71 | -16.94 | 6 |
| CupHandle IS | 2017 | 1.89 | -10.89 | 4 |
| CupHandle IS | 2018 | 11.88 | -11.81 | 3 |
| CupHandle IS | 2019 | 9.83 | -15.21 | 6 |
| CupHandle OOS | 2020 | 0.83 | -14.81 | 6 |
| CupHandle OOS | 2021 | 26.92 | -10.84 | 5 |
| CupHandle OOS | 2022 | -20.35 | -20.98 | 1 |
| CupHandle OOS | 2023 | 13.73 | -9.69 | 6 |
| CupHandle OOS | 2024 | 22.92 | -13.65 | 5 |
| CupHandle OOS | 2025 | 46.91 | -13.35 | 5 |
| CupHandle OOS | 2026 | 55.5 | -13.09 | 2 |
| SMH IS | 2010 | 14.5 | -20.3 | 0 |
| SMH IS | 2011 | -6.91 | -26.07 | 0 |
| SMH IS | 2012 | 7.07 | -16.93 | 0 |
| SMH IS | 2013 | 28.25 | -7.05 | 0 |
| SMH IS | 2014 | 31.59 | -14.52 | 0 |
| SMH IS | 2015 | -0.1 | -23.66 | 0 |
| SMH IS | 2016 | 36.98 | -13.45 | 0 |
| SMH IS | 2017 | 38.25 | -9.14 | 0 |
| SMH IS | 2018 | -11.37 | -27.02 | 0 |
| SMH IS | 2019 | 63.25 | -17.96 | 0 |
| SMH OOS | 2020 | 52.02 | -33.62 | 0 |
| SMH OOS | 2021 | 41.85 | -15.58 | 0 |
| SMH OOS | 2022 | -34.97 | -45.14 | 0 |
| SMH OOS | 2023 | 74.72 | -14.42 | 0 |
| SMH OOS | 2024 | 43.96 | -24.82 | 0 |
| SMH OOS | 2025 | 47.58 | -32.65 | 0 |
| SMH OOS | 2026 | 60.44 | -14.93 | 0 |

## Outputs

- Signals: `reports\smh_daily_cup_handle\smh_daily_cup_handle_signals.csv`
- Comparison CSV: `reports\smh_daily_cup_handle\smh_daily_cup_handle_comparison.csv`
- Annual CSV: `reports\smh_daily_cup_handle\smh_daily_cup_handle_annual_return_drawdown.csv`
- OOS curve: `reports\smh_daily_cup_handle\smh_daily_cup_handle_oos_curves.png`
