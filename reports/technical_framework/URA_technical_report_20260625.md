# URA Technical Analysis Sample

Generated: 2026-06-26 06:53:32
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (17/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [URA_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/URA_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $43.92             |
| SMA20             | $47.30             |
| SMA50             | $51.12             |
| SMA200            | $49.26             |
| RSI14             | 38.4               |
| MACD / Signal     | -1.53 / -1.47      |
| ADX14 / +DI / -DI | 17.3 / 16.7 / 28.0 |
| ATR14             | $2.23 (5.08%)      |
| 63-day range      | $42.23 - $58.97    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 43.92 vs 47.30               |
| Trend        | Close above SMA50                         | 0      | 8   | 43.92 vs 51.12               |
| Trend        | Close above SMA200                        | 0      | 8   | 43.92 vs 49.26               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 47.30 vs 51.12               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 51.12 vs 49.26               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.67                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 38.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | -1.53 vs -1.47               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.13              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -12.44%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.68x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 137144800 vs 148164950       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.65x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.3, +DI 16.7, -DI 28.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 53.15               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.08%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 25.52%                       |

## Support And Resistance

- Support levels: $42.11, $44.23
- Resistance levels: $45.14, $50.13, $53.33, $55.06, $56.67

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $51.12 - $52.24 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $47.77 | $57.82   | $62.29   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $41.00 - $42.67 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $39.88 | $46.30   | $48.53   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $45.14 - $46.26 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $42.11 | $52.88   | $56.47   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
