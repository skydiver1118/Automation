# QLD Technical Analysis Sample

Generated: 2026-07-09 16:40:30
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (71/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QLD_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QLD_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $93.14             |
| SMA20             | $92.94             |
| SMA50             | $91.80             |
| SMA200            | $75.24             |
| RSI14             | 51.2               |
| MACD / Signal     | 0.01 / 0.47        |
| ADX14 / +DI / -DI | 18.1 / 23.3 / 29.7 |
| ATR14             | $4.05 (4.35%)      |
| 63-day range      | $66.41 - $101.12   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 93.14 vs 92.94               |
| Trend        | Close above SMA50                         | 8      | 8   | 93.14 vs 91.80               |
| Trend        | Close above SMA200                        | 8      | 8   | 93.14 vs 75.24               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 92.94 vs 91.80               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 91.80 vs 75.24               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 9.02                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 51.2                   |
| Momentum     | MACD above signal                         | 0      | 7   | 0.01 vs 0.47                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.09              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 3.42%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.57x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 217117619 vs 219243446       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.08x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.1, +DI 23.3, -DI 29.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 99.41               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.35%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 7.89%                        |

## Support And Resistance

- Support levels: $65.16, $68.45, $71.08, $86.86, $92.44
- Resistance levels: $94.42, $99.62

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $90.91 - $93.96 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $87.75 | $101.81  | $106.50  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $94.42 - $96.44 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $92.94 | $103.54  | $107.59  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
