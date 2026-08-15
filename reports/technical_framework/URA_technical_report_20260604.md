# URA Technical Analysis Sample

Generated: 2026-06-04 19:39:36
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (53/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [URA_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/URA_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $50.28             |
| SMA20             | $51.38             |
| SMA50             | $52.11             |
| SMA200            | $48.71             |
| RSI14             | 46.1               |
| MACD / Signal     | -0.67 / -0.75      |
| ADX14 / +DI / -DI | 13.0 / 20.5 / 18.7 |
| ATR14             | $2.29 (4.56%)      |
| 63-day range      | $44.76 - $58.97    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 50.28 vs 51.38               |
| Trend        | Close above SMA50                         | 0      | 8   | 50.28 vs 52.11               |
| Trend        | Close above SMA200                        | 8      | 8   | 50.28 vs 48.71               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 51.38 vs 52.11               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 52.11 vs 48.71               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.16                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.67 vs -0.75               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.39               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -13.70%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.61x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 157335956 vs 156802103       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.74x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 13.0, +DI 20.5, -DI 18.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 56.93               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.56%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 14.74%                       |

## Support And Resistance

- Support levels: $40.69, $42.67, $45.54, $47.45, $49.49
- Resistance levels: $50.49, $53.34, $55.06, $56.80, $58.80

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $48.34 - $50.06 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $47.20 | $53.79   | $56.09   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $50.49 - $51.63 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $49.49 | $55.65   | $57.94   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
