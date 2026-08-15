# VRSN Technical Analysis Sample

Generated: 2026-07-09 16:40:41
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (53/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [VRSN_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/VRSN_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $269.98            |
| SMA20             | $262.86            |
| SMA50             | $278.77            |
| SMA200            | $255.73            |
| RSI14             | 52.3               |
| MACD / Signal     | -4.78 / -6.94      |
| ADX14 / +DI / -DI | 25.7 / 22.7 / 23.0 |
| ATR14             | $8.09 (3.00%)      |
| 63-day range      | $244.74 - $312.48  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 269.98 vs 262.86             |
| Trend        | Close above SMA50                         | 0      | 8   | 269.98 vs 278.77             |
| Trend        | Close above SMA200                        | 8      | 8   | 269.98 vs 255.73             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 262.86 vs 278.77             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 278.77 vs 255.73             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -1.59                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 52.3                   |
| Momentum     | MACD above signal                         | 7      | 7   | -4.78 vs -6.94               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.75               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -4.90%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.87x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 26616417 vs 25074501         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.83x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 25.7, +DI 22.7, -DI 23.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 286.49              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.00%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.60%                       |

## Support And Resistance

- Support levels: $238.19, $244.48, $252.84, $260.48, $265.70
- Resistance levels: $272.00, $279.87, $288.07, $302.97, $312.48

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $261.65 - $267.72 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $257.61 | $280.86  | $288.95  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $272.00 - $276.04 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $265.70 | $290.68  | $299.00  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
