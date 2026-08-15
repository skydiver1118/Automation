# RKT Technical Analysis Sample

Generated: 2026-06-28 17:42:30
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (60/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKT_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKT_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $15.00             |
| SMA20             | $13.64             |
| SMA50             | $14.25             |
| SMA200            | $17.11             |
| RSI14             | 57.7               |
| MACD / Signal     | 0.12 / -0.11       |
| ADX14 / +DI / -DI | 14.1 / 24.8 / 16.6 |
| ATR14             | $0.94 (6.24%)      |
| 63-day range      | $12.17 - $17.36    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 15.00 vs 13.64               |
| Trend        | Close above SMA50                         | 8      | 8   | 15.00 vs 14.25               |
| Trend        | Close above SMA200                        | 0      | 8   | 15.00 vs 17.11               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 13.64 vs 14.25               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 14.25 vs 17.11               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.36                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 57.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.12 vs -0.11                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.09               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 4.17%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.21x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 315122400 vs 133772595       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.69x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.1, +DI 24.8, -DI 16.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 15.21               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.24%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.59%                       |

## Support And Resistance

- Support levels: $12.20, $13.86, $14.98
- Resistance levels: $15.60, $17.36, $18.49, $20.30, $21.19

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $14.52 - $15.22 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $13.31 | $17.98   | $19.54   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $15.60 - $16.06 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $14.98 | $17.70   | $18.64   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
