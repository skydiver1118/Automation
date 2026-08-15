# RKLB Technical Analysis Sample

Generated: 2026-06-02 16:57:36
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (76/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKLB_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKLB_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $123.32            |
| SMA20             | $122.42            |
| SMA50             | $93.38             |
| SMA200            | $69.92             |
| RSI14             | 53.9               |
| MACD / Signal     | 12.75 / 14.31      |
| ADX14 / +DI / -DI | 40.1 / 28.0 / 19.0 |
| ATR14             | $10.98 (8.90%)     |
| 63-day range      | $56.13 - $151.00   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 123.32 vs 122.42             |
| Trend        | Close above SMA50                         | 8      | 8   | 123.32 vs 93.38              |
| Trend        | Close above SMA200                        | 8      | 8   | 123.32 vs 69.92              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 122.42 vs 93.38              |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 93.38 vs 69.92               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 20.71                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | 12.75 vs 14.31               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -4.03              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 53.55%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.61x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1923752840 vs 1886235812     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.07x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 40.1, +DI 28.0, -DI 19.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 164.57              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.90%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 18.33%                       |

## Support And Resistance

- Support levels: $54.98, $65.49, $78.09, $93.38, $120.11
- Resistance levels: $138.38, $151.00, $164.57

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $116.93 - $125.17 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $82.40  | $198.35  | $236.99  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $138.38 - $143.87 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $122.42 | $178.53  | $197.23  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
