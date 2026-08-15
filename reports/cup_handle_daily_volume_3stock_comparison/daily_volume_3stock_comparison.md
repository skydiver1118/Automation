# Daily Cup-And-Handle Volume 3-Stock Rerun

This is technical strategy research, not investment advice.

## Setup

- Pattern timeframe: daily candles, scanned every 5 trading days for historical runtime control.
- Daily pattern volume gate: handle average volume <= `1.05x` cup average volume for formed patterns.
- Entry volume gate: breakout-day daily volume >= `1.40x` prior 50-trading-day average volume.
- Candidate pool: top 10 daily-pattern scores per scan date after `TargetReturnPct > 30%`.
- Portfolio: maximum 3 concurrent stocks.
- Signals generated: `13753`.
- IS: `2010-01-01` to `2020-01-01`; OOS: `2020-01-01` to `2026-05-30`.

## S&P 500 Benchmark

| Segment | Total Return % | Sharpe |
| --- | ---: | ---: |
| IS | 185.16 | 0.785 |
| OOS | 132.67 | 0.747 |

## Comparison Summary

| Family | Selection | Variant | IS_TotalReturnPct | IS_Sharpe | IS_Trades | OOS_TotalReturnPct | OOS_Sharpe | OOS_Trades | IS_Return_vs_SP500_PctPts | IS_Sharpe_vs_SP500 | OOS_Return_vs_SP500_PctPts | OOS_Sharpe_vs_SP500 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Base 3-stock rotation | Single rule | daily pattern + volume gates | 262.33 | 0.905 | 80.0 | 173.94 | 1.008 | 62.0 | 77.17 | 0.12 | 41.27 | 0.261 |
| Trend filters | Best by IS return | stock_close_gt_sma50_sma50_gt_sma200__market_spx_sma200_rising | 336.81 | 1.046 | 65.0 | 72.74 | 0.684 | 46.0 | 151.65 | 0.261 | -59.93 | -0.063 |
| Trend filters | Best by OOS return | stock_close_gt_sma50_rs63_gt_spx__market_none | 218.02 | 0.827 | 76.0 | 186.71 | 1.057 | 61.0 | 32.86 | 0.042 | 54.04 | 0.31 |
| ATR exits | Best by IS return | tighter_3x_atrtrail_target_60d | 296.68 | 1.223 | 100.0 | 99.17 | 0.911 | 71.0 | 111.52 | 0.438 | -33.5 | 0.164 |
| ATR exits | Best by OOS return | tighter_1.5x_no_target_60d | 190.93 | 0.819 | 79.0 | 237.05 | 1.225 | 54.0 | 5.77 | 0.034 | 104.38 | 0.478 |
| Entry window 3-10 days | Best by IS return | 9 trading days | 462.02 | 1.027 | 79.0 | 233.81 | 1.127 | 49.0 | 276.86 | 0.242 | 101.14 | 0.38 |
| Entry window 3-10 days | Best by OOS return | 7 trading days | 391.64 | 0.977 | 75.0 | 263.74 | 1.212 | 48.0 | 206.48 | 0.192 | 131.07 | 0.465 |

## Files

- `daily_volume_3stock_summary.csv`
- `daily_volume_all_variant_results.csv`
