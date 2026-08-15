# Momentum IS/OOS Strategy Search

In-sample: 2010-01-01 to 2019-12-31.
Out-of-sample: 2020-01-01 to latest available data through 2026-05-23.
Universe: monthly point-in-time union of S&P 500 and Nasdaq-100 stocks.
Execution: monthly signal after prior month-end close; trade at next month first open; final open position marked to latest close.
Score: Close[t-skip] / Close[t-lookback] - 1.
Cash/DCA tested: no cash filter, QQQ SMA100, QQQ SMA200, QQQ SMA200 plus selected stocks above SMA200; DCA1 and DCA3.
Candidates tested: 192. Passed IS max drawdown < 50%: 118.

## Top 20 Passed Candidates Ranked by IS Sharpe

| strategy | is_return | is_cagr | is_max_drawdown | is_sharpe | oos_return | oos_cagr | oos_max_drawdown | oos_sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| COMBINED Top5 L63 S21 none DCA3 | 565.33% | 20.88% | -26.61% | 0.92 | 571.72% | 34.72% | -41.95% | 0.96 |
| COMBINED Top2 L63 S21 none DCA3 | 1210.72% | 29.36% | -42.36% | 0.91 | 527.62% | 33.30% | -43.86% | 0.76 |
| COMBINED Top5 L63 S21 none DCA1 | 546.07% | 20.52% | -26.61% | 0.90 | 571.72% | 34.72% | -41.95% | 0.96 |
| COMBINED Top2 L63 S21 none DCA1 | 1124.12% | 28.48% | -42.36% | 0.89 | 527.62% | 33.30% | -43.86% | 0.76 |
| COMBINED Top3 L63 S21 none DCA3 | 749.99% | 23.87% | -33.39% | 0.87 | 624.66% | 36.33% | -37.30% | 0.91 |
| COMBINED Top5 L126 S21 none DCA1 | 439.26% | 18.36% | -29.67% | 0.87 | 878.16% | 42.89% | -30.47% | 1.09 |
| COMBINED Top5 L126 S21 none DCA3 | 431.44% | 18.19% | -29.67% | 0.86 | 878.16% | 42.89% | -30.47% | 1.09 |
| COMBINED Top3 L63 S21 none DCA1 | 735.20% | 23.66% | -33.39% | 0.86 | 624.66% | 36.33% | -37.30% | 0.91 |
| COMBINED Top3 L252 S21 none DCA1 | 605.09% | 21.58% | -45.65% | 0.85 | 2183.68% | 63.16% | -26.34% | 1.18 |
| COMBINED Top5 L252 S21 none DCA1 | 493.24% | 19.50% | -39.39% | 0.84 | 1070.02% | 46.95% | -27.35% | 1.06 |
| COMBINED Top1 L252 S21 benchmark_sma100 DCA3 | 879.99% | 25.65% | -44.71% | 0.83 | 287.34% | 23.60% | -63.95% | 0.64 |
| COMBINED Top5 L252 S21 none DCA3 | 473.98% | 19.10% | -39.39% | 0.83 | 1070.02% | 46.95% | -27.35% | 1.06 |
| COMBINED Top3 L252 S21 none DCA3 | 548.67% | 20.57% | -45.65% | 0.82 | 2183.68% | 63.16% | -26.34% | 1.18 |
| COMBINED Top2 L63 S21 benchmark_sma200 DCA1 | 694.73% | 23.04% | -39.51% | 0.80 | 98.93% | 11.36% | -51.80% | 0.43 |
| COMBINED Top1 L63 S21 none DCA3 | 1413.83% | 31.24% | -44.08% | 0.78 | 1805.14% | 58.60% | -59.76% | 0.85 |
| COMBINED Top5 L63 S21 both_sma200 DCA1 | 299.29% | 14.86% | -36.59% | 0.78 | 338.68% | 26.03% | -40.27% | 0.82 |
| COMBINED Top1 L63 S21 none DCA1 | 1333.69% | 30.52% | -44.08% | 0.77 | 1805.14% | 58.60% | -59.76% | 0.85 |
| COMBINED Top5 L252 S21 both_sma200 DCA1 | 292.08% | 14.65% | -27.27% | 0.77 | 338.10% | 26.01% | -34.59% | 0.79 |
| COMBINED Top3 L63 S21 benchmark_sma200 DCA1 | 445.33% | 18.49% | -37.75% | 0.76 | 121.59% | 13.26% | -41.31% | 0.50 |
| COMBINED Top5 L63 S21 benchmark_sma200 DCA1 | 310.14% | 15.16% | -33.02% | 0.76 | 252.18% | 21.78% | -41.95% | 0.72 |

## Output Files

- Excel workbook: `reports\momentum_is2010_2019_oos2020_2026ytd_combined_cash_dca_fast.xlsx`
- CSV: `reports\momentum_is2010_2019_oos2020_2026ytd_combined_cash_dca_fast.csv`
- Markdown report: `reports\momentum_is2010_2019_oos2020_2026ytd_combined_cash_dca_fast.md`

Important limitations: delisted tickers with no Yahoo price history are skipped implicitly; Nasdaq-100 point-in-time membership is reconstructed from Wikipedia's current members and changes table.
