# HOOD Technical Analysis Sample

Generated: 2026-06-08 21:13:18
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (69/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [HOOD_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/HOOD_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $85.04             |
| SMA20             | $80.87             |
| SMA50             | $78.54             |
| SMA200            | $103.19            |
| RSI14             | 54.0               |
| MACD / Signal     | 2.18 / 1.63        |
| ADX14 / +DI / -DI | 22.3 / 25.7 / 16.1 |
| ATR14             | $5.31 (6.24%)      |
| 63-day range      | $63.51 - $94.40    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 85.04 vs 80.87               |
| Trend        | Close above SMA50                         | 8      | 8   | 85.04 vs 78.54               |
| Trend        | Close above SMA200                        | 0      | 8   | 85.04 vs 103.19              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 80.87 vs 78.54               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 78.54 vs 103.19              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 2.07                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 54.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 2.18 vs 1.63                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.14              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 10.40%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.72x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1354802583 vs 1318391189     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.29x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 22.3, +DI 25.7, -DI 16.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 92.94               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.24%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 9.92%                        |

## Support And Resistance

- Support levels: $63.51, $70.70, $74.25, $80.24
- Resistance levels: $88.60, $93.89, $111.46, $120.88, $124.35

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $79.41 - $83.40 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $73.23 | $97.75   | $105.92  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $88.60 - $91.25 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $82.07 | $105.65  | $113.50  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
