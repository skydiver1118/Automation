# TSSI Technical Analysis Sample

Generated: 2026-06-28 17:42:44
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (26/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSSI_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSSI_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $11.32             |
| SMA20             | $13.25             |
| SMA50             | $13.51             |
| SMA200            | $12.51             |
| RSI14             | 40.8               |
| MACD / Signal     | -0.35 / -0.18      |
| ADX14 / +DI / -DI | 14.0 / 19.0 / 30.0 |
| ATR14             | $1.13 (9.98%)      |
| 63-day range      | $10.31 - $17.49    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 11.32 vs 13.25               |
| Trend        | Close above SMA50                         | 0      | 8   | 11.32 vs 13.51               |
| Trend        | Close above SMA200                        | 0      | 8   | 11.32 vs 12.51               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 13.25 vs 13.51               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 13.51 vs 12.51               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.17                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 40.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.35 vs -0.18               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.16              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -16.40%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.59x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 19323300 vs 23603985         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.36x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.0, +DI 19.0, -DI 30.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 15.94               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.98%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 35.28%                       |

## Support And Resistance

- Support levels: $7.34, $8.65, $10.35
- Resistance levels: $12.71, $14.17, $15.94, $16.70, $17.46

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $13.51 - $14.08 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $11.82 | $16.90   | $19.16   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $9.79 - $10.64  | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $9.22  | $12.71   | $13.60   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $12.71 - $13.27 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $10.35 | $18.27   | $20.91   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
