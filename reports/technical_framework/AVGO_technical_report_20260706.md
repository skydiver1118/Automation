# AVGO Technical Analysis Sample

Generated: 2026-07-06 16:40:12
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (36/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AVGO_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AVGO_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $373.90            |
| SMA20             | $381.76            |
| SMA50             | $407.93            |
| SMA200            | $360.28            |
| RSI14             | 44.8               |
| MACD / Signal     | -11.06 / -9.52     |
| ADX14 / +DI / -DI | 21.6 / 18.8 / 29.8 |
| ATR14             | $18.21 (4.87%)     |
| 63-day range      | $309.79 - $494.22  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 373.90 vs 381.76             |
| Trend        | Close above SMA50                         | 0      | 8   | 373.90 vs 407.93             |
| Trend        | Close above SMA200                        | 8      | 8   | 373.90 vs 360.28             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 381.76 vs 407.93             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 407.93 vs 360.28             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.49                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 44.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | -11.06 vs -9.52              |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.78               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -10.60%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.69x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 892524419 vs 899819426       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.98x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 21.6, +DI 18.8, -DI 29.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 405.64              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.87%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 24.35%                       |

## Support And Resistance

- Support levels: $291.86, $310.27, $329.29, $357.15, $369.74
- Resistance levels: $383.15, $411.64, $435.76, $494.22

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $407.93 - $417.03 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $380.61 | $462.56  | $498.98  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $360.64 - $374.30 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $351.53 | $403.89  | $422.10  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $383.15 - $392.26 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $369.74 | $424.13  | $442.34  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
