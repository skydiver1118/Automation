# OPEN Technical Analysis Sample

Generated: 2026-07-09 16:40:28
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (56/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [OPEN_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/OPEN_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $5.30              |
| SMA20             | $4.61              |
| SMA50             | $4.76              |
| SMA200            | $5.90              |
| RSI14             | 63.4               |
| MACD / Signal     | 0.08 / -0.00       |
| ADX14 / +DI / -DI | 17.2 / 30.6 / 14.6 |
| ATR14             | $0.38 (7.20%)      |
| 63-day range      | $4.08 - $6.00      |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 5.30 vs 4.61                 |
| Trend        | Close above SMA50                         | 8      | 8   | 5.30 vs 4.76                 |
| Trend        | Close above SMA200                        | 0      | 8   | 5.30 vs 5.90                 |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 4.61 vs 4.76                 |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 4.76 vs 5.90                 |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.11                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 63.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.08 vs -0.00                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.03               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 22.12%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.66x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 6471295095 vs 6152877790     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.38x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.2, +DI 30.6, -DI 14.6 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 5.19                |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.20%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.67%                       |

## Support And Resistance

- Support levels: $4.13, $4.66, $4.98
- Resistance levels: $5.55, $6.00, $7.92

## Entry Plans

| Plan           | Entry zone    | Trigger                                                                                                      | Stop  | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ------------- | ------------------------------------------------------------------------------------------------------------ | ----- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $4.79 - $5.08 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $4.38 | $6.03    | $6.58    | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $5.55 - $5.75 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $4.98 | $6.99    | $7.66    | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
