# S&P 500 Top1 Point-in-Time Membership Backtest

Period: 2020-01-01 through 2026-05-17.
Execution: monthly signal after month-end close, buy/sell at next trading day's open, hold open-to-open.
Ranking: 126 trading-day momentum, skipping the latest 21 trading days.
Point-in-time rule: walk down the momentum ranking and skip any ticker whose S&P 500 `Date added` is after the purchase date.

| Strategy | Return | Max DD | Trades | Buys | Rebalances | Skipped future members | Membership violations | Final holding | SPMO return | Excess vs SPMO |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| Top1 current-member baseline | 19998.50% | -60.36% | 81 | 41 | 77 | 0 | 25 | SNDK | 264.77% | 19733.72% |
| Top1 PIT S&P membership | 1464.21% | -53.85% | 87 | 44 | 77 | 109 | 0 | SNDK | 264.77% | 1199.44% |

The filtered strategy removes buys before each stock's available S&P 500 `Date added` value.
Important limitation: this is still based on today's S&P 500 constituent list plus each member's `Date added`. It prevents buying future additions, but it does not include stocks that were historical S&P 500 members and have since been removed.

## Output Files

- Excel workbook: `reports\sp500_top1_point_in_time_membership_2020_2026ytd.xlsx`
- Summary CSV: `reports\sp500_top1_point_in_time_membership_2020_2026ytd_summary.csv`
- Trade CSV: `reports\sp500_top1_point_in_time_membership_2020_2026ytd_trades.csv`
- Monthly decisions CSV: `reports\sp500_top1_point_in_time_membership_2020_2026ytd_monthly_rebalances.csv`
- Equity curve CSV: `reports\sp500_top1_point_in_time_membership_2020_2026ytd_equity_curve.csv`
