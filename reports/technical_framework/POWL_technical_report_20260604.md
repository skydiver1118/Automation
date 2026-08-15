# POWL Technical Analysis Sample

Generated: 2026-06-04 19:39:38
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (71/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [POWL_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/POWL_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $300.06            |
| SMA20             | $291.63            |
| SMA50             | $255.34            |
| SMA200            | $159.02            |
| RSI14             | 60.7               |
| MACD / Signal     | 9.95 / 11.03       |
| ADX14 / +DI / -DI | 28.2 / 21.9 / 13.4 |
| ATR14             | $18.31 (6.10%)     |
| 63-day range      | $157.45 - $327.89  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 300.06 vs 291.63             |
| Trend        | Close above SMA50                         | 8      | 8   | 300.06 vs 255.34             |
| Trend        | Close above SMA200                        | 8      | 8   | 300.06 vs 159.02             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 291.63 vs 255.34             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 255.34 vs 159.02             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 47.29                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 60.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | 9.95 vs 11.03                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.26               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -6.29%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.68x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 33304750 vs 32737998         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.77x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 28.2, +DI 21.9, -DI 13.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 322.87              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.10%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 8.49%                        |

## Support And Resistance

- Support levels: $174.85, $223.92, $255.32, $271.00, $288.45
- Resistance levels: $301.97, $326.63

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $282.48 - $296.21 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $237.03 | $393.96  | $446.27  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $301.97 - $311.12 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $291.63 | $343.16  | $361.47  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
