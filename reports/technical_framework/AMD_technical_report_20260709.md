# AMD Technical Analysis Sample

Generated: 2026-07-09 16:40:45
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (81/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AMD_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AMD_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $546.72            |
| SMA20             | $525.68            |
| SMA50             | $477.20            |
| SMA200            | $285.67            |
| RSI14             | 55.9               |
| MACD / Signal     | 17.71 / 22.26      |
| ADX14 / +DI / -DI | 22.4 / 31.9 / 20.5 |
| ATR14             | $37.46 (6.85%)     |
| 63-day range      | $230.91 - $584.73  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 546.72 vs 525.68             |
| Trend        | Close above SMA50                         | 8      | 8   | 546.72 vs 477.20             |
| Trend        | Close above SMA200                        | 8      | 8   | 546.72 vs 285.67             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 525.68 vs 477.20             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 477.20 vs 285.67             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 107.28                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 55.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | 17.71 vs 22.26               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -3.31              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 14.98%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.87x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1265523994 vs 1228027590     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.62x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 22.4, +DI 31.9, -DI 20.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 579.40              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.85%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 6.50%                        |

## Support And Resistance

- Support levels: $230.91, $393.36, $437.23, $485.66, $523.67
- Resistance levels: $548.75, $583.40

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $506.95 - $535.04 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $439.74 | $683.50  | $764.76  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $548.75 - $567.48 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $525.68 | $633.03  | $670.49  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
