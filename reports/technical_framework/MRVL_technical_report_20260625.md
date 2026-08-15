# MRVL Technical Analysis Sample

Generated: 2026-06-26 06:53:36
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (76/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MRVL_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MRVL_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $281.26            |
| SMA20             | $275.14            |
| SMA50             | $210.57            |
| SMA200            | $117.45            |
| RSI14             | 56.5               |
| MACD / Signal     | 23.89 / 28.10      |
| ADX14 / +DI / -DI | 35.9 / 26.6 / 19.4 |
| ATR14             | $27.35 (9.72%)     |
| 63-day range      | $86.57 - $329.88   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 281.26 vs 275.14             |
| Trend        | Close above SMA50                         | 8      | 8   | 281.26 vs 210.57             |
| Trend        | Close above SMA200                        | 8      | 8   | 281.26 vs 117.45             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 275.14 vs 210.57             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 210.57 vs 117.45             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 68.54                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 56.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | 23.89 vs 28.10               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -4.19              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 41.55%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.54x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1227630400 vs 1071896145     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.93x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 35.9, +DI 26.6, -DI 19.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 340.54              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.72%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 14.74%                       |

## Support And Resistance

- Support levels: $128.42, $155.89, $210.16, $244.00, $268.42
- Resistance levels: $330.88

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $261.47 - $281.98 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $183.22 | $448.73  | $537.23  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $329.88 - $343.55 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $275.14 | $459.86  | $521.44  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
