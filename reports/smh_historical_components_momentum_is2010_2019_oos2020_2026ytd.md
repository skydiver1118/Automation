# SMH Historical Components Momentum IS/OOS Search

In-sample: 2010-01-01 to 2019-12-31.
Out-of-sample: 2020-01-01 to latest available data through 2026-05-24.
Universe: historical SMH / legacy Semiconductor HOLDRS holdings extracted from public SEC filings.
Point-in-time rule: each month uses only the latest holdings snapshot whose SEC filing date is on or before the signal date.
Execution: monthly signal after prior month-end close; trade at next month first open; final open position marked to latest close.
Score: Close[t-skip] / Close[t-lookback] - 1.
Cash/DCA tested: no cash filter, SMH SMA100, SMH SMA200, SMH SMA200 plus selected stocks above SMA200; DCA1 and DCA3.
Historical tickers in SEC list: 41. Price-available tickers: 31. Candidates tested: 192. Passed IS max drawdown < 50%: 163.

## Top 3 Strategies by IS Sharpe

| strategy | is_return | is_cagr | is_max_drawdown | is_sharpe | oos_return | oos_cagr | oos_max_drawdown | oos_sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SMH_HIST_PIT Top2 L252 S0 smh_sma100 DCA3 | 1957.01% | 35.32% | -21.33% | 1.44 | 679.66% | 37.88% | -25.78% | 1.11 |
| SMH_HIST_PIT Top2 L252 S0 smh_sma100 DCA1 | 2249.91% | 37.14% | -22.84% | 1.37 | 993.60% | 45.38% | -26.89% | 1.23 |
| SMH_HIST_PIT Top1 L252 S0 smh_sma100 DCA3 | 3117.29% | 41.52% | -21.53% | 1.35 | 1106.79% | 47.64% | -40.24% | 1.12 |

## SMH Benchmark

| strategy | is_return | is_cagr | is_max_drawdown | is_sharpe | oos_return | oos_cagr | oos_max_drawdown | oos_sharpe |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SMH buy-and-hold monthly open-to-open | 475.52% | 19.13% | -22.46% | 0.96 | 731.93% | 39.29% | -39.84% | 1.21 |

## Price Data Caveat

Some acquired/delisted historical holdings do not have usable Yahoo Finance price history in this run.
Unavailable tickers: ALTR, ATML, BRCM, CREE, IDTI, LLTC, LSI, MXIM, NVLS, XLNX.

## Output Files

- Excel workbook: `reports\smh_historical_components_momentum_is2010_2019_oos2020_2026ytd.xlsx`
- CSV: `reports\smh_historical_components_momentum_is2010_2019_oos2020_2026ytd.csv`
- Markdown report: `reports\smh_historical_components_momentum_is2010_2019_oos2020_2026ytd.md`