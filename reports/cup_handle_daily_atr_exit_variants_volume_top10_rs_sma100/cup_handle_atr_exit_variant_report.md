# Cup-And-Handle ATR Exit Variant Search

This is technical strategy research, not investment advice.

## Setup

- Saved cup-and-handle signals tested: `13739`
- Symbols with usable cached data: `389`
- Entry stock condition: `stock_close_gt_sma50_rs63_gt_spx`
- Entry market condition: `market_spx_close_gt_sma100`
- Entry volume condition: `enabled`, breakout-day volume >= 1.40x prior 50-day average.
- Exit variants tested: initial ATR stops, handle/ATR tighter or wider stops, ATR trailing stops, target on/off.
- Selection rule: rank by IS total return; evaluate the IS winner OOS.

## Benchmark

| Segment | Total Return % | CAGR % | Max Drawdown % | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| S&P 500 IS | 185.16 | 11.06 | -19.78 | 0.785 |
| S&P 500 OOS | 132.67 | 14.1 | -33.92 | 0.747 |

## Selected IS Winner

- Variant: `tighter_3x_atrtrail_target_60d`
- IS return: `296.68%` versus S&P 500 `185.16%`
- OOS return: `99.17%` versus S&P 500 `132.67%`
- OOS max drawdown: `-15.63%`
- ATR variants beating S&P 500 IS: `31`
- ATR variants beating S&P 500 OOS: `20`

## Top 15 By IS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tighter_3x_atrtrail_target_60d | 296.68 | 14.79 | -16.59 | 1.223 | 100 | 99.17 | 11.36 | -15.63 | 0.911 | 71 |
| handle_3x_atrtrail_target_60d | 296.68 | 14.79 | -16.59 | 1.223 | 100 | 97.46 | 11.21 | -15.63 | 0.899 | 71 |
| tighter_3x_atrtrail_no_target_60d | 295.78 | 14.77 | -16.59 | 1.172 | 98 | 94.7 | 10.97 | -15.63 | 0.871 | 70 |
| atr_3x_atrtrail_target_60d | 294.89 | 14.74 | -16.59 | 1.219 | 100 | 98.79 | 11.33 | -15.63 | 0.909 | 71 |
| wider_3x_atrtrail_target_60d | 294.89 | 14.74 | -16.59 | 1.219 | 100 | 97.09 | 11.18 | -15.63 | 0.897 | 71 |
| atr_3x_atrtrail_no_target_60d | 293.99 | 14.72 | -16.59 | 1.169 | 98 | 94.34 | 10.93 | -15.63 | 0.868 | 70 |
| wider_3x_atrtrail_no_target_60d | 293.99 | 14.72 | -16.59 | 1.169 | 98 | 92.67 | 10.78 | -15.63 | 0.856 | 70 |
| atr_3.5x_atrtrail_no_target_60d | 291.38 | 14.64 | -19.5 | 1.057 | 90 | 68.02 | 8.44 | -20.99 | 0.637 | 67 |
| wider_3.5x_atrtrail_no_target_60d | 291.16 | 14.63 | -19.5 | 1.056 | 90 | 67.64 | 8.4 | -20.99 | 0.633 | 67 |
| tighter_3.5x_atrtrail_no_target_60d | 289.52 | 14.58 | -19.17 | 1.053 | 91 | 65.79 | 8.21 | -20.68 | 0.626 | 68 |
| atr_3.5x_atrtrail_target_60d | 256.76 | 13.58 | -19.5 | 1.077 | 93 | 77.26 | 9.35 | -20.99 | 0.705 | 68 |
| wider_3.5x_atrtrail_target_60d | 256.56 | 13.57 | -19.5 | 1.076 | 93 | 76.87 | 9.31 | -20.99 | 0.702 | 68 |
| tighter_3.5x_atrtrail_target_60d | 256.06 | 13.56 | -19.17 | 1.076 | 94 | 74.92 | 9.12 | -20.68 | 0.694 | 69 |
| wider_3x_no_target_60d | 256.01 | 13.56 | -22.07 | 0.846 | 67 | 107.44 | 12.07 | -18.65 | 0.776 | 48 |
| wider_2.5x_no_target_60d | 251.61 | 13.42 | -22.07 | 0.838 | 68 | 112.48 | 12.49 | -18.18 | 0.802 | 49 |

## Top 10 By OOS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| tighter_1.5x_no_target_60d | 190.93 | 11.28 | -18.48 | 0.819 | 79 | 237.05 | 20.89 | -15.97 | 1.225 | 54 |
| atr_1.5x_no_target_60d | 189.31 | 11.22 | -18.48 | 0.815 | 79 | 237.02 | 20.89 | -15.97 | 1.225 | 54 |
| tighter_1.5x_target_60d | 187.85 | 11.17 | -15.18 | 0.88 | 83 | 229.18 | 20.45 | -15.97 | 1.292 | 57 |
| atr_1.5x_target_60d | 186.25 | 11.1 | -15.18 | 0.875 | 83 | 229.14 | 20.45 | -15.97 | 1.292 | 57 |
| tighter_2x_no_target_60d | 178.81 | 10.81 | -20.77 | 0.762 | 76 | 189.61 | 18.06 | -15.97 | 1.105 | 49 |
| atr_2x_no_target_60d | 171.87 | 10.53 | -20.77 | 0.744 | 76 | 188.23 | 17.98 | -15.97 | 1.101 | 49 |
| tighter_2x_target_60d | 173.14 | 10.58 | -16.29 | 0.802 | 80 | 181.23 | 17.52 | -15.97 | 1.135 | 51 |
| atr_2x_target_60d | 166.35 | 10.31 | -16.29 | 0.782 | 80 | 179.88 | 17.44 | -15.97 | 1.13 | 51 |
| tighter_3x_target_60d | 173.21 | 10.59 | -17.1 | 0.765 | 76 | 159.58 | 16.06 | -14.34 | 1.065 | 51 |
| tighter_3.5x_target_60d | 164.11 | 10.21 | -17.33 | 0.727 | 75 | 157.26 | 15.9 | -14.86 | 1.053 | 52 |

