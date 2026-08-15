# AAPL Technical Analysis Sample

Generated: 2026-06-03 19:36:40
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (88/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AAPL_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AAPL_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $310.26            |
| SMA20             | $302.03            |
| SMA50             | $278.79            |
| SMA200            | $263.97            |
| RSI14             | 65.9               |
| MACD / Signal     | 9.56 / 9.80        |
| ADX14 / +DI / -DI | 45.1 / 33.9 / 10.2 |
| ATR14             | $6.07 (1.96%)      |
| 63-day range      | $245.28 - $316.94  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 310.26 vs 302.03             |
| Trend        | Close above SMA50                         | 8      | 8   | 310.26 vs 278.79             |
| Trend        | Close above SMA200                        | 8      | 8   | 310.26 vs 263.97             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 302.03 vs 278.79             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 278.79 vs 263.97             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 17.21                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 65.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | 9.56 vs 9.80                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.10              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 9.28%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.06x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 2158204350 vs 2121576522     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.38x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 45.1, +DI 33.9, -DI 10.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 318.93              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 1.96%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 2.11%                        |

## Support And Resistance

- Support levels: $253.90, $265.64, $278.79, $285.13, $302.51
- Resistance levels: $317.44

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $299.48 - $304.03 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $272.72 | $359.82  | $388.86  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $316.94 - $319.98 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $302.51 | $350.35  | $366.30  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
