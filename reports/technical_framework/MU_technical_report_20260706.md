# MU Technical Analysis Sample

Generated: 2026-07-06 16:40:17
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (48/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MU_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MU_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $984.75             |
| SMA20             | $1,042.71           |
| SMA50             | $862.03             |
| SMA200            | $448.35             |
| RSI14             | 49.0                |
| MACD / Signal     | 52.85 / 78.83       |
| ADX14 / +DI / -DI | 19.9 / 24.2 / 33.1  |
| ATR14             | $93.08 (9.45%)      |
| 63-day range      | $364.10 - $1,255.00 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 984.75 vs 1042.71            |
| Trend        | Close above SMA50                         | 8      | 8   | 984.75 vs 862.03             |
| Trend        | Close above SMA200                        | 8      | 8   | 984.75 vs 448.35             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1042.71 vs 862.03            |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 862.03 vs 448.35             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 254.32                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | 52.85 vs 78.83               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -26.45             |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -1.13%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.62x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1279278870 vs 1285901588     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 1.00x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 19.9, +DI 24.2, -DI 33.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 1241.84             |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.45%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 21.53%                       |

## Support And Resistance

- Support levels: $338.32, $435.90, $652.21, $853.32, $970.69
- Resistance levels: $1,089.29, $1,251.71

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop    | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $924.15 - $993.96     | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $768.95 | $1,339.26 | $1,529.36 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,089.29 - $1,135.83 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $970.69 | $1,396.30 | $1,538.17 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
