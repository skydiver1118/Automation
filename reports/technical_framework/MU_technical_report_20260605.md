# MU Technical Analysis Sample

Generated: 2026-06-05 16:40:38
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (88/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MU_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MU_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $864.01             |
| SMA20             | $849.82             |
| SMA50             | $617.35             |
| SMA200            | $360.72             |
| RSI14             | 55.2                |
| MACD / Signal     | 109.04 / 107.09     |
| ADX14 / +DI / -DI | 40.3 / 35.1 / 26.6  |
| ATR14             | $65.79 (7.61%)      |
| 63-day range      | $311.49 - $1,089.29 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 864.01 vs 849.82             |
| Trend        | Close above SMA50                         | 8      | 8   | 864.01 vs 617.35             |
| Trend        | Close above SMA200                        | 8      | 8   | 864.01 vs 360.72             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 849.82 vs 617.35             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 617.35 vs 360.72             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 175.09                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 55.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 109.04 vs 107.09             |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -14.47             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 33.62%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.33x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1225040897 vs 1134598375     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.42x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 40.3, +DI 35.1, -DI 26.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 1105.04             |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.61%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 20.68%                       |

## Support And Resistance

- Support levels: $360.63, $435.90, $605.98, $652.21, $853.05
- Resistance levels: $1,093.23

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop    | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $820.15 - $869.49     | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $551.56 | $1,431.35 | $1,724.61 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,089.29 - $1,122.19 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $853.05 | $1,611.12 | $1,863.82 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
