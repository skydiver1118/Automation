# Nasdaq-100 Top1 Point-in-Time Membership Backtest

Period: 2020-01-01 through 2026-05-17.
Execution: monthly signal after month-end close, trade next trading day's open, hold open-to-open.
Ranking: 126 trading-day momentum, skipping the latest 21 trading days.
Point-in-time rule: if the top-ranked stock has a known Nasdaq-100 add date after the purchase date, skip it and choose the next eligible stock.
Add-date source: Wikipedia Nasdaq-100 changes table, cached locally.

| Strategy | Return | Max DD | Sharpe | Trades | Buys | Skipped Future Members | Violations | Known-Date Buys | Assumed Pre-window Buys | QQQ | VGT | Excess vs QQQ | Excess vs VGT | Final Holding |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Nasdaq-100 Top1 current-member baseline | 3606.85% | -67.36% | 1.09 | 77 | 39 | 0 | 0 | 35 | 4 | 240.31% | 280.61% | 3366.54% | 3326.24% | SNDK |
| Nasdaq-100 Top1 PIT membership | 3642.62% | -60.36% | 1.17 | 79 | 40 | 77 | 0 | 30 | 10 | 240.31% | 280.61% | 3402.31% | 3362.02% | SNDK |

Important limitation: this uses today's Nasdaq-100 constituents plus the changes table to prevent buying known future additions. It still does not add historical members that were later removed.

## Output Files

- Excel workbook: `reports\nasdaq100_top1_point_in_time_membership_2020_2026ytd.xlsx`
- Summary CSV: `reports\nasdaq100_top1_point_in_time_membership_2020_2026ytd_summary.csv`
- Trades CSV: `reports\nasdaq100_top1_point_in_time_membership_2020_2026ytd_trades.csv`
- Monthly decisions CSV: `reports\nasdaq100_top1_point_in_time_membership_2020_2026ytd_monthly_decisions.csv`
- Equity curve CSV: `reports\nasdaq100_top1_point_in_time_membership_2020_2026ytd_equity_curve.csv`
