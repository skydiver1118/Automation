# QTUM Technical Analysis Sample

Generated: 2026-07-06 16:40:22
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (60/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QTUM_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QTUM_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $156.94            |
| SMA20             | $160.05            |
| SMA50             | $151.62            |
| SMA200            | $121.85            |
| RSI14             | 49.2               |
| MACD / Signal     | 1.89 / 3.39        |
| ADX14 / +DI / -DI | 15.6 / 20.5 / 26.3 |
| ATR14             | $5.98 (3.81%)      |
| 63-day range      | $108.11 - $169.72  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 156.94 vs 160.05             |
| Trend        | Close above SMA50                         | 8      | 8   | 156.94 vs 151.62             |
| Trend        | Close above SMA200                        | 8      | 8   | 156.94 vs 121.85             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 160.05 vs 151.62             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 151.62 vs 121.85             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 17.54                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.2                   |
| Momentum     | MACD above signal                         | 0      | 7   | 1.89 vs 3.39                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.07              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -5.58%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.40x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 21396262 vs 21643423         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.01x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.6, +DI 20.5, -DI 26.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 169.97              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.81%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 7.53%                        |

## Support And Resistance

- Support levels: $114.44, $127.31, $137.43, $149.67, $153.61
- Resistance levels: $168.94

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $150.62 - $155.10 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $145.64 | $168.94  | $174.52  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $168.94 - $171.93 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $153.61 | $204.09  | $220.92  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
