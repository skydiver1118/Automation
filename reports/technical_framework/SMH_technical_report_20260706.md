# SMH Technical Analysis Sample

Generated: 2026-07-06 16:40:26
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (50/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SMH_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SMH_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $604.30            |
| SMA20             | $618.47            |
| SMA50             | $582.05            |
| SMA200            | $427.23            |
| RSI14             | 49.2               |
| MACD / Signal     | 10.35 / 17.07      |
| ADX14 / +DI / -DI | 15.0 / 21.3 / 30.2 |
| ATR14             | $30.65 (5.07%)     |
| 63-day range      | $389.64 - $671.83  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 604.30 vs 618.47             |
| Trend        | Close above SMA50                         | 8      | 8   | 604.30 vs 582.05             |
| Trend        | Close above SMA200                        | 8      | 8   | 604.30 vs 427.23             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 618.47 vs 582.05             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 582.05 vs 427.23             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 78.53                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.2                   |
| Momentum     | MACD above signal                         | 0      | 7   | 10.35 vs 17.07               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.92              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -3.70%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.73x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 267450384 vs 276572419       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.97x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.0, +DI 21.3, -DI 30.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 672.52              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.07%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.05%                       |

## Support And Resistance

- Support levels: $376.19, $397.77, $527.87, $559.54, $582.33
- Resistance levels: $651.26, $672.00

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $567.00 - $589.99 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $551.40 | $651.26  | $670.45  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $651.26 - $666.58 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $582.33 | $812.10  | $888.69  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
