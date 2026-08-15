# MU Technical Analysis Sample

Generated: 2026-06-10 20:55:07
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (71/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MU_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MU_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $891.88             |
| SMA20             | $873.24             |
| SMA50             | $652.21             |
| SMA200            | $372.85             |
| RSI14             | 55.5                |
| MACD / Signal     | 86.90 / 100.93      |
| ADX14 / +DI / -DI | 33.3 / 25.4 / 24.8  |
| ATR14             | $73.01 (8.19%)      |
| 63-day range      | $311.49 - $1,089.29 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 891.88 vs 873.24             |
| Trend        | Close above SMA50                         | 8      | 8   | 891.88 vs 652.21             |
| Trend        | Close above SMA200                        | 8      | 8   | 891.88 vs 372.85             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 873.24 vs 652.21             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 652.21 vs 372.85             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 188.57                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 55.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | 86.90 vs 100.93              |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -37.93             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 16.35%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.98x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1108896892 vs 1115330470     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.11x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 33.3, +DI 25.4, -DI 24.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 1123.29             |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.19%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 18.12%                       |

## Support And Resistance

- Support levels: $311.49, $360.63, $435.90, $642.53, $864.14
- Resistance levels: $1,097.79

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop    | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $836.73 - $891.49     | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $579.20 | $1,433.93 | $1,718.84 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,089.29 - $1,125.80 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $873.24 | $1,576.16 | $1,810.47 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
