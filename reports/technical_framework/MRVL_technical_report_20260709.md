# MRVL Technical Analysis Sample

Generated: 2026-07-09 16:40:44
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (56/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MRVL_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MRVL_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $243.27            |
| SMA20             | $273.01            |
| SMA50             | $229.82            |
| SMA200            | $125.91            |
| RSI14             | 47.0               |
| MACD / Signal     | 1.49 / 11.09       |
| ADX14 / +DI / -DI | 24.5 / 23.1 / 27.5 |
| ATR14             | $25.11 (10.32%)    |
| 63-day range      | $117.77 - $329.88  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 243.27 vs 273.01             |
| Trend        | Close above SMA50                         | 8      | 8   | 243.27 vs 229.82             |
| Trend        | Close above SMA200                        | 8      | 8   | 243.27 vs 125.91             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 273.01 vs 229.82             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 229.82 vs 125.91             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 57.22                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 47.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | 1.49 vs 11.09                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -4.11              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -8.85%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.41x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1161863388 vs 1110613684     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.55x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 24.5, +DI 23.1, -DI 27.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 321.68              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.32%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 26.26%                       |

## Support And Resistance

- Support levels: $79.49, $123.10, $155.89, $225.70
- Resistance levels: $300.00, $327.10

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $217.26 - $236.10 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $204.71 | $300.00  | $302.02  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $300.00 - $312.56 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $229.82 | $459.20  | $535.66  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
