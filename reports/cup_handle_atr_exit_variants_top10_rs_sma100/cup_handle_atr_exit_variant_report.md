# Cup-And-Handle ATR Exit Variant Search

This is technical strategy research, not investment advice.

## Setup

- Saved cup-and-handle signals tested: `6492`
- Symbols with usable cached data: `444`
- Entry stock condition: `stock_close_gt_sma50_rs63_gt_spx`
- Entry market condition: `market_spx_close_gt_sma100`
- Exit variants tested: initial ATR stops, handle/ATR tighter or wider stops, ATR trailing stops, target on/off.
- Selection rule: rank by IS total return; evaluate the IS winner OOS.

## Benchmark

| Segment | Total Return % | CAGR % | Max Drawdown % | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| S&P 500 IS | 185.16 | 11.06 | -19.78 | 0.785 |
| S&P 500 OOS | 132.67 | 14.1 | -33.92 | 0.747 |

## Selected IS Winner

- Variant: `atr_3x_no_target_60d`
- IS return: `219.61%` versus S&P 500 `185.16%`
- OOS return: `89.99%` versus S&P 500 `132.67%`
- OOS max drawdown: `-22.17%`
- ATR variants beating S&P 500 IS: `5`
- ATR variants beating S&P 500 OOS: `3`

## Top 15 By IS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atr_3x_no_target_60d | 219.61 | 12.34 | -18.45 | 0.911 | 108 | 89.99 | 10.54 | -22.17 | 0.744 | 75 |
| tighter_3x_no_target_60d | 213.74 | 12.13 | -18.12 | 0.898 | 109 | 90.1 | 10.55 | -22.17 | 0.744 | 75 |
| tighter_3.5x_no_target_60d | 198.16 | 11.56 | -18.48 | 0.846 | 105 | 129.63 | 13.86 | -15.15 | 0.929 | 72 |
| atr_3.5x_no_target_60d | 193.57 | 11.39 | -18.48 | 0.83 | 105 | 134.36 | 14.22 | -15.92 | 0.937 | 72 |
| atr_3x_target_60d | 189.3 | 11.22 | -18.45 | 0.843 | 110 | 113.19 | 12.55 | -22.17 | 0.83 | 76 |
| tighter_3x_target_60d | 183.98 | 11.02 | -18.12 | 0.83 | 111 | 113.31 | 12.56 | -22.17 | 0.831 | 76 |
| tighter_3.5x_target_60d | 178.18 | 10.79 | -18.48 | 0.8 | 106 | 157.88 | 15.94 | -15.15 | 1.007 | 73 |
| atr_3.5x_target_60d | 173.9 | 10.61 | -18.48 | 0.784 | 106 | 162.99 | 16.3 | -15.92 | 1.014 | 73 |
| wider_1.5x_target_60d | 141.34 | 9.22 | -20.81 | 0.686 | 99 | 118.3 | 12.97 | -24.16 | 0.846 | 70 |
| wider_1.5x_no_target_60d | 141.34 | 9.22 | -20.81 | 0.686 | 99 | 94.27 | 10.93 | -24.16 | 0.759 | 69 |
| wider_2x_target_60d | 141.34 | 9.22 | -20.81 | 0.686 | 99 | 118.3 | 12.97 | -24.16 | 0.846 | 70 |
| wider_2x_no_target_60d | 141.34 | 9.22 | -20.81 | 0.686 | 99 | 94.27 | 10.93 | -24.16 | 0.759 | 69 |
| wider_2.5x_target_60d | 141.22 | 9.22 | -20.81 | 0.685 | 99 | 118.3 | 12.97 | -24.16 | 0.846 | 70 |
| wider_2.5x_no_target_60d | 141.22 | 9.22 | -20.81 | 0.685 | 99 | 94.27 | 10.93 | -24.16 | 0.759 | 69 |
| wider_3x_target_60d | 139.35 | 9.13 | -20.81 | 0.68 | 99 | 118.06 | 12.95 | -24.16 | 0.844 | 70 |

## Top 10 By OOS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atr_3.5x_target_60d | 173.9 | 10.61 | -18.48 | 0.784 | 106 | 162.99 | 16.3 | -15.92 | 1.014 | 73 |
| tighter_3.5x_target_60d | 178.18 | 10.79 | -18.48 | 0.8 | 106 | 157.88 | 15.94 | -15.15 | 1.007 | 73 |
| atr_3.5x_no_target_60d | 193.57 | 11.39 | -18.48 | 0.83 | 105 | 134.36 | 14.22 | -15.92 | 0.937 | 72 |
| tighter_3.5x_no_target_60d | 198.16 | 11.56 | -18.48 | 0.846 | 105 | 129.63 | 13.86 | -15.15 | 0.929 | 72 |
| wider_2x_target_60d | 141.34 | 9.22 | -20.81 | 0.686 | 99 | 118.3 | 12.97 | -24.16 | 0.846 | 70 |
| wider_1.5x_target_60d | 141.34 | 9.22 | -20.81 | 0.686 | 99 | 118.3 | 12.97 | -24.16 | 0.846 | 70 |
| wider_2.5x_target_60d | 141.22 | 9.22 | -20.81 | 0.685 | 99 | 118.3 | 12.97 | -24.16 | 0.846 | 70 |
| wider_3x_target_60d | 139.35 | 9.13 | -20.81 | 0.68 | 99 | 118.06 | 12.95 | -24.16 | 0.844 | 70 |
| wider_3.5x_target_60d | 135.2 | 8.94 | -20.81 | 0.665 | 99 | 113.31 | 12.56 | -24.82 | 0.822 | 70 |
| tighter_3x_target_60d | 183.98 | 11.02 | -18.12 | 0.83 | 111 | 113.31 | 12.56 | -22.17 | 0.831 | 76 |

