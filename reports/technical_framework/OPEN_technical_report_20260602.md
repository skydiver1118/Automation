# OPEN Technical Analysis Sample

Generated: 2026-06-02 16:57:32
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (55/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [OPEN_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/OPEN_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $5.41              |
| SMA20             | $4.81              |
| SMA50             | $4.92              |
| SMA200            | $6.09              |
| RSI14             | 63.2               |
| MACD / Signal     | 0.02 / -0.08       |
| ADX14 / +DI / -DI | 18.4 / 28.6 / 13.7 |
| ATR14             | $0.38 (6.95%)      |
| 63-day range      | $4.12 - $6.00      |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 5.41 vs 4.81                 |
| Trend        | Close above SMA50                         | 8      | 8   | 5.41 vs 4.92                 |
| Trend        | Close above SMA200                        | 0      | 8   | 5.41 vs 6.09                 |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 4.81 vs 4.92                 |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 4.92 vs 6.09                 |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.12                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 63.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.02 vs -0.08                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.15               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 5.46%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.46x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 5924456656 vs 5852067908     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.81x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.4, +DI 28.6, -DI 13.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 5.60                |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.95%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 9.83%                        |

## Support And Resistance

- Support levels: $4.13, $4.36, $4.80
- Resistance levels: $5.57, $6.00, $7.81

## Entry Plans

| Plan           | Entry zone    | Trigger                                                                                                      | Stop  | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ------------- | ------------------------------------------------------------------------------------------------------------ | ----- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $4.73 - $5.01 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $4.54 | $5.62    | $6.00    | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $5.57 - $5.76 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $4.92 | $7.17    | $7.93    | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
