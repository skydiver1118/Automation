# APLD Technical Analysis Sample

Generated: 2026-06-05 16:41:03
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (51/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APLD_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APLD_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $39.62             |
| SMA20             | $44.45             |
| SMA50             | $36.16             |
| SMA200            | $29.99             |
| RSI14             | 45.7               |
| MACD / Signal     | 2.18 / 3.08        |
| ADX14 / +DI / -DI | 26.0 / 19.8 / 28.8 |
| ATR14             | $4.07 (10.27%)     |
| 63-day range      | $20.00 - $50.72    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 39.62 vs 44.45               |
| Trend        | Close above SMA50                         | 8      | 8   | 39.62 vs 36.16               |
| Trend        | Close above SMA200                        | 8      | 8   | 39.62 vs 29.99               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 44.45 vs 36.16               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 36.16 vs 29.99               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 6.85                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 45.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | 2.18 vs 3.08                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.14              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -4.60%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.03x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1597580512 vs 1636166006     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.92x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 26.0, +DI 19.8, -DI 28.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 51.74               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.27%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 21.89%                       |

## Support And Resistance

- Support levels: $20.64, $24.23, $28.94, $32.32, $37.11
- Resistance levels: $39.34, $42.27, $47.79, $50.98

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $35.07 - $38.12 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $32.09 | $45.60   | $50.11   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $42.27 - $44.30 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $37.11 | $55.65   | $61.83   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
