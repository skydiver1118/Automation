# TSLA Technical Analysis Sample

Generated: 2026-07-07 16:40:28
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (55/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSLA_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSLA_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $402.90            |
| SMA20             | $399.82            |
| SMA50             | $407.65            |
| SMA200            | $418.48            |
| RSI14             | 49.6               |
| MACD / Signal     | -0.16 / -2.14      |
| ADX14 / +DI / -DI | 14.4 / 22.2 / 23.6 |
| ATR14             | $20.15 (5.00%)     |
| 63-day range      | $337.24 - $453.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 402.90 vs 399.82             |
| Trend        | Close above SMA50                         | 0      | 8   | 402.90 vs 407.65             |
| Trend        | Close above SMA200                        | 0      | 8   | 402.90 vs 418.48             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 399.82 vs 407.65             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 407.65 vs 418.48             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 12.36                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.6                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.16 vs -2.14               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.12               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 3.04%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.75x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 2785282356 vs 2717299973     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.21x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.4, +DI 22.2, -DI 23.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 429.80              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.00%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.14%                       |

## Support And Resistance

- Support levels: $337.24, $363.81, $387.44, $403.00
- Resistance levels: $414.23, $432.97, $452.78

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $389.74 - $404.86 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $379.67 | $437.60  | $457.75  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $414.23 - $424.30 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $399.82 | $459.56  | $479.71  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
