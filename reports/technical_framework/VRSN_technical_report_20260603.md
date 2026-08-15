# VRSN Technical Analysis Sample

Generated: 2026-06-03 19:37:23
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (83/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [VRSN_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/VRSN_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $297.08            |
| SMA20             | $294.77            |
| SMA50             | $277.01            |
| SMA200            | $256.69            |
| RSI14             | 57.0               |
| MACD / Signal     | 6.28 / 7.96        |
| ADX14 / +DI / -DI | 24.8 / 22.6 / 20.8 |
| ATR14             | $8.60 (2.90%)      |
| 63-day range      | $233.58 - $312.48  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 297.08 vs 294.77             |
| Trend        | Close above SMA50                         | 8      | 8   | 297.08 vs 277.01             |
| Trend        | Close above SMA200                        | 8      | 8   | 297.08 vs 256.69             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 294.77 vs 277.01             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 277.01 vs 256.69             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 24.16                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 57.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | 6.28 vs 7.96                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.01              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 8.01%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.53x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 24221586 vs 23761639         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.27x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 24.8, +DI 22.6, -DI 20.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 313.99              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.90%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 4.93%                        |

## Support And Resistance

- Support levels: $252.84, $258.09, $276.28, $281.99, $293.59
- Resistance levels: $302.97, $312.86

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $290.47 - $296.92 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $268.40 | $344.28  | $369.58  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $302.97 - $307.27 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $294.77 | $325.82  | $336.17  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
