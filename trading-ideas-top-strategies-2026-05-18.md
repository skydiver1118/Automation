# Trading Ideas: Top Stock/ETF Trading Strategies

Research date: May 18, 2026  
Scope: stock and ETF strategies only. Crypto, futures, forex, and options-only evidence were excluded from ranking, even when they appeared inside mixed-platform search results.

## Method

I searched the open web, Reddit, TradingView ideas/scripts, X-indexed search results, and the requested Wenxuecity blog area. Public X search did not expose reliable comparable post counts, so X was treated as qualitative coverage only. For Reddit, I used the public search endpoint for the past year with `limit=100`; several strategy queries hit the 100-result cap, so the posting numbers below are capped proxies, not exact platform totals.

Reddit capped-frequency proxy: `VWAP stock trading strategy` = 100, `moving average crossover stock strategy` = 100, `RSI Bollinger Bands stock strategy` = 100, `momentum trading stock strategy` = 100, `MACD stock trading strategy` = 100, `breakout trading stocks` = 100, exact `opening range breakout stock strategy` = 28. Because many strategies tied at the cap, the final posting rank also considers TradingView coverage, recent publication activity, and whether the term is used as a complete strategy rather than just a confirming indicator. MACD was active but mostly appeared as confirmation inside RSI, VWAP, breakout, or moving-average systems, so it was excluded from the top five as a standalone strategy.

## Ranked Comparison Table

| Performance rank | Strategy family | Posting rank | Typical stock/ETF entry | Typical exit / risk method | Performance evidence found | Topic coverage and growth signal |
|---:|---|---:|---|---|---|---|
| 1 | Opening Range Breakout / volume-confirmed breakout | 5 | Define the first 5-15 minute opening range; enter long on a confirmed break above the range high or short below the range low, preferably with relative-volume / news filter. TradingView ORB scripts also use retest mode and volume > average filters. | Stop at opposite side/midpoint/ATR-based level; take profit by risk-reward multiple, close late-day positions, or exit at EOD. | Concretum/Barbon/Aziz U.S. equity ORB paper: 7,000+ U.S. stocks from 2016-2023; top-20 stocks-in-play 5-minute ORB reported over 1,600% net performance, Sharpe 2.81, annualized alpha 36%, versus 198% passive S&P 500 return. | Lower exact Reddit count than broad "breakout," but very strong recent research and TradingView script growth. Strongest performance evidence, but highly dependent on intraday execution and stock-in-play filtering. |
| 2 | VWAP trend / VWAP pullback / reclaim | 1 | Long when price is above rising VWAP, reclaims VWAP on volume, or pulls back to a rising VWAP after an impulse move; short when price fails VWAP under a falling VWAP. | Stop just beyond VWAP or structure with ATR buffer; first target prior high/low, measured move, or VWAP reversion; trail remaining shares. | Zarattini/Aziz SSRN VWAP study on QQQ/TQQQ, Jan. 2 2018-Sept. 28 2023: QQQ VWAP trend strategy grew $25,000 to $192,656 net of commissions, 671% return, 9.4% max drawdown, Sharpe 2.1; QQQ buy-and-hold returned 126%, max drawdown 37%, Sharpe 0.7. | Strongest posting score: capped Reddit count, active TradingView VWAP idea page, and fresh 2026 educational content. Appears to be one of the fastest-growing retail day-trading topics. |
| 3 | Relative-strength / momentum rotation | 2 | Rank stocks or ETFs by 6-12 month return, usually skipping the most recent month; buy strongest names or rotate into strongest ETF, optionally only when absolute momentum is positive. | Monthly/semiannual rebalance; exit when rank falls, when absolute momentum turns negative, or when a defensive ETF/risk-free proxy ranks better. | Evidence is mixed. Classic Jegadeesh/Titman momentum found significant historical excess returns, including 12.01% compounded annual excess for a 6-month winner-minus-loser strategy over 1965-1989. BestFolio's GEM ETF implementation shows 11.3% CAGR, 0.80 Sharpe, -33.7% max drawdown over 1990-2026. But newer U.S. large-cap / pure U.S. stock momentum studies show weak or negative recent results, including -2.07% net annualized return for S&P 500 12-1 momentum from 2005-2024 and 4.43% CAGR vs. 7.77% for SPY from 2000-2025. | Very broad coverage on Reddit and TradingView; fastest growth seems tied to AI/semiconductor momentum and ETF rotation posts. Needs filters because naive U.S. momentum is crowded and crash-prone. |
| 4 | Moving-average crossover / trend following | 3 | Buy or stay long when a fast MA crosses above a slow MA, price closes above a 200-day SMA, or a pullback resolves above a reference MA. | Exit when fast MA crosses below slow MA, price closes below the long MA, or stop/trailing stop is hit. | AlgorithmicFIRE SPYM 50/200 MA backtest as of May 18, 2026: full-history CAGR 11.63% vs. 11.21% buy-and-hold, Sharpe 0.90 vs. 0.56, max drawdown -20.02% vs. -53.40%, with 11 total trades. | Evergreen and high-frequency discussion: capped Reddit count and TradingView search pages with hundreds of pages of "moving average strategy" results. Growth is steady rather than new. |
| 5 | RSI / Bollinger mean reversion | 4 | Buy pullbacks when RSI is deeply oversold or price is at/below a lower Bollinger Band, usually only if the larger trend filter is positive; some variants require RSI to cross back above a centerline. | Exit on mean reversion to a short moving average/middle band, overbought RSI, trailing stop, or stop-loss. | `data not available` for comparable net return. StockCharts describes Connors' RSI(2) entry/exit framework and cautions that it is a starting point, not a complete standalone system. A 2025 SSRN S&P 500 equities paper reports significant gross risk-adjusted mean-reversion results using Bollinger + OU filters, but the accessible abstract does not provide exact return metrics and says results are gross of transaction costs. | High posting frequency and active TradingView scripts, but evidence quality is weaker. Retail growth is strong because the rules are simple; robustness depends heavily on trend/regime filters and costs. |

