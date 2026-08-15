# SHLD Technical Analysis Sample

Generated: 2026-07-08 16:40:24
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (34/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SHLD_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SHLD_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $62.67             |
| SMA20             | $61.83             |
| SMA50             | $63.90             |
| SMA200            | $68.43             |
| RSI14             | 50.1               |
| MACD / Signal     | -0.49 / -1.05      |
| ADX14 / +DI / -DI | 24.6 / 30.7 / 31.5 |
| ATR14             | $1.48 (2.37%)      |
| 63-day range      | $57.70 - $75.03    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 62.67 vs 61.83               |
| Trend        | Close above SMA50                         | 0      | 8   | 62.67 vs 63.90               |
| Trend        | Close above SMA200                        | 0      | 8   | 62.67 vs 68.43               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 61.83 vs 63.90               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 63.90 vs 68.43               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.13                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 50.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.49 vs -1.05               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.82               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -0.31%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.72x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 28187632 vs 29973827         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.63x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 24.6, +DI 30.7, -DI 31.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 66.35               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.37%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 16.47%                       |

## Support And Resistance

- Support levels: $57.57, $61.98
- Resistance levels: $64.97, $66.35, $67.88, $68.81, $74.88

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $63.90 - $64.64 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $61.68 | $68.35   | $71.32   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $61.55 - $62.66 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $60.81 | $65.07   | $66.56   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $64.97 - $65.72 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $62.29 | $71.45   | $74.51   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
