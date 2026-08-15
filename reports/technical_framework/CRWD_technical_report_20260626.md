# CRWD Technical Analysis Sample

Generated: 2026-06-28 17:42:20
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (78/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWD_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWD_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $701.09            |
| SMA20             | $694.75            |
| SMA50             | $594.02            |
| SMA200            | $495.98            |
| RSI14             | 60.7               |
| MACD / Signal     | 21.33 / 28.47      |
| ADX14 / +DI / -DI | 28.4 / 25.0 / 16.5 |
| ATR14             | $32.13 (4.58%)     |
| 63-day range      | $361.81 - $785.66  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 701.09 vs 694.75             |
| Trend        | Close above SMA50                         | 8      | 8   | 701.09 vs 594.02             |
| Trend        | Close above SMA200                        | 8      | 8   | 701.09 vs 495.98             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 694.75 vs 594.02             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 594.02 vs 495.98             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 117.42                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 60.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | 21.33 vs 28.47               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.80               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 4.48%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.91x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 7856800 vs 3556015           |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.76x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 28.4, +DI 25.0, -DI 16.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 769.24              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.58%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.76%                       |

## Support And Resistance

- Support levels: $470.67, $594.02, $623.70, $665.99, $694.75
- Resistance levels: $706.40, $781.56

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2  | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $678.68 - $702.78 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $561.89 | $948.41  | $1,077.25 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $706.40 - $722.46 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $694.75 | $778.69  | $810.82   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
