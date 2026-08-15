# AAPL Technical Analysis Sample

Generated: 2026-06-04 19:39:13
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (83/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AAPL_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AAPL_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value             |
| ----------------- | ----------------- |
| Close             | $311.23           |
| SMA20             | $303.23           |
| SMA50             | $279.99           |
| SMA200            | $264.38           |
| RSI14             | 66.6              |
| MACD / Signal     | 9.20 / 9.68       |
| ADX14 / +DI / -DI | 45.7 / 32.3 / 9.7 |
| ATR14             | $5.92 (1.90%)     |
| 63-day range      | $245.28 - $316.94 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                    |
| ------------ | ----------------------------------------- | ------ | --- | --------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 311.23 vs 303.23            |
| Trend        | Close above SMA50                         | 8      | 8   | 311.23 vs 279.99            |
| Trend        | Close above SMA200                        | 8      | 8   | 311.23 vs 264.38            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 303.23 vs 279.99            |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 279.99 vs 264.38            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 18.10                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 66.6                  |
| Momentum     | MACD above signal                         | 0      | 7   | 9.20 vs 9.68                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.28             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 8.35%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.80x                       |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 2140795159 vs 2076321568    |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.68x                       |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 45.7, +DI 32.3, -DI 9.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 319.09             |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 1.90%                 |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 1.80%                       |

## Support And Resistance

- Support levels: $253.90, $265.64, $279.99, $287.38, $303.24
- Resistance levels: $317.48

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $300.28 - $304.72 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $274.07 | $359.35  | $387.78  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $316.94 - $319.90 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $303.24 | $348.78  | $363.97  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
