# APP Technical Analysis Sample

Generated: 2026-06-04 19:39:14
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (77/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APP_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APP_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $558.87            |
| SMA20             | $521.97            |
| SMA50             | $469.36            |
| SMA200            | $539.33            |
| RSI14             | 58.5               |
| MACD / Signal     | 33.76 / 28.12      |
| ADX14 / +DI / -DI | 29.2 / 28.0 / 15.2 |
| ATR14             | $34.13 (6.11%)     |
| 63-day range      | $364.64 - $622.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 558.87 vs 521.97             |
| Trend        | Close above SMA50                         | 8      | 8   | 558.87 vs 469.36             |
| Trend        | Close above SMA200                        | 8      | 8   | 558.87 vs 539.33             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 521.97 vs 469.36             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 469.36 vs 539.33             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 25.53                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 58.5                   |
| Momentum     | MACD above signal                         | 7      | 7   | 33.76 vs 28.12               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -4.14              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 19.21%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.93x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 400772041 vs 388579172       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.61x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 29.2, +DI 28.0, -DI 15.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 630.40              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.11%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.15%                       |

## Support And Resistance

- Support levels: $363.62, $416.47, $457.79, $520.82, $554.23
- Resistance levels: $569.92, $624.10, $679.69, $732.42

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $537.17 - $562.76 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $435.23 | $779.43  | $894.17  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $569.92 - $586.98 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $554.23 | $646.71  | $680.84  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
