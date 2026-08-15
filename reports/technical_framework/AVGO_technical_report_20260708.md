# AVGO Technical Analysis Sample

Generated: 2026-07-08 16:40:11
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (59/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AVGO_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AVGO_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $388.69            |
| SMA20             | $380.68            |
| SMA50             | $406.29            |
| SMA200            | $360.65            |
| RSI14             | 50.3               |
| MACD / Signal     | -9.03 / -9.62      |
| ADX14 / +DI / -DI | 21.1 / 24.8 / 29.0 |
| ATR14             | $18.23 (4.69%)     |
| 63-day range      | $341.99 - $494.22  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 388.69 vs 380.68             |
| Trend        | Close above SMA50                         | 0      | 8   | 388.69 vs 406.29             |
| Trend        | Close above SMA200                        | 8      | 8   | 388.69 vs 360.65             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 380.68 vs 406.29             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 406.29 vs 360.65             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 6.77                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 50.3                   |
| Momentum     | MACD above signal                         | 7      | 7   | -9.03 vs -9.62               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.84               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -1.84%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.93x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 936954848 vs 934339232       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 1.00x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 21.1, +DI 24.8, -DI 29.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 404.26              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.69%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 21.35%                       |

## Support And Resistance

- Support levels: $310.39, $329.29, $341.99, $356.76, $378.41
- Resistance levels: $399.67, $414.64, $435.76, $494.22

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $375.71 - $389.38 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $366.59 | $419.00  | $437.22  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $399.67 - $408.79 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $384.82 | $443.05  | $462.46  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
