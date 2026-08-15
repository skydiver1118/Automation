# TSLA Technical Analysis Sample

Generated: 2026-06-05 16:40:51
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (28/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSLA_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSLA_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $391.00            |
| SMA20             | $425.87            |
| SMA50             | $395.29            |
| SMA200            | $414.14            |
| RSI14             | 40.4               |
| MACD / Signal     | 4.14 / 8.61        |
| ADX14 / +DI / -DI | 17.5 / 23.4 / 31.4 |
| ATR14             | $16.31 (4.17%)     |
| 63-day range      | $337.24 - $453.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 391.00 vs 425.87             |
| Trend        | Close above SMA50                         | 0      | 8   | 391.00 vs 395.29             |
| Trend        | Close above SMA200                        | 0      | 8   | 391.00 vs 414.14             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 425.87 vs 395.29             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 395.29 vs 414.14             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 12.49                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 40.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | 4.14 vs 8.61                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -5.16              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -5.05%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.22x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 3735600620 vs 3811209731     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.90x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.5, +DI 23.4, -DI 31.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 454.89              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.17%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.76%                       |

## Support And Resistance

- Support levels: $337.24, $352.14, $364.24, $390.30
- Resistance levels: $396.23, $413.65, $440.98, $454.38, $498.83

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $425.87 - $434.03 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $401.41 | $474.80  | $507.42  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $382.14 - $394.38 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $373.99 | $420.88  | $437.19  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $396.23 - $404.39 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $390.30 | $432.93  | $449.24  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
