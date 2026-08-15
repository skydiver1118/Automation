# CRWV Technical Analysis Sample

Generated: 2026-07-09 16:40:23
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (20/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWV_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWV_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $89.70             |
| SMA20             | $98.71             |
| SMA50             | $106.46            |
| SMA200            | $99.48             |
| RSI14             | 42.5               |
| MACD / Signal     | -5.54 / -4.25      |
| ADX14 / +DI / -DI | 17.5 / 22.8 / 30.5 |
| ATR14             | $8.17 (9.11%)      |
| 63-day range      | $79.46 - $138.25   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 89.70 vs 98.71               |
| Trend        | Close above SMA50                         | 0      | 8   | 89.70 vs 106.46              |
| Trend        | Close above SMA200                        | 0      | 8   | 89.70 vs 99.48               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 98.71 vs 106.46              |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 106.46 vs 99.48              |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -1.19                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 42.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | -5.54 vs -4.25               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.53               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -8.89%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.81x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 367708322 vs 478032031       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.75x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.5, +DI 22.8, -DI 30.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 120.65              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.11%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 35.12%                       |

## Support And Resistance

- Support levels: $70.56, $77.75, $85.78
- Resistance levels: $97.92, $103.21, $114.45, $122.35, $132.15

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $106.46 - $110.54 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $94.19 | $130.98  | $147.33  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $81.70 - $87.83   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $77.61 | $101.11  | $109.29  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $97.92 - $102.01  | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $85.78 | $128.33  | $142.51  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
