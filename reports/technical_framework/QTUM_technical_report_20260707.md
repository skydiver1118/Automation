# QTUM Technical Analysis Sample

Generated: 2026-07-07 16:40:22
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (37/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QTUM_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QTUM_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $151.44            |
| SMA20             | $160.00            |
| SMA50             | $152.06            |
| SMA200            | $122.11            |
| RSI14             | 44.3               |
| MACD / Signal     | 1.08 / 2.93        |
| ADX14 / +DI / -DI | 16.4 / 18.7 / 31.6 |
| ATR14             | $6.08 (4.01%)      |
| 63-day range      | $108.11 - $169.72  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 151.44 vs 160.00             |
| Trend        | Close above SMA50                         | 0      | 8   | 151.44 vs 152.06             |
| Trend        | Close above SMA200                        | 8      | 8   | 151.44 vs 122.11             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 160.00 vs 152.06             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 152.06 vs 122.11             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 17.16                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 44.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | 1.08 vs 2.93                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.49              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -0.71%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.66x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 20880450 vs 21620742         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.82x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 16.4, +DI 18.7, -DI 31.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 170.10              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.01%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.77%                       |

## Support And Resistance

- Support levels: $107.94, $114.22, $127.31, $137.43, $149.69
- Resistance levels: $168.96

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $160.00 - $163.04 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $150.88 | $178.23  | $190.39  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $146.65 - $151.21 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $143.61 | $168.96  | $167.17  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $168.96 - $172.00 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $149.69 | $212.06  | $232.85  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
