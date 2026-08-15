# TSSI Technical Analysis Sample

Generated: 2026-06-04 19:39:45
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (72/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSSI_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSSI_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $14.49             |
| SMA20             | $12.84             |
| SMA50             | $13.69             |
| SMA200            | $12.65             |
| RSI14             | 54.5               |
| MACD / Signal     | 0.32 / 0.00        |
| ADX14 / +DI / -DI | 25.7 / 30.1 / 21.0 |
| ATR14             | $1.40 (9.66%)      |
| 63-day range      | $8.65 - $17.49     |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 14.49 vs 12.84               |
| Trend        | Close above SMA50                         | 8      | 8   | 14.49 vs 13.69               |
| Trend        | Close above SMA200                        | 8      | 8   | 14.49 vs 12.65               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 12.84 vs 13.69               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 13.69 vs 12.65               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.82                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 54.5                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.32 vs 0.00                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.22               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -15.21%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.54x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 25669445 vs 21859322         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.99x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 25.7, +DI 30.1, -DI 21.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 16.47               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.66%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.15%                       |

## Support And Resistance

- Support levels: $7.23, $8.84, $10.25, $11.67, $13.67
- Resistance levels: $14.36, $17.17

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $12.99 - $14.04 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $12.29 | $17.17   | $17.72   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $17.17 - $17.87 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $13.69 | $25.18   | $29.01   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
