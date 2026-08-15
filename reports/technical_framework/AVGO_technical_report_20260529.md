# AVGO Technical Analysis Sample

Generated: 2026-05-31 20:25:40
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (88/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AVGO_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AVGO_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $446.77            |
| SMA20             | $422.91            |
| SMA50             | $385.67            |
| SMA200            | $351.39            |
| RSI14             | 65.9               |
| MACD / Signal     | 9.96 / 10.86       |
| ADX14 / +DI / -DI | 23.2 / 32.0 / 15.3 |
| ATR14             | $15.77 (3.53%)     |
| 63-day range      | $289.96 - $448.90  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 446.77 vs 422.91             |
| Trend        | Close above SMA50                         | 8      | 8   | 446.77 vs 385.67             |
| Trend        | Close above SMA200                        | 8      | 8   | 446.77 vs 351.39             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 422.91 vs 385.67             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 385.67 vs 351.39             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 38.24                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 65.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | 9.96 vs 10.86                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.18               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 7.03%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 2.13x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1165857000 vs 1160801445     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.74x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 23.2, +DI 32.0, -DI 15.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 440.68              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.53%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.47%                        |

## Support And Resistance

- Support levels: $329.81, $369.17, $390.16, $405.52, $420.69
- Resistance levels: $448.90

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $415.02 - $426.85 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $369.90 | $523.00  | $574.04  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $448.90 - $456.79 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $422.91 | $512.72  | $542.66  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
