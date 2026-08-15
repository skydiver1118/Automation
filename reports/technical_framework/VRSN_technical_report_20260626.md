# VRSN Technical Analysis Sample

Generated: 2026-06-28 17:42:36
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (33/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [VRSN_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/VRSN_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $255.62            |
| SMA20             | $275.49            |
| SMA50             | $280.60            |
| SMA200            | $256.68            |
| RSI14             | 35.3               |
| MACD / Signal     | -9.59 / -6.09      |
| ADX14 / +DI / -DI | 33.6 / 12.1 / 32.3 |
| ATR14             | $8.55 (3.34%)      |
| 63-day range      | $244.74 - $312.48  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 255.62 vs 275.49             |
| Trend        | Close above SMA50                         | 0      | 8   | 255.62 vs 280.60             |
| Trend        | Close above SMA200                        | 0      | 8   | 255.62 vs 256.68             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 275.49 vs 280.60             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 280.60 vs 256.68             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 7.97                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 35.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | -9.59 vs -6.09               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.51               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -13.68%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.13x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 22580000 vs 24868445         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.77x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 33.6, +DI 12.1, -DI 32.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 310.71              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.34%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 18.20%                       |

## Support And Resistance

- Support levels: $209.34, $234.90, $243.18, $252.84, $258.09
- Resistance levels: $253.61, $279.87, $302.97, $311.89

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $280.60 - $284.88 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $267.78 | $306.25  | $323.35  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $248.56 - $254.97 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $244.29 | $279.87  | $277.42  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $279.87 - $284.14 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $252.84 | $340.33  | $369.50  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
