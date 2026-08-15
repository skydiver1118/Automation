# SMH Technical Analysis Sample

Generated: 2026-06-28 17:42:32
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (60/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SMH_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SMH_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $611.61            |
| SMA20             | $618.44            |
| SMA50             | $566.44            |
| SMA200            | $419.30            |
| RSI14             | 51.6               |
| MACD / Signal     | 18.68 / 22.48      |
| ADX14 / +DI / -DI | 17.0 / 25.1 / 26.1 |
| ATR14             | $28.91 (4.73%)     |
| 63-day range      | $359.86 - $671.83  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 611.61 vs 618.44             |
| Trend        | Close above SMA50                         | 8      | 8   | 611.61 vs 566.44             |
| Trend        | Close above SMA200                        | 8      | 8   | 611.61 vs 419.30             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 618.44 vs 566.44             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 566.44 vs 419.30             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 85.82                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 51.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | 18.68 vs 22.48               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -4.23              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 1.96%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.04x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 307609100 vs 315081670       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.97x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.0, +DI 25.1, -DI 26.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 669.84              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.73%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 8.96%                        |

## Support And Resistance

- Support levels: $371.37, $397.77, $527.87, $562.72, $612.49
- Resistance levels: $642.77, $671.33

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $551.99 - $573.67 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $537.53 | $642.77  | $649.56  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $642.77 - $657.23 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $566.44 | $817.10  | $900.66  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
