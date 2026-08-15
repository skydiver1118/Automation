# AMD Technical Analysis Sample

Generated: 2026-06-28 17:42:40
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (76/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AMD_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AMD_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $521.58            |
| SMA20             | $512.39            |
| SMA50             | $439.12            |
| SMA200            | $270.47            |
| RSI14             | 56.1               |
| MACD / Signal     | 24.87 / 28.79      |
| ADX14 / +DI / -DI | 24.2 / 28.6 / 20.8 |
| ATR14             | $33.13 (6.35%)     |
| 63-day range      | $192.87 - $562.99  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 521.58 vs 512.39             |
| Trend        | Close above SMA50                         | 8      | 8   | 521.58 vs 439.12             |
| Trend        | Close above SMA200                        | 8      | 8   | 521.58 vs 270.47             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 512.39 vs 439.12             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 439.12 vs 270.47             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 117.31                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 56.1                   |
| Momentum     | MACD above signal                         | 0      | 7   | 24.87 vs 28.79               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.78              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 0.67%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.64x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1414478500 vs 1417457400     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.95x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 24.2, +DI 28.6, -DI 20.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 565.25              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.35%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 7.36%                        |

## Support And Resistance

- Support levels: $194.26, $393.36, $438.18, $459.54, $506.29
- Resistance levels: $536.82, $562.52

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $495.83 - $520.68 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $405.99 | $712.78  | $815.04  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $536.82 - $553.38 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $512.39 | $611.36  | $644.48  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
