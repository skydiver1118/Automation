# SMH Technical Analysis Sample

Generated: 2026-07-07 16:40:25
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (52/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SMH_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SMH_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $581.45            |
| SMA20             | $619.06            |
| SMA50             | $584.05            |
| SMA200            | $428.61            |
| RSI14             | 45.4               |
| MACD / Signal     | 6.51 / 14.95       |
| ADX14 / +DI / -DI | 16.1 / 19.5 / 36.2 |
| ATR14             | $31.14 (5.36%)     |
| 63-day range      | $389.64 - $671.83  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 581.45 vs 619.06             |
| Trend        | Close above SMA50                         | 0      | 8   | 581.45 vs 584.05             |
| Trend        | Close above SMA200                        | 8      | 8   | 581.45 vs 428.61             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 619.06 vs 584.05             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 584.05 vs 428.61             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 77.11                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 45.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | 6.51 vs 14.95                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -4.82              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 2.06%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.11x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 253404081 vs 275702514       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.77x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 16.1, +DI 19.5, -DI 36.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 671.10              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.36%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.45%                       |

## Support And Resistance

- Support levels: $377.24, $397.77, $527.87, $562.84, $584.05
- Resistance levels: $581.17, $651.26, $671.65

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $619.06 - $634.63 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $572.35 | $712.48  | $774.76  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $547.27 - $570.62 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $531.70 | $651.26  | $652.37  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $651.26 - $666.83 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $562.84 | $851.45  | $947.65  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
