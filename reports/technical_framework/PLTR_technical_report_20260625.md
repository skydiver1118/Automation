# PLTR Technical Analysis Sample

Generated: 2026-06-26 06:53:20
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (11/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [PLTR_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/PLTR_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $107.27            |
| SMA20             | $133.70            |
| SMA50             | $137.04            |
| SMA200            | $159.09            |
| RSI14             | 27.4               |
| MACD / Signal     | -6.64 / -3.85      |
| ADX14 / +DI / -DI | 21.2 / 14.9 / 40.5 |
| ATR14             | $6.53 (6.09%)      |
| 63-day range      | $106.37 - $163.70  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 107.27 vs 133.70             |
| Trend        | Close above SMA50                         | 0      | 8   | 107.27 vs 137.04             |
| Trend        | Close above SMA200                        | 0      | 8   | 107.27 vs 159.09             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 133.70 vs 137.04             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 137.04 vs 159.09             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.91                        |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 27.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | -6.64 vs -3.85               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.78              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -19.05%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.38x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 3988267500 vs 4282437720     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.41x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 21.2, +DI 14.9, -DI 40.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 160.92              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.09%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 34.47%                       |

## Support And Resistance

- Support levels: $106.41
- Resistance levels: $136.10, $140.96, $151.16, $156.51, $162.99

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $137.04 - $140.31 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $127.24 | $156.64  | $169.70  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $103.14 - $108.04 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $99.88  | $136.10  | $125.19  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $136.10 - $139.37 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $106.41 | $200.38  | $231.71  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
