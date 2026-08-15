# VRSN Technical Analysis Sample

Generated: 2026-06-02 16:57:45
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (83/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [VRSN_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/VRSN_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $297.41            |
| SMA20             | $293.67            |
| SMA50             | $275.87            |
| SMA200            | $256.53            |
| RSI14             | 57.3               |
| MACD / Signal     | 6.69 / 8.38        |
| ADX14 / +DI / -DI | 26.4 / 23.8 / 21.9 |
| ATR14             | $8.80 (2.96%)      |
| 63-day range      | $232.22 - $312.48  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 297.41 vs 293.67             |
| Trend        | Close above SMA50                         | 8      | 8   | 297.41 vs 275.87             |
| Trend        | Close above SMA200                        | 8      | 8   | 297.41 vs 256.53             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 293.67 vs 275.87             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 275.87 vs 256.53             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 24.30                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 57.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | 6.69 vs 8.38                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -3.12              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 8.77%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.69x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 25105478 vs 24463164         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.14x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 26.4, +DI 23.8, -DI 21.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 314.77              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.96%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 4.82%                        |

## Support And Resistance

- Support levels: $243.10, $255.47, $274.22, $281.99, $292.81
- Resistance levels: $302.97, $313.05

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $289.27 - $295.87 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $267.07 | $343.57  | $369.07  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $302.97 - $307.37 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $293.67 | $328.17  | $339.67  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
