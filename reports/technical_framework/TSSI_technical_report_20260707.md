# TSSI Technical Analysis Sample

Generated: 2026-07-07 16:40:37
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (20/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSSI_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSSI_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $11.18             |
| SMA20             | $12.30             |
| SMA50             | $13.09             |
| SMA200            | $12.40             |
| RSI14             | 41.9               |
| MACD / Signal     | -0.47 / -0.36      |
| ADX14 / +DI / -DI | 14.9 / 17.6 / 28.8 |
| ATR14             | $1.03 (9.18%)      |
| 63-day range      | $10.31 - $17.49    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 11.18 vs 12.30               |
| Trend        | Close above SMA50                         | 0      | 8   | 11.18 vs 13.09               |
| Trend        | Close above SMA200                        | 0      | 8   | 11.18 vs 12.40               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 12.30 vs 13.09               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 13.09 vs 12.40               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.60                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 41.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.47 vs -0.36               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.03               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -16.44%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.60x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 19293029 vs 21569856         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.67x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.9, +DI 17.6, -DI 28.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 13.79               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.18%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 36.08%                       |

## Support And Resistance

- Support levels: $7.62, $8.65, $10.44
- Resistance levels: $12.61, $14.09, $16.70, $17.45

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $13.09 - $13.60 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $11.55 | $16.17   | $18.22   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $9.92 - $10.69  | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $9.41  | $12.61   | $13.39   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $12.61 - $13.12 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $10.44 | $17.71   | $20.14   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
