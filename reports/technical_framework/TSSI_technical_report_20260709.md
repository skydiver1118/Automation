# TSSI Technical Analysis Sample

Generated: 2026-07-09 16:40:49
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (20/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSSI_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSSI_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $11.43             |
| SMA20             | $12.15             |
| SMA50             | $12.93             |
| SMA200            | $12.36             |
| RSI14             | 43.8               |
| MACD / Signal     | -0.48 / -0.40      |
| ADX14 / +DI / -DI | 15.9 / 18.1 / 26.7 |
| ATR14             | $0.95 (8.34%)      |
| 63-day range      | $10.31 - $17.49    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 11.43 vs 12.15               |
| Trend        | Close above SMA50                         | 0      | 8   | 11.43 vs 12.93               |
| Trend        | Close above SMA200                        | 0      | 8   | 11.43 vs 12.36               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 12.15 vs 12.93               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 12.93 vs 12.36               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.79                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 43.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.48 vs -0.40               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.02               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -8.05%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.43x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 20181813 vs 21318986         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.95x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.9, +DI 18.1, -DI 26.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 13.65               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.34%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 34.65%                       |

## Support And Resistance

- Support levels: $7.76, $8.65, $10.42
- Resistance levels: $12.61, $14.07, $16.70, $17.45

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $12.93 - $13.40 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $11.49 | $15.79   | $17.69   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $9.94 - $10.66  | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $9.47  | $12.61   | $13.16   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $12.61 - $13.08 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $10.42 | $17.69   | $20.11   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
