# IREN Technical Analysis Sample

Generated: 2026-07-06 16:40:36
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (24/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [IREN_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/IREN_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $43.91             |
| SMA20             | $52.41             |
| SMA50             | $54.39             |
| SMA200            | $49.15             |
| RSI14             | 39.4               |
| MACD / Signal     | -3.68 / -1.98      |
| ADX14 / +DI / -DI | 24.6 / 13.4 / 31.9 |
| ATR14             | $4.98 (11.35%)     |
| 63-day range      | $33.19 - $70.71    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 43.91 vs 52.41               |
| Trend        | Close above SMA50                         | 0      | 8   | 43.91 vs 54.39               |
| Trend        | Close above SMA200                        | 0      | 8   | 43.91 vs 49.15               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 52.41 vs 54.39               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 54.39 vs 49.15               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 4.76                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 39.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | -3.68 vs -1.98               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.04              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -29.02%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.25x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 449396792 vs 641538425       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.50x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 24.6, +DI 13.4, -DI 31.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 65.69               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 11.35%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 37.90%                       |

## Support And Resistance

- Support levels: $31.97, $38.05, $43.92
- Resistance levels: $45.97, $54.14, $58.75, $64.25, $69.85

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $54.39 - $56.88 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $46.91 | $69.34   | $79.31   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $35.56 - $39.30 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $33.06 | $47.40   | $52.38   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $45.97 - $48.46 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $38.05 | $65.55   | $74.71   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
