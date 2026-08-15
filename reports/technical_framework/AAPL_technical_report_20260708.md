# AAPL Technical Analysis Sample

Generated: 2026-07-08 16:40:10
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (89/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AAPL_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AAPL_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $313.39            |
| SMA20             | $295.63            |
| SMA50             | $295.85            |
| SMA200            | $271.44            |
| RSI14             | 62.2               |
| MACD / Signal     | 2.97 / 0.55        |
| ADX14 / +DI / -DI | 23.2 / 27.1 / 19.2 |
| ATR14             | $8.35 (2.66%)      |
| 63-day range      | $255.83 - $317.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 313.39 vs 295.63             |
| Trend        | Close above SMA50                         | 8      | 8   | 313.39 vs 295.85             |
| Trend        | Close above SMA200                        | 8      | 8   | 313.39 vs 271.44             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 295.63 vs 295.85             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 295.85 vs 271.44             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 13.79                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 62.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 2.97 vs 0.55                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 4.52               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 3.93%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.58x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1807084149 vs 1595159012     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.81x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 23.2, +DI 27.1, -DI 19.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 315.56              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.66%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 1.26%                        |

## Support And Resistance

- Support levels: $264.83, $274.73, $287.38, $296.79, $305.02
- Resistance levels: $316.26

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $300.85 - $307.11 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $287.51 | $336.92  | $353.39  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $316.26 - $320.44 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $305.02 | $345.01  | $358.34  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
