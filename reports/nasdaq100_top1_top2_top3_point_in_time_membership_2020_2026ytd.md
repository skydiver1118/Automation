# Nasdaq-100 Top1/Top2/Top3 Point-in-Time Membership Backtest

Period: 2020-01-01 through 2026-05-17.
Execution: monthly signal after month-end close, trade next trading day's open, hold open-to-open.
Ranking: 126 trading-day momentum, skipping the latest 21 trading days.
Point-in-time rule: fill each Top N slot by walking down the rank list and skipping stocks with known Nasdaq-100 add dates after the purchase date.
Add-date source: Wikipedia Nasdaq-100 changes table, cached locally.

| Top N | Strategy | Return | Max DD | Sharpe | Trades | Buys | Skipped Future Members | Violations | Known-Date Buys | Assumed Pre-window Buys | QQQ | VGT | Final Holdings |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | Current members only | 3606.85% | -67.36% | 1.09 | 77 | 39 | 0 | 0 | 35 | 4 | 240.31% | 280.61% | SNDK |
| 1 | Nasdaq-100 changes date | 3642.62% | -60.36% | 1.17 | 79 | 40 | 77 | 0 | 30 | 10 | 240.31% | 280.61% | SNDK |
| 2 | Current members only | 6982.73% | -52.79% | 1.38 | 138 | 70 | 0 | 0 | 61 | 9 | 240.31% | 280.61% | SNDK, WDC |
| 2 | Nasdaq-100 changes date | 2811.06% | -52.49% | 1.23 | 146 | 74 | 123 | 0 | 60 | 14 | 240.31% | 280.61% | SNDK, WDC |
| 3 | Current members only | 13331.01% | -45.49% | 1.68 | 205 | 104 | 0 | 0 | 93 | 11 | 240.31% | 280.61% | SNDK, WDC, STX |
| 3 | Nasdaq-100 changes date | 1857.30% | -45.49% | 1.22 | 213 | 108 | 161 | 0 | 88 | 20 | 240.31% | 280.61% | SNDK, WDC, STX |

Important limitation: this uses today's Nasdaq-100 constituents plus the changes table to prevent buying known future additions. It still does not add historical members that were later removed.

## Output Files

- Excel workbook: `reports\nasdaq100_top1_top2_top3_point_in_time_membership_2020_2026ytd.xlsx`
- Summary CSV: `reports\nasdaq100_top1_top2_top3_point_in_time_membership_2020_2026ytd_summary.csv`
- Trades CSV: `reports\nasdaq100_top1_top2_top3_point_in_time_membership_2020_2026ytd_trades.csv`
- Monthly decisions CSV: `reports\nasdaq100_top1_top2_top3_point_in_time_membership_2020_2026ytd_monthly_decisions.csv`
- Equity curve CSV: `reports\nasdaq100_top1_top2_top3_point_in_time_membership_2020_2026ytd_equity_curve.csv`
