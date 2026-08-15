# VRSN Technical Analysis Sample

Generated: 2026-06-10 20:55:21
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (75/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [VRSN_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/VRSN_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $288.09            |
| SMA20             | $296.43            |
| SMA50             | $281.14            |
| SMA200            | $257.22            |
| RSI14             | 49.1               |
| MACD / Signal     | 2.18 / 4.95        |
| ADX14 / +DI / -DI | 20.6 / 18.4 / 24.5 |
| ATR14             | $8.39 (2.91%)      |
| 63-day range      | $233.58 - $312.48  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 288.09 vs 296.43             |
| Trend        | Close above SMA50                         | 8      | 8   | 288.09 vs 281.14             |
| Trend        | Close above SMA200                        | 8      | 8   | 288.09 vs 257.22             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 296.43 vs 281.14             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 281.14 vs 257.22             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 22.20                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.1                   |
| Momentum     | MACD above signal                         | 0      | 7   | 2.18 vs 4.95                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.09              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 1.07%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.20x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 24372648 vs 23398032         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.27x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 20.6, +DI 18.4, -DI 24.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 311.52              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.91%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 7.81%                        |

## Support And Resistance

- Support levels: $243.10, $252.84, $258.09, $281.21, $290.90
- Resistance levels: $302.97, $312.24

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $277.02 - $283.31 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $272.75 | $302.97  | $305.33  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $302.97 - $307.16 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $281.21 | $352.78  | $376.64  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
