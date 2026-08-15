# Cup-And-Handle Trend Filter Variant Search

This is technical strategy research, not investment advice.

## Summary

- Saved cup-and-handle signals tested: `13753`
- Symbols with signals/data requested: `389`
- Variant selection rule: rank by in-sample total return only, then evaluate the selected winner out of sample.
- Entry filter timing: stock and market trend conditions are checked only when the breakout buy stop is touched.
- Entry volume condition: `enabled`, breakout-day volume >= 1.40x prior 50-day average.

## Benchmark

| Segment | Total Return % | CAGR % | Max Drawdown % | Sharpe |
| --- | ---: | ---: | ---: | ---: |
| S&P 500 IS | 185.16 | 11.06 | -19.78 | 0.785 |
| S&P 500 OOS | 132.67 | 14.1 | -33.92 | 0.747 |

## Selected IS Winner

- Variant: `stock_close_gt_sma50_sma50_gt_sma200__market_spx_sma200_rising`
- IS return: `336.81%` versus S&P 500 `185.16%`
- OOS return: `72.74%` versus S&P 500 `132.67%`
- OOS max drawdown: `-16.44%`
- Variants beating S&P 500 OOS: `22`

## Top 15 By IS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock_close_gt_sma50_sma50_gt_sma200__market_spx_sma200_rising | 336.81 | 15.91 | -17.42 | 1.046 | 65 | 72.74 | 8.91 | -16.44 | 0.684 | 46 |
| stock_close_gt_sma50_sma50_gt_sma200__market_spx_close_gt_sma200_sma200_rising | 336.81 | 15.91 | -17.42 | 1.046 | 65 | 81.85 | 9.79 | -14.37 | 0.752 | 44 |
| stock_close_gt_sma200_sma50_gt_sma200__market_spx_sma200_rising | 336.81 | 15.91 | -17.42 | 1.046 | 65 | 77.72 | 9.4 | -16.44 | 0.712 | 47 |
| stock_close_gt_sma200_sma50_gt_sma200__market_spx_close_gt_sma200_sma200_rising | 336.81 | 15.91 | -17.42 | 1.046 | 65 | 81.85 | 9.79 | -14.37 | 0.752 | 44 |
| stock_close_gt_sma50_sma50_gt_sma200__market_none | 327.35 | 15.65 | -17.42 | 1.01 | 72 | 119.26 | 13.04 | -16.49 | 0.829 | 56 |
| stock_close_gt_sma200_sma50_gt_sma200__market_none | 327.35 | 15.65 | -17.42 | 1.01 | 72 | 125.57 | 13.55 | -16.49 | 0.852 | 57 |
| stock_close_gt_sma50_sma50_gt_sma200__market_spx_close_gt_sma200 | 319.21 | 15.43 | -17.42 | 1.012 | 68 | 81.29 | 9.74 | -14.37 | 0.744 | 46 |
| stock_close_gt_sma200_sma50_gt_sma200__market_spx_close_gt_sma200 | 319.21 | 15.43 | -17.42 | 1.012 | 68 | 81.29 | 9.74 | -14.37 | 0.744 | 46 |
| stock_close_gt_sma50_sma50_gt_sma200__market_spx_close_gt_sma100 | 291.38 | 14.64 | -17.42 | 0.962 | 68 | 85.39 | 10.12 | -14.37 | 0.752 | 49 |
| stock_close_gt_sma200_sma50_gt_sma200__market_spx_close_gt_sma100 | 291.38 | 14.64 | -17.42 | 0.962 | 68 | 85.39 | 10.12 | -14.37 | 0.752 | 49 |
| stock_close_gt_sma50_sma50_gt_sma200__market_spx_sma50_gt_sma200 | 291.03 | 14.63 | -16.81 | 1.005 | 65 | 63.41 | 7.97 | -16.44 | 0.6 | 47 |
| stock_close_gt_sma200_sma50_gt_sma200__market_spx_sma50_gt_sma200 | 291.03 | 14.63 | -16.81 | 1.005 | 65 | 68.12 | 8.45 | -16.44 | 0.628 | 48 |
| stock_none__market_spx_close_gt_sma100 | 283.26 | 14.4 | -18.93 | 0.942 | 73 | 128.64 | 13.78 | -14.37 | 0.943 | 53 |
| stock_close_gt_sma50__market_spx_close_gt_sma100 | 283.26 | 14.4 | -18.93 | 0.942 | 73 | 128.64 | 13.78 | -14.37 | 0.943 | 53 |
| stock_close_gt_sma200__market_spx_close_gt_sma100 | 283.26 | 14.4 | -18.93 | 0.942 | 73 | 128.64 | 13.78 | -14.37 | 0.943 | 53 |

## Top 10 By OOS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock_close_gt_sma50_rs63_gt_spx__market_none | 218.02 | 12.28 | -17.42 | 0.827 | 76 | 186.71 | 17.88 | -16.49 | 1.057 | 61 |
| stock_none__market_none | 262.33 | 13.76 | -17.42 | 0.905 | 77 | 173.62 | 17.02 | -16.49 | 1.009 | 62 |
| stock_close_gt_sma200__market_none | 262.33 | 13.76 | -17.42 | 0.905 | 77 | 173.62 | 17.02 | -16.49 | 1.009 | 62 |
| stock_close_gt_sma50__market_none | 262.33 | 13.76 | -17.42 | 0.905 | 77 | 162.37 | 16.26 | -16.49 | 0.973 | 62 |
| stock_close_gt_sma200__market_spx_close_gt_sma50_sma50_gt_sma200 | 197.01 | 11.52 | -17.97 | 0.852 | 61 | 159.65 | 16.07 | -14.37 | 1.092 | 47 |
| stock_close_gt_sma50_rs63_gt_spx__market_spx_close_gt_sma50_sma50_gt_sma200 | 158.43 | 9.97 | -17.97 | 0.757 | 60 | 159.65 | 16.07 | -14.37 | 1.092 | 47 |
| stock_close_gt_sma50__market_spx_close_gt_sma50_sma50_gt_sma200 | 197.01 | 11.52 | -17.97 | 0.852 | 61 | 159.65 | 16.07 | -14.37 | 1.092 | 47 |
| stock_none__market_spx_close_gt_sma50_sma50_gt_sma200 | 197.01 | 11.52 | -17.97 | 0.852 | 61 | 159.65 | 16.07 | -14.37 | 1.092 | 47 |
| stock_close_gt_sma50_rs63_gt_spx__market_spx_close_gt_sma200_sma200_rising | 217.54 | 12.26 | -17.42 | 0.855 | 68 | 153.91 | 15.66 | -14.37 | 1.085 | 49 |
| stock_close_gt_sma50_rs63_gt_spx__market_spx_close_gt_sma200 | 223.84 | 12.49 | -18.84 | 0.848 | 72 | 153.13 | 15.61 | -14.37 | 1.075 | 51 |

