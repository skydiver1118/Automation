# IREN Technical Analysis Sample

Generated: 2026-06-28 17:42:42
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (30/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [IREN_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/IREN_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $47.21             |
| SMA20             | $57.67             |
| SMA50             | $54.80             |
| SMA200            | $48.93             |
| RSI14             | 38.8               |
| MACD / Signal     | -1.37 / 0.29       |
| ADX14 / +DI / -DI | 17.6 / 15.8 / 30.9 |
| ATR14             | $5.10 (10.80%)     |
| 63-day range      | $30.76 - $70.71    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 47.21 vs 57.67               |
| Trend        | Close above SMA50                         | 0      | 8   | 47.21 vs 54.80               |
| Trend        | Close above SMA200                        | 0      | 8   | 47.21 vs 48.93               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 57.67 vs 54.80               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 54.80 vs 48.93               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 7.46                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 38.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | -1.37 vs 0.29                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.17              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -26.29%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.13x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 569193600 vs 737820490       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.60x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.6, +DI 15.8, -DI 30.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 69.00               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.80%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 33.23%                       |

## Support And Resistance

- Support levels: $30.76, $37.79, $44.51
- Resistance levels: $48.30, $54.14, $58.75, $64.12, $69.85

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $57.67 - $60.21 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $50.02 | $72.96   | $83.16   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $41.96 - $45.79 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $39.41 | $54.07   | $59.17   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $48.30 - $50.85 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $44.51 | $59.77   | $64.87   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
