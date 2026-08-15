# APP Technical Analysis Sample

Generated: 2026-07-08 16:40:11
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (46/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APP_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APP_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $522.18            |
| SMA20             | $499.92            |
| SMA50             | $504.80            |
| SMA200            | $538.72            |
| RSI14             | 52.4               |
| MACD / Signal     | 5.03 / 0.31        |
| ADX14 / +DI / -DI | 17.6 / 26.8 / 21.6 |
| ATR14             | $33.91 (6.49%)     |
| 63-day range      | $364.64 - $622.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 522.18 vs 499.92             |
| Trend        | Close above SMA50                         | 8      | 8   | 522.18 vs 504.80             |
| Trend        | Close above SMA200                        | 0      | 8   | 522.18 vs 538.72             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 499.92 vs 504.80             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 504.80 vs 538.72             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 29.58                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 52.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 5.03 vs 0.31                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 6.50               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -7.36%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.84x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 376985590 vs 388007590       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.53x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.6, +DI 26.8, -DI 21.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 561.46              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.49%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 16.05%                       |

## Support And Resistance

- Support levels: $363.62, $417.70, $447.46, $472.00, $506.55
- Resistance levels: $519.75, $571.08, $622.00, $679.69

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $495.05 - $520.48 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $470.89 | $581.52  | $618.40  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $571.08 - $588.03 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $512.00 | $714.65  | $782.20  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
