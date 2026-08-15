# IREN Technical Analysis Sample

Generated: 2026-07-07 16:40:35
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (24/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [IREN_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/IREN_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $39.81             |
| SMA20             | $51.68             |
| SMA50             | $54.14             |
| SMA200            | $49.16             |
| RSI14             | 35.5               |
| MACD / Signal     | -4.06 / -2.39      |
| ADX14 / +DI / -DI | 26.2 / 12.5 / 33.4 |
| ATR14             | $4.97 (12.47%)     |
| 63-day range      | $33.19 - $70.71    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 39.81 vs 51.68               |
| Trend        | Close above SMA50                         | 0      | 8   | 39.81 vs 54.14               |
| Trend        | Close above SMA200                        | 0      | 8   | 39.81 vs 49.16               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 51.68 vs 54.14               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 54.14 vs 49.16               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 4.26                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 35.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | -4.06 vs -2.39               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.11               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -26.74%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.96x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 410834532 vs 626499557       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.39x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 26.2, +DI 12.5, -DI 33.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 66.06               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 12.47%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 43.69%                       |

## Support And Resistance

- Support levels: $31.97, $37.79
- Resistance levels: $45.97, $54.14, $58.75, $64.32, $69.85

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $54.14 - $56.63 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $46.70 | $69.04   | $78.97   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $35.30 - $39.03 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $32.82 | $47.10   | $52.06   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $45.97 - $48.45 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $37.79 | $66.06   | $75.48   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
