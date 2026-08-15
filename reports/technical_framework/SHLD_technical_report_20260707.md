# SHLD Technical Analysis Sample

Generated: 2026-07-07 16:40:24
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (46/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SHLD_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SHLD_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $63.79             |
| SMA20             | $61.84             |
| SMA50             | $64.00             |
| SMA200            | $68.44             |
| RSI14             | 54.3               |
| MACD / Signal     | -0.59 / -1.19      |
| ADX14 / +DI / -DI | 26.4 / 33.3 / 26.7 |
| ATR14             | $1.47 (2.31%)      |
| 63-day range      | $57.70 - $75.03    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 63.79 vs 61.84               |
| Trend        | Close above SMA50                         | 0      | 8   | 63.79 vs 64.00               |
| Trend        | Close above SMA200                        | 0      | 8   | 63.79 vs 68.44               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 61.84 vs 64.00               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 64.00 vs 68.44               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.21                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 54.3                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.59 vs -1.19               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.00               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 1.50%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.69x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 29457651 vs 30220143         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.75x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 26.4, +DI 33.3, -DI 26.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 66.37               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.31%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 14.98%                       |

## Support And Resistance

- Support levels: $57.57, $61.93, $64.00
- Resistance levels: $64.97, $66.37, $67.88, $68.81, $74.88

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $61.52 - $62.62 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $60.78 | $65.02   | $66.49   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $64.97 - $65.71 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $62.25 | $71.52   | $74.61   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
