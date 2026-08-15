# QLD Technical Analysis Sample

Generated: 2026-06-28 17:42:27
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (42/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QLD_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QLD_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $89.12             |
| SMA20             | $94.34             |
| SMA50             | $89.36             |
| SMA200            | $74.18             |
| RSI14             | 45.4               |
| MACD / Signal     | 0.53 / 1.57        |
| ADX14 / +DI / -DI | 22.2 / 20.6 / 29.6 |
| ATR14             | $4.20 (4.71%)      |
| 63-day range      | $56.56 - $101.12   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 89.12 vs 94.34               |
| Trend        | Close above SMA50                         | 0      | 8   | 89.12 vs 89.36               |
| Trend        | Close above SMA200                        | 8      | 8   | 89.12 vs 74.18               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 94.34 vs 89.36               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 89.36 vs 74.18               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.98                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 45.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | 0.53 vs 1.57                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.61              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -8.80%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.83x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 237384500 vs 249756120       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.68x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 22.2, +DI 20.6, -DI 29.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 103.00              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.71%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.87%                       |

## Support And Resistance

- Support levels: $61.32, $64.95, $68.91, $86.50, $89.36
- Resistance levels: $94.42, $100.46, $103.00

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $94.34 - $96.44 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $88.04 | $106.93  | $115.33  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $84.40 - $87.55 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $82.30 | $94.42   | $98.56   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $94.42 - $96.52 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $86.50 | $113.40  | $122.37  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
