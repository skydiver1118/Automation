# TSSI Technical Analysis Sample

Generated: 2026-06-05 16:41:05
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (62/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSSI_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSSI_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $13.38             |
| SMA20             | $12.72             |
| SMA50             | $13.69             |
| SMA200            | $12.64             |
| RSI14             | 49.3               |
| MACD / Signal     | 0.26 / 0.05        |
| ADX14 / +DI / -DI | 24.7 / 27.7 / 22.2 |
| ATR14             | $1.41 (10.56%)     |
| 63-day range      | $8.65 - $17.49     |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 13.38 vs 12.72               |
| Trend        | Close above SMA50                         | 0      | 8   | 13.38 vs 13.69               |
| Trend        | Close above SMA200                        | 8      | 8   | 13.38 vs 12.64               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 12.72 vs 13.69               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 13.69 vs 12.64               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.68                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.3                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.26 vs 0.05                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.15              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -15.53%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.52x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 24609897 vs 21752185         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.31x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 24.7, +DI 27.7, -DI 22.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 16.07               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.56%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 23.50%                       |

## Support And Resistance

- Support levels: $7.23, $8.89, $10.25, $11.67
- Resistance levels: $14.36, $16.39, $17.46

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $12.01 - $13.07 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $11.31 | $15.37   | $16.78   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $14.36 - $15.06 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $12.72 | $18.69   | $20.69   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
