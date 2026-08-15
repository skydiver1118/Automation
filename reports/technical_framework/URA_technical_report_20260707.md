# URA Technical Analysis Sample

Generated: 2026-07-07 16:40:29
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (19/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [URA_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/URA_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $41.75             |
| SMA20             | $44.89             |
| SMA50             | $49.39             |
| SMA200            | $49.32             |
| RSI14             | 34.4               |
| MACD / Signal     | -1.76 / -1.65      |
| ADX14 / +DI / -DI | 21.4 / 13.8 / 30.6 |
| ATR14             | $2.05 (4.91%)      |
| 63-day range      | $41.19 - $58.97    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 41.75 vs 44.89               |
| Trend        | Close above SMA50                         | 0      | 8   | 41.75 vs 49.39               |
| Trend        | Close above SMA200                        | 0      | 8   | 41.75 vs 49.32               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 44.89 vs 49.39               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 49.39 vs 49.32               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -2.64                        |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 34.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | -1.76 vs -1.65               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.02               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -7.86%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 1.00x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 134989142 vs 142437402       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.61x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 21.4, +DI 13.8, -DI 30.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 48.63               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.91%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 29.20%                       |

## Support And Resistance

- Support levels: $41.44
- Resistance levels: $44.95, $49.40, $50.83, $53.34, $55.06

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $49.39 - $50.41 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $46.31 | $55.54   | $59.65   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $40.42 - $41.95 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $39.39 | $45.29   | $47.34   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $44.95 - $45.98 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $41.44 | $53.51   | $57.53   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
