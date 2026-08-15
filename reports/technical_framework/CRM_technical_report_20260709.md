# CRM Technical Analysis Sample

Generated: 2026-07-09 16:40:46
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (34/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRM_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRM_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $162.50            |
| SMA20             | $160.45            |
| SMA50             | $172.96            |
| SMA200            | $209.71            |
| RSI14             | 46.2               |
| MACD / Signal     | -2.66 / -4.38      |
| ADX14 / +DI / -DI | 14.7 / 25.8 / 32.6 |
| ATR14             | $7.00 (4.31%)      |
| 63-day range      | $146.32 - $210.80  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 162.50 vs 160.45             |
| Trend        | Close above SMA50                         | 0      | 8   | 162.50 vs 172.96             |
| Trend        | Close above SMA200                        | 0      | 8   | 162.50 vs 209.71             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 160.45 vs 172.96             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 172.96 vs 209.71             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -7.68                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | -2.66 vs -4.38               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.41               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -7.09%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.69x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | -222813895 vs -178427045     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.33x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.7, +DI 25.8, -DI 32.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 173.63              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.31%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 22.91%                       |

## Support And Resistance

- Support levels: $146.63, $158.46, $163.87
- Resistance levels: $173.70, $188.27, $193.06, $202.41, $210.80

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $172.96 - $176.46 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $162.46 | $193.96  | $207.96  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $156.95 - $162.20 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $153.45 | $173.70  | $180.57  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $173.70 - $177.20 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $160.45 | $205.45  | $220.45  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
