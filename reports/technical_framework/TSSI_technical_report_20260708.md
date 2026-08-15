# TSSI Technical Analysis Sample

Generated: 2026-07-08 16:40:37
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (20/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSSI_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSSI_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $11.37             |
| SMA20             | $12.20             |
| SMA50             | $13.00             |
| SMA200            | $12.38             |
| RSI14             | 43.3               |
| MACD / Signal     | -0.48 / -0.38      |
| ADX14 / +DI / -DI | 15.6 / 16.9 / 27.6 |
| ATR14             | $0.99 (8.72%)      |
| 63-day range      | $10.31 - $17.49    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 11.37 vs 12.20               |
| Trend        | Close above SMA50                         | 0      | 8   | 11.37 vs 13.00               |
| Trend        | Close above SMA200                        | 0      | 8   | 11.37 vs 12.38               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 12.20 vs 13.00               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 13.00 vs 12.38               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.70                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 43.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.48 vs -0.38               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.00               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -14.70%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.65x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 19482035 vs 21057197         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.83x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.6, +DI 16.9, -DI 27.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 13.66               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.72%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 34.99%                       |

## Support And Resistance

- Support levels: $7.70, $8.65, $10.43
- Resistance levels: $12.61, $14.07, $16.70, $17.45

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $13.00 - $13.49 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $11.51 | $15.97   | $17.96   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $9.93 - $10.68  | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $9.44  | $12.61   | $13.28   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $12.61 - $13.10 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $10.43 | $17.70   | $20.12   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
