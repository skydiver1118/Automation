# NVDA Technical Analysis Sample

Generated: 2026-07-08 16:40:18
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (59/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [NVDA_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/NVDA_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $204.12            |
| SMA20             | $201.69            |
| SMA50             | $209.52            |
| SMA200            | $191.39            |
| RSI14             | 51.0               |
| MACD / Signal     | -3.30 / -3.41      |
| ADX14 / +DI / -DI | 18.5 / 20.1 / 24.2 |
| ATR14             | $7.12 (3.49%)      |
| 63-day range      | $180.30 - $236.54  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 204.12 vs 201.69             |
| Trend        | Close above SMA50                         | 0      | 8   | 204.12 vs 209.52             |
| Trend        | Close above SMA200                        | 8      | 8   | 204.12 vs 191.39             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 201.69 vs 209.52             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 209.52 vs 191.39             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 5.32                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 51.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | -3.30 vs -3.41               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.42               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -2.17%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.97x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 2476370599 vs 2458008215     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.93x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.5, +DI 20.1, -DI 24.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 213.48              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.49%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.71%                       |

## Support And Resistance

- Support levels: $173.23, $179.25, $190.28, $197.10, $201.87
- Resistance levels: $205.15, $214.20, $235.12

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $198.49 - $203.83 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $194.93 | $215.41  | $222.53  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $205.15 - $208.71 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $202.05 | $221.18  | $228.30  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
