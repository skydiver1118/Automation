# PLTR Technical Analysis Sample

Generated: 2026-07-07 16:40:20
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (52/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [PLTR_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/PLTR_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $134.37            |
| SMA20             | $125.45            |
| SMA50             | $134.04            |
| SMA200            | $157.56            |
| RSI14             | 55.8               |
| MACD / Signal     | -2.59 / -4.53      |
| ADX14 / +DI / -DI | 18.7 / 30.5 / 24.3 |
| ATR14             | $6.85 (5.10%)      |
| 63-day range      | $106.37 - $163.70  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 134.37 vs 125.45             |
| Trend        | Close above SMA50                         | 8      | 8   | 134.37 vs 134.04             |
| Trend        | Close above SMA200                        | 0      | 8   | 134.37 vs 157.56             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 125.45 vs 134.04             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 134.04 vs 157.56             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -6.86                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 55.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | -2.59 vs -4.53               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.97               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -0.86%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.18x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 4138613963 vs 4007798468     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.98x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.7, +DI 30.5, -DI 24.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 143.03              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.10%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.92%                       |

## Support And Resistance

- Support levels: $106.87, $126.45, $133.56
- Resistance levels: $138.72, $143.03, $151.16, $156.51, $163.27

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $130.61 - $135.75 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $127.19 | $146.88  | $153.73  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $138.72 - $142.14 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $134.04 | $154.13  | $160.98  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
