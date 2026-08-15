# SNDK Technical Analysis Sample

Generated: 2026-05-31 20:26:02
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (90/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SNDK_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SNDK_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $1,694.98           |
| SMA20             | $1,452.22           |
| SMA50             | $1,078.61           |
| SMA200            | $488.24             |
| RSI14             | 72.2                |
| MACD / Signal     | 153.69 / 147.12     |
| ADX14 / +DI / -DI | 42.5 / 31.7 / 10.5  |
| ATR14             | $109.26 (6.45%)     |
| 63-day range      | $517.00 - $1,708.82 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 1694.98 vs 1452.22           |
| Trend        | Close above SMA50                         | 8      | 8   | 1694.98 vs 1078.61           |
| Trend        | Close above SMA200                        | 8      | 8   | 1694.98 vs 488.24            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1452.22 vs 1078.61           |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 1078.61 vs 488.24            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 327.03                       |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 72.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 153.69 vs 147.12             |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 15.77              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 54.58%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.60x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 537890300 vs 498398120       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.79x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 42.5, +DI 31.7, -DI 10.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 1710.73             |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.45%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.81%                        |

## Support And Resistance

- Support levels: $541.44, $1,078.61, $1,193.72, $1,277.33, $1,433.56
- Resistance levels: $1,709.30

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop      | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | --------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $1,397.60 - $1,479.54 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $969.35   | $2,377.01 | $2,846.23 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,708.82 - $1,763.45 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $1,476.46 | $2,255.50 | $2,515.18 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
