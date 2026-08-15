# OPEN Technical Analysis Sample

Generated: 2026-07-08 16:40:19
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (60/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [OPEN_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/OPEN_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $4.79              |
| SMA20             | $4.56              |
| SMA50             | $4.77              |
| SMA200            | $5.92              |
| RSI14             | 53.3               |
| MACD / Signal     | 0.04 / -0.03       |
| ADX14 / +DI / -DI | 15.8 / 23.3 / 16.7 |
| ATR14             | $0.36 (7.52%)      |
| 63-day range      | $4.08 - $6.00      |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 4.79 vs 4.56                 |
| Trend        | Close above SMA50                         | 8      | 8   | 4.79 vs 4.77                 |
| Trend        | Close above SMA200                        | 0      | 8   | 4.79 vs 5.92                 |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 4.56 vs 4.77                 |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 4.77 vs 5.92                 |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.11                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.3                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.04 vs -0.03                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.04               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 11.14%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.60x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 6359688400 vs 6126037270     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.21x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.8, +DI 23.3, -DI 16.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 5.06                |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.52%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 20.17%                       |

## Support And Resistance

- Support levels: $4.13, $4.65
- Resistance levels: $5.03, $5.50, $5.72, $6.00, $7.92

## Entry Plans

| Plan           | Entry zone    | Trigger                                                                                                      | Stop  | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ------------- | ------------------------------------------------------------------------------------------------------------ | ----- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $4.59 - $4.86 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $4.41 | $5.44    | $5.80    | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $5.03 - $5.21 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $4.77 | $5.84    | $6.20    | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
