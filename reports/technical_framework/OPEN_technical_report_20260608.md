# OPEN Technical Analysis Sample

Generated: 2026-06-08 21:13:22
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (14/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [OPEN_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/OPEN_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $4.31              |
| SMA20             | $4.68              |
| SMA50             | $4.88              |
| SMA200            | $6.11              |
| RSI14             | 39.5               |
| MACD / Signal     | -0.06 / -0.04      |
| ADX14 / +DI / -DI | 16.7 / 20.8 / 24.8 |
| ATR14             | $0.39 (8.94%)      |
| 63-day range      | $4.12 - $6.00      |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 4.31 vs 4.68                 |
| Trend        | Close above SMA50                         | 0      | 8   | 4.31 vs 4.88                 |
| Trend        | Close above SMA200                        | 0      | 8   | 4.31 vs 6.11                 |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 4.68 vs 4.88                 |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 4.88 vs 6.11                 |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.17                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 39.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.06 vs -0.04               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.10              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -13.97%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.61x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 5867551643 vs 5848093967     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.87x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 16.7, +DI 20.8, -DI 24.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 5.36                |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.94%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 28.17%                       |

## Support And Resistance

- Support levels: $4.19
- Resistance levels: $5.01, $5.55, $6.00, $7.85

## Entry Plans

| Plan           | Entry zone    | Trigger                                                                                                      | Stop  | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ------------- | ------------------------------------------------------------------------------------------------------------ | ----- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $4.88 - $5.07 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $4.30 | $6.04    | $6.81    | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $3.99 - $4.28 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $3.80 | $5.01    | $5.30    | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $5.01 - $5.20 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $4.19 | $6.94    | $7.86    | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
