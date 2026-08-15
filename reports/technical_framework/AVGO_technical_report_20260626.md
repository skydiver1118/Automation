# AVGO Technical Analysis Sample

Generated: 2026-06-28 17:42:18
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (31/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AVGO_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AVGO_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $365.02            |
| SMA20             | $403.21            |
| SMA50             | $411.37            |
| SMA200            | $360.01            |
| RSI14             | 39.9               |
| MACD / Signal     | -10.00 / -6.69     |
| ADX14 / +DI / -DI | 19.4 / 19.0 / 32.1 |
| ATR14             | $19.52 (5.35%)     |
| 63-day range      | $289.50 - $494.22  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 365.02 vs 403.21             |
| Trend        | Close above SMA50                         | 0      | 8   | 365.02 vs 411.37             |
| Trend        | Close above SMA200                        | 8      | 8   | 365.02 vs 360.01             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 403.21 vs 411.37             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 411.37 vs 360.01             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 28.94                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 39.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | -10.00 vs -6.69              |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.14              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -14.30%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.91x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1048360000 vs 1113048335     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.66x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 19.4, +DI 19.0, -DI 32.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 473.35              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.35%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 26.14%                       |

## Support And Resistance

- Support levels: $291.07, $310.39, $331.17, $343.42, $366.79
- Resistance levels: $414.64, $435.76, $473.35, $494.22

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $411.37 - $421.13 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $382.10 | $469.93  | $508.97  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $333.67 - $348.30 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $323.91 | $414.64  | $399.54  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $414.64 - $424.40 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $343.42 | $571.71  | $647.80  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
