# SMH Technical Analysis Sample

Generated: 2026-06-03 19:37:15
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (92/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SMH_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SMH_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $637.90            |
| SMA20             | $578.72            |
| SMA50             | $498.87            |
| SMA200            | $393.19            |
| RSI14             | 78.0               |
| MACD / Signal     | 33.96 / 31.49      |
| ADX14 / +DI / -DI | 37.3 / 39.1 / 12.9 |
| ATR14             | $19.21 (3.01%)     |
| 63-day range      | $359.86 - $642.77  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 637.90 vs 578.72             |
| Trend        | Close above SMA50                         | 8      | 8   | 637.90 vs 498.87             |
| Trend        | Close above SMA200                        | 8      | 8   | 637.90 vs 393.19             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 578.72 vs 498.87             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 498.87 vs 393.19             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 72.29                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 78.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 33.96 vs 31.49               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.48               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 22.04%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.94x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 330732287 vs 306205684       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.28x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 37.3, +DI 39.1, -DI 12.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 634.56              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.01%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.76%                        |

## Support And Resistance

- Support levels: $378.24, $397.77, $498.87, $525.37, $576.47
- Resistance levels: $640.72

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $569.11 - $583.52 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $479.66 | $769.64  | $866.30  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $640.72 - $650.32 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $599.48 | $737.60  | $783.65  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
