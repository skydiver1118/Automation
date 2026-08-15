# QLD Technical Analysis Sample

Generated: 2026-06-05 16:40:42
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (65/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QLD_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QLD_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $89.54             |
| SMA20             | $94.33             |
| SMA50             | $81.55             |
| SMA200            | $72.10             |
| RSI14             | 46.9               |
| MACD / Signal     | 4.15 / 4.94        |
| ADX14 / +DI / -DI | 37.1 / 27.2 / 31.4 |
| ATR14             | $3.04 (3.40%)      |
| 63-day range      | $56.60 - $101.19   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 89.54 vs 94.33               |
| Trend        | Close above SMA50                         | 8      | 8   | 89.54 vs 81.55               |
| Trend        | Close above SMA200                        | 8      | 8   | 89.54 vs 72.10               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 94.33 vs 81.55               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 81.55 vs 72.10               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.28                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | 4.15 vs 4.94                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.87              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 2.14%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.74x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 268932675 vs 270048724       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.07x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 37.1, +DI 27.2, -DI 31.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 101.92              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.40%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.51%                       |

## Support And Resistance

- Support levels: $68.38, $71.84, $81.55, $87.13, $89.28
- Resistance levels: $94.48, $101.37

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $87.76 - $90.04 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $78.51 | $109.68  | $120.07  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $94.48 - $96.00 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $89.28 | $107.16  | $113.12  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
