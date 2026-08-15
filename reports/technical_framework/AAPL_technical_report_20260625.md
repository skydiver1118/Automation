# AAPL Technical Analysis Sample

Generated: 2026-06-26 06:53:04
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (39/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AAPL_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AAPL_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $275.15            |
| SMA20             | $299.73            |
| SMA50             | $291.06            |
| SMA200            | $268.83            |
| RSI14             | 32.2               |
| MACD / Signal     | -1.57 / 1.23       |
| ADX14 / +DI / -DI | 23.9 / 13.9 / 31.7 |
| ATR14             | $7.88 (2.86%)      |
| 63-day range      | $245.28 - $317.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 275.15 vs 299.73             |
| Trend        | Close above SMA50                         | 0      | 8   | 275.15 vs 291.06             |
| Trend        | Close above SMA200                        | 8      | 8   | 275.15 vs 268.83             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 299.73 vs 291.06             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 291.06 vs 268.83             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 18.37                        |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 32.2                   |
| Momentum     | MACD above signal                         | 0      | 7   | -1.57 vs 1.23                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.39              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -11.48%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.90x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1662175700 vs 1855657575     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.49x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 23.9, +DI 13.9, -DI 31.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 319.50              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.86%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.31%                       |

## Support And Resistance

- Support levels: $244.96, $253.90, $266.94, $273.75
- Resistance levels: $276.80, $302.81, $317.92

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $299.73 - $303.67 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $287.90 | $323.37  | $339.13  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $269.81 - $275.72 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $265.87 | $288.53  | $296.41  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $276.80 - $280.74 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $273.75 | $294.54  | $302.42  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
