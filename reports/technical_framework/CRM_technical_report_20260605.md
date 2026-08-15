# CRM Technical Analysis Sample

Generated: 2026-06-05 16:41:01
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (48/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRM_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRM_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $185.66            |
| SMA20             | $181.61            |
| SMA50             | $181.22            |
| SMA200            | $219.47            |
| RSI14             | 51.0               |
| MACD / Signal     | 3.01 / 1.76        |
| ADX14 / +DI / -DI | 14.6 / 27.9 / 21.7 |
| ATR14             | $9.60 (5.17%)      |
| 63-day range      | $163.52 - $211.34  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 185.66 vs 181.61             |
| Trend        | Close above SMA50                         | 8      | 8   | 185.66 vs 181.22             |
| Trend        | Close above SMA200                        | 0      | 8   | 185.66 vs 219.47             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 181.61 vs 181.22             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 181.22 vs 219.47             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -5.13                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 51.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 3.01 vs 1.76                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.03               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -0.36%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.82x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | -9133329 vs 26971459         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.69x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.6, +DI 27.9, -DI 21.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 202.74              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.17%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 12.15%                       |

## Support And Resistance

- Support levels: $162.96, $172.36, $181.79
- Resistance levels: $189.95, $202.89, $211.34, $235.15, $267.47

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $180.12 - $187.32 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $171.62 | $207.91  | $220.00  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $189.95 - $194.75 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $184.92 | $211.55  | $221.15  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
