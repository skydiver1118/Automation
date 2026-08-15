# URA Technical Analysis Sample

Generated: 2026-06-08 21:13:32
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (23/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [URA_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/URA_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $45.92             |
| SMA20             | $50.37             |
| SMA50             | $52.02             |
| SMA200            | $48.82             |
| RSI14             | 37.6               |
| MACD / Signal     | -1.32 / -0.92      |
| ADX14 / +DI / -DI | 14.6 / 16.6 / 27.6 |
| ATR14             | $2.44 (5.31%)      |
| 63-day range      | $44.76 - $58.97    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 45.92 vs 50.37               |
| Trend        | Close above SMA50                         | 0      | 8   | 45.92 vs 52.02               |
| Trend        | Close above SMA200                        | 0      | 8   | 45.92 vs 48.82               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 50.37 vs 52.02               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 52.02 vs 48.82               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.04                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 37.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | -1.32 vs -0.92               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.30              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -16.78%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.70x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 150879313 vs 153529991       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.66x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.6, +DI 16.6, -DI 27.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 56.07               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.31%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 22.13%                       |

## Support And Resistance

- Support levels: $40.69, $42.54, $44.99
- Resistance levels: $47.08, $50.49, $53.34, $55.93, $58.67

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $52.02 - $53.24 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $48.36 | $59.34   | $64.21   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $43.77 - $45.60 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $42.55 | $49.56   | $52.00   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $47.08 - $48.30 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $44.99 | $53.10   | $55.81   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
