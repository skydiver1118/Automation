# CHAT Technical Analysis Sample

Generated: 2026-06-03 19:36:48
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (83/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CHAT_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CHAT_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $102.77            |
| SMA20             | $90.69             |
| SMA50             | $79.02             |
| SMA200            | $64.91             |
| RSI14             | 78.4               |
| MACD / Signal     | 6.36 / 5.26        |
| ADX14 / +DI / -DI | 36.3 / 46.4 / 15.4 |
| ATR14             | $2.89 (2.82%)      |
| 63-day range      | $58.52 - $104.21   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 102.77 vs 90.69              |
| Trend        | Close above SMA50                         | 8      | 8   | 102.77 vs 79.02              |
| Trend        | Close above SMA200                        | 8      | 8   | 102.77 vs 64.91              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 90.69 vs 79.02               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 79.02 vs 64.91               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 10.70                        |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 78.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 6.36 vs 5.26                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.76               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 24.81%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.94x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 22827828 vs 19747406         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.88x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 36.3, +DI 46.4, -DI 15.4 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 104.08              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.82%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 1.38%                        |

## Support And Resistance

- Support levels: $62.69, $74.70, $78.16, $81.50, $90.93
- Resistance levels: $104.18

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $89.72 - $91.89   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $76.13 | $120.14  | $134.81  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $104.18 - $105.63 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $96.98 | $120.74  | $128.66  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
