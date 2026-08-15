# PLTR Technical Analysis Sample

Generated: 2026-05-31 20:25:52
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (63/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [PLTR_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/PLTR_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $156.54            |
| SMA20             | $137.81            |
| SMA50             | $141.79            |
| SMA200            | $161.78            |
| RSI14             | 67.4               |
| MACD / Signal     | 0.48 / -1.41       |
| ADX14 / +DI / -DI | 14.4 / 35.3 / 18.4 |
| ATR14             | $6.58 (4.21%)      |
| 63-day range      | $122.68 - $162.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 156.54 vs 137.81             |
| Trend        | Close above SMA50                         | 8      | 8   | 156.54 vs 141.79             |
| Trend        | Close above SMA200                        | 0      | 8   | 156.54 vs 161.78             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 137.81 vs 141.79             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 141.79 vs 161.78             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -3.21                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 67.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.48 vs -1.41                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.63               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 12.53%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 2.04x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 4432614700 vs 4308948135     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.32x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.4, +DI 35.3, -DI 18.4 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 149.49              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.21%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 3.61%                        |

## Support And Resistance

- Support levels: $125.88, $133.44, $139.66, $148.83
- Resistance levels: $157.15, $162.83, $172.00, $182.43, $188.83

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $145.54 - $150.48 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $135.21 | $173.62  | $186.42  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $157.15 - $160.44 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $148.83 | $178.71  | $188.67  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
