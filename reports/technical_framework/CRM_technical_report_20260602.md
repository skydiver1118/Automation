# CRM Technical Analysis Sample

Generated: 2026-06-02 16:57:50
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (62/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRM_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRM_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $200.84            |
| SMA20             | $181.09            |
| SMA50             | $181.10            |
| SMA200            | $220.29            |
| RSI14             | 62.5               |
| MACD / Signal     | 3.53 / 0.31        |
| ADX14 / +DI / -DI | 14.3 / 35.3 / 18.2 |
| ATR14             | $9.46 (4.71%)      |
| 63-day range      | $163.52 - $211.34  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 200.84 vs 181.09             |
| Trend        | Close above SMA50                         | 8      | 8   | 200.84 vs 181.10             |
| Trend        | Close above SMA200                        | 0      | 8   | 200.84 vs 220.29             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 181.09 vs 181.10             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 181.10 vs 220.29             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -5.24                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 62.5                   |
| Momentum     | MACD above signal                         | 7      | 7   | 3.53 vs 0.31                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.66               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 8.28%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.03x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 47320877 vs 46113894         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.86x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.3, +DI 35.3, -DI 18.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 201.70              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.71%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 4.97%                        |

## Support And Resistance

- Support levels: $162.96, $172.36, $180.84, $189.62
- Resistance levels: $202.62, $211.34, $235.15, $267.47

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $184.89 - $191.98 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $171.64 | $222.02  | $238.81  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $202.62 - $207.35 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $189.62 | $235.73  | $251.11  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
