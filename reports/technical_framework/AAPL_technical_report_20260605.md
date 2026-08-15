# AAPL Technical Analysis Sample

Generated: 2026-06-05 16:40:29
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (83/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AAPL_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AAPL_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $307.34            |
| SMA20             | $304.24            |
| SMA50             | $281.09            |
| SMA200            | $264.76            |
| RSI14             | 60.8               |
| MACD / Signal     | 8.51 / 9.45        |
| ADX14 / +DI / -DI | 45.5 / 29.2 / 11.8 |
| ATR14             | $6.07 (1.97%)      |
| 63-day range      | $245.28 - $316.94  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 307.34 vs 304.24             |
| Trend        | Close above SMA50                         | 8      | 8   | 307.34 vs 281.09             |
| Trend        | Close above SMA200                        | 8      | 8   | 307.34 vs 264.76             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 304.24 vs 281.09             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 281.09 vs 264.76             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 18.93                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 60.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | 8.51 vs 9.45                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.55              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 7.02%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.35x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 2125312536 vs 2126239282     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.29x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 45.5, +DI 29.2, -DI 11.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 318.25              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 1.97%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 3.03%                        |

## Support And Resistance

- Support levels: $253.90, $265.64, $281.09, $290.23, $303.75
- Resistance levels: $317.27

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $301.21 - $305.76 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $275.02 | $360.41  | $388.87  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $316.94 - $319.97 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $304.24 | $346.89  | $361.11  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
