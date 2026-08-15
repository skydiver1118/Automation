# APLD Technical Analysis Sample

Generated: 2026-07-07 16:40:36
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (16/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APLD_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APLD_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $30.71             |
| SMA20             | $40.56             |
| SMA50             | $41.26             |
| SMA200            | $32.40             |
| RSI14             | 29.9               |
| MACD / Signal     | -2.39 / -0.91      |
| ADX14 / +DI / -DI | 22.0 / 12.6 / 33.2 |
| ATR14             | $3.73 (12.14%)     |
| 63-day range      | $24.38 - $50.72    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 30.71 vs 40.56               |
| Trend        | Close above SMA50                         | 0      | 8   | 30.71 vs 41.26               |
| Trend        | Close above SMA200                        | 0      | 8   | 30.71 vs 32.40               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 40.56 vs 41.26               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 41.26 vs 32.40               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 5.09                         |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 29.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | -2.39 vs -0.91               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.54              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -22.49%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.72x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1473681715 vs 1583364606     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.57x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 22.0, +DI 12.6, -DI 33.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 50.12               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 12.14%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 39.46%                       |

## Support And Resistance

- Support levels: $20.00, $24.55, $29.59
- Resistance levels: $31.80, $39.34, $42.27, $49.27

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $41.26 - $43.12 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $35.66 | $52.44   | $59.90   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $27.72 - $30.52 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $25.86 | $36.58   | $40.31   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $31.80 - $33.66 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $29.59 | $40.19   | $43.92   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
