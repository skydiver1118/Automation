# SOFI Technical Analysis Sample

Generated: 2026-06-03 19:37:18
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (61/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SOFI_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SOFI_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $16.68             |
| SMA20             | $16.27             |
| SMA50             | $16.75             |
| SMA200            | $23.12             |
| RSI14             | 49.7               |
| MACD / Signal     | 0.14 / -0.12       |
| ADX14 / +DI / -DI | 21.8 / 27.7 / 19.5 |
| ATR14             | $0.93 (5.58%)      |
| 63-day range      | $14.92 - $20.13    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 16.68 vs 16.27               |
| Trend        | Close above SMA50                         | 0      | 8   | 16.68 vs 16.75               |
| Trend        | Close above SMA200                        | 0      | 8   | 16.68 vs 23.12               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 16.27 vs 16.75               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 16.75 vs 23.12               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.75                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.14 vs -0.12                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.18               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 4.12%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.04x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1347266085 vs 1195056544     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.18x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 21.8, +DI 27.7, -DI 19.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 18.13               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.58%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.14%                       |

## Support And Resistance

- Support levels: $14.88, $15.50, $16.60
- Resistance levels: $17.99, $18.80, $19.55, $20.13, $22.00

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $16.13 - $16.83 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $15.67 | $18.34   | $19.28   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $17.99 - $18.46 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $16.60 | $21.48   | $23.11   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
