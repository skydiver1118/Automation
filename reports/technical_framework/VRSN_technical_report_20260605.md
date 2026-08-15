# VRSN Technical Analysis Sample

Generated: 2026-06-05 16:40:54
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (77/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [VRSN_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/VRSN_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $294.92            |
| SMA20             | $296.57            |
| SMA50             | $278.95            |
| SMA200            | $256.97            |
| RSI14             | 54.7               |
| MACD / Signal     | 5.14 / 7.02        |
| ADX14 / +DI / -DI | 21.8 / 21.3 / 21.0 |
| ATR14             | $8.23 (2.79%)      |
| 63-day range      | $233.58 - $312.48  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 294.92 vs 296.57             |
| Trend        | Close above SMA50                         | 8      | 8   | 294.92 vs 278.95             |
| Trend        | Close above SMA200                        | 8      | 8   | 294.92 vs 256.97             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 296.57 vs 278.95             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 278.95 vs 256.97             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 23.58                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 54.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | 5.14 vs 7.02                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.22              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 6.19%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.60x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 24193391 vs 23869180         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.00x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 21.8, +DI 21.3, -DI 21.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 311.16              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.79%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 5.62%                        |

## Support And Resistance

- Support levels: $243.10, $252.84, $258.09, $280.97, $293.46
- Resistance levels: $302.97, $312.15

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $289.35 - $295.52 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $270.72 | $335.86  | $357.57  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $302.97 - $307.08 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $293.46 | $328.16  | $339.72  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
