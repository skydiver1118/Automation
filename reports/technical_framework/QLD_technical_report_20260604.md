# QLD Technical Analysis Sample

Generated: 2026-06-04 19:39:26
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (80/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QLD_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QLD_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $99.02             |
| SMA20             | $94.23             |
| SMA50             | $81.03             |
| SMA200            | $71.96             |
| RSI14             | 72.9               |
| MACD / Signal     | 5.10 / 5.14        |
| ADX14 / +DI / -DI | 39.5 / 35.2 / 17.6 |
| ATR14             | $2.53 (2.55%)      |
| 63-day range      | $56.60 - $101.19   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 99.02 vs 94.23               |
| Trend        | Close above SMA50                         | 8      | 8   | 99.02 vs 81.03               |
| Trend        | Close above SMA200                        | 8      | 8   | 99.02 vs 71.96               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 94.23 vs 81.03               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 81.03 vs 71.96               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.11                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 72.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | 5.10 vs 5.14                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.07              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 12.71%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.89x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 273741287 vs 266456994       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.42x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 39.5, +DI 35.2, -DI 17.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 102.11              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.55%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 2.14%                        |

## Support And Resistance

- Support levels: $71.48, $81.03, $86.94, $93.78, $96.88
- Resistance levels: $101.42

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $95.62 - $97.51   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $78.50 | $132.69  | $150.75  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $101.19 - $102.45 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $96.88 | $111.71  | $116.65  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
