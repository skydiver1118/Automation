# Top Five Stock/ETF Strategy Rerun - Source-Aligned Backtests

Run date: May 19, 2026  
Universe: stocks and ETFs only. Crypto, futures, forex, and options-only strategies excluded.  
Local data: Yahoo Finance via `yfinance`; no commissions, slippage, borrow costs, financing costs, or tax effects.  
Asset return: buy-and-hold return of the tested symbol or benchmark over the same period as the strategy row.  
TrendSpider status: I reclaimed the TrendSpider workspace and reloaded the expanded `VWAP Trend QQQ Signals` custom indicator. The editor visibly showed the new signal names, but the follow-up Strategy Tester save/run state could not be verified in this compacted retry, so the ranking below uses the completed local rerun rather than labeling these as TrendSpider Strategy Tester outputs.

## Three-Paragraph Summary

The original VWAP strategy is a 1-minute QQQ/TQQQ intraday strategy and includes both long and short logic. That matters: the earlier TrendSpider comparison used a 2-hour QQQ long-only proxy, so it was useful for platform testing but not faithful to the source. For this retry I went back to the original strategy sources and matched the asset/timeframe as closely as public local data allowed: VWAP on QQQ/TQQQ intraday, ORB on QQQ/TQQQ as an ETF substitute for stocks-in-play, momentum and moving averages on daily ETFs, and Connors-style RSI(2) on daily index ETFs.

The best replicated performance came from daily trend/momentum on TQQQ, especially the absolute momentum rule of `close > SMA200` and `close > close 252 bars ago`, which returned 752.36% from January 2, 2018 through May 19, 2026. That result is not a free lunch: TQQQ buy-and-hold returned 1,159.15% over the same period, and the strategy still had a -50.01% max drawdown. The cleaner non-leveraged result was QQQ SMA50/SMA200 at 287.48% with a -28.56% drawdown and only four completed positions. VWAP could not be replicated at its original 1-minute 2018-2023 granularity with Yahoo data; the best available local substitute, TQQQ 5-minute long-only VWAP over February 24, 2026 to May 19, 2026, returned only 1.11%.

By posting and topic coverage, VWAP still appears to be the fastest-growing retail trading topic, followed by momentum/relative strength and ORB/breakout. By replicated performance in this retry, the order changed to momentum, moving-average trend following, RSI(2), ORB, then VWAP. The gap is mostly a data-fit problem: VWAP and ORB are highly intraday and execution-sensitive, while the local rerun had much better daily-history coverage than 1-minute intraday history. The practical read is that VWAP remains the strategy to rerun inside TrendSpider at its original 1-minute QQQ/TQQQ settings, while daily ETF momentum and trend following are the strongest source-aligned local results.

## Source-Aligned Setup

| Strategy family | Original/source asset and timeframe | Long/short? | Local rerun used here | Local tested period | Asset return in tested period | Why this is the most appropriate available proxy |
|---|---|---:|---|---|---:|---|
| VWAP trend / VWAP pullback / reclaim | QQQ/TQQQ, 1-minute, January 2, 2018 to September 28, 2023 | Both long and short | Best available local proxy: TQQQ 5-minute long-only VWAP | 2026-02-24 to 2026-05-19 | 51.68% | Original is intraday QQQ/TQQQ. Yahoo intraday history did not support 2018-2023 1-minute, so the closest local repeat was QQQ/TQQQ intraday at available intervals. |
| Opening range breakout / ORB | U.S. stocks-in-play, 5-minute opening range, 2016-2023 | Both long and short in practical implementations | Best available local proxy: TQQQ 60-minute long+short ORB | 2023-06-22 to 2026-05-19 | 268.76% | The paper depends on selecting active stocks; QQQ/TQQQ are ETF substitutes only, not a true stocks-in-play universe. |
| Relative strength / momentum rotation | ETF rotation such as GEM using SPY/VEU/AGG/BIL with daily signals and monthly rebalance; also absolute trend filters | Long / defensive rotation | Best local return: TQQQ daily absolute momentum; source-aligned GEM also tested | 2018-01-02 to 2026-05-19 | 1,159.15% | Daily ETF data covers the full 2018-2026 requested window cleanly. GEM benchmark SPY returned 210.16%. |
| Moving-average crossover / trend following | SPYM/SPY daily 50-day/200-day moving average trend following | Long / cash | Best local return: TQQQ daily SMA50/SMA200; QQQ/SPY/SPYM also tested | 2018-01-02 to 2026-05-19 | 1,159.15% | This directly matches the daily trend-following source style. Non-leveraged QQQ returned 367.00%. |
| RSI(2) / mean reversion | Connors-style RSI(2) pullback while above 200-day SMA; exit above a short SMA, often 5-day | Long / cash | Best local return: TQQQ daily RSI(2); QQQ/SPY/SPYM also tested | 2018-01-02 to 2026-05-19 | 1,159.15% | This is the standard StockCharts/Connors ETF-compatible framework. Non-leveraged QQQ returned 367.00%. |

