# SNDK Technical Analysis Sample

Generated: 2026-06-10 20:55:17
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (76/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SNDK_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SNDK_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $1,643.23           |
| SMA20             | $1,572.18           |
| SMA50             | $1,242.68           |
| SMA200            | $554.22             |
| RSI14             | 58.5                |
| MACD / Signal     | 122.69 / 144.11     |
| ADX14 / +DI / -DI | 41.8 / 26.5 / 13.7  |
| ATR14             | $134.04 (8.16%)     |
| 63-day range      | $558.58 - $1,861.00 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 1643.23 vs 1572.18           |
| Trend        | Close above SMA50                         | 8      | 8   | 1643.23 vs 1242.68           |
| Trend        | Close above SMA200                        | 8      | 8   | 1643.23 vs 554.22            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1572.18 vs 1242.68           |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 1242.68 vs 554.22            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 370.18                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 58.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | 122.69 vs 144.11             |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -36.04             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 13.17%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.91x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 542656351 vs 515815163       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.82x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 41.8, +DI 26.5, -DI 13.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 1865.44             |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.16%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.70%                       |

## Support And Resistance

- Support levels: $217.37, $549.76, $1,266.31, $1,548.27
- Resistance levels: $1,862.11

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop      | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | --------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $1,505.16 - $1,605.69 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $1,108.65 | $2,448.97 | $2,895.74 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,861.00 - $1,928.02 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $1,572.18 | $2,539.18 | $2,861.51 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
