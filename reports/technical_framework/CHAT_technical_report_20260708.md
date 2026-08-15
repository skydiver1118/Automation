# CHAT Technical Analysis Sample

Generated: 2026-07-08 16:40:12
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (57/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CHAT_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CHAT_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $89.81             |
| SMA20             | $94.51             |
| SMA50             | $90.78             |
| SMA200            | $69.58             |
| RSI14             | 46.0               |
| MACD / Signal     | -0.27 / 1.16       |
| ADX14 / +DI / -DI | 17.7 / 22.4 / 37.2 |
| ATR14             | $4.43 (4.93%)      |
| 63-day range      | $66.85 - $105.20   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 89.81 vs 94.51               |
| Trend        | Close above SMA50                         | 0      | 8   | 89.81 vs 90.78               |
| Trend        | Close above SMA200                        | 8      | 8   | 89.81 vs 69.58               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 94.51 vs 90.78               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 90.78 vs 69.58               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 9.87                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.27 vs 1.16                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.84              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -4.05%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.15x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 19841258 vs 19781318         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.16x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.7, +DI 22.4, -DI 37.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 103.59              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.93%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 14.63%                       |

## Support And Resistance

- Support levels: $62.69, $66.85, $74.70, $81.50, $85.78
- Resistance levels: $89.07, $104.68

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $94.51 - $96.72   | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $87.86 | $107.79  | $116.65  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $83.57 - $86.89   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $81.35 | $104.68  | $98.52   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $104.68 - $106.90 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $85.78 | $145.80  | $165.80  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
