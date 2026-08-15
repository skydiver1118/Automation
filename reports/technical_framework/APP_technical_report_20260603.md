# APP Technical Analysis Sample

Generated: 2026-06-03 19:36:43
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (84/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APP_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APP_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $570.83            |
| SMA20             | $517.47            |
| SMA50             | $466.90            |
| SMA200            | $538.73            |
| RSI14             | 61.5               |
| MACD / Signal     | 36.11 / 26.71      |
| ADX14 / +DI / -DI | 29.1 / 30.1 / 13.8 |
| ATR14             | $34.23 (6.00%)     |
| 63-day range      | $364.64 - $622.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 570.83 vs 517.47             |
| Trend        | Close above SMA50                         | 8      | 8   | 570.83 vs 466.90             |
| Trend        | Close above SMA200                        | 8      | 8   | 570.83 vs 538.73             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 517.47 vs 466.90             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 466.90 vs 538.73             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 24.58                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 61.5                   |
| Momentum     | MACD above signal                         | 7      | 7   | 36.11 vs 26.71               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 4.00               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 19.39%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.62x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 410049330 vs 391111022       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.27x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 29.1, +DI 30.1, -DI 13.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 626.92              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 6.00%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 8.23%                        |

## Support And Resistance

- Support levels: $363.62, $415.09, $456.97, $518.41, $565.04
- Resistance levels: $569.92, $623.23, $679.69, $732.42

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $547.92 - $573.60 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $432.67 | $816.95  | $945.05  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $622.00 - $639.12 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $565.04 | $761.59  | $827.11  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
