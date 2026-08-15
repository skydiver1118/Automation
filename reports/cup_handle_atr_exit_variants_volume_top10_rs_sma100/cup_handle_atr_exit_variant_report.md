# Cup-And-Handle ATR Exit Variant Search

This is technical strategy research, not investment advice.

## Setup

- Saved cup-and-handle signals tested: `6212`
- Symbols with usable cached data: `439`
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

- Variant: `atr_2x_target_60d`
- IS return: `101.85%` versus S&P 500 `185.16%`
- OOS return: `71.79%` versus S&P 500 `132.67%`
- OOS max drawdown: `-13.32%`
- ATR variants beating S&P 500 IS: `0`
- ATR variants beating S&P 500 OOS: `0`

## Top 15 By IS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atr_2x_target_60d | 101.85 | 7.29 | -13.89 | 0.748 | 58 | 71.79 | 8.82 | -13.32 | 0.875 | 44 |
| atr_2x_no_target_60d | 101.85 | 7.29 | -13.89 | 0.748 | 58 | 59.78 | 7.59 | -13.32 | 0.77 | 43 |
| tighter_2x_target_60d | 101.85 | 7.29 | -13.89 | 0.748 | 58 | 71.79 | 8.82 | -13.32 | 0.875 | 44 |
| tighter_2x_no_target_60d | 101.85 | 7.29 | -13.89 | 0.748 | 58 | 59.78 | 7.59 | -13.32 | 0.77 | 43 |
| atr_3x_target_60d | 89.29 | 6.6 | -15.57 | 0.645 | 56 | 55.06 | 7.09 | -21.85 | 0.685 | 38 |
| atr_3x_no_target_60d | 89.29 | 6.6 | -15.57 | 0.645 | 56 | 44.15 | 5.88 | -21.85 | 0.583 | 37 |
| wider_3x_target_60d | 89.15 | 6.59 | -17.43 | 0.611 | 52 | 65.8 | 8.22 | -12.76 | 0.737 | 37 |
| wider_3x_no_target_60d | 89.15 | 6.59 | -17.43 | 0.611 | 52 | 54.15 | 6.99 | -12.76 | 0.642 | 36 |
| wider_3.5x_target_60d | 87.24 | 6.48 | -17.43 | 0.601 | 52 | 64.32 | 8.06 | -13.28 | 0.724 | 37 |
| wider_3.5x_no_target_60d | 87.24 | 6.48 | -17.43 | 0.601 | 52 | 52.78 | 6.84 | -13.28 | 0.63 | 36 |
| atr_3.5x_target_60d | 86.75 | 6.45 | -16.41 | 0.621 | 56 | 69.86 | 8.63 | -12.57 | 0.792 | 38 |
| atr_3.5x_no_target_60d | 86.75 | 6.45 | -16.41 | 0.621 | 56 | 57.93 | 7.4 | -12.57 | 0.695 | 37 |
| tighter_3x_target_60d | 81.76 | 6.17 | -15.57 | 0.613 | 56 | 55.15 | 7.1 | -21.85 | 0.686 | 38 |
| tighter_3x_no_target_60d | 81.76 | 6.17 | -15.57 | 0.613 | 56 | 44.23 | 5.89 | -21.85 | 0.584 | 37 |
| wider_1.5x_target_60d | 81.63 | 6.16 | -17.43 | 0.58 | 52 | 65.89 | 8.22 | -12.72 | 0.738 | 37 |

## Top 10 By OOS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atr_2x_target_60d | 101.85 | 7.29 | -13.89 | 0.748 | 58 | 71.79 | 8.82 | -13.32 | 0.875 | 44 |
| tighter_2x_target_60d | 101.85 | 7.29 | -13.89 | 0.748 | 58 | 71.79 | 8.82 | -13.32 | 0.875 | 44 |
| tighter_3.5x_target_60d | 81.16 | 6.13 | -16.41 | 0.599 | 56 | 71.48 | 8.79 | -12.35 | 0.806 | 38 |
| atr_3.5x_target_60d | 86.75 | 6.45 | -16.41 | 0.621 | 56 | 69.86 | 8.63 | -12.57 | 0.792 | 38 |
| wider_1.5x_target_60d | 81.63 | 6.16 | -17.43 | 0.58 | 52 | 65.89 | 8.22 | -12.72 | 0.738 | 37 |
| wider_2.5x_target_60d | 81.63 | 6.16 | -17.43 | 0.58 | 52 | 65.89 | 8.22 | -12.72 | 0.738 | 37 |
| wider_2x_target_60d | 81.63 | 6.16 | -17.43 | 0.58 | 52 | 65.89 | 8.22 | -12.72 | 0.738 | 37 |
| wider_3x_target_60d | 89.15 | 6.59 | -17.43 | 0.611 | 52 | 65.8 | 8.22 | -12.76 | 0.737 | 37 |
| wider_3.5x_target_60d | 87.24 | 6.48 | -17.43 | 0.601 | 52 | 64.32 | 8.06 | -13.28 | 0.724 | 37 |
| tighter_2.5x_target_60d | 81.52 | 6.15 | -14.71 | 0.632 | 56 | 60.93 | 7.71 | -15.55 | 0.741 | 41 |

