# MRVL Technical Analysis Sample

Generated: 2026-06-04 19:39:40
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (86/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MRVL_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MRVL_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $316.43            |
| SMA20             | $203.35            |
| SMA50             | $162.03            |
| SMA200            | $102.46            |
| RSI14             | 88.1               |
| MACD / Signal     | 34.04 / 22.13      |
| ADX14 / +DI / -DI | 51.4 / 48.8 / 10.8 |
| ATR14             | $20.61 (6.51%)     |
| 63-day range      | $83.36 - $324.20   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 316.43 vs 203.35             |
| Trend        | Close above SMA50                         | 8      | 8   | 316.43 vs 162.03             |
| Trend        | Close above SMA200                        | 8      | 8   | 316.43 vs 102.46             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 203.35 vs 162.03             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 162.03 vs 102.46             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 46.85                        |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 88.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | 34.04 vs 22.13               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 10.65              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 83.81%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 2.07x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1167092145 vs 763219002      |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 5.45x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 51.4, +DI 48.8, -DI 10.8 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 295.27              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.51%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 2.40%                        |

## Support And Resistance

- Support levels: $80.40, $111.43, $128.42, $157.42, $208.65
- Resistance levels: $324.20

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $203.65 - $219.11 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $141.42 | $351.29  | $421.25  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $324.20 - $334.51 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $275.20 | $437.66  | $491.81  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
