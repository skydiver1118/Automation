# TSSI Technical Analysis Sample

Generated: 2026-07-06 16:40:38
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (20/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSSI_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSSI_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $11.67             |
| SMA20             | $12.41             |
| SMA50             | $13.18             |
| SMA200            | $12.42             |
| RSI14             | 44.5               |
| MACD / Signal     | -0.43 / -0.33      |
| ADX14 / +DI / -DI | 14.2 / 18.9 / 27.7 |
| ATR14             | $1.03 (8.79%)      |
| 63-day range      | $10.31 - $17.49    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 11.67 vs 12.41               |
| Trend        | Close above SMA50                         | 0      | 8   | 11.67 vs 13.18               |
| Trend        | Close above SMA200                        | 0      | 8   | 11.67 vs 12.42               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 12.41 vs 13.18               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 13.18 vs 12.42               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.51                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 44.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.43 vs -0.33               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.07               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -19.46%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.61x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 19831488 vs 21783714         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.65x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.2, +DI 18.9, -DI 27.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 13.87               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.79%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 33.28%                       |

## Support And Resistance

- Support levels: $7.40, $8.65, $10.33, $11.25
- Resistance levels: $12.61, $14.12, $16.70, $17.45

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $13.18 - $13.69 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $11.64 | $16.26   | $18.31   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $10.74 - $11.51 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $10.23 | $13.18   | $14.20   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $12.61 - $13.12 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $11.25 | $16.08   | $17.69   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
