# AAPL Technical Analysis Sample

Generated: 2026-06-10 20:55:00
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (45/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AAPL_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AAPL_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $291.58            |
| SMA20             | $304.40            |
| SMA50             | $283.81            |
| SMA200            | $265.80            |
| RSI14             | 43.8               |
| MACD / Signal     | 4.17 / 7.52        |
| ADX14 / +DI / -DI | 39.5 / 19.5 / 25.4 |
| ATR14             | $7.30 (2.50%)      |
| 63-day range      | $245.28 - $317.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 291.58 vs 304.40             |
| Trend        | Close above SMA50                         | 8      | 8   | 291.58 vs 283.81             |
| Trend        | Close above SMA200                        | 8      | 8   | 291.58 vs 265.80             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 304.40 vs 283.81             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 283.81 vs 265.80             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 20.06                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 43.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | 4.17 vs 7.52                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -3.10              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -1.09%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.97x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1897208215 vs 2000438531     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.92x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 39.5, +DI 19.5, -DI 25.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 318.46              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.50%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 8.13%                        |

## Support And Resistance

- Support levels: $244.96, $253.90, $265.64, $285.59, $290.34
- Resistance levels: $303.20, $317.66

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $286.69 - $292.16 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $276.51 | $315.25  | $328.17  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $303.20 - $306.85 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $290.34 | $334.40  | $349.09  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
