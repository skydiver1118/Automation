# TSSI Technical Analysis Sample

Generated: 2026-06-10 20:55:29
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (29/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSSI_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSSI_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $11.85             |
| SMA20             | $12.81             |
| SMA50             | $13.72             |
| SMA200            | $12.60             |
| RSI14             | 42.7               |
| MACD / Signal     | -0.06 / 0.06       |
| ADX14 / +DI / -DI | 21.2 / 23.2 / 25.8 |
| ATR14             | $1.35 (11.39%)     |
| 63-day range      | $10.28 - $17.49    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 11.85 vs 12.81               |
| Trend        | Close above SMA50                         | 0      | 8   | 11.85 vs 13.72               |
| Trend        | Close above SMA200                        | 0      | 8   | 11.85 vs 12.60               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 12.81 vs 13.72               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 13.72 vs 12.60               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.57                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 42.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.06 vs 0.06                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.47              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 1.89%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.48x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 21563743 vs 21841472         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.14x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 21.2, +DI 23.2, -DI 25.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 16.13               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 11.39%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 32.25%                       |

## Support And Resistance

- Support levels: $7.23, $8.65, $10.14, $11.70
- Resistance levels: $12.71, $14.36, $16.42, $17.46

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $13.72 - $14.39 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $11.69 | $17.77   | $20.46   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $11.03 - $12.04 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $10.35 | $14.23   | $15.58   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $12.71 - $13.38 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $11.70 | $15.75   | $17.10   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
