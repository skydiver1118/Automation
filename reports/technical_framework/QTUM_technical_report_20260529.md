# QTUM Technical Analysis Sample

Generated: 2026-05-31 20:25:55
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (97/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QTUM_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QTUM_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $159.75            |
| SMA20             | $146.70            |
| SMA50             | $129.78            |
| SMA200            | $114.05            |
| RSI14             | 73.7               |
| MACD / Signal     | 7.70 / 6.92        |
| ADX14 / +DI / -DI | 34.6 / 39.0 / 16.8 |
| ATR14             | $4.07 (2.55%)      |
| 63-day range      | $101.41 - $160.79  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 159.75 vs 146.70             |
| Trend        | Close above SMA50                         | 8      | 8   | 159.75 vs 129.78             |
| Trend        | Close above SMA200                        | 8      | 8   | 159.75 vs 114.05             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 146.70 vs 129.78             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 129.78 vs 114.05             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 13.34                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 73.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | 7.70 vs 6.92                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.13               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 19.19%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.24x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 22621100 vs 18377825         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.53x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 34.6, +DI 39.0, -DI 16.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 161.58              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.55%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.65%                        |

## Support And Resistance

- Support levels: $114.63, $128.65, $131.82, $137.66, $146.52
- Resistance levels: $160.99

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $144.66 - $147.72 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $125.71 | $187.16  | $207.65  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $160.79 - $162.83 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $151.60 | $182.22  | $192.43  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
