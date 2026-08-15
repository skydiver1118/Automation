# IREN Technical Analysis Sample

Generated: 2026-06-26 06:53:39
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (25/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [IREN_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/IREN_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $47.74             |
| SMA20             | $58.51             |
| SMA50             | $54.83             |
| SMA200            | $48.85             |
| RSI14             | 39.3               |
| MACD / Signal     | -0.78 / 0.70       |
| ADX14 / +DI / -DI | 16.5 / 16.5 / 29.4 |
| ATR14             | $5.23 (10.96%)     |
| 63-day range      | $30.76 - $70.71    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 47.74 vs 58.51               |
| Trend        | Close above SMA50                         | 0      | 8   | 47.74 vs 54.83               |
| Trend        | Close above SMA200                        | 0      | 8   | 47.74 vs 48.85               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 58.51 vs 54.83               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 54.83 vs 48.85               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 7.91                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 39.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.78 vs 0.70                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.84              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -29.63%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.81x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 606225300 vs 737042565       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.60x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 16.5, +DI 16.5, -DI 29.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 69.05               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.96%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 32.48%                       |

## Support And Resistance

- Support levels: $30.76, $37.79, $43.92
- Resistance levels: $48.30, $54.14, $58.75, $64.12, $69.86

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $58.51 - $61.12 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $50.66 | $74.21   | $84.68   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $41.31 - $45.23 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $38.69 | $53.74   | $58.97   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $48.30 - $50.92 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $43.92 | $60.98   | $66.66   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
