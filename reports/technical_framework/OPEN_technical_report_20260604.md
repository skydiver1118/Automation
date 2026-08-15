# OPEN Technical Analysis Sample

Generated: 2026-06-04 19:39:24
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (45/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [OPEN_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/OPEN_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $4.95              |
| SMA20             | $4.76              |
| SMA50             | $4.90              |
| SMA200            | $6.10              |
| RSI14             | 51.1               |
| MACD / Signal     | 0.02 / -0.04       |
| ADX14 / +DI / -DI | 18.3 / 24.2 / 17.1 |
| ATR14             | $0.38 (7.76%)      |
| 63-day range      | $4.12 - $6.00      |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 4.95 vs 4.76                 |
| Trend        | Close above SMA50                         | 8      | 8   | 4.95 vs 4.90                 |
| Trend        | Close above SMA200                        | 0      | 8   | 4.95 vs 6.10                 |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 4.76 vs 4.90                 |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 4.90 vs 6.10                 |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.14                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 51.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.02 vs -0.04                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.04               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -9.34%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.68x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 5913028195 vs 5845447340     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.79x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.3, +DI 24.2, -DI 17.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 5.46                |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.76%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.50%                       |

## Support And Resistance

- Support levels: $4.18, $4.80
- Resistance levels: $5.01, $5.56, $6.00, $7.81

## Entry Plans

| Plan           | Entry zone    | Trigger                                                                                                      | Stop  | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ------------- | ------------------------------------------------------------------------------------------------------------ | ----- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $4.71 - $5.00 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $4.52 | $5.62    | $6.01    | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $5.01 - $5.20 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $4.90 | $5.87    | $6.26    | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
