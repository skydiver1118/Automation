# Cup-And-Handle ATR Exit Variant Search

This is technical strategy research, not investment advice.

## Setup

- Saved cup-and-handle signals tested: `16916`
- Symbols with usable cached data: `510`
- Entry stock condition: `stock_close_gt_sma200_sma200_rising`
- Entry market condition: `market_spx_close_gt_sma200_sma200_rising`
- Exit variants tested: initial ATR stops, handle/ATR tighter or wider stops, ATR trailing stops, target on/off.
- Selection rule: rank by IS total return; evaluate the IS winner OOS.

## Benchmark

| Segment | Total Return % | CAGR % | Max Drawdown % | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| S&P 500 IS | 185.16 | 11.06 | -19.78 | 0.785 |
| S&P 500 OOS | 132.67 | 14.1 | -33.92 | 0.747 |

## Selected IS Winner

- Variant: `wider_1.5x_target_60d`
- IS return: `273.95%` versus S&P 500 `185.16%`
- OOS return: `55.85%` versus S&P 500 `132.67%`
- OOS max drawdown: `-27.49%`
- ATR variants beating S&P 500 IS: `10`
- ATR variants beating S&P 500 OOS: `0`

## Top 15 By IS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| wider_1.5x_target_60d | 273.95 | 14.12 | -15.93 | 0.968 | 92 | 55.85 | 7.17 | -27.49 | 0.552 | 63 |
| wider_1.5x_no_target_60d | 273.95 | 14.12 | -15.93 | 0.968 | 92 | 54.42 | 7.02 | -27.49 | 0.542 | 63 |
| wider_2x_target_60d | 273.95 | 14.12 | -15.93 | 0.968 | 92 | 55.85 | 7.17 | -27.49 | 0.552 | 63 |
| wider_2x_no_target_60d | 273.95 | 14.12 | -15.93 | 0.968 | 92 | 54.42 | 7.02 | -27.49 | 0.542 | 63 |
| wider_2.5x_target_60d | 273.95 | 14.12 | -15.93 | 0.968 | 92 | 55.85 | 7.17 | -27.49 | 0.552 | 63 |
| wider_2.5x_no_target_60d | 273.95 | 14.12 | -15.93 | 0.968 | 92 | 54.42 | 7.02 | -27.49 | 0.542 | 63 |
| wider_3x_target_60d | 273.52 | 14.1 | -15.93 | 0.967 | 92 | 54.38 | 7.02 | -28.13 | 0.541 | 63 |
| wider_3x_no_target_60d | 273.52 | 14.1 | -15.93 | 0.967 | 92 | 52.96 | 6.86 | -28.13 | 0.531 | 63 |
| wider_3.5x_target_60d | 270.45 | 14.01 | -15.93 | 0.961 | 92 | 41.31 | 5.55 | -29.56 | 0.441 | 63 |
| wider_3.5x_no_target_60d | 270.45 | 14.01 | -15.93 | 0.961 | 92 | 41.38 | 5.56 | -29.56 | 0.442 | 63 |
| tighter_3x_target_60d | 130.9 | 8.74 | -13.99 | 0.706 | 101 | 27.7 | 3.89 | -30.33 | 0.335 | 73 |
| tighter_3x_no_target_60d | 130.9 | 8.74 | -13.99 | 0.706 | 101 | 26.56 | 3.75 | -30.33 | 0.325 | 73 |
| atr_3x_target_60d | 129.72 | 8.68 | -13.99 | 0.702 | 101 | 26.57 | 3.75 | -30.91 | 0.325 | 73 |
| atr_3x_no_target_60d | 129.72 | 8.68 | -13.99 | 0.702 | 101 | 25.44 | 3.6 | -30.91 | 0.316 | 73 |
| tighter_3.5x_target_60d | 119.79 | 8.2 | -15.81 | 0.655 | 99 | 56.22 | 7.21 | -20.72 | 0.56 | 69 |

## Top 10 By OOS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tighter_3.5x_target_60d | 119.79 | 8.2 | -15.81 | 0.655 | 99 | 56.22 | 7.21 | -20.72 | 0.56 | 69 |
| wider_1.5x_target_60d | 273.95 | 14.12 | -15.93 | 0.968 | 92 | 55.85 | 7.17 | -27.49 | 0.552 | 63 |
| wider_2.5x_target_60d | 273.95 | 14.12 | -15.93 | 0.968 | 92 | 55.85 | 7.17 | -27.49 | 0.552 | 63 |
| wider_2x_target_60d | 273.95 | 14.12 | -15.93 | 0.968 | 92 | 55.85 | 7.17 | -27.49 | 0.552 | 63 |
| tighter_3.5x_no_target_60d | 119.79 | 8.2 | -15.81 | 0.655 | 99 | 54.81 | 7.06 | -20.72 | 0.55 | 69 |
| wider_1.5x_no_target_60d | 273.95 | 14.12 | -15.93 | 0.968 | 92 | 54.42 | 7.02 | -27.49 | 0.542 | 63 |
| wider_2x_no_target_60d | 273.95 | 14.12 | -15.93 | 0.968 | 92 | 54.42 | 7.02 | -27.49 | 0.542 | 63 |
| wider_2.5x_no_target_60d | 273.95 | 14.12 | -15.93 | 0.968 | 92 | 54.42 | 7.02 | -27.49 | 0.542 | 63 |
| wider_3x_target_60d | 273.52 | 14.1 | -15.93 | 0.967 | 92 | 54.38 | 7.02 | -28.13 | 0.541 | 63 |
| wider_3x_no_target_60d | 273.52 | 14.1 | -15.93 | 0.967 | 92 | 52.96 | 6.86 | -28.13 | 0.531 | 63 |

