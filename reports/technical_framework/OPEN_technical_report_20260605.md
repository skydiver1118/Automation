# OPEN Technical Analysis Sample

Generated: 2026-06-05 16:40:40
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (21/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [OPEN_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/OPEN_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $4.42              |
| SMA20             | $4.72              |
| SMA50             | $4.89              |
| SMA200            | $6.11              |
| RSI14             | 41.2               |
| MACD / Signal     | -0.02 / -0.04      |
| ADX14 / +DI / -DI | 17.3 / 21.7 / 24.1 |
| ATR14             | $0.40 (8.99%)      |
| 63-day range      | $4.12 - $6.00      |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 4.42 vs 4.72                 |
| Trend        | Close above SMA50                         | 0      | 8   | 4.42 vs 4.89                 |
| Trend        | Close above SMA200                        | 0      | 8   | 4.42 vs 6.11                 |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 4.72 vs 4.89                 |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 4.89 vs 6.11                 |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.16                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 41.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.02 vs -0.04               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.03              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -16.92%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.93x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 5866815103 vs 5829039540     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.83x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.3, +DI 21.7, -DI 24.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 5.38                |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.99%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 26.33%                       |

## Support And Resistance

- Support levels: $4.21
- Resistance levels: $5.01, $5.56, $6.00, $7.81

## Entry Plans

| Plan           | Entry zone    | Trigger                                                                                                      | Stop  | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ------------- | ------------------------------------------------------------------------------------------------------------ | ----- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $4.89 - $5.09 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $4.30 | $6.08    | $6.88    | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $4.01 - $4.31 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $3.81 | $5.01    | $5.35    | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $5.01 - $5.21 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $4.21 | $6.91    | $7.82    | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
