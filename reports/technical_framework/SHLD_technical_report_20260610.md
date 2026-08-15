# SHLD Technical Analysis Sample

Generated: 2026-06-10 20:55:15
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (16/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SHLD_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SHLD_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $62.36             |
| SMA20             | $64.44             |
| SMA50             | $68.00             |
| SMA200            | $68.78             |
| RSI14             | 36.4               |
| MACD / Signal     | -1.23 / -1.16      |
| ADX14 / +DI / -DI | 30.4 / 15.8 / 34.0 |
| ATR14             | $1.39 (2.22%)      |
| 63-day range      | $61.80 - $77.19    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 62.36 vs 64.44               |
| Trend        | Close above SMA50                         | 0      | 8   | 62.36 vs 68.00               |
| Trend        | Close above SMA200                        | 0      | 8   | 62.36 vs 68.78               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 64.44 vs 68.00               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 68.00 vs 68.78               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.14                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 36.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | -1.23 vs -1.16               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.31              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -3.53%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.59x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 32911480 vs 33236754         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.38x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 30.4, +DI 15.8, -DI 34.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 67.51               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.22%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 19.22%                       |

## Support And Resistance

- Support levels: $61.95
- Resistance levels: $65.06, $66.46, $67.90, $69.03, $75.05

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $68.00 - $68.69 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $65.92 | $72.16   | $74.93   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $61.26 - $62.30 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $60.57 | $65.06   | $65.94   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $65.06 - $65.76 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $61.95 | $72.33   | $75.79   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
