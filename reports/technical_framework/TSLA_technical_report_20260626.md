# TSLA Technical Analysis Sample

Generated: 2026-06-28 17:42:35
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (22/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSLA_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSLA_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $379.71            |
| SMA20             | $401.55            |
| SMA50             | $404.76            |
| SMA200            | $417.96            |
| RSI14             | 41.2               |
| MACD / Signal     | -7.98 / -4.37      |
| ADX14 / +DI / -DI | 17.9 / 19.9 / 27.7 |
| ATR14             | $16.78 (4.42%)     |
| 63-day range      | $337.24 - $453.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 379.71 vs 401.55             |
| Trend        | Close above SMA50                         | 0      | 8   | 379.71 vs 404.76             |
| Trend        | Close above SMA200                        | 0      | 8   | 379.71 vs 417.96             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 401.55 vs 404.76             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 404.76 vs 417.96             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 13.83                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 41.2                   |
| Momentum     | MACD above signal                         | 0      | 7   | -7.98 vs -4.37               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.26              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -14.11%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.13x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 3614496700 vs 3615099015     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.81x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.9, +DI 19.9, -DI 27.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 436.06              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.42%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 16.25%                       |

## Support And Resistance

- Support levels: $337.24, $352.14, $366.03
- Resistance levels: $383.14, $396.23, $414.23, $439.77, $453.38

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $404.76 - $413.16 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $379.59 | $455.12  | $488.68  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $357.64 - $370.23 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $349.25 | $397.50  | $414.28  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $383.14 - $391.53 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $366.03 | $429.95  | $451.25  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
