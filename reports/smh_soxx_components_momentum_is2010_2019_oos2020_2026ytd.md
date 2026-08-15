# SMH/SOXX Components Momentum IS/OOS Search

In-sample: 2010-01-01 to 2019-12-31.
Out-of-sample: 2020-01-01 to latest available data through 2026-05-24.
Universe: current SMH holdings union current SOXX holdings, treated as the semiconductor index universe.
Execution: monthly signal after prior month-end close; trade at next month first open; final open position marked to latest close.
Score: Close[t-skip] / Close[t-lookback] - 1.
Cash/DCA tested: no cash filter, SMH SMA100, SMH SMA200, SMH SMA200 plus selected stocks above SMA200; DCA1 and DCA3.
Holdings count in union: 30. Candidates tested: 192. Passed IS max drawdown < 50%: 170.

## Top 3 Strategies by IS Sharpe

| strategy | is_return | is_cagr | is_max_drawdown | is_sharpe | oos_return | oos_cagr | oos_max_drawdown | oos_sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SMH_UNION Top3 L252 S21 smh_sma100 DCA3 | 1706.80% | 33.58% | -15.17% | 1.52 | 434.24% | 29.97% | -34.03% | 1.03 |
| SMH_UNION Top3 L252 S21 smh_sma100 DCA1 | 2134.83% | 36.45% | -24.33% | 1.45 | 618.92% | 36.15% | -38.69% | 1.11 |
| SMH_UNION Top3 L252 S0 smh_sma100 DCA3 | 1524.81% | 32.17% | -17.42% | 1.41 | 458.65% | 30.88% | -30.46% | 1.05 |

## SMH Benchmark

| strategy | is_return | is_cagr | is_max_drawdown | is_sharpe | oos_return | oos_cagr | oos_max_drawdown | oos_sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SMH buy-and-hold monthly open-to-open | 475.52% | 19.13% | -22.46% | 0.96 | 731.93% | 39.29% | -39.84% | 1.21 |

## Output Files

- Excel workbook: `reports\smh_soxx_components_momentum_is2010_2019_oos2020_2026ytd.xlsx`
- CSV: `reports\smh_soxx_components_momentum_is2010_2019_oos2020_2026ytd.csv`
- Markdown report: `reports\smh_soxx_components_momentum_is2010_2019_oos2020_2026ytd.md`

Important limitation: this uses current SMH/SOXX holdings, not historical holdings, because a clean long-run historical holdings file was not available. This can introduce survivorship/constituent lookahead bias.