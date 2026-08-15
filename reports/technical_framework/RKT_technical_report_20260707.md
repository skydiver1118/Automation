# RKT Technical Analysis Sample

Generated: 2026-07-07 16:40:23
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (56/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKT_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKT_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $14.63             |
| SMA20             | $14.22             |
| SMA50             | $14.19             |
| SMA200            | $16.94             |
| RSI14             | 51.2               |
| MACD / Signal     | 0.43 / 0.28        |
| ADX14 / +DI / -DI | 18.4 / 23.6 / 20.4 |
| ATR14             | $0.90 (6.15%)      |
| 63-day range      | $12.17 - $17.36    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 14.63 vs 14.22               |
| Trend        | Close above SMA50                         | 8      | 8   | 14.63 vs 14.19               |
| Trend        | Close above SMA200                        | 0      | 8   | 14.63 vs 16.94               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 14.22 vs 14.19               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 14.19 vs 16.94               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.34                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 51.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.43 vs 0.28                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.12              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 15.65%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.72x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 368995542 vs 221583752       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.63x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.4, +DI 23.6, -DI 20.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 16.47               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.15%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 15.73%                       |

## Support And Resistance

- Support levels: $12.17, $13.99
- Resistance levels: $14.64, $16.19, $17.36, $18.49, $20.30

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $14.14 - $14.81 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $13.29 | $16.85   | $18.04   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $14.64 - $15.09 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $14.59 | $16.66   | $17.56   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
