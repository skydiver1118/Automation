# APLD Technical Analysis Sample

Generated: 2026-06-03 19:37:36
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (66/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APLD_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APLD_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $44.71             |
| SMA20             | $44.55             |
| SMA50             | $35.59             |
| SMA200            | $29.73             |
| RSI14             | 54.4               |
| MACD / Signal     | 3.20 / 3.42        |
| ADX14 / +DI / -DI | 28.3 / 23.6 / 20.2 |
| ATR14             | $3.96 (8.85%)      |
| 63-day range      | $20.00 - $50.72    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 44.71 vs 44.55               |
| Trend        | Close above SMA50                         | 8      | 8   | 44.71 vs 35.59               |
| Trend        | Close above SMA200                        | 8      | 8   | 44.71 vs 29.73               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 44.55 vs 35.59               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 35.59 vs 29.73               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 6.80                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 54.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | 3.20 vs 3.42                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.44              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 12.11%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.71x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1642386761 vs 1648121283     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.89x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 28.3, +DI 23.6, -DI 20.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 51.62               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.85%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.86%                       |

## Support And Resistance

- Support levels: $27.24, $31.41, $36.25, $38.83, $44.24
- Resistance levels: $47.79, $50.95

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $42.57 - $45.54 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $31.63 | $68.90   | $81.33   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $47.79 - $49.77 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $44.55 | $57.24   | $61.47   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
