# SNDK Technical Analysis Sample

Generated: 2026-07-07 16:40:26
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (43/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SNDK_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SNDK_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $1,617.70           |
| SMA20             | $1,953.87           |
| SMA50             | $1,639.47           |
| SMA200            | $719.24             |
| RSI14             | 43.8                |
| MACD / Signal     | 61.71 / 134.00      |
| ADX14 / +DI / -DI | 31.3 / 25.4 / 33.5  |
| ATR14             | $208.44 (12.88%)    |
| 63-day range      | $687.68 - $2,354.39 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 1617.70 vs 1953.87           |
| Trend        | Close above SMA50                         | 0      | 8   | 1617.70 vs 1639.47           |
| Trend        | Close above SMA200                        | 8      | 8   | 1617.70 vs 719.24            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1953.87 vs 1639.47           |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 1639.47 vs 719.24            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 459.59                       |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 43.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | 61.71 vs 134.00              |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -67.45             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 3.74%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.17x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 504369015 vs 553134856       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.75x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 31.3, +DI 25.4, -DI 33.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 2403.15             |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 12.88%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 31.29%                       |

## Support And Resistance

- Support levels: $266.33, $547.56, $687.68, $1,277.33, $1,501.32
- Resistance levels: $1,861.00, $2,366.58

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop      | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | --------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $1,953.87 - $2,058.08 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $1,641.21 | $2,579.18 | $2,996.05 | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $1,397.10 - $1,553.43 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $1,292.88 | $1,892.14 | $2,100.58 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,861.00 - $1,965.22 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $1,501.32 | $2,736.69 | $3,148.47 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
