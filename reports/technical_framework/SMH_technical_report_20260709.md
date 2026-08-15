# SMH Technical Analysis Sample

Generated: 2026-07-09 16:40:36
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (60/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SMH_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SMH_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $607.73            |
| SMA20             | $619.64            |
| SMA50             | $587.81            |
| SMA200            | $431.47            |
| RSI14             | 50.4               |
| MACD / Signal     | 3.77 / 11.02       |
| ADX14 / +DI / -DI | 16.5 / 24.9 / 32.4 |
| ATR14             | $29.97 (4.93%)     |
| 63-day range      | $422.63 - $671.83  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 607.73 vs 619.64             |
| Trend        | Close above SMA50                         | 8      | 8   | 607.73 vs 587.81             |
| Trend        | Close above SMA200                        | 8      | 8   | 607.73 vs 431.47             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 619.64 vs 587.81             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 587.81 vs 431.47             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 72.18                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 50.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | 3.77 vs 11.02                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -3.91              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 2.83%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.74x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 259299001 vs 262821210       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.19x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 16.5, +DI 24.9, -DI 32.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 670.81              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.93%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 9.54%                        |

## Support And Resistance

- Support levels: $397.77, $422.63, $527.87, $563.32, $587.81
- Resistance levels: $651.26, $671.58

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $572.82 - $595.30 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $557.83 | $651.26  | $673.98  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $651.26 - $666.24 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $587.81 | $800.63  | $871.57  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
