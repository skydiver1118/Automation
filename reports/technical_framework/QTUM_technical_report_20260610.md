# QTUM Technical Analysis Sample

Generated: 2026-06-10 20:55:12
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (60/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QTUM_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QTUM_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $150.99            |
| SMA20             | $154.23            |
| SMA50             | $138.09            |
| SMA200            | $116.75            |
| RSI14             | 50.5               |
| MACD / Signal     | 5.50 / 7.16        |
| ADX14 / +DI / -DI | 31.0 / 22.0 / 28.7 |
| ATR14             | $5.89 (3.90%)      |
| 63-day range      | $101.41 - $170.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 150.99 vs 154.23             |
| Trend        | Close above SMA50                         | 8      | 8   | 150.99 vs 138.09             |
| Trend        | Close above SMA200                        | 8      | 8   | 150.99 vs 116.75             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 154.23 vs 138.09             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 138.09 vs 116.75             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 17.69                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 50.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | 5.50 vs 7.16                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.90              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 4.87%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.91x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 19762620 vs 20616256         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.19x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 31.0, +DI 22.0, -DI 28.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 171.28              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.90%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.18%                       |

## Support And Resistance

- Support levels: $108.02, $114.63, $127.52, $137.65, $147.51
- Resistance levels: $170.32

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $144.57 - $148.98 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $132.21 | $175.91  | $190.48  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $170.00 - $172.94 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $147.51 | $219.39  | $243.36  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
