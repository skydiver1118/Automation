# Nasdaq-100 Top1/Top2/Top3 Point-in-Time Filter Only

Period: 2020-01-01 through 2024-12-31.
Execution: monthly signal after month-end close, trade next trading day's open, hold open-to-open.
Ranking: 126 trading-day momentum, skipping the latest 21 trading days.
Point-in-time rule: fill each Top N slot by walking down the rank list and skipping stocks with known Nasdaq-100 add dates after the purchase date.

| Top N | Return | Max DD | Sharpe | Trades | Buys | Skipped Future Members | Violations | QQQ | VGT | Final Holdings |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | 858.70% | -59.43% | 1.03 | 69 | 35 | 66 | 0 | 143.86% | 159.63% | APP |
| 2 | 628.40% | -45.61% | 1.05 | 118 | 60 | 111 | 0 | 143.86% | 159.63% | APP, TSLA |
| 3 | 456.49% | -39.26% | 1.01 | 165 | 84 | 143 | 0 | 143.86% | 159.63% | APP, TSLA, ADSK |

Important limitation: this uses today's Nasdaq-100 constituents plus the changes table to prevent buying known future additions. It still does not add historical members that were later removed.

## Output Files

- Excel workbook: `reports\nasdaq100_top1_top2_top3_pit_2020_2024.xlsx`
- Summary CSV: `reports\nasdaq100_top1_top2_top3_pit_2020_2024_summary.csv`
- Trades CSV: `reports\nasdaq100_top1_top2_top3_pit_2020_2024_trades.csv`
- Monthly decisions CSV: `reports\nasdaq100_top1_top2_top3_pit_2020_2024_monthly_decisions.csv`
- Equity curve CSV: `reports\nasdaq100_top1_top2_top3_pit_2020_2024_equity_curve.csv`
