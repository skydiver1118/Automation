# CRWD Technical Analysis Sample

Generated: 2026-06-08 21:13:16
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (73/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWD_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWD_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $658.79            |
| SMA20             | $654.45            |
| SMA50             | $521.03            |
| SMA200            | $479.23            |
| RSI14             | 56.0               |
| MACD / Signal     | 56.25 / 62.31      |
| ADX14 / +DI / -DI | 49.2 / 33.2 / 21.0 |
| ATR14             | $34.88 (5.29%)     |
| 63-day range      | $361.81 - $785.66  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 658.79 vs 654.45             |
| Trend        | Close above SMA50                         | 8      | 8   | 658.79 vs 521.03             |
| Trend        | Close above SMA200                        | 8      | 8   | 658.79 vs 479.23             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 654.45 vs 521.03             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 521.03 vs 479.23             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 95.35                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 56.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | 56.25 vs 62.31               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -19.03             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 24.83%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.86x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | -50137701 vs -38812595       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.08x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 49.2, +DI 33.2, -DI 21.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 795.01              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.29%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 16.15%                       |

## Support And Resistance

- Support levels: $361.06, $439.18, $470.25, $517.46, $646.77
- Resistance levels: $788.00

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $637.01 - $663.17 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $486.15 | $977.99   | $1,141.94 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $785.66 - $803.10 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $654.45 | $1,074.23 | $1,214.16 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
