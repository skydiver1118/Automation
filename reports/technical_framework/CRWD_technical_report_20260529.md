# CRWD Technical Analysis Sample

Generated: 2026-05-31 20:25:43
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (83/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWD_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWD_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value             |
| ----------------- | ----------------- |
| Close             | $731.00           |
| SMA20             | $582.22           |
| SMA50             | $482.51           |
| SMA200            | $470.24           |
| RSI14             | 83.8              |
| MACD / Signal     | 62.41 / 53.11     |
| ADX14 / +DI / -DI | 48.6 / 48.2 / 7.6 |
| ATR14             | $28.78 (3.94%)    |
| 63-day range      | $361.81 - $731.49 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                    |
| ------------ | ----------------------------------------- | ------ | --- | --------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 731.00 vs 582.22            |
| Trend        | Close above SMA50                         | 8      | 8   | 731.00 vs 482.51            |
| Trend        | Close above SMA200                        | 8      | 8   | 731.00 vs 470.24            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 582.22 vs 482.51            |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 482.51 vs 470.24            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 69.78                       |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 83.8                  |
| Momentum     | MACD above signal                         | 7      | 7   | 62.41 vs 53.11              |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -3.56             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 63.99%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.49x                       |
| Confirmation | OBV above 20-day average                  | 5      | 5   | -15483700 vs -32491740      |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 4.01x                       |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 48.6, +DI 48.2, -DI 7.6 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 744.65             |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.94%                 |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.07%                       |

## Support And Resistance

- Support levels: $431.77, $449.45, $477.33, $588.01, $633.09
- Resistance levels: $734.78

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2  | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $618.70 - $640.29 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $453.73 | $981.02  | $1,156.78 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $731.49 - $745.88 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $673.44 | $869.19  | $934.44   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
