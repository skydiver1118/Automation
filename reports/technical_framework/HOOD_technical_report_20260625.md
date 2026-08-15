# HOOD Technical Analysis Sample

Generated: 2026-06-26 06:53:14
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (69/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [HOOD_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/HOOD_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $93.47             |
| SMA20             | $93.00             |
| SMA50             | $84.99             |
| SMA200            | $102.68            |
| RSI14             | 52.4               |
| MACD / Signal     | 5.26 / 5.05        |
| ADX14 / +DI / -DI | 25.7 / 25.4 / 21.5 |
| ATR14             | $6.66 (7.12%)      |
| 63-day range      | $63.51 - $112.50   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 93.47 vs 93.00               |
| Trend        | Close above SMA50                         | 8      | 8   | 93.47 vs 84.99               |
| Trend        | Close above SMA200                        | 0      | 8   | 93.47 vs 102.68              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 93.00 vs 84.99               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 84.99 vs 102.68              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 8.75                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 52.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 5.26 vs 5.05                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.60              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 22.62%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.63x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1452737300 vs 1442456405     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.19x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 25.7, +DI 25.4, -DI 21.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 109.09              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.12%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 16.92%                       |

## Support And Resistance

- Support levels: $63.51, $71.30, $77.93, $84.99, $92.95
- Resistance levels: $93.86, $111.61, $122.13

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $89.73 - $94.72 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $78.34 | $119.99  | $133.88  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $93.86 - $97.19 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $93.05 | $108.84  | $115.50  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
