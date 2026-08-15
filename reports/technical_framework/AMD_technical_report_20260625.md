# AMD Technical Analysis Sample

Generated: 2026-06-26 06:53:37
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (86/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AMD_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AMD_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $532.57            |
| SMA20             | $512.22            |
| SMA50             | $433.85            |
| SMA200            | $268.64            |
| RSI14             | 58.5               |
| MACD / Signal     | 26.55 / 29.77      |
| ADX14 / +DI / -DI | 24.8 / 30.6 / 21.3 |
| ATR14             | $33.37 (6.27%)     |
| 63-day range      | $192.87 - $562.99  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 532.57 vs 512.22             |
| Trend        | Close above SMA50                         | 8      | 8   | 532.57 vs 433.85             |
| Trend        | Close above SMA200                        | 8      | 8   | 532.57 vs 268.64             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 512.22 vs 433.85             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 433.85 vs 268.64             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 118.47                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 58.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | 26.55 vs 29.77               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.49               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 7.47%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.87x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1501158500 vs 1453738185     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.03x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 24.8, +DI 30.6, -DI 21.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 564.97              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.27%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 5.40%                        |

## Support And Resistance

- Support levels: $194.26, $393.36, $435.54, $459.47, $505.94
- Resistance levels: $536.82, $562.46

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $495.53 - $520.56 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $400.48 | $723.19  | $830.76  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $536.82 - $553.51 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $512.22 | $611.90  | $645.28  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
