# PLTR Technical Analysis Sample

Generated: 2026-06-10 20:55:10
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (16/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [PLTR_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/PLTR_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $130.21            |
| SMA20             | $138.98            |
| SMA50             | $140.31            |
| SMA200            | $160.71            |
| RSI14             | 40.8               |
| MACD / Signal     | -1.05 / 0.22       |
| ADX14 / +DI / -DI | 14.8 / 22.3 / 33.5 |
| ATR14             | $6.89 (5.29%)      |
| 63-day range      | $122.68 - $163.70  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 130.21 vs 138.98             |
| Trend        | Close above SMA50                         | 0      | 8   | 130.21 vs 140.31             |
| Trend        | Close above SMA200                        | 0      | 8   | 130.21 vs 160.71             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 138.98 vs 140.31             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 140.31 vs 160.71             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -5.20                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 40.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | -1.05 vs 0.22                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -3.11              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -4.26%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.73x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 4260422087 vs 4313323124     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.28x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.8, +DI 22.3, -DI 33.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 155.84              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.29%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 20.46%                       |

## Support And Resistance

- Support levels: $125.56
- Resistance levels: $140.96, $151.16, $156.29, $163.34, $172.00

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $140.31 - $143.76 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $129.98 | $160.98  | $174.76  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $122.12 - $127.29 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $118.67 | $140.96  | $145.37  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $140.96 - $144.41 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $125.56 | $176.93  | $194.05  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
