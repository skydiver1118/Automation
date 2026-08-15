# SHLD Technical Analysis Sample

Generated: 2026-07-09 16:40:35
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (28/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SHLD_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SHLD_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $61.46             |
| SMA20             | $61.76             |
| SMA50             | $63.79             |
| SMA200            | $68.40             |
| RSI14             | 46.0               |
| MACD / Signal     | -0.50 / -0.94      |
| ADX14 / +DI / -DI | 23.5 / 28.5 / 34.1 |
| ATR14             | $1.49 (2.42%)      |
| 63-day range      | $57.70 - $74.69    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 61.46 vs 61.76               |
| Trend        | Close above SMA50                         | 0      | 8   | 61.46 vs 63.79               |
| Trend        | Close above SMA200                        | 0      | 8   | 61.46 vs 68.40               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 61.76 vs 63.79               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 63.79 vs 68.40               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.11                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.50 vs -0.94               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.49               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -2.30%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.44x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 27325236 vs 29482522         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.64x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 23.5, +DI 28.5, -DI 34.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 66.25               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.42%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.72%                       |

## Support And Resistance

- Support levels: $57.56, $61.75
- Resistance levels: $64.97, $66.25, $67.88, $68.81, $74.77

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $63.79 - $64.53 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $61.56 | $68.24   | $71.22   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $56.82 - $57.93 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $56.07 | $64.97   | $61.83   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $64.97 - $65.72 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $58.49 | $79.06   | $85.92   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
