# POWL Technical Analysis Sample

Generated: 2026-06-02 16:57:46
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (73/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [POWL_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/POWL_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $299.07            |
| SMA20             | $292.38            |
| SMA50             | $250.70            |
| SMA200            | $156.87            |
| RSI14             | 60.3               |
| MACD / Signal     | 9.57 / 11.66       |
| ADX14 / +DI / -DI | 28.9 / 23.1 / 16.1 |
| ATR14             | $17.77 (5.94%)     |
| 63-day range      | $157.45 - $327.89  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 299.07 vs 292.38             |
| Trend        | Close above SMA50                         | 8      | 8   | 299.07 vs 250.70             |
| Trend        | Close above SMA200                        | 8      | 8   | 299.07 vs 156.87             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 292.38 vs 250.70             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 250.70 vs 156.87             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 47.58                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 60.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | 9.57 vs 11.66                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.87               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 10.83%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.73x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 31255385 vs 32124299         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.65x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 28.9, +DI 23.1, -DI 16.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 325.82              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.94%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 8.79%                        |

## Support And Resistance

- Support levels: $174.85, $223.92, $253.29, $271.00, $287.29
- Resistance levels: $298.53, $327.37

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $283.49 - $296.82 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $232.92 | $404.62  | $461.85  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $327.37 - $336.26 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $292.38 | $410.68  | $450.11  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
