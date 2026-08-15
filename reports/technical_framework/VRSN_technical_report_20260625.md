# VRSN Technical Analysis Sample

Generated: 2026-06-26 06:53:33
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (20/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [VRSN_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/VRSN_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $250.85            |
| SMA20             | $277.52            |
| SMA50             | $280.98            |
| SMA200            | $256.81            |
| RSI14             | 30.0               |
| MACD / Signal     | -9.59 / -5.22      |
| ADX14 / +DI / -DI | 32.6 / 12.7 / 33.8 |
| ATR14             | $8.79 (3.51%)      |
| 63-day range      | $244.74 - $312.48  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 250.85 vs 277.52             |
| Trend        | Close above SMA50                         | 0      | 8   | 250.85 vs 280.98             |
| Trend        | Close above SMA200                        | 0      | 8   | 250.85 vs 256.81             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 277.52 vs 280.98             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 280.98 vs 256.81             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 9.44                         |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 30.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | -9.59 vs -5.22               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.44              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -15.15%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.82x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 20607300 vs 24145920         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.55x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 32.6, +DI 12.7, -DI 33.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 312.58              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.51%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 19.72%                       |

## Support And Resistance

- Support levels: $209.34, $234.90, $243.54
- Resistance levels: $253.61, $279.87, $302.97, $312.51

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $280.98 - $285.38 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $267.79 | $307.36  | $324.95  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $239.14 - $245.74 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $234.75 | $260.03  | $268.82  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $253.61 - $258.01 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $243.54 | $280.34  | $292.61  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
