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

- Variant: `wider_3.5x_target_60d`
- IS return: `378.61%` versus S&P 500 `185.16%`
- OOS return: `-30.18%` versus S&P 500 `132.67%`
- OOS max drawdown: `-50.91%`
- ATR variants beating S&P 500 IS: `22`
- ATR variants beating S&P 500 OOS: `0`

## Top 15 By IS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| wider_3.5x_target_60d | 378.61 | 16.97 | -42.65 | 0.832 | 32 | -30.18 | -5.46 | -50.91 | -0.133 | 23 |
| wider_3.5x_no_target_60d | 378.61 | 16.97 | -42.65 | 0.832 | 32 | -30.18 | -5.46 | -50.91 | -0.133 | 23 |
| wider_1.5x_target_60d | 372.52 | 16.82 | -42.62 | 0.828 | 32 | -41.28 | -7.98 | -56.2 | -0.258 | 24 |
| wider_1.5x_no_target_60d | 372.52 | 16.82 | -42.62 | 0.828 | 32 | -41.28 | -7.98 | -56.2 | -0.258 | 24 |
| wider_2x_target_60d | 372.52 | 16.82 | -42.62 | 0.828 | 32 | -41.28 | -7.98 | -56.2 | -0.258 | 24 |
| wider_2x_no_target_60d | 372.52 | 16.82 | -42.62 | 0.828 | 32 | -41.28 | -7.98 | -56.2 | -0.258 | 24 |
| wider_2.5x_target_60d | 372.52 | 16.82 | -42.62 | 0.828 | 32 | -41.28 | -7.98 | -56.2 | -0.258 | 24 |
| wider_2.5x_no_target_60d | 372.52 | 16.82 | -42.62 | 0.828 | 32 | -41.28 | -7.98 | -56.2 | -0.258 | 24 |
| wider_3x_target_60d | 369.03 | 16.74 | -42.62 | 0.825 | 32 | -42.49 | -8.28 | -57.1 | -0.272 | 24 |
| wider_3x_no_target_60d | 369.03 | 16.74 | -42.62 | 0.825 | 32 | -42.49 | -8.28 | -57.1 | -0.272 | 24 |
| atr_2x_target_60d | 251.36 | 13.41 | -31.68 | 0.754 | 38 | -2.85 | -0.45 | -42.33 | 0.084 | 35 |
| atr_2x_no_target_60d | 251.36 | 13.41 | -31.68 | 0.754 | 38 | -2.85 | -0.45 | -42.33 | 0.084 | 35 |
| tighter_2x_target_60d | 251.36 | 13.41 | -31.68 | 0.754 | 38 | -2.85 | -0.45 | -42.33 | 0.084 | 35 |
| tighter_2x_no_target_60d | 251.36 | 13.41 | -31.68 | 0.754 | 38 | -2.85 | -0.45 | -42.33 | 0.084 | 35 |
| atr_1.5x_target_60d | 199.7 | 11.62 | -29.87 | 0.687 | 44 | 4.71 | 0.72 | -37.44 | 0.133 | 39 |

## Top 10 By OOS Return

| Variant | TotalReturnPct_IS | CagrPct_IS | MaxDrawdownPct_IS | Sharpe_IS | Trades_IS | TotalReturnPct_OOS | CagrPct_OOS | MaxDrawdownPct_OOS | Sharpe_OOS | Trades_OOS |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atr_1.5x_atrtrail_no_target_60d | 61.06 | 4.89 | -21.82 | 0.493 | 109 | 39.86 | 5.38 | -26.67 | 0.441 | 83 |
| atr_1.5x_atrtrail_target_60d | 61.06 | 4.89 | -21.82 | 0.493 | 109 | 39.86 | 5.38 | -26.67 | 0.441 | 83 |
| tighter_1.5x_atrtrail_no_target_60d | 61.06 | 4.89 | -21.82 | 0.493 | 109 | 39.86 | 5.38 | -26.67 | 0.441 | 83 |
| tighter_1.5x_atrtrail_target_60d | 61.06 | 4.89 | -21.82 | 0.493 | 109 | 39.86 | 5.38 | -26.67 | 0.441 | 83 |
| wider_1.5x_atrtrail_no_target_60d | 61.05 | 4.89 | -21.82 | 0.493 | 109 | 39.54 | 5.34 | -26.84 | 0.439 | 83 |
| wider_1.5x_atrtrail_target_60d | 61.05 | 4.89 | -21.82 | 0.493 | 109 | 39.54 | 5.34 | -26.84 | 0.439 | 83 |
| tighter_1.5x_target_60d | 199.7 | 11.62 | -29.87 | 0.687 | 44 | 4.71 | 0.72 | -37.44 | 0.133 | 39 |
| atr_1.5x_target_60d | 199.7 | 11.62 | -29.87 | 0.687 | 44 | 4.71 | 0.72 | -37.44 | 0.133 | 39 |
| atr_2x_atrtrail_target_60d | 84.11 | 6.3 | -22.11 | 0.546 | 85 | 4.6 | 0.7 | -30.0 | 0.12 | 60 |
| tighter_2x_atrtrail_target_60d | 84.11 | 6.3 | -22.11 | 0.546 | 85 | 4.6 | 0.7 | -30.0 | 0.12 | 60 |

