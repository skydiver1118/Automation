# PLTR Technical Analysis Sample

Generated: 2026-06-05 16:40:41
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (18/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [PLTR_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/PLTR_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $135.53            |
| SMA20             | $139.58            |
| SMA50             | $140.90            |
| SMA200            | $161.07            |
| RSI14             | 44.8               |
| MACD / Signal     | 1.09 / 0.79        |
| ADX14 / +DI / -DI | 14.5 / 26.6 / 30.8 |
| ATR14             | $7.23 (5.33%)      |
| 63-day range      | $122.68 - $163.70  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 135.53 vs 139.58             |
| Trend        | Close above SMA50                         | 0      | 8   | 135.53 vs 140.90             |
| Trend        | Close above SMA200                        | 0      | 8   | 135.53 vs 161.07             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 139.58 vs 140.90             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 140.90 vs 161.07             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.76                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 44.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | 1.09 vs 0.79                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.59              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -1.11%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.88x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 4265309144 vs 4271111442     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 1.00x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.5, +DI 26.6, -DI 30.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 155.65              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.33%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.21%                       |

## Support And Resistance

- Support levels: $125.51, $133.56
- Resistance levels: $140.96, $151.16, $156.23, $163.34, $172.00

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $140.90 - $144.51 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $130.06 | $162.58  | $177.03  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $129.94 - $135.36 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $126.33 | $147.10  | $154.33  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $140.96 - $144.58 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $133.56 | $161.19  | $170.41  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
