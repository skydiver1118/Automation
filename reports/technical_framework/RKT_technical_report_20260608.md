# RKT Technical Analysis Sample

Generated: 2026-06-08 21:13:27
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (11/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKT_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKT_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $12.35             |
| SMA20             | $13.73             |
| SMA50             | $14.50             |
| SMA200            | $17.43             |
| RSI14             | 35.8               |
| MACD / Signal     | -0.45 / -0.34      |
| ADX14 / +DI / -DI | 15.4 / 17.4 / 33.8 |
| ATR14             | $0.73 (5.89%)      |
| 63-day range      | $12.17 - $17.36    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 12.35 vs 13.73               |
| Trend        | Close above SMA50                         | 0      | 8   | 12.35 vs 14.50               |
| Trend        | Close above SMA200                        | 0      | 8   | 12.35 vs 17.43               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 13.73 vs 14.50               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 14.50 vs 17.43               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.55                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 35.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.45 vs -0.34               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.22              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -21.29%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.87x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 53078017 vs 90089731         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.67x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.4, +DI 17.4, -DI 33.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 15.20               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.89%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 28.86%                       |

## Support And Resistance

- Support levels: $12.25
- Resistance levels: $14.68, $15.37, $15.85, $17.36, $18.49

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $14.50 - $14.86 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $13.41 | $16.68   | $18.14   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $11.88 - $12.43 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $11.52 | $14.68   | $14.34   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $14.68 - $15.05 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $12.25 | $20.10   | $22.71   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
