# Separate Momentum IS/OOS Strategy Search

In-sample: 2010-01-01 to 2019-12-31.
Out-of-sample: 2020-01-01 to latest available data through 2026-05-23.
Universes searched separately: point-in-time S&P 500 and reconstructed point-in-time Nasdaq-100.
Execution: monthly signal after prior month-end close; trade at next month first open; final open position marked to latest close.
Score: Close[t-skip] / Close[t-lookback] - 1.
Cash/DCA tested: no cash filter, universe benchmark SMA100/SMA200, benchmark SMA200 plus selected stocks above SMA200; DCA1 and DCA3.
Candidates tested: 384. Passed IS max drawdown < 50%: 266.

## Top Passed Candidates by Universe Ranked by IS Sharpe

| universe | strategy | is_return | is_cagr | is_max_drawdown | is_sharpe | oos_return | oos_cagr | oos_max_drawdown | oos_sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 none DCA3 | 1597.21% | 32.75% | -19.45% | 1.53 | 883.03% | 43.00% | -22.21% | 1.25 |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 none DCA1 | 1459.78% | 31.63% | -19.45% | 1.45 | 883.03% | 43.00% | -22.21% | 1.25 |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 benchmark_sma200 DCA1 | 794.86% | 24.51% | -19.45% | 1.23 | 537.36% | 33.62% | -17.07% | 1.14 |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 benchmark_sma200 DCA3 | 687.73% | 22.93% | -19.45% | 1.22 | 329.92% | 25.64% | -21.78% | 1.00 |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 benchmark_sma100 DCA3 | 619.33% | 21.82% | -19.45% | 1.22 | 255.04% | 21.93% | -16.66% | 0.94 |
| NASDAQ100 | NASDAQ100 Top3 L63 S21 none DCA3 | 1148.81% | 28.73% | -26.91% | 1.22 | 652.62% | 37.14% | -40.03% | 1.00 |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 both_sma200 DCA1 | 728.41% | 23.56% | -18.13% | 1.19 | 564.03% | 34.48% | -16.84% | 1.17 |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 both_sma200 DCA3 | 638.50% | 22.14% | -18.21% | 1.19 | 362.00% | 27.06% | -17.73% | 1.06 |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 benchmark_sma100 DCA1 | 684.26% | 22.88% | -19.59% | 1.19 | 432.42% | 29.91% | -18.38% | 1.08 |
| NASDAQ100 | NASDAQ100 Top5 L252 S0 none DCA3 | 1265.63% | 29.89% | -27.09% | 1.18 | 683.02% | 38.00% | -49.95% | 0.99 |
| NASDAQ100 | NASDAQ100 Top3 L63 S21 none DCA1 | 1088.37% | 28.10% | -26.91% | 1.18 | 652.62% | 37.14% | -40.03% | 1.00 |
| NASDAQ100 | NASDAQ100 Top3 L252 S0 none DCA3 | 1580.18% | 32.61% | -35.94% | 1.17 | 1486.39% | 54.12% | -56.32% | 1.06 |
| NASDAQ100 | NASDAQ100 Top2 L63 S21 none DCA3 | 1432.87% | 31.40% | -37.61% | 1.16 | 591.80% | 35.35% | -46.52% | 0.86 |
| NASDAQ100 | NASDAQ100 Top3 L252 S0 none DCA1 | 1574.48% | 32.57% | -35.94% | 1.15 | 1486.39% | 54.12% | -56.32% | 1.06 |
| NASDAQ100 | NASDAQ100 Top5 L252 S0 none DCA1 | 1223.86% | 29.49% | -27.09% | 1.15 | 683.02% | 38.00% | -49.95% | 0.99 |
| NASDAQ100 | NASDAQ100 Top5 L63 S21 none DCA3 | 845.05% | 25.19% | -29.73% | 1.15 | 768.35% | 40.25% | -35.38% | 1.14 |
| NASDAQ100 | NASDAQ100 Top2 L63 S21 none DCA1 | 1347.93% | 30.65% | -37.61% | 1.12 | 591.80% | 35.35% | -46.52% | 0.86 |
| NASDAQ100 | NASDAQ100 Top3 L63 S0 none DCA3 | 1130.65% | 28.55% | -34.27% | 1.11 | 1505.86% | 54.41% | -33.02% | 1.24 |
| NASDAQ100 | NASDAQ100 Top5 L252 S21 none DCA3 | 1075.79% | 27.96% | -30.54% | 1.11 | 859.99% | 42.47% | -47.50% | 1.08 |
| NASDAQ100 | NASDAQ100 Top5 L126 S0 none DCA3 | 688.58% | 22.95% | -26.85% | 1.10 | 989.15% | 45.31% | -34.49% | 1.16 |
| SP500 | SP500 Top1 L252 S21 benchmark_sma100 DCA3 | 803.89% | 24.64% | -43.34% | 0.88 | 35.65% | 4.89% | -67.50% | 0.31 |
| SP500 | SP500 Top5 L252 S21 none DCA1 | 472.25% | 19.07% | -39.39% | 0.86 | 430.81% | 29.85% | -30.05% | 0.86 |
| SP500 | SP500 Top5 L126 S21 none DCA1 | 395.85% | 17.37% | -31.47% | 0.85 | 440.38% | 30.22% | -32.16% | 0.87 |
| SP500 | SP500 Top5 L126 S21 none DCA3 | 388.66% | 17.20% | -31.47% | 0.85 | 440.38% | 30.22% | -32.16% | 0.87 |
| SP500 | SP500 Top5 L252 S21 none DCA3 | 462.02% | 18.85% | -39.39% | 0.85 | 430.81% | 29.85% | -30.05% | 0.86 |
| SP500 | SP500 Top2 L63 S21 none DCA3 | 885.81% | 25.72% | -42.51% | 0.84 | 162.84% | 16.33% | -55.27% | 0.52 |
| SP500 | SP500 Top2 L63 S21 none DCA1 | 820.67% | 24.87% | -42.51% | 0.82 | 162.84% | 16.33% | -55.27% | 0.52 |
| SP500 | SP500 Top3 L126 S21 none DCA1 | 547.73% | 20.55% | -34.74% | 0.82 | 567.06% | 34.58% | -30.70% | 0.89 |
| SP500 | SP500 Top3 L126 S21 none DCA3 | 521.02% | 20.04% | -34.74% | 0.80 | 567.06% | 34.58% | -30.70% | 0.89 |
| SP500 | SP500 Top5 L63 S0 none DCA3 | 352.68% | 16.31% | -32.36% | 0.80 | 810.89% | 41.30% | -18.21% | 1.25 |
| SP500 | SP500 Top5 L63 S0 none DCA1 | 333.96% | 15.82% | -32.36% | 0.78 | 810.89% | 41.30% | -18.21% | 1.25 |
| SP500 | SP500 Top3 L63 S21 none DCA3 | 508.58% | 19.80% | -36.32% | 0.77 | 144.28% | 15.00% | -54.03% | 0.54 |
| SP500 | SP500 Top5 L252 S21 both_sma200 DCA3 | 245.12% | 13.19% | -33.97% | 0.77 | 69.17% | 8.57% | -22.26% | 0.47 |
| SP500 | SP500 Top5 L252 S21 benchmark_sma200 DCA3 | 254.08% | 13.48% | -35.93% | 0.77 | 64.01% | 8.05% | -19.81% | 0.44 |
| SP500 | SP500 Top3 L63 S21 none DCA1 | 498.00% | 19.59% | -36.32% | 0.77 | 144.28% | 15.00% | -54.03% | 0.54 |
| SP500 | SP500 Top5 L63 S21 none DCA3 | 359.45% | 16.48% | -29.51% | 0.76 | 306.59% | 24.55% | -39.86% | 0.77 |
| SP500 | SP500 Top2 L252 S21 benchmark_sma100 DCA1 | 463.03% | 18.87% | -45.16% | 0.76 | 220.99% | 20.02% | -38.87% | 0.73 |
| SP500 | SP500 Top5 L252 S21 benchmark_sma100 DCA1 | 238.03% | 12.96% | -30.75% | 0.75 | 62.87% | 7.93% | -34.50% | 0.42 |
| SP500 | SP500 Top5 L252 S21 benchmark_sma200 DCA1 | 268.55% | 13.94% | -41.69% | 0.75 | 104.12% | 11.81% | -27.43% | 0.54 |
| SP500 | SP500 Top5 L126 S21 both_sma200 DCA3 | 228.19% | 12.62% | -31.70% | 0.75 | 113.15% | 12.57% | -36.92% | 0.52 |

## Output Files

- Excel workbook: `reports\momentum_is2010_2019_oos2020_2026ytd_separate_sp500_nasdaq_cash_dca.xlsx`
- CSV: `reports\momentum_is2010_2019_oos2020_2026ytd_separate_sp500_nasdaq_cash_dca.csv`
- Markdown report: `reports\momentum_is2010_2019_oos2020_2026ytd_separate_sp500_nasdaq_cash_dca.md`

Important limitations: delisted tickers with no Yahoo price history are skipped implicitly; Nasdaq-100 point-in-time membership is reconstructed from Wikipedia's current members and changes table.
