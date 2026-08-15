# VRSN Technical Analysis Sample

Generated: 2026-07-06 16:40:30
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (36/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [VRSN_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/VRSN_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $259.13            |
| SMA20             | $265.76            |
| SMA50             | $278.92            |
| SMA200            | $255.95            |
| RSI14             | 41.6               |
| MACD / Signal     | -8.26 / -8.08      |
| ADX14 / +DI / -DI | 31.6 / 16.1 / 25.4 |
| ATR14             | $8.06 (3.11%)      |
| 63-day range      | $244.74 - $312.48  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 259.13 vs 265.76             |
| Trend        | Close above SMA50                         | 0      | 8   | 259.13 vs 278.92             |
| Trend        | Close above SMA200                        | 8      | 8   | 259.13 vs 255.95             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 265.76 vs 278.92             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 278.92 vs 255.95             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.85                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 41.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | -8.26 vs -8.08               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.32               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -11.80%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.77x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 24400739 vs 25405862         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.68x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 31.6, +DI 16.1, -DI 25.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 295.80              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.11%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.07%                       |

## Support And Resistance

- Support levels: $209.34, $235.11, $243.76, $252.84, $258.09
- Resistance levels: $260.00, $279.87, $295.82, $302.97, $312.48

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $278.92 - $282.95 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $266.82 | $303.11  | $319.24  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $254.06 - $260.11 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $250.03 | $273.21  | $281.28  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $260.00 - $264.03 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $258.09 | $278.14  | $286.21  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
