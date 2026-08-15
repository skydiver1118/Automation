# CRWV Technical Analysis Sample

Generated: 2026-07-07 16:40:14
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (19/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWV_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWV_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $83.53             |
| SMA20             | $99.77             |
| SMA50             | $107.31            |
| SMA200            | $99.82             |
| RSI14             | 36.6               |
| MACD / Signal     | -5.82 / -3.48      |
| ADX14 / +DI / -DI | 17.2 / 16.3 / 34.2 |
| ATR14             | $8.44 (10.10%)     |
| 63-day range      | $79.46 - $138.25   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 83.53 vs 99.77               |
| Trend        | Close above SMA50                         | 0      | 8   | 83.53 vs 107.31              |
| Trend        | Close above SMA200                        | 0      | 8   | 83.53 vs 99.82               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 99.77 vs 107.31              |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 107.31 vs 99.82              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.57                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 36.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | -5.82 vs -3.48               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.09              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -16.79%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.75x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 369114324 vs 488270846       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.65x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.2, +DI 16.3, -DI 34.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 120.89              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.10%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 39.58%                       |

## Support And Resistance

- Support levels: $71.19, $78.78
- Resistance levels: $87.18, $101.26, $114.45, $122.40, $132.15

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $107.31 - $111.53 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $94.65 | $132.63  | $149.50  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $74.56 - $80.89   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $70.34 | $94.61   | $103.05  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $87.18 - $91.40   | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $78.78 | $110.32  | $120.83  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
