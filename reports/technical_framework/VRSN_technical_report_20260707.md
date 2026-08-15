# VRSN Technical Analysis Sample

Generated: 2026-07-07 16:40:30
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (55/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [VRSN_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/VRSN_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $266.78            |
| SMA20             | $264.35            |
| SMA50             | $278.73            |
| SMA200            | $255.86            |
| RSI14             | 49.3               |
| MACD / Signal     | -7.02 / -7.87      |
| ADX14 / +DI / -DI | 29.4 / 23.4 / 23.1 |
| ATR14             | $8.22 (3.08%)      |
| 63-day range      | $244.74 - $312.48  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 266.78 vs 264.35             |
| Trend        | Close above SMA50                         | 0      | 8   | 266.78 vs 278.73             |
| Trend        | Close above SMA200                        | 8      | 8   | 266.78 vs 255.86             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 264.35 vs 278.73             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 278.73 vs 255.86             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.22                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.3                   |
| Momentum     | MACD above signal                         | 7      | 7   | -7.02 vs -7.87               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.76               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -9.54%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.80x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 25127698 vs 25282960         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.83x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 29.4, +DI 23.4, -DI 23.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 291.10              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.08%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 14.62%                       |

## Support And Resistance

- Support levels: $235.58, $243.76, $252.84, $258.09, $264.69
- Resistance levels: $269.34, $279.87, $291.80, $302.97, $312.48

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $260.93 - $267.09 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $256.82 | $280.44  | $288.66  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $269.34 - $273.45 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $265.04 | $287.83  | $296.05  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
