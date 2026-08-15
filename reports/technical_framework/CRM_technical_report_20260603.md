# CRM Technical Analysis Sample

Generated: 2026-06-03 19:37:31
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (53/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRM_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRM_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $190.61            |
| SMA20             | $181.27            |
| SMA50             | $181.02            |
| SMA200            | $220.03            |
| RSI14             | 54.6               |
| MACD / Signal     | 3.57 / 0.96        |
| ADX14 / +DI / -DI | 14.8 / 32.4 / 21.2 |
| ATR14             | $9.57 (5.02%)      |
| 63-day range      | $163.52 - $211.34  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 190.61 vs 181.27             |
| Trend        | Close above SMA50                         | 8      | 8   | 190.61 vs 181.02             |
| Trend        | Close above SMA200                        | 0      | 8   | 190.61 vs 220.03             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 181.27 vs 181.02             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 181.02 vs 220.03             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -5.51                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 54.6                   |
| Momentum     | MACD above signal                         | 7      | 7   | 3.57 vs 0.96                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.11               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 1.94%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.89x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 40935675 vs 55129189         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.83x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.8, +DI 32.4, -DI 21.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 202.16              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.02%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 9.81%                        |

## Support And Resistance

- Support levels: $162.94, $172.36, $180.98, $189.62
- Resistance levels: $189.95, $202.74, $211.34, $235.15, $267.47

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $184.83 - $192.01 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $171.44 | $222.37  | $239.35  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $202.74 - $207.53 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $189.62 | $236.17  | $251.69  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
