# MSFT Technical Analysis Sample

Generated: 2026-07-07 16:40:32
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (44/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MSFT_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MSFT_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $388.84            |
| SMA20             | $383.50            |
| SMA50             | $405.79            |
| SMA200            | $442.60            |
| RSI14             | 49.2               |
| MACD / Signal     | -7.35 / -9.78      |
| ADX14 / +DI / -DI | 19.4 / 27.8 / 27.8 |
| ATR14             | $12.51 (3.22%)     |
| 63-day range      | $349.20 - $466.32  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 388.84 vs 383.50             |
| Trend        | Close above SMA50                         | 0      | 8   | 388.84 vs 405.79             |
| Trend        | Close above SMA200                        | 0      | 8   | 388.84 vs 442.60             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 383.50 vs 405.79             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 405.79 vs 442.60             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -1.88                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | -7.35 vs -9.78               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 5.64               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -6.68%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.59x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | -45765111 vs -174094861      |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.20x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 19.4, +DI 27.8, -DI 27.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 412.68              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.22%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 16.62%                       |

## Support And Resistance

- Support levels: $352.06, $387.02
- Resistance levels: $395.57, $412.15, $428.48, $466.32, $484.56

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $405.79 - $412.05 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $387.03 | $443.32  | $468.34  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $381.09 - $390.48 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $374.84 | $410.81  | $423.32  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $395.57 - $401.82 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $387.35 | $423.72  | $436.23  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
