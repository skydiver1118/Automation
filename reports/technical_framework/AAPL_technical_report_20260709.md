# AAPL Technical Analysis Sample

Generated: 2026-07-09 16:40:18
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (95/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AAPL_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AAPL_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $316.22            |
| SMA20             | $296.92            |
| SMA50             | $296.83            |
| SMA200            | $271.80            |
| RSI14             | 63.9               |
| MACD / Signal     | 3.96 / 1.23        |
| ADX14 / +DI / -DI | 23.0 / 26.6 / 17.8 |
| ATR14             | $8.35 (2.64%)      |
| 63-day range      | $255.83 - $317.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 316.22 vs 296.92             |
| Trend        | Close above SMA50                         | 8      | 8   | 316.22 vs 296.83             |
| Trend        | Close above SMA200                        | 8      | 8   | 316.22 vs 271.80             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 296.92 vs 296.83             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 296.83 vs 271.80             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 13.93                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 63.9                   |
| Momentum     | MACD above signal                         | 7      | 7   | 3.96 vs 1.23                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.99               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 8.83%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.69x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1792196263 vs 1553260833     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.80x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 23.0, +DI 26.6, -DI 17.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 318.69              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.64%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.37%                        |

## Support And Resistance

- Support levels: $264.83, $274.45, $287.38, $298.07, $305.02
- Resistance levels: $317.31

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $300.85 - $307.11 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $288.48 | $334.97  | $350.46  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $317.31 - $321.48 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $305.02 | $348.15  | $362.52  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
