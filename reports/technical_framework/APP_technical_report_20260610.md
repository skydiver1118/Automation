# APP Technical Analysis Sample

Generated: 2026-06-10 20:55:00
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (44/100).**

Not bullish under the framework; classify as Bearish because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APP_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APP_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $492.98            |
| SMA20             | $531.88            |
| SMA50             | $480.43            |
| SMA200            | $541.58            |
| RSI14             | 43.7               |
| MACD / Signal     | 18.15 / 26.11      |
| ADX14 / +DI / -DI | 25.9 / 21.4 / 23.2 |
| ATR14             | $35.35 (7.17%)     |
| 63-day range      | $364.64 - $622.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 492.98 vs 531.88             |
| Trend        | Close above SMA50                         | 8      | 8   | 492.98 vs 480.43             |
| Trend        | Close above SMA200                        | 0      | 8   | 492.98 vs 541.58             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 531.88 vs 480.43             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 480.43 vs 541.58             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 32.56                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 43.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | 18.15 vs 26.11               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -17.36             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 0.47%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.01x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 410932735 vs 413330357       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.41x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 25.9, +DI 21.4, -DI 23.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 635.95              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.17%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 20.74%                       |

## Support And Resistance

- Support levels: $363.62, $420.04, $452.00, $486.53
- Resistance levels: $516.15, $569.92, $625.49, $679.69, $732.42

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $531.88 - $549.56 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $478.86 | $637.93  | $708.63  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $468.85 - $495.37 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $445.08 | $556.17  | $593.20  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $516.15 - $533.82 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $486.53 | $601.89  | $640.35  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
