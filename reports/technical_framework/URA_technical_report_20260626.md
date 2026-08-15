# URA Technical Analysis Sample

Generated: 2026-06-28 17:42:36
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (17/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [URA_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/URA_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $43.59             |
| SMA20             | $46.94             |
| SMA50             | $50.90             |
| SMA200            | $49.27             |
| RSI14             | 37.6               |
| MACD / Signal     | -1.62 / -1.50      |
| ADX14 / +DI / -DI | 18.2 / 15.9 / 29.7 |
| ATR14             | $2.18 (5.00%)      |
| 63-day range      | $42.23 - $58.97    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 43.59 vs 46.94               |
| Trend        | Close above SMA50                         | 0      | 8   | 43.59 vs 50.90               |
| Trend        | Close above SMA200                        | 0      | 8   | 43.59 vs 49.27               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 46.94 vs 50.90               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 50.90 vs 49.27               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.90                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 37.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | -1.62 vs -1.50               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.31              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -14.11%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.53x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 132648200 vs 144880570       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.54x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.2, +DI 15.9, -DI 29.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 52.78               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.00%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 26.08%                       |

## Support And Resistance

- Support levels: $42.18
- Resistance levels: $50.13, $53.26, $55.06, $56.67, $58.86

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $50.90 - $51.99 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $47.63 | $57.43   | $61.79   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $41.09 - $42.72 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $40.00 | $50.13   | $48.44   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $50.13 - $51.22 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $42.18 | $67.66   | $76.16   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
