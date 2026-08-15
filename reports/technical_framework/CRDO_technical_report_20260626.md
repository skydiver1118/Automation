# CRDO Technical Analysis Sample

Generated: 2026-06-28 17:42:45
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (63/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRDO_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRDO_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $238.00            |
| SMA20             | $245.46            |
| SMA50             | $210.52            |
| SMA200            | $156.87            |
| RSI14             | 50.3               |
| MACD / Signal     | 17.52 / 19.17      |
| ADX14 / +DI / -DI | 36.6 / 22.6 / 18.1 |
| ATR14             | $26.71 (11.22%)    |
| 63-day range      | $86.49 - $308.67   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 238.00 vs 245.46             |
| Trend        | Close above SMA50                         | 8      | 8   | 238.00 vs 210.52             |
| Trend        | Close above SMA200                        | 8      | 8   | 238.00 vs 156.87             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 245.46 vs 210.52             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 210.52 vs 156.87             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 54.16                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 50.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | 17.52 vs 19.17               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -3.45              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 7.04%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 3.27x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 201262400 vs 228788245       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.92x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 36.6, +DI 22.6, -DI 18.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 293.81              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 11.22%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 22.90%                       |

## Support And Resistance

- Support levels: $144.41, $164.80, $193.30, $210.52, $240.01
- Resistance levels: $245.95, $270.21, $304.96

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $197.17 - $217.20 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $183.82 | $260.60  | $287.30  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $245.95 - $259.30 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $210.52 | $336.83  | $378.93  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
