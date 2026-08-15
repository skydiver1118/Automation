# CRM Technical Analysis Sample

Generated: 2026-07-07 16:40:35
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (34/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRM_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRM_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $169.52            |
| SMA20             | $161.84            |
| SMA50             | $173.53            |
| SMA200            | $210.51            |
| RSI14             | 53.4               |
| MACD / Signal     | -3.38 / -5.31      |
| ADX14 / +DI / -DI | 15.8 / 30.3 / 25.1 |
| ATR14             | $6.92 (4.08%)      |
| 63-day range      | $146.32 - $210.80  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 169.52 vs 161.84             |
| Trend        | Close above SMA50                         | 0      | 8   | 169.52 vs 173.53             |
| Trend        | Close above SMA200                        | 0      | 8   | 169.52 vs 210.51             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 161.84 vs 173.53             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 173.53 vs 210.51             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -7.23                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | -3.38 vs -5.31               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.84               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -8.46%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.66x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | -201627264 vs -159154843     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.32x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.8, +DI 30.3, -DI 25.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 179.14              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.08%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 19.58%                       |

## Support And Resistance

- Support levels: $145.73, $163.37
- Resistance levels: $172.38, $179.14, $187.34, $193.06, $202.41

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $173.53 - $176.98 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $163.15 | $194.28  | $208.12  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $161.18 - $166.37 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $157.72 | $177.61  | $184.53  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $172.38 - $175.84 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $164.64 | $193.06  | $202.53  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
