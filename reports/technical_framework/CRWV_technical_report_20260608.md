# CRWV Technical Analysis Sample

Generated: 2026-06-08 21:13:17
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (35/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWV_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWV_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $102.37            |
| SMA20             | $108.28            |
| SMA50             | $107.17            |
| SMA200            | $99.98             |
| RSI14             | 44.9               |
| MACD / Signal     | -0.65 / 0.33       |
| ADX14 / +DI / -DI | 13.4 / 25.7 / 31.6 |
| ATR14             | $8.97 (8.77%)      |
| 63-day range      | $67.15 - $138.25   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 102.37 vs 108.28             |
| Trend        | Close above SMA50                         | 0      | 8   | 102.37 vs 107.17             |
| Trend        | Close above SMA200                        | 8      | 8   | 102.37 vs 99.98              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 108.28 vs 107.17             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 107.17 vs 99.98              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.37                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 44.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.65 vs 0.33                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.29              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -10.32%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.81x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 495576916 vs 508744756       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.90x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 13.4, +DI 25.7, -DI 31.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 120.93              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.77%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 25.95%                       |

## Support And Resistance

- Support levels: $68.27, $77.24, $85.78, $97.34
- Resistance levels: $114.45, $122.68, $132.15, $138.25

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $108.28 - $112.77 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $94.82 | $135.20  | $153.15  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $92.85 - $99.59   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $88.37 | $114.45  | $123.14  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $114.45 - $118.94 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $97.34 | $155.40  | $174.75  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
