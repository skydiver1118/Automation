# SHLD Technical Analysis Sample

Generated: 2026-06-03 19:37:14
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (24/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SHLD_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SHLD_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $63.31             |
| SMA20             | $65.07             |
| SMA50             | $68.79             |
| SMA200            | $68.73             |
| RSI14             | 37.8               |
| MACD / Signal     | -0.96 / -1.20      |
| ADX14 / +DI / -DI | 29.7 / 21.7 / 37.1 |
| ATR14             | $1.39 (2.19%)      |
| 63-day range      | $62.21 - $78.45    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 63.31 vs 65.07               |
| Trend        | Close above SMA50                         | 0      | 8   | 63.31 vs 68.79               |
| Trend        | Close above SMA200                        | 0      | 8   | 63.31 vs 68.73               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 65.07 vs 68.79               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 68.79 vs 68.73               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.28                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 37.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.96 vs -1.20               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.16              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -6.25%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.61x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 32145339 vs 33555212         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.73x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 29.7, +DI 21.7, -DI 37.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 68.05               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.19%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 19.30%                       |

## Support And Resistance

- Support levels: $60.81, $62.27, $63.27
- Resistance levels: $65.06, $66.46, $68.10, $69.03, $75.05

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $68.79 - $69.48 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $66.70 | $72.96   | $75.73   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $62.58 - $63.62 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $61.88 | $65.87   | $67.26   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $65.06 - $65.76 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $63.27 | $69.69   | $71.84   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
