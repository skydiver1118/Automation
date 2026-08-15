# RKT Technical Analysis Sample

Generated: 2026-06-10 20:55:14
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (11/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKT_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKT_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $12.54             |
| SMA20             | $13.54             |
| SMA50             | $14.47             |
| SMA200            | $17.38             |
| RSI14             | 39.9               |
| MACD / Signal     | -0.48 / -0.38      |
| ADX14 / +DI / -DI | 16.4 / 18.4 / 29.0 |
| ATR14             | $0.74 (5.89%)      |
| 63-day range      | $12.17 - $17.36    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 12.54 vs 13.54               |
| Trend        | Close above SMA50                         | 0      | 8   | 12.54 vs 14.47               |
| Trend        | Close above SMA200                        | 0      | 8   | 12.54 vs 17.38               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 13.54 vs 14.47               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 14.47 vs 17.38               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.48                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 39.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.48 vs -0.38               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.11              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -15.27%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.51x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 59705482 vs 81812729         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.88x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 16.4, +DI 18.4, -DI 29.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 14.90               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.89%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 27.76%                       |

## Support And Resistance

- Support levels: $12.23
- Resistance levels: $14.79, $15.85, $17.36, $18.49, $20.13

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $14.47 - $14.84 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $13.36 | $16.69   | $18.16   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $11.86 - $12.41 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $11.49 | $14.79   | $14.35   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $14.79 - $15.15 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $12.23 | $20.46   | $23.21   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