## Performance Ranking From Local Rerun

| Perf rank | Strategy family | Posting rank | Best local variant | Entry method | Exit method | Test window | Net perf | Asset perf | Max DD | Positions | Win rate | Notes |
|---:|---|---:|---|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | Relative strength / absolute momentum | 2 | TQQQ daily absolute momentum | Close above SMA200 and above close 252 bars ago | Exit when close falls below SMA200 or below close 252 bars ago | 2018-01-02 to 2026-05-19 | 752.36% | 1,159.15% | -50.01% | 23 | 43.48% | Highest local return, but uses leveraged ETF exposure and still suffered a very large drawdown. Source-aligned GEM ETF rotation returned 133.59%. |
| 2 | Moving-average crossover / trend following | 3 | TQQQ daily SMA50/SMA200 | SMA50 crosses above SMA200 | SMA50 crosses below SMA200 | 2018-01-02 to 2026-05-19 | 321.76% | 1,159.15% | -69.92% | 5 | 60.00% | Leveraged ETF version ranks second by return but has the worst drawdown. QQQ daily SMA50/SMA200 returned 287.48% with -28.56% max drawdown. |
| 3 | RSI(2) / mean reversion | 4 | TQQQ daily Connors-style RSI(2) | Close above SMA200 and RSI(2) <= 5 | Exit when close rises above SMA5 or falls below SMA200 | 2018-01-02 to 2026-05-19 | 214.45% | 1,159.15% | -41.14% | 144 | 62.50% | Best mean-reversion return. Non-leveraged QQQ version returned 80.08% with -13.35% max drawdown. |
| 4 | Opening range breakout / ORB | 5 | TQQQ 60-minute long+short ORB proxy | Break above/below first session bar with volume filter | Opposite first-bar break, VWAP failure/reclaim, or day-end style exit proxy | 2023-06-22 to 2026-05-19 | 29.16% | 268.76% | -23.32% | 305 | 54.10% | ETF proxy cannot reproduce the original stocks-in-play selection. QQQ 60-minute long+short returned 18.34%. |
| 5 | VWAP trend / reclaim | 1 | TQQQ 5-minute long-only VWAP proxy | Price confirms above first-bar VWAP/trend proxy | VWAP/trend failure proxy | 2026-02-24 to 2026-05-19 | 1.11% | 51.68% | -7.24% | 36 | 27.78% | Original 1-minute long+short 2018-2023 QQQ/TQQQ test was not reproducible with available Yahoo intraday history. This row should be treated as an incomplete proxy, not a rejection of the paper. |

## Best Non-Leveraged ETF Variants

| Strategy family | Best non-leveraged ETF variant | Test window | Net perf | Asset return in tested period | Max DD | Positions | Win rate |
|---|---|---|---:|---:|---:|---:|---:|
| Moving-average crossover | QQQ daily SMA50/SMA200 | 2018-01-02 to 2026-05-19 | 287.48% | 367.00% | -28.56% | 4 | 100.00% |
| Relative strength / absolute momentum | QQQ daily close > SMA200 and > 252 bars ago | 2018-01-02 to 2026-05-19 | 238.51% | 367.00% | -21.88% | 17 | 47.06% |
| Momentum / relative strength | GEM ETF rotation: SPY/VEU/AGG/BIL | 2018-01-02 to 2026-05-19 | 133.59% | 210.16% | -33.72% | 17 | 64.71% |
| RSI(2) / mean reversion | QQQ daily RSI(2) <= 5 above SMA200, exit above SMA5 | 2018-01-02 to 2026-05-19 | 80.08% | 367.00% | -13.35% | 157 | 63.06% |
| ORB proxy | QQQ 60-minute long+short ORB | 2023-06-22 to 2026-05-19 | 18.34% | 92.54% | -7.87% | 305 | 56.07% |
| VWAP proxy | QQQ 5-minute long-only VWAP | 2026-02-24 to 2026-05-19 | -1.79% | 16.77% | -2.91% | 36 | 22.22% |

## Posting And Coverage Ranking

