# AVGO Technical Analysis Sample

Generated: 2026-06-26 06:53:08
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (36/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AVGO_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AVGO_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $378.91            |
| SMA20             | $406.25            |
| SMA50             | $412.00            |
| SMA200            | $359.86            |
| RSI14             | 43.4               |
| MACD / Signal     | -8.53 / -5.86      |
| ADX14 / +DI / -DI | 18.9 / 20.2 / 30.5 |
| ATR14             | $19.86 (5.24%)     |
| 63-day range      | $289.50 - $494.22  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 378.91 vs 406.25             |
| Trend        | Close above SMA50                         | 0      | 8   | 378.91 vs 412.00             |
| Trend        | Close above SMA200                        | 8      | 8   | 378.91 vs 359.86             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 406.25 vs 412.00             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 412.00 vs 359.86             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 31.67                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 43.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | -8.53 vs -5.86               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.92               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -10.04%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.62x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1051481800 vs 1086594590     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.83x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.9, +DI 20.2, -DI 30.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 474.68              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.24%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 23.33%                       |

## Support And Resistance

- Support levels: $291.07, $310.39, $334.80, $371.22
- Resistance levels: $414.64, $435.76, $474.68, $494.22

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $412.00 - $421.93 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $382.21 | $471.58  | $511.29  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $361.29 - $376.19 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $351.36 | $414.64  | $428.32  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $414.64 - $424.57 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $371.22 | $516.37  | $564.75  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
