# HOOD Technical Analysis Sample

Generated: 2026-07-08 16:40:15
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (89/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [HOOD_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/HOOD_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $113.53            |
| SMA20             | $101.48            |
| SMA50             | $88.33             |
| SMA200            | $102.31            |
| RSI14             | 64.5               |
| MACD / Signal     | 7.11 / 6.11        |
| ADX14 / +DI / -DI | 28.2 / 30.9 / 15.8 |
| ATR14             | $6.65 (5.86%)      |
| 63-day range      | $67.80 - $120.05   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 113.53 vs 101.48             |
| Trend        | Close above SMA50                         | 8      | 8   | 113.53 vs 88.33              |
| Trend        | Close above SMA200                        | 8      | 8   | 113.53 vs 102.31             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 101.48 vs 88.33              |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 88.33 vs 102.31              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 9.79                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 64.5                   |
| Momentum     | MACD above signal                         | 7      | 7   | 7.11 vs 6.11                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.15               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 33.50%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.54x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1571395668 vs 1483532513     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.23x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 28.2, +DI 30.9, -DI 15.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 119.91              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.86%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 5.43%                        |

## Support And Resistance

- Support levels: $88.33, $92.80, $102.59, $108.89, $113.87
- Resistance levels: $120.19, $124.35

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $105.56 - $110.55 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $81.68  | $160.82  | $187.20  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $120.05 - $123.38 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $108.89 | $147.36  | $160.18  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
