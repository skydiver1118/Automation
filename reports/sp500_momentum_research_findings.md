# Momentum Strategy Research Findings

Goal: find a S&P 500 stock-rotation strategy that beats SPMO over 2020-01-01 to 2025-12-31.

Benchmark:

- SPMO total return: 202.49%.

Research inputs:

- S&P's momentum methodology uses 12-month momentum excluding the most recent month, and the S&P 500 Momentum Index rebalances semiannually.
- S&P also describes risk-adjusted momentum as momentum divided by volatility.
- Reddit ETF discussions repeatedly highlighted SPMO's slower six-month rebalance schedule, FMTM-style faster rebalance approaches, equal weighting, and tactical market filters as possible improvements.

Rules tested:

- Existing baseline: daily rebalance, top 5, 126-trading-day raw momentum.
- Skip-month momentum: rank using 126-day or 252-day momentum, excluding the most recent 21 trading days.
- Volatility-adjusted momentum: divide momentum by recent realized volatility.
- SMA50/SMA100 top-N gate: rank first, then only hold top-N names that are above the SMA.
- SPY SMA200 market filter: hold cash when SPY is below its SMA200.
- Monthly rebalance variant.
- Concentration: top 1, top 2, top 3, top 4, and top 5.

Best observed candidates:

| Variant | Positions | Return | Excess vs SPMO | Max DD | Sharpe |
| --- | ---: | ---: | ---: | ---: | ---: |
| 126 raw + SMA50 topN | 1 | 451.63% | 249.13% | -63.58% | 0.77 |
| 126 raw + SPY SMA200 | 1 | 410.99% | 208.50% | -60.74% | 0.76 |
| 126 raw baseline | 1 | 395.88% | 193.39% | -67.67% | 0.74 |
| 126 skip21 | 2 | 347.25% | 144.76% | -45.59% | 0.77 |
| 126 skip21 | 3 | 317.08% | 114.59% | -41.78% | 0.78 |
| 126 skip21 | 4 | 251.60% | 49.10% | -38.64% | 0.74 |
| 126 raw baseline | 3 | 234.07% | 31.58% | -44.88% | 0.68 |
| 252 skip21 | 3 | 206.09% | 3.60% | -36.66% | 0.66 |

Interpretation:

- The strongest return came from top-1 concentration, but the drawdown was too large for a practical default.
- The best balanced candidate found so far is top 3 using 126-trading-day momentum excluding the most recent 21 trading days. It beat SPMO by 114.59 percentage points, with max drawdown of -41.78%.
- Top 4 with the same 126 skip21 rule also beat SPMO, but by less, and had slightly lower drawdown.
- The SMA50 gate helped the single-stock raw momentum version, but hurt the top-2/top-3/top-4 skip-month versions.
- The SPY SMA200 market filter and monthly rebalance did not improve the best top-3 candidate in this test window.
- Volatility-adjusted momentum performed poorly in this specific daily stock-rotation setup.

Current candidate to carry forward:

- Rank S&P 500 stocks daily by 126-trading-day momentum excluding the most recent 21 trading days.
- Hold the top 3 names, equal weight.
- Execute exits and entries at the next trading day's open.
- No SMA gate for now.

Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.
