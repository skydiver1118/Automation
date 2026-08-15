# VRSN Technical Analysis Sample

Generated: 2026-07-08 16:40:30
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (60/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [VRSN_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/VRSN_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $267.58            |
| SMA20             | $263.56            |
| SMA50             | $278.71            |
| SMA200            | $255.78            |
| RSI14             | 50.1               |
| MACD / Signal     | -5.91 / -7.48      |
| ADX14 / +DI / -DI | 27.7 / 24.4 / 21.8 |
| ATR14             | $8.11 (3.03%)      |
| 63-day range      | $244.74 - $312.48  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 267.58 vs 263.56             |
| Trend        | Close above SMA50                         | 0      | 8   | 267.58 vs 278.71             |
| Trend        | Close above SMA200                        | 8      | 8   | 267.58 vs 255.78             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 263.56 vs 278.71             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 278.71 vs 255.78             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.90                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 50.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | -5.91 vs -7.48               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.96               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -5.59%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.93x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 26307319 vs 25590171         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.85x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 27.7, +DI 24.4, -DI 21.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 288.83              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.03%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 14.37%                       |

## Support And Resistance

- Support levels: $237.38, $244.48, $252.84, $258.09, $264.41
- Resistance levels: $271.98, $279.87, $289.24, $302.97, $312.48

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $261.21 - $267.29 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $257.16 | $280.46  | $288.57  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $271.98 - $276.03 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $265.27 | $291.49  | $300.22  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
