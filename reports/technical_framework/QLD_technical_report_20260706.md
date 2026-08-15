# QLD Technical Analysis Sample

Generated: 2026-07-06 16:40:21
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (66/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QLD_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QLD_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $93.14             |
| SMA20             | $92.88             |
| SMA50             | $91.10             |
| SMA200            | $74.88             |
| RSI14             | 50.8               |
| MACD / Signal     | 0.45 / 0.91        |
| ADX14 / +DI / -DI | 17.8 / 21.8 / 27.6 |
| ATR14             | $4.18 (4.49%)      |
| 63-day range      | $61.13 - $101.12   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 93.14 vs 92.88               |
| Trend        | Close above SMA50                         | 8      | 8   | 93.14 vs 91.10               |
| Trend        | Close above SMA200                        | 8      | 8   | 93.14 vs 74.88               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 92.88 vs 91.10               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 91.10 vs 74.88               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 10.12                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 50.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | 0.45 vs 0.91                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.58               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -5.88%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.52x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 222353121 vs 229464536       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.80x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.8, +DI 21.8, -DI 27.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 99.39               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.49%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 7.89%                        |

## Support And Resistance

- Support levels: $61.22, $64.95, $68.91, $86.67, $92.35
- Resistance levels: $94.42, $99.62

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $90.98 - $94.12 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $86.91 | $103.82  | $109.46  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $94.42 - $96.51 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $93.07 | $103.83  | $108.01  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
