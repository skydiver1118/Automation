# NVDA Technical Analysis Sample

Generated: 2026-06-28 17:42:24
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (36/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [NVDA_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/NVDA_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $192.53            |
| SMA20             | $207.71            |
| SMA50             | $209.92            |
| SMA200            | $190.43            |
| RSI14             | 37.6               |
| MACD / Signal     | -3.64 / -1.73      |
| ADX14 / +DI / -DI | 16.0 / 16.8 / 30.3 |
| ATR14             | $7.29 (3.79%)      |
| 63-day range      | $164.08 - $236.26  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 192.53 vs 207.71             |
| Trend        | Close above SMA50                         | 0      | 8   | 192.53 vs 209.92             |
| Trend        | Close above SMA200                        | 8      | 8   | 192.53 vs 190.43             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 207.71 vs 209.92             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 209.92 vs 190.43             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.42                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 37.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | -3.64 vs -1.73               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.96              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -10.03%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.05x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 2346323600 vs 2914816415     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.61x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 16.0, +DI 16.8, -DI 30.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 224.20              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.79%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 18.51%                       |

## Support And Resistance

- Support levels: $164.08, $173.90, $179.35, $185.68, $192.32
- Resistance levels: $192.07, $197.39, $214.43, $224.20, $234.14

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $209.92 - $213.56 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $198.99 | $231.78  | $246.36  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $188.68 - $194.14 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $185.03 | $205.99  | $213.27  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $197.39 - $201.03 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $192.32 | $213.79  | $221.07  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
