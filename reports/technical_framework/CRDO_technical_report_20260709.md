# CRDO Technical Analysis Sample

Generated: 2026-07-09 16:40:50
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (64/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRDO_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRDO_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $265.65            |
| SMA20             | $258.87            |
| SMA50             | $223.06            |
| SMA200            | $160.55            |
| RSI14             | 55.1               |
| MACD / Signal     | 10.15 / 12.93      |
| ADX14 / +DI / -DI | 25.2 / 23.7 / 17.2 |
| ATR14             | $27.51 (10.35%)    |
| 63-day range      | $106.09 - $308.67  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 265.65 vs 258.87             |
| Trend        | Close above SMA50                         | 8      | 8   | 265.65 vs 223.06             |
| Trend        | Close above SMA200                        | 8      | 8   | 265.65 vs 160.55             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 258.87 vs 223.06             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 223.06 vs 160.55             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 47.22                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 55.1                   |
| Momentum     | MACD above signal                         | 0      | 7   | 10.15 vs 12.93               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.23              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 13.37%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.67x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 209857438 vs 224924877       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.81x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 25.2, +DI 23.7, -DI 17.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 290.58              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.35%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.94%                       |

## Support And Resistance

- Support levels: $156.87, $182.80, $200.00, $228.72, $255.09
- Resistance levels: $280.43, $308.67

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $245.12 - $265.75 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $195.55 | $375.20  | $435.08  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $280.43 - $294.18 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $258.87 | $344.17  | $372.61  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
