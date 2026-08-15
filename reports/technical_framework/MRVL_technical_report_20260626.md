# MRVL Technical Analysis Sample

Generated: 2026-06-28 17:42:39
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (68/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MRVL_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MRVL_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $266.77            |
| SMA20             | $278.24            |
| SMA50             | $213.21            |
| SMA200            | $118.45            |
| RSI14             | 52.6               |
| MACD / Signal     | 20.96 / 26.67      |
| ADX14 / +DI / -DI | 34.4 / 25.3 / 18.8 |
| ATR14             | $26.77 (10.03%)    |
| 63-day range      | $86.57 - $329.88   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 266.77 vs 278.24             |
| Trend        | Close above SMA50                         | 8      | 8   | 266.77 vs 213.21             |
| Trend        | Close above SMA200                        | 8      | 8   | 266.77 vs 118.45             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 278.24 vs 213.21             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 213.21 vs 118.45             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 68.90                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 52.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | 20.96 vs 26.67               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -6.35              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 30.24%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.58x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1179674900 vs 1085965210     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.71x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 34.4, +DI 25.3, -DI 18.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 334.89              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.03%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 19.13%                       |

## Support And Resistance

- Support levels: $128.42, $155.89, $217.40, $244.00, $268.91
- Resistance levels: $329.75

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $253.10 - $273.17 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $186.44 | $416.52  | $493.22  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $329.75 - $343.13 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $266.48 | $476.35  | $546.31  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
