# SNDK Technical Analysis Sample

Generated: 2026-06-03 19:37:17
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (92/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SNDK_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SNDK_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $1,831.50           |
| SMA20             | $1,525.23           |
| SMA50             | $1,141.11           |
| SMA200            | $514.10             |
| RSI14             | 74.2                |
| MACD / Signal     | 170.91 / 156.28     |
| ADX14 / +DI / -DI | 45.8 / 36.4 / 8.4   |
| ATR14             | $109.82 (6.00%)     |
| 63-day range      | $517.00 - $1,861.00 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                    |
| ------------ | ----------------------------------------- | ------ | --- | --------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 1831.50 vs 1525.23          |
| Trend        | Close above SMA50                         | 8      | 8   | 1831.50 vs 1141.11          |
| Trend        | Close above SMA200                        | 8      | 8   | 1831.50 vs 514.10           |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1525.23 vs 1141.11          |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 1141.11 vs 514.10           |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 351.29                      |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 74.2                  |
| Momentum     | MACD above signal                         | 7      | 7   | 170.91 vs 156.28            |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 15.99             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 30.23%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.89x                       |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 552074104 vs 508330230      |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.30x                       |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 45.8, +DI 36.4, -DI 8.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 1818.68            |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 6.00%                 |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 1.59%                       |

## Support And Resistance

- Support levels: $207.48, $541.44, $1,141.11, $1,254.56, $1,514.47
- Resistance levels: $1,850.42

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop      | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | --------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $1,470.32 - $1,552.69 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $1,031.28 | $2,471.94 | $2,952.16 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,850.42 - $1,905.33 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $1,611.86 | $2,409.91 | $2,675.93 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
