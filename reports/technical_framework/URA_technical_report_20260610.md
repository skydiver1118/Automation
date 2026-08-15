# URA Technical Analysis Sample

Generated: 2026-06-10 20:55:20
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (19/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [URA_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/URA_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $42.35             |
| SMA20             | $49.12             |
| SMA50             | $51.91             |
| SMA200            | $48.88             |
| RSI14             | 31.7               |
| MACD / Signal     | -2.02 / -1.25      |
| ADX14 / +DI / -DI | 18.1 / 13.8 / 32.2 |
| ATR14             | $2.53 (5.97%)      |
| 63-day range      | $42.23 - $58.97    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 42.35 vs 49.12               |
| Trend        | Close above SMA50                         | 0      | 8   | 42.35 vs 51.91               |
| Trend        | Close above SMA200                        | 0      | 8   | 42.35 vs 48.88               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 49.12 vs 51.91               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 51.91 vs 48.88               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.08                        |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 31.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | -2.02 vs -1.25               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.88              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -22.08%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.31x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 142503695 vs 155114775       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.63x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.1, +DI 13.8, -DI 32.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 54.98               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.97%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 28.18%                       |

## Support And Resistance

- Support levels: $40.69, $42.56
- Resistance levels: $45.14, $46.92, $50.49, $54.04, $56.67

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $51.91 - $53.17 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $48.12 | $59.49   | $64.55   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $39.42 - $41.32 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $38.16 | $45.43   | $47.96   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $45.14 - $46.41 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $40.69 | $55.96   | $61.04   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
