# APP Technical Analysis Sample

Generated: 2026-07-07 16:40:11
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (46/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APP_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APP_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $527.98            |
| SMA20             | $502.00            |
| SMA50             | $503.32            |
| SMA200            | $539.22            |
| RSI14             | 53.6               |
| MACD / Signal     | 4.77 / -0.87       |
| ADX14 / +DI / -DI | 18.2 / 28.0 / 20.2 |
| ATR14             | $34.87 (6.60%)     |
| 63-day range      | $364.64 - $622.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 527.98 vs 502.00             |
| Trend        | Close above SMA50                         | 8      | 8   | 527.98 vs 503.32             |
| Trend        | Close above SMA200                        | 0      | 8   | 527.98 vs 539.22             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 502.00 vs 503.32             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 503.32 vs 539.22             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 31.55                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.6                   |
| Momentum     | MACD above signal                         | 7      | 7   | 4.77 vs -0.87                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 10.93              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -5.24%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.87x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 379868805 vs 387909125       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.53x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.2, +DI 28.0, -DI 20.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 569.24              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.60%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 15.12%                       |

## Support And Resistance

- Support levels: $363.62, $421.11, $458.67, $506.34
- Resistance levels: $573.02, $622.00, $679.69

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $493.55 - $519.70 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $468.45 | $582.99  | $621.17  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $573.02 - $590.45 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $510.99 | $723.24  | $793.99  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
