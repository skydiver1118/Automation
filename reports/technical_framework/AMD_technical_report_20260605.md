# AMD Technical Analysis Sample

Generated: 2026-06-05 16:41:00
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (65/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AMD_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AMD_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $466.38            |
| SMA20             | $473.93            |
| SMA50             | $358.72            |
| SMA200            | $245.97            |
| RSI14             | 54.5               |
| MACD / Signal     | 43.42 / 47.59      |
| ADX14 / +DI / -DI | 43.3 / 30.0 / 24.5 |
| ATR14             | $29.41 (6.31%)     |
| 63-day range      | $189.02 - $546.44  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 466.38 vs 473.93             |
| Trend        | Close above SMA50                         | 8      | 8   | 466.38 vs 358.72             |
| Trend        | Close above SMA200                        | 8      | 8   | 466.38 vs 245.97             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 473.93 vs 358.72             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 358.72 vs 245.97             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 109.24                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 54.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | 43.42 vs 47.59               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -7.12              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 14.18%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.34x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1167829124 vs 1200788416     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.88x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 43.3, +DI 30.0, -DI 24.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 551.65              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.31%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 14.65%                       |

## Support And Resistance

- Support levels: $194.21, $214.14, $358.72, $394.79, $467.29
- Resistance levels: $469.22, $527.20, $547.74

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $449.25 - $471.31 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $329.31 | $722.21  | $853.17  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $469.22 - $483.93 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $463.95 | $535.40  | $564.81  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
