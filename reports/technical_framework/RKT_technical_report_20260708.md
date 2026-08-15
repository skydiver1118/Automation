# RKT Technical Analysis Sample

Generated: 2026-07-08 16:40:23
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (50/100).**

Not bullish yet under the framework; classify as Neutral because close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKT_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKT_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $14.16             |
| SMA20             | $14.31             |
| SMA50             | $14.16             |
| SMA200            | $16.91             |
| RSI14             | 47.6               |
| MACD / Signal     | 0.33 / 0.29        |
| ADX14 / +DI / -DI | 17.5 / 21.9 / 24.3 |
| ATR14             | $0.90 (6.34%)      |
| 63-day range      | $12.17 - $17.36    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 14.16 vs 14.31               |
| Trend        | Close above SMA50                         | 8      | 8   | 14.16 vs 14.16               |
| Trend        | Close above SMA200                        | 0      | 8   | 14.16 vs 16.91               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 14.31 vs 14.16               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 14.16 vs 16.91               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.34                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 47.6                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.33 vs 0.29                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.25              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 14.66%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.75x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 341639538 vs 237975352       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.18x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.5, +DI 21.9, -DI 24.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 16.38               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.34%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 18.43%                       |

## Support And Resistance

- Support levels: $12.24, $13.91
- Resistance levels: $14.64, $16.17, $17.36, $18.49, $20.30

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $13.71 - $14.38 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $13.26 | $15.84   | $16.74   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $14.64 - $15.09 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $14.16 | $16.66   | $17.56   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
