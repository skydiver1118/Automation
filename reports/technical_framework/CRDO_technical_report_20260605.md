# CRDO Technical Analysis Sample

Generated: 2026-06-05 16:41:06
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (79/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRDO_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRDO_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $206.89            |
| SMA20             | $202.94            |
| SMA50             | $170.54            |
| SMA200            | $147.80            |
| RSI14             | 53.7               |
| MACD / Signal     | 13.40 / 14.45      |
| ADX14 / +DI / -DI | 30.8 / 22.9 / 14.2 |
| ATR14             | $20.74 (10.02%)    |
| 63-day range      | $86.49 - $245.95   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 206.89 vs 202.94             |
| Trend        | Close above SMA50                         | 8      | 8   | 206.89 vs 170.54             |
| Trend        | Close above SMA200                        | 8      | 8   | 206.89 vs 147.80             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 202.94 vs 170.54             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 170.54 vs 147.80             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 37.55                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | 13.40 vs 14.45               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -4.30              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 9.88%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.87x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 200131343 vs 194736572       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.14x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 30.8, +DI 22.9, -DI 14.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 247.76              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.02%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 15.88%                       |

## Support And Resistance

- Support levels: $119.40, $136.32, $157.29, $176.67, $202.28
- Resistance levels: $210.97, $246.40

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $193.53 - $209.09 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $149.80 | $304.33  | $355.84  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $210.97 - $221.34 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $203.90 | $257.63  | $278.37  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
