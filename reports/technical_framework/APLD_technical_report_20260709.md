# APLD Technical Analysis Sample

Generated: 2026-07-09 16:40:48
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (16/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APLD_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APLD_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $32.29             |
| SMA20             | $39.61             |
| SMA50             | $41.16             |
| SMA200            | $32.52             |
| RSI14             | 34.7               |
| MACD / Signal     | -2.81 / -1.57      |
| ADX14 / +DI / -DI | 24.6 / 14.4 / 30.9 |
| ATR14             | $3.51 (10.88%)     |
| 63-day range      | $25.07 - $50.72    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 32.29 vs 39.61               |
| Trend        | Close above SMA50                         | 0      | 8   | 32.29 vs 41.16               |
| Trend        | Close above SMA200                        | 0      | 8   | 32.29 vs 32.52               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 39.61 vs 41.16               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 41.16 vs 32.52               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 4.33                         |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 34.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | -2.81 vs -1.57               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.05              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -22.95%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.82x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1517244428 vs 1582013531     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.58x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 24.6, +DI 14.4, -DI 30.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 50.52               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.88%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 36.34%                       |

## Support And Resistance

- Support levels: $20.00, $24.78, $29.25, $32.32
- Resistance levels: $39.34, $42.27, $48.34, $50.66

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $41.16 - $42.91 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $35.89 | $51.70   | $58.72   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $27.50 - $30.13 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $25.74 | $39.34   | $39.35   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $39.34 - $41.10 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $29.25 | $62.15   | $73.12   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
