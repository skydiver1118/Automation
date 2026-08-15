# Cup-And-Handle Trend Filter Variant Search

This is technical strategy research, not investment advice.

## Summary

- Saved cup-and-handle signals tested: `16916`
- Symbols with signals/data requested: `510`
- Variant selection rule: rank by in-sample total return only, then evaluate the selected winner out of sample.
- Entry filter timing: stock and market trend conditions are checked only when the breakout buy stop is touched.

## Benchmark

| Segment | Total Return % | CAGR % | Max Drawdown % | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| S&P 500 IS | 185.16 | 11.06 | -19.78 | 0.785 |
| S&P 500 OOS | 132.67 | 14.1 | -33.92 | 0.747 |

## Selected IS Winner

- Variant: `stock_close_gt_sma200_sma200_rising__market_spx_close_gt_sma200_sma200_rising`
- IS return: `273.95%` versus S&P 500 `185.16%`
- OOS return: `55.85%` versus S&P 500 `132.67%`
- OOS max drawdown: `-27.49%`
- Variants beating S&P 500 OOS: `0`

## Top 15 By IS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock_close_gt_sma200_sma200_rising__market_spx_close_gt_sma200_sma200_rising | 273.95 | 14.12 | -15.93 | 0.968 | 92 | 55.85 | 7.17 | -27.49 | 0.552 | 63 |
| stock_close_gt_sma50_rs63_gt_spx__market_spx_sma200_rising | 251.61 | 13.42 | -18.82 | 0.935 | 95 | 64.37 | 8.07 | -34.59 | 0.571 | 68 |
| stock_close_gt_sma200_sma200_rising__market_spx_sma200_rising | 244.41 | 13.18 | -16.06 | 0.938 | 93 | 44.32 | 5.9 | -32.85 | 0.459 | 65 |
| stock_close_gt_sma50_rs63_gt_spx__market_spx_close_gt_sma200_sma200_rising | 237.59 | 12.95 | -18.82 | 0.896 | 94 | 93.08 | 10.82 | -26.8 | 0.759 | 65 |
| stock_close_gt_sma200_sma200_rising__market_none | 235.77 | 12.89 | -15.93 | 0.906 | 102 | 49.64 | 6.5 | -34.32 | 0.471 | 77 |
| stock_none__market_spx_close_gt_sma200_sma200_rising | 220.13 | 12.36 | -22.47 | 0.859 | 96 | 43.77 | 5.83 | -27.47 | 0.461 | 68 |
| stock_close_gt_sma50__market_spx_close_gt_sma200_sma200_rising | 220.13 | 12.36 | -22.47 | 0.859 | 96 | 49.18 | 6.45 | -27.47 | 0.503 | 67 |
| stock_close_gt_sma200__market_spx_close_gt_sma200_sma200_rising | 220.13 | 12.36 | -22.47 | 0.859 | 96 | 43.77 | 5.83 | -27.47 | 0.461 | 68 |
| stock_close_gt_sma50_sma50_rising__market_spx_sma200_rising | 215.73 | 12.2 | -21.08 | 0.858 | 94 | 67.59 | 8.4 | -20.29 | 0.615 | 67 |
| stock_close_gt_sma50_sma50_gt_sma200__market_spx_close_gt_sma200_sma200_rising | 212.06 | 12.07 | -22.47 | 0.861 | 95 | 53.57 | 6.93 | -27.47 | 0.53 | 69 |
| stock_close_gt_sma200_sma50_gt_sma200__market_spx_close_gt_sma200_sma200_rising | 212.06 | 12.07 | -22.47 | 0.861 | 95 | 48.0 | 6.31 | -27.47 | 0.488 | 70 |
| stock_none__market_spx_sma200_rising | 212.01 | 12.07 | -22.47 | 0.866 | 97 | 22.39 | 3.21 | -35.18 | 0.282 | 71 |
| stock_close_gt_sma50__market_spx_sma200_rising | 212.01 | 12.07 | -22.47 | 0.866 | 97 | 26.99 | 3.8 | -35.18 | 0.321 | 70 |
| stock_close_gt_sma200__market_spx_sma200_rising | 212.01 | 12.07 | -22.47 | 0.866 | 97 | 22.39 | 3.21 | -35.18 | 0.282 | 71 |
| stock_close_gt_sma50_rs63_gt_spx__market_none | 205.53 | 11.83 | -22.66 | 0.806 | 109 | 59.38 | 7.55 | -34.38 | 0.513 | 79 |

## Top 10 By OOS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock_close_gt_sma50_rs63_gt_spx__market_spx_close_gt_sma100 | 141.34 | 9.19 | -22.66 | 0.659 | 105 | 118.3 | 12.89 | -24.16 | 0.846 | 70 |
| stock_close_gt_sma50_rs63_gt_spx__market_spx_close_gt_sma50_sma50_gt_sma200 | 67.62 | 5.31 | -26.45 | 0.471 | 71 | 101.7 | 11.4 | -20.41 | 0.835 | 57 |
| stock_close_gt_sma50_rs63_gt_spx__market_spx_sma50_gt_sma200 | 124.81 | 8.44 | -23.42 | 0.631 | 87 | 96.71 | 10.98 | -26.82 | 0.792 | 64 |
| stock_close_gt_sma50_rs63_gt_spx__market_spx_close_gt_sma200 | 175.29 | 10.66 | -22.66 | 0.765 | 98 | 95.49 | 10.87 | -32.76 | 0.738 | 69 |
| stock_close_gt_sma50_rs63_gt_spx__market_spx_close_gt_sma200_sma200_rising | 237.59 | 12.95 | -18.82 | 0.896 | 94 | 93.08 | 10.82 | -26.8 | 0.759 | 65 |
| stock_close_gt_sma50_sma50_rising__market_spx_sma50_gt_sma200 | 72.89 | 5.62 | -26.87 | 0.43 | 85 | 89.24 | 10.27 | -17.53 | 0.763 | 65 |
| stock_close_gt_sma50_sma50_rising__market_spx_close_gt_sma100 | 132.49 | 8.8 | -26.63 | 0.629 | 102 | 87.38 | 10.06 | -17.55 | 0.695 | 70 |
| stock_close_gt_sma20_sma20_gt_sma50__market_none | 162.09 | 10.12 | -27.07 | 0.617 | 114 | 81.64 | 9.39 | -26.85 | 0.657 | 78 |
| stock_close_gt_sma20_sma20_gt_sma50__market_spx_sma50_gt_sma200 | 80.37 | 6.08 | -20.02 | 0.478 | 88 | 80.32 | 9.25 | -17.51 | 0.717 | 65 |
| stock_close_gt_sma20_sma20_gt_sma50__market_spx_close_gt_sma100 | 131.1 | 8.74 | -22.15 | 0.632 | 105 | 77.97 | 8.99 | -17.53 | 0.672 | 69 |

