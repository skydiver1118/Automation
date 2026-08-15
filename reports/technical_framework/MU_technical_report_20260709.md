# MU Technical Analysis Sample

Generated: 2026-07-09 16:40:27
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (63/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MU_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MU_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $991.64             |
| SMA20             | $1,049.06           |
| SMA50             | $889.42             |
| SMA200            | $460.23             |
| RSI14             | 50.0                |
| MACD / Signal     | 24.48 / 54.99       |
| ADX14 / +DI / -DI | 19.7 / 27.3 / 33.4  |
| ATR14             | $90.33 (9.11%)      |
| 63-day range      | $398.38 - $1,254.81 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 991.64 vs 1049.06            |
| Trend        | Close above SMA50                         | 8      | 8   | 991.64 vs 889.42             |
| Trend        | Close above SMA200                        | 8      | 8   | 991.64 vs 460.23             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1049.06 vs 889.42            |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 889.42 vs 460.23             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 248.71                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 50.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | 24.48 vs 54.99               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -19.31             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 5.97%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.74x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1267043820 vs 1238500346     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.23x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 19.7, +DI 27.3, -DI 33.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 1231.21             |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.11%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 20.97%                       |

## Support And Resistance

- Support levels: $338.44, $417.11, $652.11, $875.55
- Resistance levels: $1,062.31, $1,248.91

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop    | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $844.26 - $912.01     | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $799.09 | $1,062.31 | $1,149.13 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,062.31 - $1,107.48 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $889.42 | $1,475.84 | $1,671.31 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
