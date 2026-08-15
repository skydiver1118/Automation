# QLD Technical Analysis Sample

Generated: 2026-06-26 06:53:21
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (50/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QLD_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QLD_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $91.77             |
| SMA20             | $94.77             |
| SMA50             | $89.06             |
| SMA200            | $74.05             |
| RSI14             | 49.0               |
| MACD / Signal     | 0.95 / 1.82        |
| ADX14 / +DI / -DI | 22.5 / 21.9 / 30.3 |
| ATR14             | $4.25 (4.63%)      |
| 63-day range      | $56.56 - $101.12   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 91.77 vs 94.77               |
| Trend        | Close above SMA50                         | 8      | 8   | 91.77 vs 89.06               |
| Trend        | Close above SMA200                        | 8      | 8   | 91.77 vs 74.05               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 94.77 vs 89.06               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 89.06 vs 74.05               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 12.30                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | 0.95 vs 1.82                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.17              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -4.53%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.88x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 245269900 vs 253882060       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.82x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 22.5, +DI 21.9, -DI 30.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 103.19              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.63%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 9.25%                        |

## Support And Resistance

- Support levels: $61.32, $64.95, $69.69, $86.12, $88.93
- Resistance levels: $94.42, $100.46, $103.19

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $86.93 - $90.12 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $84.81 | $97.04   | $101.29  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $94.42 - $96.54 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $89.06 | $108.32  | $114.74  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
