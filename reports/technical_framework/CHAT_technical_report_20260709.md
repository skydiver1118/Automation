# CHAT Technical Analysis Sample

Generated: 2026-07-09 16:40:21
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (70/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CHAT_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CHAT_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $92.39             |
| SMA20             | $94.57             |
| SMA50             | $91.06             |
| SMA200            | $69.75             |
| RSI14             | 49.3               |
| MACD / Signal     | -0.28 / 0.87       |
| ADX14 / +DI / -DI | 17.4 / 26.4 / 35.1 |
| ATR14             | $4.35 (4.71%)      |
| 63-day range      | $67.03 - $105.20   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 92.39 vs 94.57               |
| Trend        | Close above SMA50                         | 8      | 8   | 92.39 vs 91.06               |
| Trend        | Close above SMA200                        | 8      | 8   | 92.39 vs 69.75               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 94.57 vs 91.06               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 91.06 vs 69.75               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 9.53                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.28 vs 0.87                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.36              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 1.46%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.19x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 20506427 vs 19755286         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.47x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.4, +DI 26.4, -DI 35.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 103.57              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.71%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 12.18%                       |

## Support And Resistance

- Support levels: $67.03, $74.70, $81.50, $85.83, $92.98
- Resistance levels: $93.18, $104.68

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $88.88 - $92.15 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $86.70 | $99.22   | $103.58  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $93.18 - $95.36 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $91.06 | $102.98  | $107.33  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
