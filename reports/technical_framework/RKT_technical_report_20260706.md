# RKT Technical Analysis Sample

Generated: 2026-07-06 16:40:24
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (57/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKT_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKT_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $15.55             |
| SMA20             | $14.12             |
| SMA50             | $14.20             |
| SMA200            | $16.97             |
| RSI14             | 59.5               |
| MACD / Signal     | 0.49 / 0.24        |
| ADX14 / +DI / -DI | 19.3 / 25.9 / 14.3 |
| ATR14             | $0.88 (5.67%)      |
| 63-day range      | $12.17 - $17.36    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 15.55 vs 14.12               |
| Trend        | Close above SMA50                         | 8      | 8   | 15.55 vs 14.20               |
| Trend        | Close above SMA200                        | 0      | 8   | 15.55 vs 16.97               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 14.12 vs 14.20               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 14.20 vs 16.97               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.36                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 59.5                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.49 vs 0.24                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.01               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 17.54%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.56x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 398338040 vs 207447112       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.75x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 19.3, +DI 25.9, -DI 14.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 16.47               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.67%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.43%                       |

## Support And Resistance

- Support levels: $12.12, $13.92, $14.78
- Resistance levels: $15.85, $16.41, $17.36, $18.49, $20.30

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $14.34 - $15.01 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $13.32 | $17.39   | $18.74   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $15.85 - $16.29 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $14.78 | $18.64   | $19.93   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
