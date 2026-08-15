# APLD Technical Analysis Sample

Generated: 2026-05-31 20:26:19
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (93/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APLD_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APLD_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $47.28             |
| SMA20             | $42.98             |
| SMA50             | $34.38             |
| SMA200            | $29.24             |
| RSI14             | 60.0               |
| MACD / Signal     | 3.65 / 3.41        |
| ADX14 / +DI / -DI | 31.0 / 28.7 / 16.0 |
| ATR14             | $3.99 (8.44%)      |
| 63-day range      | $20.00 - $50.72    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 47.28 vs 42.98               |
| Trend        | Close above SMA50                         | 8      | 8   | 47.28 vs 34.38               |
| Trend        | Close above SMA200                        | 8      | 8   | 47.28 vs 29.24               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 42.98 vs 34.38               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 34.38 vs 29.24               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 5.96                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 60.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 3.65 vs 3.41                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.37               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 38.04%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.93x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1663966500 vs 1645821270     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.44x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 31.0, +DI 28.7, -DI 16.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 52.01               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.44%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 6.79%                        |

## Support And Resistance

- Support levels: $27.62, $31.41, $34.67, $38.83, $42.72
- Resistance levels: $47.79, $51.05

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $40.98 - $43.98 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $30.39 | $66.66   | $78.75   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $47.79 - $49.78 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $42.98 | $60.41   | $66.21   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
