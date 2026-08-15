# PLTR Technical Analysis Sample

Generated: 2026-07-08 16:40:20
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (39/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [PLTR_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/PLTR_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $132.22            |
| SMA20             | $125.24            |
| SMA50             | $133.82            |
| SMA200            | $157.33            |
| RSI14             | 53.6               |
| MACD / Signal     | -1.87 / -4.00      |
| ADX14 / +DI / -DI | 17.4 / 28.1 / 27.3 |
| ATR14             | $6.91 (5.22%)      |
| 63-day range      | $106.37 - $163.70  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 132.22 vs 125.24             |
| Trend        | Close above SMA50                         | 0      | 8   | 132.22 vs 133.82             |
| Trend        | Close above SMA200                        | 0      | 8   | 132.22 vs 157.33             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 125.24 vs 133.82             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 133.82 vs 157.33             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -6.86                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.6                   |
| Momentum     | MACD above signal                         | 7      | 7   | -1.87 vs -4.00               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.62               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -3.11%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.87x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 4153258657 vs 4058455778     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.98x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.4, +DI 28.1, -DI 27.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 142.35              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.22%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 19.23%                       |

## Support And Resistance

- Support levels: $106.96, $126.48, $133.52
- Resistance levels: $139.44, $151.16, $156.51, $163.27, $172.00

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $133.82 - $137.27 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $123.46 | $154.54  | $168.35  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $124.13 - $129.31 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $120.68 | $140.53  | $147.44  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $139.44 - $142.90 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $127.58 | $168.35  | $181.93  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
