# IBIT Technical Analysis Sample

Generated: 2026-05-31 20:07:55
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (33/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [IBIT_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/IBIT_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $41.63             |
| SMA20             | $44.41             |
| SMA50             | $42.44             |
| SMA200            | $51.21             |
| RSI14             | 38.8               |
| MACD / Signal     | -0.27 / 0.26       |
| ADX14 / +DI / -DI | 11.9 / 24.4 / 30.7 |
| ATR14             | $1.15 (2.77%)      |
| 63-day range      | $37.13 - $46.56    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 41.63 vs 44.41               |
| Trend        | Close above SMA50                         | 0      | 8   | 41.63 vs 42.44               |
| Trend        | Close above SMA200                        | 0      | 8   | 41.63 vs 51.21               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 44.41 vs 42.44               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 42.44 vs 51.21               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 2.04                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 38.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.27 vs 0.26                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.17              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -3.90%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.02x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | -909601900 vs -899200805     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.06x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 11.9, +DI 24.4, -DI 30.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 47.50               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.77%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.59%                       |

## Support And Resistance

- Support levels: $35.45, $37.09, $39.00, $41.17
- Resistance levels: $42.26, $44.24, $45.08, $46.56, $47.50

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $44.41 - $44.98 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $42.68 | $47.86   | $50.17   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $40.59 - $41.45 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $40.01 | $43.32   | $44.48   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $42.26 - $42.84 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $41.17 | $45.31   | $46.70   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
