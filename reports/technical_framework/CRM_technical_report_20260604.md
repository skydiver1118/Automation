# CRM Technical Analysis Sample

Generated: 2026-06-04 19:39:42
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (53/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRM_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRM_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $188.75            |
| SMA20             | $181.65            |
| SMA50             | $181.14            |
| SMA200            | $219.76            |
| RSI14             | 53.2               |
| MACD / Signal     | 3.42 / 1.45        |
| ADX14 / +DI / -DI | 14.9 / 29.8 / 21.4 |
| ATR14             | $9.67 (5.12%)      |
| 63-day range      | $163.52 - $211.34  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 188.75 vs 181.65             |
| Trend        | Close above SMA50                         | 8      | 8   | 188.75 vs 181.14             |
| Trend        | Close above SMA200                        | 0      | 8   | 188.75 vs 219.76             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 181.65 vs 181.14             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 181.14 vs 219.76             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -5.31                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 3.42 vs 1.45                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.60               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 4.17%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.85x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 16532797 vs 42229930         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.68x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.9, +DI 29.8, -DI 21.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 202.81              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.12%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.69%                       |

## Support And Resistance

- Support levels: $162.96, $172.36, $181.16, $188.80
- Resistance levels: $189.95, $202.90, $211.34, $235.15, $267.47

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $180.01 - $187.26 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $171.47 | $207.96  | $220.13  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $189.95 - $194.79 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $184.84 | $211.71  | $221.38  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
