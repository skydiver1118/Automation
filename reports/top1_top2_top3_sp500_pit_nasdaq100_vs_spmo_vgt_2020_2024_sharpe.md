# Top1/Top2/Top3 Monthly Skip-Momentum Comparison With Sharpe

Period: 2020-01-01 through 2024-12-31.
Execution: monthly signal after month-end close, trade at next trading day's open, hold open-to-open.
Ranking: 126 trading-day momentum, skipping the latest 21 trading days.
Sharpe ratio: annualized from daily open-to-open strategy returns, risk-free rate assumed 0%.
S&P 500 rule: skip stocks whose `Date added` is after the purchase date, then choose the next eligible ranked stock.
Nasdaq-100 note: the cached Nasdaq-100 constituent table has no add-date field, so Nasdaq-100 rows use current constituents only.

| Universe | Top N | Membership Filter | Return | Max DD | Sharpe | Trades | Buys | Skipped Future Members | Violations | SPMO | VGT | Final Holdings |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |
| S&P 500 | 1 | Date added | 127.97% | -53.85% | 0.57 | 77 | 39 | 101 | 0 | 138.97% | 159.63% | PLTR |
| S&P 500 | 2 | Date added | 87.13% | -49.12% | 0.50 | 146 | 74 | 151 | 0 | 138.97% | 159.63% | PLTR, TPL |
| S&P 500 | 3 | Date added | 71.37% | -46.23% | 0.47 | 207 | 105 | 197 | 0 | 138.97% | 159.63% | PLTR, TPL, GEV |
| Nasdaq-100 | 1 | Not available/current constituents | 258.39% | -67.36% | 0.71 | 71 | 36 | 0 | N/A | 138.97% | 159.63% | APP |
| Nasdaq-100 | 2 | Not available/current constituents | 760.71% | -52.79% | 1.05 | 116 | 59 | 0 | N/A | 138.97% | 159.63% | APP, PLTR |
| Nasdaq-100 | 3 | Not available/current constituents | 1531.43% | -44.95% | 1.38 | 171 | 87 | 0 | N/A | 138.97% | 159.63% | APP, PLTR, ALNY |

## Output Files

- Excel workbook: `reports\top1_top2_top3_sp500_pit_nasdaq100_vs_spmo_vgt_2020_2024_sharpe.xlsx`
- Summary CSV: `reports\top1_top2_top3_sp500_pit_nasdaq100_vs_spmo_vgt_2020_2024_sharpe.csv`
- Trades CSV: `reports\top1_top2_top3_sp500_pit_nasdaq100_vs_spmo_vgt_2020_2024_sharpe_trades.csv`
- Monthly decisions CSV: `reports\top1_top2_top3_sp500_pit_nasdaq100_vs_spmo_vgt_2020_2024_sharpe_monthly_decisions.csv`
- Equity curve CSV: `reports\top1_top2_top3_sp500_pit_nasdaq100_vs_spmo_vgt_2020_2024_sharpe_equity_curve.csv`
