# QLD Technical Analysis Sample

Generated: 2026-07-08 16:40:21
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (42/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QLD_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QLD_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $90.14             |
| SMA20             | $92.79             |
| SMA50             | $91.54             |
| SMA200            | $75.11             |
| RSI14             | 47.0               |
| MACD / Signal     | -0.07 / 0.59       |
| ADX14 / +DI / -DI | 18.5 / 19.1 / 31.6 |
| ATR14             | $4.11 (4.56%)      |
| 63-day range      | $66.25 - $101.12   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 90.14 vs 92.79               |
| Trend        | Close above SMA50                         | 0      | 8   | 90.14 vs 91.54               |
| Trend        | Close above SMA200                        | 8      | 8   | 90.14 vs 75.11               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 92.79 vs 91.54               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 91.54 vs 75.11               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 9.41                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 47.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.07 vs 0.59                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.22              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -2.22%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.89x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 218591037 vs 223916512       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.86x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.5, +DI 19.1, -DI 31.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 99.39               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.56%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.86%                       |

## Support And Resistance

- Support levels: $61.32, $65.13, $68.45, $71.08, $86.81
- Resistance levels: $94.42, $99.62

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $92.79 - $94.84 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $86.62 | $105.13  | $113.36  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $84.75 - $87.84 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $82.69 | $94.52   | $98.63   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $94.42 - $96.47 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $86.81 | $112.72  | $121.36  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
