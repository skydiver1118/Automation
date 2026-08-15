# RKT Technical Analysis Sample

Generated: 2026-05-31 20:25:58
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (49/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKT_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKT_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $14.51             |
| SMA20             | $14.13             |
| SMA50             | $14.61             |
| SMA200            | $17.59             |
| RSI14             | 51.5               |
| MACD / Signal     | -0.23 / -0.34      |
| ADX14 / +DI / -DI | 13.7 / 25.8 / 22.9 |
| ATR14             | $0.76 (5.26%)      |
| 63-day range      | $12.38 - $17.65    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 14.51 vs 14.13               |
| Trend        | Close above SMA50                         | 0      | 8   | 14.51 vs 14.61               |
| Trend        | Close above SMA200                        | 0      | 8   | 14.51 vs 17.59               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 14.13 vs 14.61               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 14.61 vs 17.59               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.82                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 51.5                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.23 vs -0.34               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.20               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -0.75%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.30x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 153129700 vs 115069390       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.02x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 13.7, +DI 25.8, -DI 22.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 15.48               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.26%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.79%                       |

## Support And Resistance

- Support levels: $12.51, $13.43, $14.12
- Resistance levels: $14.68, $15.76, $17.51, $18.49, $20.13

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $13.86 - $14.43 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $13.48 | $15.67   | $16.44   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $14.68 - $15.06 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $14.24 | $16.40   | $17.16   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
