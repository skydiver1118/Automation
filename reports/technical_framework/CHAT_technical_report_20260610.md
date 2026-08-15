# CHAT Technical Analysis Sample

Generated: 2026-06-10 20:55:02
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (55/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CHAT_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CHAT_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $87.62             |
| SMA20             | $92.50             |
| SMA50             | $82.10             |
| SMA200            | $65.94             |
| RSI14             | 46.6               |
| MACD / Signal     | 3.27 / 4.71        |
| ADX14 / +DI / -DI | 29.3 / 22.9 / 32.5 |
| ATR14             | $4.05 (4.62%)      |
| 63-day range      | $58.52 - $104.21   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 87.62 vs 92.50               |
| Trend        | Close above SMA50                         | 8      | 8   | 87.62 vs 82.10               |
| Trend        | Close above SMA200                        | 8      | 8   | 87.62 vs 65.94               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 92.50 vs 82.10               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 82.10 vs 65.94               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.70                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | 3.27 vs 4.71                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.54              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 4.01%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.78x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 19192055 vs 20269323         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 1.00x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 29.3, +DI 22.9, -DI 32.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 105.06              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.62%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 15.92%                       |

## Support And Resistance

- Support levels: $58.46, $62.69, $74.70, $81.26, $86.06
- Resistance levels: $89.07, $104.42

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $84.04 - $87.07 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $78.05 | $100.56  | $108.07  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $89.07 - $91.10 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $86.06 | $98.18   | $102.23  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
