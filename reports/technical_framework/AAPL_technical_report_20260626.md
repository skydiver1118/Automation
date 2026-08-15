# AAPL Technical Analysis Sample

Generated: 2026-06-28 17:42:16
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (47/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AAPL_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AAPL_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $283.78            |
| SMA20             | $298.29            |
| SMA50             | $291.41            |
| SMA200            | $269.08            |
| RSI14             | 41.3               |
| MACD / Signal     | -2.24 / 0.53       |
| ADX14 / +DI / -DI | 25.0 / 12.5 / 28.4 |
| ATR14             | $8.16 (2.87%)      |
| 63-day range      | $245.28 - $317.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 283.78 vs 298.29             |
| Trend        | Close above SMA50                         | 0      | 8   | 283.78 vs 291.41             |
| Trend        | Close above SMA200                        | 8      | 8   | 283.78 vs 269.08             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 298.29 vs 291.41             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 291.41 vs 269.08             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 17.55                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 41.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | -2.24 vs 0.53                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.73              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -9.19%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 3.91x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1874096600 vs 1800708725     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.95x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 25.0, +DI 12.5, -DI 28.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 318.33              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.87%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.59%                       |

## Support And Resistance

- Support levels: $244.96, $253.90, $264.83, $272.72, $278.25
- Resistance levels: $302.81, $317.63

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $298.29 - $302.37 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $286.05 | $322.76  | $339.08  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $274.17 - $280.29 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $270.09 | $302.81  | $301.70  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $302.81 - $306.89 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $278.25 | $358.04  | $384.64  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
