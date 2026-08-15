# AVGO Technical Analysis Sample

Generated: 2026-07-07 16:40:11
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (36/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AVGO_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AVGO_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $370.78            |
| SMA20             | $381.04            |
| SMA50             | $406.96            |
| SMA200            | $360.42            |
| RSI14             | 43.9               |
| MACD / Signal     | -10.79 / -9.77     |
| ADX14 / +DI / -DI | 22.1 / 17.9 / 32.1 |
| ATR14             | $17.76 (4.79%)     |
| 63-day range      | $321.29 - $494.22  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 370.78 vs 381.04             |
| Trend        | Close above SMA50                         | 0      | 8   | 370.78 vs 406.96             |
| Trend        | Close above SMA200                        | 8      | 8   | 370.78 vs 360.42             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 381.04 vs 406.96             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 406.96 vs 360.42             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 9.18                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 43.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | -10.79 vs -9.77              |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.99               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -3.72%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.68x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 873318788 vs 898582729       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.80x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 22.1, +DI 17.9, -DI 32.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 405.36              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.79%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 24.98%                       |

## Support And Resistance

- Support levels: $291.86, $310.39, $325.29, $356.58, $369.74
- Resistance levels: $383.16, $411.55, $435.76, $494.22

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $406.96 - $415.84 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $380.32 | $460.24  | $495.75  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $360.87 - $374.18 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $351.99 | $403.04  | $420.80  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $383.16 - $392.04 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $369.74 | $423.31  | $441.16  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
