# SHLD Technical Analysis Sample

Generated: 2026-06-05 16:40:47
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (18/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SHLD_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SHLD_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $63.05             |
| SMA20             | $64.75             |
| SMA50             | $68.42             |
| SMA200            | $68.75             |
| RSI14             | 38.6               |
| MACD / Signal     | -1.07 / -1.13      |
| ADX14 / +DI / -DI | 29.3 / 19.8 / 36.6 |
| ATR14             | $1.38 (2.19%)      |
| 63-day range      | $62.21 - $78.45    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 63.05 vs 64.75               |
| Trend        | Close above SMA50                         | 0      | 8   | 63.05 vs 68.42               |
| Trend        | Close above SMA200                        | 0      | 8   | 63.05 vs 68.75               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 64.75 vs 68.42               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 68.42 vs 68.75               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.35                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 38.6                   |
| Momentum     | MACD above signal                         | 7      | 7   | -1.07 vs -1.13               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.58              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -4.34%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.89x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 31200652 vs 32557048         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.93x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 29.3, +DI 19.8, -DI 36.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 67.49               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.19%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 19.63%                       |

## Support And Resistance

- Support levels: $62.30
- Resistance levels: $65.06, $66.46, $67.90, $69.03, $75.05

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $68.42 - $69.11 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $66.35 | $72.57   | $75.33   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $61.60 - $62.64 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $60.91 | $65.06   | $66.27   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $65.06 - $65.76 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $62.30 | $71.64   | $74.75   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
