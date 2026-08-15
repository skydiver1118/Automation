# APLD Technical Analysis Sample

Generated: 2026-06-04 19:39:44
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (48/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APLD_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APLD_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $44.15             |
| SMA20             | $44.55             |
| SMA50             | $35.94             |
| SMA200            | $29.86             |
| RSI14             | 53.4               |
| MACD / Signal     | 2.85 / 3.31        |
| ADX14 / +DI / -DI | 26.6 / 22.4 / 24.2 |
| ATR14             | $3.89 (8.80%)      |
| 63-day range      | $20.00 - $50.72    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 44.15 vs 44.55               |
| Trend        | Close above SMA50                         | 8      | 8   | 44.15 vs 35.94               |
| Trend        | Close above SMA200                        | 8      | 8   | 44.15 vs 29.86               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 44.55 vs 35.94               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 35.94 vs 29.86               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 6.88                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | 2.85 vs 3.31                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.81              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -0.20%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.68x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1624443518 vs 1643077151     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.93x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 26.6, +DI 22.4, -DI 24.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 51.61               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.80%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 12.96%                       |

## Support And Resistance

- Support levels: $27.24, $31.41, $36.37, $38.83, $43.33
- Resistance levels: $47.79, $50.95

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $41.64 - $44.56 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $32.05 | $65.20   | $76.25   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $47.79 - $49.73 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $43.59 | $59.11   | $64.29   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
