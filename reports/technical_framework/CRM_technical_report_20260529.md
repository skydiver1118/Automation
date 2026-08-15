# CRM Technical Analysis Sample

Generated: 2026-05-31 20:26:16
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (57/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRM_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRM_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $191.10            |
| SMA20             | $179.03            |
| SMA50             | $180.68            |
| SMA200            | $220.57            |
| RSI14             | 60.5               |
| MACD / Signal     | -0.00 / -1.22      |
| ADX14 / +DI / -DI | 11.2 / 30.9 / 21.8 |
| ATR14             | $8.26 (4.32%)      |
| 63-day range      | $163.52 - $204.35  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 191.10 vs 179.03             |
| Trend        | Close above SMA50                         | 8      | 8   | 191.10 vs 180.68             |
| Trend        | Close above SMA200                        | 0      | 8   | 191.10 vs 220.57             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 179.03 vs 180.68             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 180.68 vs 220.57             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -5.67                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 60.5                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.00 vs -1.22               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.95               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 8.25%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 2.41x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 92054000 vs 102950050        |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.89x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 11.2, +DI 30.9, -DI 21.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 191.66              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.32%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 6.48%                        |

## Support And Resistance

- Support levels: $164.44, $172.36, $179.45, $189.62
- Resistance levels: $191.39, $203.29, $235.15, $267.47

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $185.48 - $191.68 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $172.41 | $220.92  | $237.09  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $191.39 - $195.53 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $189.62 | $209.99  | $218.25  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
