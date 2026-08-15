# APLD Technical Analysis Sample

Generated: 2026-06-08 21:13:40
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (48/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APLD_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APLD_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $40.94             |
| SMA20             | $44.44             |
| SMA50             | $36.47             |
| SMA200            | $30.11             |
| RSI14             | 48.0               |
| MACD / Signal     | 1.73 / 2.81        |
| ADX14 / +DI / -DI | 25.4 / 19.0 / 27.7 |
| ATR14             | $3.93 (9.61%)      |
| 63-day range      | $20.00 - $50.72    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 40.94 vs 44.44               |
| Trend        | Close above SMA50                         | 8      | 8   | 40.94 vs 36.47               |
| Trend        | Close above SMA200                        | 8      | 8   | 40.94 vs 30.11               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 44.44 vs 36.47               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 36.47 vs 30.11               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 6.91                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 48.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | 1.73 vs 2.81                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.25              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -0.74%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.74x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1622701635 vs 1645972287     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.87x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 25.4, +DI 19.0, -DI 27.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 51.75               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.61%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 19.28%                       |

## Support And Resistance

- Support levels: $20.64, $24.23, $29.24, $32.32, $37.16
- Resistance levels: $42.27, $47.79, $50.98

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $35.19 - $38.14 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $32.53 | $44.93   | $49.06   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $42.27 - $44.24 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $37.16 | $55.45   | $61.54   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