## Posting Rank

1. VWAP trend / pullback / reclaim: strongest combined evidence from capped Reddit frequency, TradingView VWAP idea activity, and fresh 2026 content.
2. Momentum / relative strength: capped Reddit frequency plus broad academic, ETF-rotation, and day-trading discussion.
3. Moving-average crossover / trend following: capped Reddit frequency and very large TradingView search footprint; mature rather than newly accelerating.
4. RSI / Bollinger mean reversion: capped Reddit frequency and many scripts, but often discussed as an indicator combo rather than a fully specified system.
5. Breakout / ORB: broad "breakout trading stocks" hit the Reddit cap, but exact ORB stock queries were lower; still included because the U.S. stock performance evidence is unusually strong.

## Fastest-Growing Topics

VWAP momentum and ORB/breakout look like the fastest-growing active-trading topics. VWAP has recent 2026 strategy playbooks, active Reddit and TradingView discussion, and one of the better public ETF backtests. ORB has lower exact posting count but unusually strong recent institutional-style research and many new/updated TradingView scripts that combine opening range, volume, VWAP, EMA, and FVG filters.

Momentum / relative strength is growing in two different ways: discretionary traders talk about small-cap or catalyst momentum, while systematic traders talk about ETF rotation and AI/semiconductor leadership. The caveat is important: older academic momentum evidence is strong, but recent naive U.S. stock momentum has underperformed in several public tests, so the growing versions increasingly add filters such as volatility, sector leadership, trend, or defensive ETF rotation.

Moving-average and RSI/Bollinger systems remain the "evergreen" retail strategies: they are mentioned constantly, easy to code, and widely supported by TradingView/StockCharts. They do not look like the fastest-growing ideas; they look like default building blocks. Wenxuecity's requested blog area showed heavy recent interest in QQQ/TQQQ, DCA, pyramiding, cash management, and 10% stop/trailing rules, which supports the same broader theme: retail traders are shifting from pure buy-and-hold toward rule-based position sizing, trend participation, and risk control.

## Notes on Evidence Quality

Performance comparisons are not apples-to-apples. ORB and VWAP are intraday systems with high execution sensitivity; momentum and moving averages are swing/position systems; RSI/Bollinger can be intraday or daily. Where a source gave no exact return, I used `data not available` rather than estimating. All figures are historical or backtested and are not predictions.

## Source Links

- [Concretum Research PDF: A Profitable Day Trading Strategy for the U.S. Equity Market](https://concretumgroup.com/wp-content/uploads/2026/02/A-Profitable-Day-Trading-Strategy-For-The-U.S.-Equity-Market.pdf)
- [SSRN: Volume Weighted Average Price (VWAP) The Holy Grail for Day Trading Systems](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4631351)
- [TradingView: Volume Weighted Average Price (VWAP) ideas](https://www.tradingview.com/ideas/vwap/)
- [TradingView: NeuraEdge ORB Opening Range Breakout Indicator](https://www.tradingview.com/script/Sb0YgLYU-NeuraEdge-ORB-Opening-Range-Breakout-Indicator/)
- [TradingView: Bollinger Bands + RSI Strategy](https://www.tradingview.com/script/GgCbRaj6-KL-Bollinger-bands-RSI-Strategy/)
- [BestFolio: GEM Global Equities Momentum](https://bestfolio.app/strategies/gem)
- [SSRN: Is Large-Cap Momentum Dead? Evidence from the S&P 500](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5367656)
- [Trading Studio: 12-Month Momentum on U.S. Stocks](https://blog.tradingstudio.finance/momentum-12m-us-stocks-backtest/)
- [AlgorithmicFIRE: SPYM 50/200 Moving Average Trend Backtest](https://algorithmicfire.com/report/SPYM_METHOD_MA_investing.html)
- [StockCharts ChartSchool: RSI(2)](https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/rsi-2)
- [SSRN: Bollinger Bands and OU Mean Reversion in S&P 500 Equities](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5713082)
- [SnapPChart: VWAP Momentum Trading Strategy](https://www.snappchart.app/blog/strategy-playbooks/vwap-momentum-trading-strategy)
- [Reddit: Momentum trading discussion](https://www.reddit.com/r/Daytrading/comments/1tflz13/the_only_strategy_that_works_for_me_momentum/)
- [Reddit: Moving averages discussion](https://www.reddit.com/r/Daytrading/comments/1sz7q2a/one_of_the_best_things_i_ever_did_for_my_trading/)
- [Reddit: Breakout fakeout backtest discussion](https://www.reddit.com/r/swingtrading/comments/1rfn3rf/youre_not_imagining_it_most_breakouts_are/)
- [Wenxuecity BrightLine all posts](https://blog.wenxuecity.com/myblog/82458/all.html)
- [Wenxuecity: simple trading rules vs DCA](https://blog.wenxuecity.com/myblog/82458/202512/10930.html)
- [Wenxuecity: QQQ vs DCA / staged buying](https://blog.wenxuecity.com/myblog/82458/202505/12493.html)
- [Wenxuecity: position management](https://blog.wenxuecity.com/myblog/82458/202508/458.html)
