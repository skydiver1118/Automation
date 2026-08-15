# APP Technical Analysis Sample

Generated: 2026-07-09 16:40:19
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (46/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APP_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APP_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $520.43            |
| SMA20             | $499.90            |
| SMA50             | $506.00            |
| SMA200            | $538.08            |
| RSI14             | 52.1               |
| MACD / Signal     | 5.04 / 1.26        |
| ADX14 / +DI / -DI | 16.9 / 25.2 / 21.7 |
| ATR14             | $33.58 (6.45%)     |
| 63-day range      | $364.64 - $622.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 520.43 vs 499.90             |
| Trend        | Close above SMA50                         | 8      | 8   | 520.43 vs 506.00             |
| Trend        | Close above SMA200                        | 0      | 8   | 520.43 vs 538.08             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 499.90 vs 506.00             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 506.00 vs 538.08             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 27.99                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 52.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | 5.04 vs 1.26                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.06               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -0.08%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.82x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 374620081 vs 388449404       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.53x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 16.9, +DI 25.2, -DI 21.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 561.41              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.45%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 16.33%                       |

## Support And Resistance

- Support levels: $363.62, $417.70, $440.69, $466.50, $505.64
- Resistance levels: $519.75, $571.06, $622.00, $679.69

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $495.98 - $521.17 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $472.42 | $580.89  | $617.04  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $571.06 - $587.86 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $512.77 | $712.84  | $779.53  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
