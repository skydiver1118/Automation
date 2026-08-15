# Cup-And-Handle Trend Filter Variant Search

This is technical strategy research, not investment advice.

## Summary

- Saved cup-and-handle signals tested: `6212`
- Symbols with signals/data requested: `439`
- Variant selection rule: rank by in-sample total return only, then evaluate the selected winner out of sample.
- Entry filter timing: stock and market trend conditions are checked only when the breakout buy stop is touched.
- Entry volume condition: `enabled`, breakout-day volume >= 1.40x prior 50-day average.

## Benchmark

| Segment | Total Return % | CAGR % | Max Drawdown % | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| S&P 500 IS | 185.16 | 11.06 | -19.78 | 0.785 |
| S&P 500 OOS | 132.67 | 14.1 | -33.92 | 0.747 |

## Selected IS Winner

- Variant: `stock_close_gt_sma50_sma50_rising__market_spx_close_gt_sma50_sma50_gt_sma200`
- IS return: `102.73%` versus S&P 500 `185.16%`
- OOS return: `45.0%` versus S&P 500 `132.67%`
- OOS max drawdown: `-13.27%`
- Variants beating S&P 500 OOS: `0`

## Top 15 By IS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock_close_gt_sma50_sma50_rising__market_spx_close_gt_sma50_sma50_gt_sma200 | 102.73 | 7.33 | -12.21 | 0.72 | 47 | 45.0 | 5.97 | -13.27 | 0.637 | 27 |
| stock_close_gt_sma50_sma50_gt_sma200__market_spx_close_gt_sma50_sma50_gt_sma200 | 98.19 | 7.09 | -12.21 | 0.685 | 49 | 47.32 | 6.24 | -13.95 | 0.648 | 29 |
| stock_close_gt_sma200_sma50_gt_sma200__market_spx_close_gt_sma50_sma50_gt_sma200 | 98.19 | 7.09 | -12.21 | 0.685 | 49 | 42.36 | 5.67 | -13.95 | 0.592 | 30 |
| stock_close_gt_sma50_rs63_gt_spx__market_spx_close_gt_sma50_sma50_gt_sma200 | 93.05 | 6.81 | -12.21 | 0.682 | 45 | 51.1 | 6.66 | -11.12 | 0.724 | 27 |
| stock_close_gt_sma50_sma50_rising__market_none | 91.06 | 6.7 | -17.43 | 0.587 | 59 | 72.37 | 8.87 | -11.83 | 0.767 | 39 |
| stock_close_gt_sma50_sma50_rising__market_spx_close_gt_sma100 | 90.89 | 6.69 | -17.43 | 0.617 | 54 | 68.72 | 8.51 | -11.15 | 0.765 | 35 |
| stock_close_gt_sma20_sma20_gt_sma50__market_spx_close_gt_sma100 | 88.59 | 6.56 | -15.15 | 0.605 | 52 | 70.87 | 8.73 | -10.48 | 0.782 | 36 |
| stock_close_gt_sma20_sma20_gt_sma50__market_spx_close_gt_sma50_sma50_gt_sma200 | 87.86 | 6.52 | -12.21 | 0.645 | 47 | 45.76 | 6.06 | -12.49 | 0.646 | 28 |
| stock_close_gt_sma200_sma200_rising__market_spx_close_gt_sma100 | 86.92 | 6.46 | -17.43 | 0.595 | 54 | 50.0 | 6.54 | -14.84 | 0.622 | 36 |
| stock_close_gt_sma50_sma50_rising__market_spx_sma50_gt_sma200 | 85.43 | 6.38 | -16.67 | 0.587 | 55 | 65.71 | 8.21 | -12.6 | 0.784 | 32 |
| stock_none__market_spx_close_gt_sma50_sma50_gt_sma200 | 85.23 | 6.37 | -12.21 | 0.625 | 49 | 42.36 | 5.67 | -13.95 | 0.592 | 30 |
| stock_close_gt_sma50__market_spx_close_gt_sma50_sma50_gt_sma200 | 85.23 | 6.37 | -12.21 | 0.625 | 49 | 47.32 | 6.24 | -13.95 | 0.648 | 29 |
| stock_close_gt_sma200__market_spx_close_gt_sma50_sma50_gt_sma200 | 85.23 | 6.37 | -12.21 | 0.625 | 49 | 42.36 | 5.67 | -13.95 | 0.592 | 30 |
| stock_close_gt_sma50_sma50_gt_sma200__market_spx_close_gt_sma100 | 83.16 | 6.25 | -17.43 | 0.575 | 56 | 60.27 | 7.64 | -14.84 | 0.671 | 39 |
| stock_close_gt_sma200_sma50_gt_sma200__market_spx_close_gt_sma100 | 83.16 | 6.25 | -17.43 | 0.575 | 56 | 54.87 | 7.07 | -15.73 | 0.622 | 40 |

## Top 10 By OOS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock_close_gt_sma50_rs63_gt_spx__market_none | 69.97 | 5.45 | -17.43 | 0.493 | 58 | 75.67 | 9.2 | -12.72 | 0.789 | 40 |
| stock_close_gt_sma50_sma50_rising__market_none | 91.06 | 6.7 | -17.43 | 0.587 | 59 | 72.37 | 8.87 | -11.83 | 0.767 | 39 |
| stock_close_gt_sma20_sma20_gt_sma50__market_spx_close_gt_sma100 | 88.59 | 6.56 | -15.15 | 0.605 | 52 | 70.87 | 8.73 | -10.48 | 0.782 | 36 |
| stock_close_gt_sma20_sma20_gt_sma50__market_none | 81.07 | 6.12 | -15.41 | 0.545 | 57 | 70.23 | 8.66 | -13.01 | 0.726 | 40 |
| stock_close_gt_sma50_sma50_rising__market_spx_close_gt_sma100 | 90.89 | 6.69 | -17.43 | 0.617 | 54 | 68.72 | 8.51 | -11.15 | 0.765 | 35 |
| stock_close_gt_sma50_rs63_gt_spx__market_spx_sma50_gt_sma200 | 64.96 | 5.14 | -16.67 | 0.488 | 54 | 67.41 | 8.38 | -17.91 | 0.8 | 33 |
| stock_close_gt_sma50_rs63_gt_spx__market_spx_close_gt_sma200 | 54.98 | 4.48 | -17.62 | 0.419 | 57 | 66.15 | 8.25 | -12.72 | 0.74 | 37 |
| stock_close_gt_sma50_rs63_gt_spx__market_spx_close_gt_sma100 | 81.63 | 6.16 | -17.43 | 0.58 | 52 | 65.89 | 8.22 | -12.72 | 0.738 | 37 |
| stock_close_gt_sma50_sma50_rising__market_spx_sma50_gt_sma200 | 85.43 | 6.38 | -16.67 | 0.587 | 55 | 65.71 | 8.21 | -12.6 | 0.784 | 32 |
| stock_close_gt_sma20_sma20_gt_sma50__market_spx_sma200_rising | 65.6 | 5.18 | -20.63 | 0.481 | 54 | 63.25 | 7.95 | -12.61 | 0.725 | 34 |

