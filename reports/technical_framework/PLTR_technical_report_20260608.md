# PLTR Technical Analysis Sample

Generated: 2026-06-08 21:13:23
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (26/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [PLTR_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/PLTR_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $136.47            |
| SMA20             | $139.51            |
| SMA50             | $140.68            |
| SMA200            | $160.98            |
| RSI14             | 45.7               |
| MACD / Signal     | 0.53 / 0.74        |
| ADX14 / +DI / -DI | 14.0 / 25.9 / 30.0 |
| ATR14             | $6.89 (5.05%)      |
| 63-day range      | $122.68 - $163.70  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 136.47 vs 139.51             |
| Trend        | Close above SMA50                         | 0      | 8   | 136.47 vs 140.68             |
| Trend        | Close above SMA200                        | 0      | 8   | 136.47 vs 160.98             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 139.51 vs 140.68             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 140.68 vs 160.98             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -5.02                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 45.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | 0.53 vs 0.74                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -3.01              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -0.97%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.67x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 4358830604 vs 4340788920     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.19x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.0, +DI 25.9, -DI 30.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 155.62              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.05%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 16.63%                       |

## Support And Resistance

- Support levels: $125.49, $133.56
- Resistance levels: $140.96, $151.16, $156.22, $163.34, $172.00

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $140.68 - $144.12 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $130.35 | $161.33  | $175.11  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $130.11 - $135.28 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $126.67 | $146.47  | $153.35  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $140.96 - $144.41 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $133.56 | $160.94  | $170.07  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
