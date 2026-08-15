# Strategy Variant Search - Beat Asset Return Retry

Run date: May 19, 2026  
Script: `C:\Users\skydiver1118\Documents\New project\scripts\strategy_variant_search.py`  
Data: Yahoo Finance via `yfinance`; adjusted prices; no commissions, slippage, borrow cost, spread, financing, or tax effects.  
Search size: 3,400 total variants across VWAP, ORB, moving-average trend following, daily absolute momentum, RSI pullback, and GEM-style ETF rotation.

Important caveat: this is an in-sample optimizer. The results below answer the request to keep trying until a variant beats asset return, but they should not be treated as live-ready without walk-forward testing, costs, and TrendSpider confirmation.

## Found A Same-Symbol Asset Beater

The best same-symbol result was a revised TQQQ daily moving-average strategy:

| Strategy | Entry | Exit | Period tested | Strategy return | Asset return | Excess vs asset | Max DD | Positions | Win rate |
|---|---|---|---|---:|---:|---:|---:|---:|---:|
| TQQQ SMA3/SMA252 crossover | Buy TQQQ when SMA3 crosses above SMA252 | Exit when SMA3 crosses below SMA252 | 2018-01-02 to 2026-05-19 | 1,576.97% | 1,159.15% | 417.83 pp | -48.14% | 7 | 71.43% |

This is the first clean "beat asset return" result because the benchmark asset is the same ETF being traded: TQQQ. The rule is still aggressive because TQQQ itself is leveraged, but it improved the full-period return while cutting max drawdown versus buy-and-hold TQQQ. A quick subperiod check is mixed: it underperformed TQQQ in 2018-2021 and 2024-2026, but strongly outperformed through the 2022 bear market/recovery segment.

## Best Variant By Strategy Family

| Rank by excess | Family | Best variant found | Symbol / benchmark | Timeframe | Period tested | Strategy return | Asset return | Excess vs asset | Beat asset? | Max DD | Positions | Win rate |
|---:|---|---|---|---|---|---:|---:|---:|---|---:|---:|---:|
| 1 | Moving-average crossover / trend following | SMA3/SMA252 cross, no stop | TQQQ / TQQQ | Daily | 2018-01-02 to 2026-05-19 | 1,576.97% | 1,159.15% | 417.83 pp | Yes | -48.14% | 7 | 71.43% |
| 2 | GEM-style momentum rotation | SPY/QQQ/TQQQ rotation, 9-month lookback, defensive BIL | Rotation / SPY | Daily signal, monthly rebalance | 2018-01-02 to 2026-05-19 | 431.06% | 210.16% | 220.89 pp | Yes | -69.92% | 22 | 72.73% |
| 3 | Opening range breakout | Long-only, 3-bar ORB, no volume filter, 2.0R target | QQQ / QQQ | 5-minute | 2026-02-24 to 2026-05-19 | 8.39% | 16.77% | -8.37 pp | No | -4.39% | 56 | 62.50% |
| 4 | VWAP trend / reclaim | Long-only reclaim, after 3 bars, no target, no stop | QQQ / QQQ | 5-minute | 2026-02-24 to 2026-05-19 | 7.68% | 16.77% | -9.09 pp | No | -6.16% | 155 | 29.03% |
| 5 | Absolute momentum | 252-day positive return, above SMA150, no stop | SPY / SPY | Daily | 2018-01-02 to 2026-05-19 | 157.33% | 210.16% | -52.84 pp | No | -18.22% | 18 | 38.89% |
| 6 | RSI(2) / mean reversion | RSI2 <= 10, above SMA150, exit above SMA5, no stop | SPY / SPY | Daily | 2018-01-02 to 2026-05-19 | 72.33% | 210.16% | -137.84 pp | No | -12.06% | 182 | 61.54% |

Momentum is split into two rows because the script tested both single-symbol absolute momentum and GEM-style cross-ETF rotation. The GEM-style rotation found benchmark-beating versions, but those are not same-symbol comparisons because the benchmark is SPY or QQQ while the strategy can rotate into TQQQ.

## Best Beating Variants

| Rank | Family | Variant | Symbol | Benchmark | Strategy return | Asset return | Excess | Max DD | Positions |
|---:|---|---|---|---|---:|---:|---:|---:|---:|
| 1 | Moving-average trend | SMA3/SMA252 cross, no stop | TQQQ | TQQQ | 1,576.97% | 1,159.15% | 417.83 pp | -48.14% | 7 |
| 2 | Moving-average trend | SMA3/SMA252 state, no stop | TQQQ | TQQQ | 1,576.97% | 1,159.15% | 417.83 pp | -48.14% | 7 |
| 3 | GEM-style rotation | SPY/QQQ/TQQQ, 9-month lookback, defensive BIL | SPY/QQQ/TQQQ/BIL | SPY | 431.06% | 210.16% | 220.89 pp | -69.92% | 22 |
| 4 | GEM-style rotation | SPY/QQQ/TQQQ, 12-month lookback, defensive BIL | SPY/QQQ/TQQQ/BIL | SPY | 419.07% | 210.16% | 208.91 pp | -69.92% | 17 |
| 5 | GEM-style rotation | QQQ/TQQQ, 3-month lookback, defensive BIL | QQQ/TQQQ/BIL | QQQ | 555.38% | 367.00% | 188.38 pp | -42.02% | 38 |
| 6 | GEM-style rotation | QQQ/TQQQ, 3-month lookback, defensive AGG | QQQ/TQQQ/AGG | QQQ | 529.96% | 367.00% | 162.97 pp | -42.02% | 38 |

## What Did Not Beat

The intraday VWAP and ORB families improved from the first local proxy run, but neither beat QQQ buy-and-hold over the available 5-minute window. The best VWAP proxy returned 7.68% versus QQQ at 16.77%, and the best ORB proxy returned 8.39% versus QQQ at 16.77%. That does not invalidate the original 1-minute VWAP or stocks-in-play ORB research; it means the locally available 5-minute/60-minute ETF data did not reproduce those edges.

RSI(2) also did not beat asset return in this pass. The best variant had a strong win rate and lower drawdown, but the total return was much lower than SPY or QQQ buy-and-hold for the 2018-2026 bull-heavy period. Absolute momentum reduced drawdown versus SPY but still did not beat SPY's total return in the optimized single-symbol search.

## Output Files

- All variants: `C:\Users\skydiver1118\Documents\New project\backtest_results\strategy_variant_search_all.csv`
- Beating variants only: `C:\Users\skydiver1118\Documents\New project\backtest_results\strategy_variant_search_beating_asset.csv`
- Best by family: `C:\Users\skydiver1118\Documents\New project\backtest_results\strategy_variant_search_best_by_family.csv`
- JSON archive: `C:\Users\skydiver1118\Documents\New project\backtest_results\strategy_variant_search_all.json`