| Posting rank | Strategy | Best tested proxy period | Asset return in tested period | Coverage / growth read |
|---:|---|---|---:|---|
| 1 | VWAP trend / pullback / reclaim | TQQQ 5-minute, 2026-02-24 to 2026-05-19 | 51.68% | Strongest combined posting signal from capped Reddit frequency, TradingView VWAP activity, and fresh educational content. Also directly tied to the QQQ/TQQQ intraday source paper. |
| 2 | Momentum / relative strength | TQQQ daily, 2018-01-02 to 2026-05-19 | 1,159.15% | Very broad Reddit, TradingView, academic, ETF-rotation, and sector-leadership discussion. Growth is strongest around ETF rotation and high-beta leadership themes. |
| 3 | Moving-average crossover / trend following | TQQQ daily, 2018-01-02 to 2026-05-19 | 1,159.15% | Evergreen and heavily covered; not the newest topic, but it remains one of the most repeated rule-based stock/ETF systems. |
| 4 | RSI / Bollinger / RSI(2) mean reversion | TQQQ daily, 2018-01-02 to 2026-05-19 | 1,159.15% | High retail coverage and many scripts, but often discussed as an indicator condition rather than a complete strategy. |
| 5 | Opening range breakout / ORB | TQQQ 60-minute, 2023-06-22 to 2026-05-19 | 268.76% | Exact ORB posting frequency was lower than broad breakout/VWAP, but recent ORB research and TradingView scripts make it one of the faster-growing intraday topics. |

## TrendSpider Proxy Results Already Captured

The prior TrendSpider Strategy Tester run used QQQ, 2-hour candles, long-only entries, and TrendSpider's accepted visible range of April 9, 2014 to May 19, 2026. Those results should be read as platform proxies, not source-faithful reruns:

| TrendSpider proxy rank | Strategy proxy | Test period | Net perf | QQQ asset return in tested period | Max DD | Positions | Win rate |
|---:|---|---|---:|---:|---:|---:|---:|
| 1 | Moving-average crossover / trend following | 2014-04-09 to 2026-05-19 | 281.1% | 708.1% | 19.2% | 29 | 59% |
| 2 | VWAP trend / reclaim proxy | 2014-04-09 to 2026-05-19 | 275.8% | 708.1% | 13.3% | 1,741 | 45% |
| 3 | Relative-strength / momentum proxy | 2014-04-09 to 2026-05-19 | 269.5% | 708.1% | 19.3% | 346 | 38% |
| 4 | RSI / Bollinger mean reversion proxy | 2014-04-09 to 2026-05-19 | 79.5% | 708.1% | 19.0% | 230 | 68% |
| 5 | Opening range breakout / volume breakout proxy | 2014-04-09 to 2026-05-19 | 20.0% | 708.1% | 15.2% | 240 | 59% |

## What Changed In This Retry

- Corrected the VWAP interpretation: the original strategy is 1-minute and both long/short, not 2-hour and long-only.
- Re-tested all five families using source-appropriate instruments and timeframes where local data allowed.
- Tested multiple timeframes for intraday strategies: 5-minute and 60-minute for QQQ/TQQQ VWAP and ORB proxies.
- Tested daily variants for slower systems: SPY, SPYM, QQQ, and TQQQ for SMA crossover, absolute momentum, and RSI(2).
- Kept `data not available` behavior for source-faithful VWAP 1-minute 2018-2023 replication inside local data, rather than guessing.

## Source Links

- [SSRN: Volume Weighted Average Price (VWAP): The Holy Grail for Day Trading Systems](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4631351)
- [Concretum Research PDF: A Profitable Day Trading Strategy for the U.S. Equity Market](https://concretumgroup.com/wp-content/uploads/2026/02/A-Profitable-Day-Trading-Strategy-For-The-U.S.-Equity-Market.pdf)
- [AlgorithmicFIRE: SPYM 50/200 Moving Average Trend Backtest](https://algorithmicfire.com/report/SPYM_METHOD_MA_investing.html)
- [StockCharts ChartSchool: RSI(2)](https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/rsi-2)
- [BestFolio: GEM Global Equities Momentum](https://bestfolio.app/strategies/gem)
- [TradingView: VWAP ideas](https://www.tradingview.com/ideas/vwap/)
- [Wenxuecity BrightLine all posts](https://blog.wenxuecity.com/myblog/82458/all.html)

## Output Files

- Local rerun script: `C:\Users\skydiver1118\Documents\New project\scripts\source_aligned_backtests.py`
- Full CSV results: `C:\Users\skydiver1118\Documents\New project\backtest_results\source_aligned_backtests.csv`
- Full JSON results: `C:\Users\skydiver1118\Documents\New project\backtest_results\source_aligned_backtests.json`
- Earlier TrendSpider proxy report: `C:\Users\skydiver1118\Documents\New project\reports\top5_strategy_trendspider_comparison.md`
