# SMH Technical Analysis Sample

Generated: 2026-07-08 16:40:25
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (50/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SMH_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SMH_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $593.00            |
| SMA20             | $618.80            |
| SMA50             | $585.78            |
| SMA200            | $430.00            |
| RSI14             | 47.6               |
| MACD / Signal     | 4.34 / 12.83       |
| ADX14 / +DI / -DI | 16.8 / 20.6 / 34.5 |
| ATR14             | $30.33 (5.11%)     |
| 63-day range      | $414.99 - $671.83  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 593.00 vs 618.80             |
| Trend        | Close above SMA50                         | 8      | 8   | 593.00 vs 585.78             |
| Trend        | Close above SMA200                        | 8      | 8   | 593.00 vs 430.00             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 618.80 vs 585.78             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 585.78 vs 430.00             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 74.49                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 47.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | 4.34 vs 12.83                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -6.48              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -0.86%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.74x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 256435118 vs 268647161       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.98x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 16.8, +DI 20.6, -DI 34.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 671.32              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.11%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.73%                       |

## Support And Resistance

- Support levels: $375.18, $406.38, $527.87, $562.59, $585.78
- Resistance levels: $651.26, $671.70

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $570.61 - $593.36 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $555.45 | $651.26  | $672.97  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $651.26 - $666.42 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $585.78 | $804.96  | $878.02  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
