# AMD Technical Analysis Sample

Generated: 2026-05-31 20:26:15
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (92/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AMD_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AMD_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $516.10            |
| SMA20             | $440.11            |
| SMA50             | $328.15            |
| SMA200            | $237.58            |
| RSI14             | 76.0               |
| MACD / Signal     | 49.86 / 46.91      |
| ADX14 / +DI / -DI | 47.8 / 39.2 / 11.9 |
| ATR14             | $26.03 (5.04%)     |
| 63-day range      | $188.22 - $527.20  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 516.10 vs 440.11             |
| Trend        | Close above SMA50                         | 8      | 8   | 516.10 vs 328.15             |
| Trend        | Close above SMA200                        | 8      | 8   | 516.10 vs 237.58             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 440.11 vs 328.15             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 328.15 vs 237.58             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 95.91                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 76.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 49.86 vs 46.91               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 5.24               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 45.59%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.77x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1287035800 vs 1242689730     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.45x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 47.8, +DI 39.2, -DI 11.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 539.11              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.04%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 2.11%                        |

## Support And Resistance

- Support levels: $195.13, $211.77, $334.62, $393.36, $437.68
- Resistance levels: $530.18

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $427.09 - $446.61 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $302.11 | $706.33  | $841.07  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $527.20 - $540.22 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $464.03 | $673.06  | $742.74  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
