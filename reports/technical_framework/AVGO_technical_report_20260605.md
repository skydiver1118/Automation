# AVGO Technical Analysis Sample

Generated: 2026-06-05 16:40:31
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (42/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AVGO_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AVGO_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $385.73            |
| SMA20             | $429.02            |
| SMA50             | $398.41            |
| SMA200            | $354.92            |
| RSI14             | 39.9               |
| MACD / Signal     | 8.75 / 12.37       |
| ADX14 / +DI / -DI | 25.9 / 26.9 / 33.3 |
| ATR14             | $22.62 (5.86%)     |
| 63-day range      | $289.96 - $495.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 385.73 vs 429.02             |
| Trend        | Close above SMA50                         | 0      | 8   | 385.73 vs 398.41             |
| Trend        | Close above SMA200                        | 8      | 8   | 385.73 vs 354.92             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 429.02 vs 398.41             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 398.41 vs 354.92             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 41.94                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 39.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | 8.75 vs 12.37                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.70              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -6.50%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.81x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1117425755 vs 1210743413     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.55x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 25.9, +DI 26.9, -DI 33.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 474.82              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.86%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 22.07%                       |

## Support And Resistance

- Support levels: $291.53, $312.73, $329.81, $384.62
- Resistance levels: $412.95, $436.45, $474.82, $495.00

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $429.02 - $440.33 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $395.09 | $496.87  | $542.11  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $373.31 - $390.28 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $362.00 | $427.03  | $449.65  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $412.95 - $424.26 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $384.62 | $486.58  | $520.56  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
