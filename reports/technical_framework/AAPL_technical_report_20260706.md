# AAPL Technical Analysis Sample

Generated: 2026-07-06 16:40:10
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (95/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AAPL_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AAPL_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $312.66            |
| SMA20             | $294.87            |
| SMA50             | $294.25            |
| SMA200            | $270.70            |
| RSI14             | 62.4               |
| MACD / Signal     | 0.89 / -0.56       |
| ADX14 / +DI / -DI | 23.6 / 29.3 / 18.6 |
| ATR14             | $8.63 (2.76%)      |
| 63-day range      | $245.47 - $317.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 312.66 vs 294.87             |
| Trend        | Close above SMA50                         | 8      | 8   | 312.66 vs 294.25             |
| Trend        | Close above SMA200                        | 8      | 8   | 312.66 vs 270.70             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 294.87 vs 294.25             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 294.25 vs 270.70             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 14.27                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 62.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.89 vs -0.56                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 4.23               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 0.46%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.71x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1854724504 vs 1619444450     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.39x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 23.6, +DI 29.3, -DI 18.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 312.68              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.76%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 1.49%                        |

## Support And Resistance

- Support levels: $264.83, $275.41, $287.38, $295.08, $305.02
- Resistance levels: $315.82

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $300.71 - $307.18 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $285.63 | $340.57  | $358.89  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $315.82 - $320.13 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $305.02 | $343.87  | $356.83  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
