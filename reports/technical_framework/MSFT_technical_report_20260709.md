# MSFT Technical Analysis Sample

Generated: 2026-07-09 16:40:43
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (44/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MSFT_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MSFT_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $384.36            |
| SMA20             | $381.13            |
| SMA50             | $404.19            |
| SMA200            | $441.34            |
| RSI14             | 47.1               |
| MACD / Signal     | -6.11 / -8.56      |
| ADX14 / +DI / -DI | 18.2 / 24.8 / 33.3 |
| ATR14             | $12.09 (3.15%)     |
| 63-day range      | $349.20 - $466.32  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 384.36 vs 381.13             |
| Trend        | Close above SMA50                         | 0      | 8   | 384.36 vs 404.19             |
| Trend        | Close above SMA200                        | 0      | 8   | 384.36 vs 441.34             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 381.13 vs 404.19             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 404.19 vs 441.34             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -5.36                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 47.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | -6.11 vs -8.56               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.94               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -4.72%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.63x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | -41970149 vs -165553407      |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.41x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.2, +DI 24.8, -DI 33.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 405.14              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.15%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.58%                       |

## Support And Resistance

- Support levels: $352.76, $373.35, $382.92
- Resistance levels: $384.17, $395.57, $407.24, $428.48, $466.32

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $404.19 - $410.24 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $386.06 | $440.47  | $464.65  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $376.87 - $385.94 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $370.83 | $405.59  | $417.68  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $395.57 - $401.62 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $382.92 | $429.94  | $445.61  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
