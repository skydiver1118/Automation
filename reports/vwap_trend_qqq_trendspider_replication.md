# VWAP Trend QQQ TrendSpider Replication Attempt

## Objective

Replicate the VWAP trend / VWAP pullback / reclaim idea from the Zarattini/Aziz VWAP study inside TrendSpider Strategy Tester. The target article period was **January 2, 2018 through September 28, 2023**. The benchmark result from the source study was a QQQ VWAP trend strategy growing **$25,000 to $192,656**, or about **+671%**, with **9.4% max drawdown** and **Sharpe 2.1**.

Source: [SSRN: Volume Weighted Average Price (VWAP) The Holy Grail for Day Trading Systems](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4631351)

## TrendSpider Setup

| Item | Setting Used |
|---|---|
| Platform | TrendSpider Strategy Tester |
| Saved strategy name | `VWAP Trend QQQ 2h Proxy` |
| Symbol | `QQQ` |
| Custom indicator | `VWAP Trend QQQ Signals` |
| Entry rule | `VWAP Trend QQQ Signals, VWAP Long Entry` -> `Signal emerged` |
| Exit rule | `VWAP Trend QQQ Signals, VWAP Long Exit` -> `Signal emerged` |
| Logic | Long when the first regular-session candle closes above session VWAP; exit when price crosses below session VWAP or at session end |
| Intended timeframe | 1 minute |
| Actual runnable timeframe | 2 hours |
| Intended date range | Jan. 2, 2018 to Sept. 28, 2023 |
| Actual accepted TrendSpider date range | Aug. 19, 2011 to Sept. 28, 2023 |
| Trade cost | 0% |

The exact article setup could not be reproduced in the available TrendSpider account. Selecting the 1-minute timeframe triggered TrendSpider's upgrade modal for shorter timeframes. When the article date range was entered, the data selector snapped to a 10.0K-candle window ending on September 28, 2023, with a start date of August 19, 2011.

## Result

| Metric | TrendSpider 2h Proxy Result | Article / Study Target |
|---|---:|---:|
| Net performance | **+224.6%** | **+671%** |
| QQQ asset performance over tester window | +595.4% | +126% over Jan. 2, 2018-Sept. 28, 2023 |
| Positions | 1,744 | data not available |
| Win rate | 44% | data not available |
| Loss rate | 56% | data not available |
| Max drawdown | 13.3% | 9.4% |
| Beta vs asset | 0.2 | data not available |

## Readout

The TrendSpider proxy did not mimic the published return. The closest saved Strategy Tester run produced **+224.6%**, which is about **446 percentage points below** the paper's reported +671% QQQ VWAP strategy result. The result also lagged QQQ buy-and-hold over the accepted TrendSpider window, where the asset showed **+595.4%**.

The difference is explainable from the constraints. The published study used a 1-minute intraday VWAP method over January 2, 2018 to September 28, 2023, while the runnable TrendSpider setup was forced to 2-hour candles and a longer accepted window from August 19, 2011 to September 28, 2023. The saved Strategy Tester setup is therefore a coarse proxy, not a faithful replication.

To get closer to the paper, the next pass needs TrendSpider access to 1-minute historical data and an exact Jan. 2, 2018-Sept. 28, 2023 window. A fuller mimic should also test the short-side signals from the custom indicator or create a paired short strategy, because the saved proxy run was long-only.

Evidence screenshot: `C:\Users\skydiver1118\Documents\New project\trendspider_saved_results.png`
