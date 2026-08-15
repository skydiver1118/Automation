# MU Technical Analysis Sample

Generated: 2026-06-08 21:13:20
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (76/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MU_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MU_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $949.28             |
| SMA20             | $859.94             |
| SMA50             | $629.23             |
| SMA200            | $364.88             |
| RSI14             | 60.8                |
| MACD / Signal     | 103.40 / 106.36     |
| ADX14 / +DI / -DI | 38.4 / 31.6 / 23.8  |
| ATR14             | $68.16 (7.18%)      |
| 63-day range      | $311.49 - $1,089.29 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 949.28 vs 859.94             |
| Trend        | Close above SMA50                         | 8      | 8   | 949.28 vs 629.23             |
| Trend        | Close above SMA200                        | 8      | 8   | 949.28 vs 364.88             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 859.94 vs 629.23             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 629.23 vs 364.88             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 180.34                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 60.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | 103.40 vs 106.36             |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -23.70             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 27.11%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.96x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1250283209 vs 1119466130     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.37x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 38.4, +DI 31.6, -DI 23.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 1114.02             |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.18%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 12.85%                       |

## Support And Resistance

- Support levels: $311.49, $360.63, $435.90, $629.10, $859.57
- Resistance levels: $1,095.47

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop    | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $825.86 - $876.98     | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $561.07 | $1,432.12 | $1,722.47 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,089.29 - $1,123.37 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $859.94 | $1,599.11 | $1,845.49 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
