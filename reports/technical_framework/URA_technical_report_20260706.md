# URA Technical Analysis Sample

Generated: 2026-07-06 16:40:29
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (22/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [URA_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/URA_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $43.88             |
| SMA20             | $45.07             |
| SMA50             | $49.68             |
| SMA200            | $49.33             |
| RSI14             | 40.3               |
| MACD / Signal     | -1.66 / -1.63      |
| ADX14 / +DI / -DI | 20.1 / 15.2 / 23.9 |
| ATR14             | $2.00 (4.56%)      |
| 63-day range      | $42.23 - $58.97    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 43.88 vs 45.07               |
| Trend        | Close above SMA50                         | 0      | 8   | 43.88 vs 49.68               |
| Trend        | Close above SMA200                        | 0      | 8   | 43.88 vs 49.33               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 45.07 vs 49.68               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 49.68 vs 49.33               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -2.42                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 40.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | -1.66 vs -1.63               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.09               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -12.73%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.41x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 138351332 vs 143093992       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.74x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 20.1, +DI 15.2, -DI 23.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 48.50               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.56%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 25.59%                       |

## Support And Resistance

- Support levels: $42.48
- Resistance levels: $44.95, $49.38, $50.83, $53.34, $55.06

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $49.68 - $50.68 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $46.68 | $55.69   | $59.69   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $41.48 - $42.98 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $40.48 | $46.23   | $48.23   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $44.95 - $45.95 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $42.48 | $51.40   | $54.37   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
