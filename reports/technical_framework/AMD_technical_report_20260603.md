# AMD Technical Analysis Sample

Generated: 2026-06-03 19:37:30
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (92/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AMD_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AMD_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $542.52            |
| SMA20             | $465.95            |
| SMA50             | $347.44            |
| SMA200            | $242.74            |
| RSI14             | 77.8               |
| MACD / Signal     | 50.69 / 48.42      |
| ADX14 / +DI / -DI | 47.0 / 39.4 / 13.5 |
| ATR14             | $25.92 (4.78%)     |
| 63-day range      | $189.02 - $546.44  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 542.52 vs 465.95             |
| Trend        | Close above SMA50                         | 8      | 8   | 542.52 vs 347.44             |
| Trend        | Close above SMA200                        | 8      | 8   | 542.52 vs 242.74             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 465.95 vs 347.44             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 347.44 vs 242.74             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 106.07                       |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 77.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | 50.69 vs 48.42               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.73               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 52.71%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.77x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1349640202 vs 1306405605     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.16x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 47.0, +DI 39.4, -DI 13.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 548.00              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.78%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.72%                        |

## Support And Resistance

- Support levels: $192.84, $210.51, $347.44, $388.63, $461.85
- Resistance levels: $546.83

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $452.99 - $472.43 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $321.52 | $745.08  | $886.27  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $546.44 - $559.40 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $490.67 | $677.42  | $739.67  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
