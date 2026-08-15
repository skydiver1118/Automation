# APLD Technical Analysis Sample

Generated: 2026-06-10 20:55:28
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (53/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APLD_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APLD_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $38.92             |
| SMA20             | $44.05             |
| SMA50             | $37.20             |
| SMA200            | $30.36             |
| RSI14             | 44.8               |
| MACD / Signal     | 0.96 / 2.22        |
| ADX14 / +DI / -DI | 22.4 / 23.7 / 22.1 |
| ATR14             | $4.25 (10.92%)     |
| 63-day range      | $20.00 - $50.72    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 38.92 vs 44.05               |
| Trend        | Close above SMA50                         | 8      | 8   | 38.92 vs 37.20               |
| Trend        | Close above SMA200                        | 8      | 8   | 38.92 vs 30.36               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 44.05 vs 37.20               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 37.20 vs 30.36               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 6.97                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 44.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | 0.96 vs 2.22                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.05              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -11.40%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.96x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1643498972 vs 1645025084     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.00x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 22.4, +DI 23.7, -DI 22.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 51.84               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.92%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 23.27%                       |

## Support And Resistance

- Support levels: $20.64, $24.23, $27.62, $31.41, $37.13
- Resistance levels: $39.34, $42.27, $47.33, $51.00

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $35.07 - $38.26 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $32.95 | $45.17   | $49.42   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $39.34 - $41.47 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $37.20 | $48.91   | $53.16   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
