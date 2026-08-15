# SNDK Technical Analysis Sample

Generated: 2026-06-05 16:40:49
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (81/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SNDK_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SNDK_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $1,559.32           |
| SMA20             | $1,553.68           |
| SMA50             | $1,179.88           |
| SMA200            | $530.24             |
| RSI14             | 54.9                |
| MACD / Signal     | 150.60 / 157.27     |
| ADX14 / +DI / -DI | 45.1 / 28.9 / 19.3  |
| ATR14             | $119.27 (7.65%)     |
| 63-day range      | $517.00 - $1,861.00 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 1559.32 vs 1553.68           |
| Trend        | Close above SMA50                         | 8      | 8   | 1559.32 vs 1179.88           |
| Trend        | Close above SMA200                        | 8      | 8   | 1559.32 vs 530.24            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1553.68 vs 1179.88           |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 1179.88 vs 530.24            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 360.49                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 54.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | 150.60 vs 157.27             |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -13.24             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 16.37%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.05x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 529050126 vs 510567801       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.03x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 45.1, +DI 28.9, -DI 19.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 1844.37             |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.65%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 16.21%                       |

## Support And Resistance

- Support levels: $208.14, $541.44, $1,179.88, $1,270.16, $1,532.66
- Resistance levels: $1,600.00, $1,856.84

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop      | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | --------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $1,494.05 - $1,583.50 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $1,060.60 | $2,495.11 | $2,973.28 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,600.00 - $1,659.64 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $1,553.68 | $1,868.37 | $1,987.64 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
