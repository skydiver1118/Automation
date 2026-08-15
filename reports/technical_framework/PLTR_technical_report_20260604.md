# PLTR Technical Analysis Sample

Generated: 2026-06-04 19:39:25
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (57/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [PLTR_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/PLTR_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $141.70            |
| SMA20             | $139.65            |
| SMA50             | $141.29            |
| SMA200            | $161.18            |
| RSI14             | 49.8               |
| MACD / Signal     | 1.90 / 0.72        |
| ADX14 / +DI / -DI | 15.0 / 28.8 / 26.7 |
| ATR14             | $7.17 (5.06%)      |
| 63-day range      | $122.68 - $163.70  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 141.70 vs 139.65             |
| Trend        | Close above SMA50                         | 8      | 8   | 141.70 vs 141.29             |
| Trend        | Close above SMA200                        | 0      | 8   | 141.70 vs 161.18             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 139.65 vs 141.29             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 141.29 vs 161.18             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.32                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | 1.90 vs 0.72                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.45               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 5.91%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.97x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 4362214691 vs 4329493165     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.22x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.0, +DI 28.8, -DI 26.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 155.66              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.06%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.44%                       |

## Support And Resistance

- Support levels: $125.53, $133.44, $140.86
- Resistance levels: $140.96, $151.16, $156.23, $163.34, $172.00

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $137.70 - $143.08 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $134.12 | $154.73  | $161.90  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $151.16 - $154.74 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $141.29 | $176.28  | $187.95  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
