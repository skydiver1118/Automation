# IREN Technical Analysis Sample

Generated: 2026-07-08 16:40:35
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (24/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [IREN_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/IREN_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $43.01             |
| SMA20             | $50.87             |
| SMA50             | $53.99             |
| SMA200            | $49.19             |
| RSI14             | 40.5               |
| MACD / Signal     | -4.05 / -2.73      |
| ADX14 / +DI / -DI | 27.4 / 12.4 / 31.8 |
| ATR14             | $4.84 (11.26%)     |
| 63-day range      | $35.25 - $70.71    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 43.01 vs 50.87               |
| Trend        | Close above SMA50                         | 0      | 8   | 43.01 vs 53.99               |
| Trend        | Close above SMA200                        | 0      | 8   | 43.01 vs 49.19               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 50.87 vs 53.99               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 53.99 vs 49.19               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 3.67                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 40.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | -4.05 vs -2.73               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.43               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -27.34%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.84x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 462495695 vs 630886570       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.50x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 27.4, +DI 12.4, -DI 31.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 65.29               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 11.26%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 39.18%                       |

## Support And Resistance

- Support levels: $30.76, $37.36
- Resistance levels: $45.39, $54.14, $58.75, $64.17, $69.85

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $53.99 - $56.41 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $46.73 | $68.52   | $78.21   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $34.94 - $38.57 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $32.52 | $46.44   | $51.29   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $45.39 - $47.81 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $37.36 | $65.07   | $74.30   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
