# CRM Technical Analysis Sample

Generated: 2026-06-08 21:13:38
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (48/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRM_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRM_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $182.55            |
| SMA20             | $181.65            |
| SMA50             | $181.17            |
| SMA200            | $219.16            |
| RSI14             | 48.8               |
| MACD / Signal     | 2.40 / 1.89        |
| ADX14 / +DI / -DI | 14.1 / 27.0 / 23.5 |
| ATR14             | $9.20 (5.04%)      |
| 63-day range      | $163.52 - $211.34  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 182.55 vs 181.65             |
| Trend        | Close above SMA50                         | 8      | 8   | 182.55 vs 181.17             |
| Trend        | Close above SMA200                        | 0      | 8   | 182.55 vs 219.16             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 181.65 vs 181.17             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 181.17 vs 219.16             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.84                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 48.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | 2.40 vs 1.89                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.37              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 0.40%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.72x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | -5948219 vs 38176364         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.69x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.1, +DI 27.0, -DI 23.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 202.78              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.04%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.62%                       |

## Support And Resistance

- Support levels: $162.97, $172.36, $181.23
- Resistance levels: $189.95, $202.90, $211.34, $235.15, $267.47

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $177.05 - $183.95 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $171.98 | $198.89  | $208.08  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $189.95 - $194.55 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $181.65 | $213.46  | $224.07  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
