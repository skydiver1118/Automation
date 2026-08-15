# APP Technical Analysis Sample

Generated: 2026-06-08 21:13:13
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (79/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APP_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APP_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $563.69            |
| SMA20             | $529.65            |
| SMA50             | $475.22            |
| SMA200            | $540.81            |
| RSI14             | 59.3               |
| MACD / Signal     | 29.71 / 28.96      |
| ADX14 / +DI / -DI | 29.6 / 26.1 / 13.2 |
| ATR14             | $33.67 (5.97%)     |
| 63-day range      | $364.64 - $622.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 563.69 vs 529.65             |
| Trend        | Close above SMA50                         | 8      | 8   | 563.69 vs 475.22             |
| Trend        | Close above SMA200                        | 8      | 8   | 563.69 vs 540.81             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 529.65 vs 475.22             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 475.22 vs 540.81             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 29.37                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 59.3                   |
| Momentum     | MACD above signal                         | 7      | 7   | 29.71 vs 28.96               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -13.03             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 20.31%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.81x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 410654942 vs 402344447       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.70x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 29.6, +DI 26.1, -DI 13.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 636.53              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.97%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 9.37%                        |

## Support And Resistance

- Support levels: $418.78, $452.00, $475.22, $509.04, $538.31
- Resistance levels: $569.92, $625.63, $679.69, $732.42

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $521.48 - $546.73 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $441.55 | $719.22  | $811.78  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $569.92 - $586.76 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $538.31 | $658.39  | $698.41  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
