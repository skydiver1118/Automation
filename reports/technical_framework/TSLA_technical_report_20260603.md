# TSLA Technical Analysis Sample

Generated: 2026-06-03 19:37:20
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (64/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSLA_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSLA_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $423.70            |
| SMA20             | $425.93            |
| SMA50             | $394.48            |
| SMA200            | $413.42            |
| RSI14             | 53.6               |
| MACD / Signal     | 8.49 / 10.32       |
| ADX14 / +DI / -DI | 18.3 / 29.1 / 23.4 |
| ATR14             | $15.22 (3.59%)     |
| 63-day range      | $337.24 - $453.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 423.70 vs 425.93             |
| Trend        | Close above SMA50                         | 8      | 8   | 423.70 vs 394.48             |
| Trend        | Close above SMA200                        | 8      | 8   | 423.70 vs 413.42             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 425.93 vs 394.48             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 394.48 vs 413.42             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.36                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | 8.49 vs 10.32                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.42              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 8.82%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.86x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 3960348162 vs 3931129983     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.45x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.3, +DI 29.1, -DI 23.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 453.69              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.59%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 6.55%                        |

## Support And Resistance

- Support levels: $352.14, $364.24, $390.57, $400.51, $420.54
- Resistance levels: $436.35, $453.14, $498.83

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $412.93 - $424.35 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $379.26 | $497.41  | $536.79  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $436.35 - $443.96 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $420.54 | $479.38  | $498.99  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
