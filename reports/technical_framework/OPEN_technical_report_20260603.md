# OPEN Technical Analysis Sample

Generated: 2026-06-03 19:37:01
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (42/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [OPEN_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/OPEN_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $4.87              |
| SMA20             | $4.79              |
| SMA50             | $4.91              |
| SMA200            | $6.10              |
| RSI14             | 49.4               |
| MACD / Signal     | 0.02 / -0.06       |
| ADX14 / +DI / -DI | 18.3 / 25.5 / 18.0 |
| ATR14             | $0.39 (8.05%)      |
| 63-day range      | $4.12 - $6.00      |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 4.87 vs 4.79                 |
| Trend        | Close above SMA50                         | 0      | 8   | 4.87 vs 4.91                 |
| Trend        | Close above SMA200                        | 0      | 8   | 4.87 vs 6.10                 |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 4.79 vs 4.91                 |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 4.91 vs 6.10                 |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.13                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.02 vs -0.06                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.09               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -6.88%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.11x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 5895656596 vs 5860346955     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.66x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.3, +DI 25.5, -DI 18.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 5.55                |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.05%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 18.83%                       |

## Support And Resistance

- Support levels: $4.17, $4.80
- Resistance levels: $5.01, $5.57, $6.00, $7.81

## Entry Plans

| Plan           | Entry zone    | Trigger                                                                                                      | Stop  | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ------------- | ------------------------------------------------------------------------------------------------------------ | ----- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $4.91 - $5.11 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $4.32 | $6.08    | $6.87    | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $4.60 - $4.90 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $4.41 | $5.53    | $5.92    | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $5.01 - $5.21 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $4.80 | $5.89    | $6.28    | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
