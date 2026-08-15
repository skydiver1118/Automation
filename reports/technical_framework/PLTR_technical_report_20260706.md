# PLTR Technical Analysis Sample

Generated: 2026-07-06 16:40:20
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (39/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [PLTR_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/PLTR_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $132.54            |
| SMA20             | $125.51            |
| SMA50             | $134.18            |
| SMA200            | $157.73            |
| RSI14             | 54.3               |
| MACD / Signal     | -3.69 / -5.02      |
| ADX14 / +DI / -DI | 19.3 / 27.7 / 26.3 |
| ATR14             | $6.80 (5.13%)      |
| 63-day range      | $106.37 - $163.70  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 132.54 vs 125.51             |
| Trend        | Close above SMA50                         | 0      | 8   | 132.54 vs 134.18             |
| Trend        | Close above SMA200                        | 0      | 8   | 132.54 vs 157.73             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 125.51 vs 134.18             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 134.18 vs 157.73             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -7.11                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 54.3                   |
| Momentum     | MACD above signal                         | 7      | 7   | -3.69 vs -5.02               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.87               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -6.46%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.85x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 4085860035 vs 4006929017     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.92x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 19.3, +DI 27.7, -DI 26.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 143.22              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.13%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 19.03%                       |

## Support And Resistance

- Support levels: $106.85, $126.36, $133.59
- Resistance levels: $135.08, $142.05, $151.16, $156.51, $163.27

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $134.18 - $137.58 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $123.99 | $154.57  | $168.16  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $123.00 - $128.09 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $119.60 | $139.13  | $145.93  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $135.08 - $138.48 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $126.39 | $157.56  | $167.95  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
