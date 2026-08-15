# MSFT Technical Analysis Sample

Generated: 2026-07-08 16:40:32
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (44/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MSFT_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MSFT_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $383.34            |
| SMA20             | $382.08            |
| SMA50             | $404.98            |
| SMA200            | $441.99            |
| RSI14             | 46.6               |
| MACD / Signal     | -6.74 / -9.18      |
| ADX14 / +DI / -DI | 18.5 / 26.6 / 30.6 |
| ATR14             | $12.15 (3.17%)     |
| 63-day range      | $349.20 - $466.32  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 383.34 vs 382.08             |
| Trend        | Close above SMA50                         | 0      | 8   | 383.34 vs 404.98             |
| Trend        | Close above SMA200                        | 0      | 8   | 383.34 vs 441.99             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 382.08 vs 404.98             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 404.98 vs 441.99             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -3.62                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.6                   |
| Momentum     | MACD above signal                         | 7      | 7   | -6.74 vs -9.18               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 4.54               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -6.90%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.51x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | -52983264 vs -153698573      |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.24x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.5, +DI 26.6, -DI 30.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 408.06              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.17%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.79%                       |

## Support And Resistance

- Support levels: $352.50, $385.13
- Resistance levels: $384.17, $395.57, $409.70, $428.48, $466.32

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $404.98 - $411.06 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $386.75 | $441.44  | $465.75  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $376.00 - $385.12 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $369.93 | $404.86  | $417.02  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $384.17 - $390.24 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $382.08 | $411.51  | $423.66  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
