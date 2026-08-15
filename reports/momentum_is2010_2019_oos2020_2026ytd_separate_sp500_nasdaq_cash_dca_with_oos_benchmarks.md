# Separate Momentum IS/OOS Search With OOS Benchmarks

OOS benchmark period: 2020-01-01 through latest available data as of 2026-05-24.
S&P 500 benchmark uses SPY as a tradable proxy; Nasdaq-100 benchmark uses QQQ as a tradable proxy.

## OOS Benchmark Return and Drawdown

| benchmark | symbol | start_used | end_used | oos_return | oos_cagr | oos_max_drawdown | oos_sharpe_daily |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S&P 500 (SPY proxy) | SPY | 2020-01-02 | 2026-05-22 | 151.15% | 15.52% | -33.72% | 0.81 |
| Nasdaq-100 (QQQ proxy) | QQQ | 2020-01-02 | 2026-05-22 | 244.45% | 21.37% | -35.12% | 0.90 |

## Selected Strategy Context

| universe | strategy | is_max_drawdown | is_sharpe | oos_return | oos_cagr | oos_max_drawdown | oos_sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 none DCA3 | -19.45% | 1.53 | 883.03% | 43.00% | -22.21% | 1.25 |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 none DCA1 | -19.45% | 1.45 | 883.03% | 43.00% | -22.21% | 1.25 |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 benchmark_sma200 DCA1 | -19.45% | 1.23 | 537.36% | 33.62% | -17.07% | 1.14 |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 benchmark_sma200 DCA3 | -19.45% | 1.22 | 329.92% | 25.64% | -21.78% | 1.00 |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 benchmark_sma100 DCA3 | -19.45% | 1.22 | 255.04% | 21.93% | -16.66% | 0.94 |
| NASDAQ100 | NASDAQ100 Top3 L63 S21 none DCA3 | -26.91% | 1.22 | 652.62% | 37.14% | -40.03% | 1.00 |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 both_sma200 DCA1 | -18.13% | 1.19 | 564.03% | 34.48% | -16.84% | 1.17 |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 both_sma200 DCA3 | -18.21% | 1.19 | 362.00% | 27.06% | -17.73% | 1.06 |
| NASDAQ100 | NASDAQ100 Top5 L63 S0 benchmark_sma100 DCA1 | -19.59% | 1.19 | 432.42% | 29.91% | -18.38% | 1.08 |
| NASDAQ100 | NASDAQ100 Top5 L252 S0 none DCA3 | -27.09% | 1.18 | 683.02% | 38.00% | -49.95% | 0.99 |
| SP500 | SP500 Top1 L252 S21 benchmark_sma100 DCA3 | -43.34% | 0.88 | 35.65% | 4.89% | -67.50% | 0.31 |
| SP500 | SP500 Top5 L252 S21 none DCA1 | -39.39% | 0.86 | 430.81% | 29.85% | -30.05% | 0.86 |
| SP500 | SP500 Top5 L126 S21 none DCA1 | -31.47% | 0.85 | 440.38% | 30.22% | -32.16% | 0.87 |
| SP500 | SP500 Top5 L126 S21 none DCA3 | -31.47% | 0.85 | 440.38% | 30.22% | -32.16% | 0.87 |
| SP500 | SP500 Top5 L252 S21 none DCA3 | -39.39% | 0.85 | 430.81% | 29.85% | -30.05% | 0.86 |
| SP500 | SP500 Top2 L63 S21 none DCA3 | -42.51% | 0.84 | 162.84% | 16.33% | -55.27% | 0.52 |
| SP500 | SP500 Top2 L63 S21 none DCA1 | -42.51% | 0.82 | 162.84% | 16.33% | -55.27% | 0.52 |
| SP500 | SP500 Top3 L126 S21 none DCA1 | -34.74% | 0.82 | 567.06% | 34.58% | -30.70% | 0.89 |
| SP500 | SP500 Top3 L126 S21 none DCA3 | -34.74% | 0.80 | 567.06% | 34.58% | -30.70% | 0.89 |
| SP500 | SP500 Top5 L63 S0 none DCA3 | -32.36% | 0.80 | 810.89% | 41.30% | -18.21% | 1.25 |
| NASDAQ100 | NASDAQ100 Top3 L126 S21 none DCA1 | -31.89% | 0.94 | 2123.73% | 62.48% | -37.50% | 1.40 |
| NASDAQ100 | NASDAQ100 Top3 L126 S21 none DCA3 | -31.89% | 0.95 | 2123.73% | 62.48% | -37.50% | 1.40 |
| NASDAQ100 | NASDAQ100 Top2 L126 S21 none DCA1 | -37.47% | 0.98 | 3216.04% | 72.97% | -33.33% | 1.38 |
| NASDAQ100 | NASDAQ100 Top2 L126 S21 none DCA3 | -37.47% | 0.99 | 3216.04% | 72.97% | -33.33% | 1.38 |
| NASDAQ100 | NASDAQ100 Top2 L126 S0 none DCA1 | -32.01% | 0.79 | 2558.01% | 67.08% | -36.57% | 1.32 |
| SP500 | SP500 Top5 L63 S0 none DCA1 | -32.36% | 0.78 | 810.89% | 41.30% | -18.21% | 1.25 |
| SP500 | SP500 Top3 L126 S0 none DCA1 | -44.98% | 0.53 | 1218.08% | 49.71% | -23.69% | 1.16 |
| SP500 | SP500 Top3 L126 S0 none DCA3 | -44.98% | 0.56 | 1218.08% | 49.71% | -23.69% | 1.16 |
| SP500 | SP500 Top3 L63 S0 none DCA1 | -45.13% | 0.32 | 1163.54% | 48.73% | -23.24% | 1.15 |

## Output Files

- Excel workbook: `reports\momentum_is2010_2019_oos2020_2026ytd_separate_sp500_nasdaq_cash_dca_with_oos_benchmarks.xlsx`
- Benchmark CSV: `reports\momentum_is2010_2019_oos2020_2026ytd_separate_sp500_nasdaq_cash_dca_with_oos_benchmarks.csv`
- Markdown report: `reports\momentum_is2010_2019_oos2020_2026ytd_separate_sp500_nasdaq_cash_dca_with_oos_benchmarks.md`