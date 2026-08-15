# SNDK Technical Analysis Sample

Generated: 2026-07-09 16:40:37
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (63/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SNDK_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SNDK_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $1,858.27           |
| SMA20             | $1,968.71           |
| SMA50             | $1,669.97           |
| SMA200            | $736.16             |
| RSI14             | 50.6                |
| MACD / Signal     | 36.91 / 99.89       |
| ADX14 / +DI / -DI | 27.9 / 32.9 / 29.3  |
| ATR14             | $205.42 (11.05%)    |
| 63-day range      | $805.00 - $2,354.39 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 1858.27 vs 1968.71           |
| Trend        | Close above SMA50                         | 8      | 8   | 1858.27 vs 1669.97           |
| Trend        | Close above SMA200                        | 8      | 8   | 1858.27 vs 736.16            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1968.71 vs 1669.97           |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 1669.97 vs 736.16            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 448.70                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 50.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | 36.91 vs 99.89               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -51.96             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 12.86%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.08x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 529022391 vs 550874115       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.89x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 27.9, +DI 32.9, -DI 29.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 2385.01             |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 11.05%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 21.07%                       |

## Support And Resistance

- Support levels: $547.56, $805.00, $1,277.33, $1,517.26, $1,669.97
- Resistance levels: $1,906.79, $2,362.05

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop      | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | --------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $1,567.26 - $1,721.33 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $1,464.55 | $2,055.14 | $2,260.56 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,906.79 - $2,009.51 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $1,669.97 | $2,534.51 | $2,822.68 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
