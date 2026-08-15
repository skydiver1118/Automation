# MRVL Technical Analysis Sample

Generated: 2026-06-03 19:37:28
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (86/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MRVL_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MRVL_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value             |
| ----------------- | ----------------- |
| Close             | $301.65           |
| SMA20             | $196.14           |
| SMA50             | $157.55           |
| SMA200            | $101.26           |
| RSI14             | 86.9              |
| MACD / Signal     | 28.82 / 19.16     |
| ADX14 / +DI / -DI | 50.5 / 57.5 / 6.1 |
| ATR14             | $18.82 (6.24%)    |
| 63-day range      | $75.20 - $324.15  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                    |
| ------------ | ----------------------------------------- | ------ | --- | --------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 301.65 vs 196.14            |
| Trend        | Close above SMA50                         | 8      | 8   | 301.65 vs 157.55            |
| Trend        | Close above SMA200                        | 8      | 8   | 301.65 vs 101.26            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 196.14 vs 157.55            |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 157.55 vs 101.26            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 44.24                       |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 86.9                  |
| Momentum     | MACD above signal                         | 7      | 7   | 28.82 vs 19.16              |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 8.48              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 78.76%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 2.86x                       |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1087094156 vs 748895533     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 3.96x                       |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 50.5, +DI 57.5, -DI 6.1 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 271.92             |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.24%                 |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 6.94%                       |

## Support And Resistance

- Support levels: $79.66, $91.35, $124.39, $156.30, $199.92
- Resistance levels: $324.15

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $194.30 - $208.41 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $138.73 | $326.60  | $389.22  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $324.15 - $333.56 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $264.01 | $458.54  | $523.38  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
