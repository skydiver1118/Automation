# QTUM Technical Analysis Sample

Generated: 2026-06-03 19:37:07
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (92/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QTUM_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QTUM_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $167.76            |
| SMA20             | $151.17            |
| SMA50             | $133.18            |
| SMA200            | $115.14            |
| RSI14             | 77.4               |
| MACD / Signal     | 9.00 / 7.76        |
| ADX14 / +DI / -DI | 38.0 / 43.7 / 12.8 |
| ATR14             | $4.29 (2.56%)      |
| 63-day range      | $101.41 - $170.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 167.76 vs 151.17             |
| Trend        | Close above SMA50                         | 8      | 8   | 167.76 vs 133.18             |
| Trend        | Close above SMA200                        | 8      | 8   | 167.76 vs 115.14             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 151.17 vs 133.18             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 133.18 vs 115.14             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 15.51                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 77.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 9.00 vs 7.76                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.61               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 20.54%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.88x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 24261773 vs 19585574         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.28x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 38.0, +DI 43.7, -DI 12.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 169.14              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.56%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 1.32%                        |

## Support And Resistance

- Support levels: $114.63, $127.52, $133.19, $137.66, $151.27
- Resistance levels: $169.78

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $149.23 - $152.45 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $128.89 | $194.75  | $216.70  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $169.78 - $171.93 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $159.18 | $194.21  | $205.89  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
