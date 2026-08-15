# APLD Technical Analysis Sample

Generated: 2026-06-26 06:53:40
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (46/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APLD_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APLD_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $40.95             |
| SMA20             | $44.27             |
| SMA50             | $40.81             |
| SMA200            | $31.80             |
| RSI14             | 45.5               |
| MACD / Signal     | 0.61 / 1.13        |
| ADX14 / +DI / -DI | 17.0 / 19.2 / 20.9 |
| ATR14             | $4.10 (10.02%)     |
| 63-day range      | $20.00 - $50.72    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 40.95 vs 44.27               |
| Trend        | Close above SMA50                         | 8      | 8   | 40.95 vs 40.81               |
| Trend        | Close above SMA200                        | 8      | 8   | 40.95 vs 31.80               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 44.27 vs 40.81               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 40.81 vs 31.80               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 7.29                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 45.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | 0.61 vs 1.13                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.31              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -16.39%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.66x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1613136200 vs 1628960165     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.81x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.0, +DI 19.2, -DI 20.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 50.36               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.02%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 19.27%                       |

## Support And Resistance

- Support levels: $24.23, $27.62, $31.41, $38.02, $40.81
- Resistance levels: $42.27, $49.50

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $38.76 - $41.84 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $36.71 | $48.50   | $52.61   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $42.27 - $44.32 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $40.81 | $51.50   | $55.60   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
