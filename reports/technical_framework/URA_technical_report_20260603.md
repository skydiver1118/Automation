# URA Technical Analysis Sample

Generated: 2026-06-03 19:37:22
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (58/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [URA_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/URA_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $50.39             |
| SMA20             | $51.78             |
| SMA50             | $52.06             |
| SMA200            | $48.65             |
| RSI14             | 46.4               |
| MACD / Signal     | -0.66 / -0.77      |
| ADX14 / +DI / -DI | 13.7 / 21.2 / 18.3 |
| ATR14             | $2.39 (4.73%)      |
| 63-day range      | $44.76 - $58.97    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 50.39 vs 51.78               |
| Trend        | Close above SMA50                         | 0      | 8   | 50.39 vs 52.06               |
| Trend        | Close above SMA200                        | 8      | 8   | 50.39 vs 48.65               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 51.78 vs 52.06               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 52.06 vs 48.65               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.18                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.66 vs -0.77               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.58               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -7.03%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.16x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 156745364 vs 154514528       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.69x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 13.7, +DI 21.2, -DI 18.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 58.09               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.73%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 14.55%                       |

## Support And Resistance

- Support levels: $40.69, $42.40, $45.46, $47.45, $49.49
- Resistance levels: $50.49, $53.34, $55.06, $58.33, $62.28

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $48.30 - $50.09 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $47.10 | $53.96   | $56.35   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $50.49 - $51.68 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $49.49 | $55.85   | $58.24   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
