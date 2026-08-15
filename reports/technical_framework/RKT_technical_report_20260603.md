# RKT Technical Analysis Sample

Generated: 2026-06-03 19:37:12
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (23/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKT_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKT_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $12.94             |
| SMA20             | $14.05             |
| SMA50             | $14.58             |
| SMA200            | $17.51             |
| RSI14             | 38.7               |
| MACD / Signal     | -0.27 / -0.28      |
| ADX14 / +DI / -DI | 12.6 / 21.1 / 31.5 |
| ATR14             | $0.75 (5.79%)      |
| 63-day range      | $12.38 - $17.36    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 12.94 vs 14.05               |
| Trend        | Close above SMA50                         | 0      | 8   | 12.94 vs 14.58               |
| Trend        | Close above SMA200                        | 0      | 8   | 12.94 vs 17.51               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 14.05 vs 14.58               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 14.58 vs 17.51               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.64                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 38.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.27 vs -0.28               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.03              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -8.16%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.44x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 72861524 vs 105152421        |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.67x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 12.6, +DI 21.1, -DI 31.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 15.47               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.79%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 25.46%                       |

## Support And Resistance

- Support levels: $12.56
- Resistance levels: $14.68, $15.76, $17.36, $18.49, $20.13

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $14.58 - $14.96 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $13.46 | $16.83   | $18.33   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $12.19 - $12.75 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $11.81 | $14.68   | $14.71   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $14.68 - $15.06 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $12.56 | $19.49   | $21.79   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
