# SOXL/TQQQ Rotation With Cash Exit-Profile IS/OOS Test

Scanner: `scripts/soxl_tqqq_cash_signal_scanner.py` using the existing daily scanner config.
IS: 2010-03-11 to 2019-12-31. OOS: 2020-01-01 to 2026-05-22.

Execution model: scanner target changes are applied after the signal close, matching the existing local scanner comparison. The exit sub-module adds partial scale-outs, R-based stops, and optional loss exits while unallocated capital stays in cash.

## Selected IS Sub-Models

Top 3 profile pairs selected by IS Sharpe, then lower drawdown, then higher cumulative return:

| is_rank | profit_profile | loss_profile | cumulative_return_pct | cagr_pct | max_drawdown_pct | sharpe |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | risk_first_trend_runner | one_r_invalidation | 3599.99 | 44.51 | -53.6 | 1.138 |
| 2 | volatility_ladder | one_r_invalidation | 4395.25 | 47.41 | -52.62 | 1.099 |
| 3 | risk_first_trend_runner | time_and_volatility_failure | 3301.79 | 43.28 | -53.94 | 1.099 |

## IS/OOS Comparison

| period | strategy | profit_profile | loss_profile | start | end | cumulative_return_pct | cagr_pct | max_drawdown_pct | sharpe | daily_vol_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IS | baseline_no_exit_submodule |  |  | 2010-03-11 | 2019-12-31 | 2915.25 | 41.53 | -52.16 | 0.971 | 47.6 |
| OOS | baseline_no_exit_submodule |  |  | 2020-01-02 | 2026-05-22 | 9826.01 | 105.47 | -53.4 | 1.402 | 68.24 |
| IS | is_rank_1_with_exit_submodule | risk_first_trend_runner | one_r_invalidation | 2010-03-11 | 2019-12-31 | 3599.99 | 44.51 | -53.6 | 1.138 | 39.18 |
| OOS | is_rank_1_with_exit_submodule | risk_first_trend_runner | one_r_invalidation | 2020-01-02 | 2026-05-22 | 4073.81 | 79.4 | -43.63 | 1.311 | 57.34 |
| IS | is_rank_2_with_exit_submodule | volatility_ladder | one_r_invalidation | 2010-03-11 | 2019-12-31 | 4395.25 | 47.41 | -52.62 | 1.099 | 44.41 |
| OOS | is_rank_2_with_exit_submodule | volatility_ladder | one_r_invalidation | 2020-01-02 | 2026-05-22 | 6323.84 | 91.93 | -44.34 | 1.353 | 63.17 |
| IS | is_rank_3_with_exit_submodule | risk_first_trend_runner | time_and_volatility_failure | 2010-03-11 | 2019-12-31 | 3301.79 | 43.28 | -53.94 | 1.099 | 40.09 |
| OOS | is_rank_3_with_exit_submodule | risk_first_trend_runner | time_and_volatility_failure | 2020-01-02 | 2026-05-22 | 4229.47 | 80.43 | -43.63 | 1.325 | 57.01 |

## Top IS Exit-Profile Grid

| is_rank | profit_profile | loss_profile | cumulative_return_pct | cagr_pct | max_drawdown_pct | sharpe | event_count |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | risk_first_trend_runner | one_r_invalidation | 3599.99 | 44.51 | -53.6 | 1.138 | 305 |
| 2 | volatility_ladder | one_r_invalidation | 4395.25 | 47.41 | -52.62 | 1.099 | 274 |
| 3 | risk_first_trend_runner | time_and_volatility_failure | 3301.79 | 43.28 | -53.94 | 1.099 | 332 |
| 4 | volatility_ladder | time_and_volatility_failure | 4208.3 | 46.77 | -52.62 | 1.088 | 304 |
| 5 | risk_first_trend_runner | trend_structure_break | 3027.59 | 42.06 | -52.64 | 1.082 | 293 |
| 6 | structure_ladder | time_and_volatility_failure | 3875.22 | 45.57 | -52.75 | 1.051 | 283 |
| 7 | structure_ladder | one_r_invalidation | 3590.01 | 44.47 | -49.44 | 1.035 | 233 |
| 8 | volatility_ladder | trend_structure_break | 3463.8 | 43.96 | -50.69 | 1.027 | 338 |
| 9 | structure_ladder | trend_structure_break | 2961.43 | 41.75 | -52.16 | 0.98 | 266 |

## OOS Takeaway

Baseline OOS return was 9826.01% with -53.4% max drawdown and Sharpe 1.402.
Best top-3 exit sub-module by OOS Sharpe was `is_rank_2_with_exit_submodule` using `volatility_ladder` + `one_r_invalidation`: return 6323.84%, max drawdown -44.34%, Sharpe 1.353.

## Files

- IS grid: `C:\Users\skydiver1118\Documents\New project\reports\soxl_tqqq_cash_exit_profile_is_grid.csv`
- IS/OOS comparison: `C:\Users\skydiver1118\Documents\New project\reports\soxl_tqqq_cash_exit_profile_is_oos_comparison.csv`
- Daily curves: `C:\Users\skydiver1118\Documents\New project\reports\soxl_tqqq_cash_exit_profile_curves.csv`
- Selected sub-module events: `C:\Users\skydiver1118\Documents\New project\reports\soxl_tqqq_cash_exit_profile_top3_events.csv`