# TSSI Technical Analysis Sample

Generated: 2026-06-08 21:13:41
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (67/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSSI_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSSI_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $13.33             |
| SMA20             | $12.78             |
| SMA50             | $13.70             |
| SMA200            | $12.63             |
| RSI14             | 49.1               |
| MACD / Signal     | 0.20 / 0.08        |
| ADX14 / +DI / -DI | 23.7 / 27.0 / 21.6 |
| ATR14             | $1.35 (10.11%)     |
| 63-day range      | $10.09 - $17.49    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 13.33 vs 12.78               |
| Trend        | Close above SMA50                         | 0      | 8   | 13.33 vs 13.70               |
| Trend        | Close above SMA200                        | 8      | 8   | 13.33 vs 12.63               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 12.78 vs 13.70               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 13.70 vs 12.63               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.63                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.20 vs 0.08                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.33              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 10.90%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.51x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 23529513 vs 21763586         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.06x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 23.7, +DI 27.0, -DI 21.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 16.13               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.11%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 23.79%                       |

## Support And Resistance

- Support levels: $7.23, $9.04, $10.22, $11.67
- Resistance levels: $14.36, $16.42, $17.46

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $12.11 - $13.12 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $11.44 | $15.31   | $16.66   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $14.36 - $15.03 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $12.78 | $18.51   | $20.42   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
