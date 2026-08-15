# RKT Technical Analysis Sample

Generated: 2026-06-02 16:57:38
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (38/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKT_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKT_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $14.03             |
| SMA20             | $14.11             |
| SMA50             | $14.61             |
| SMA200            | $17.54             |
| RSI14             | 47.1               |
| MACD / Signal     | -0.20 / -0.29      |
| ADX14 / +DI / -DI | 12.0 / 23.7 / 24.6 |
| ATR14             | $0.72 (5.11%)      |
| 63-day range      | $12.38 - $17.36    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 14.03 vs 14.11               |
| Trend        | Close above SMA50                         | 0      | 8   | 14.03 vs 14.61               |
| Trend        | Close above SMA200                        | 0      | 8   | 14.03 vs 17.54               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 14.11 vs 14.61               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 14.61 vs 17.54               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.67                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 47.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.20 vs -0.29               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.10               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 0.14%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.79x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 111466930 vs 110381162       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.87x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 12.0, +DI 23.7, -DI 24.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 15.43               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.11%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 19.18%                       |

## Support And Resistance

- Support levels: $12.51, $13.43, $14.11
- Resistance levels: $14.68, $15.75, $17.36, $18.49, $20.13

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $14.61 - $14.97 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $13.53 | $16.76   | $18.19   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $13.08 - $13.61 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $12.72 | $14.78   | $15.49   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $14.68 - $15.04 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $13.43 | $17.71   | $19.14   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
