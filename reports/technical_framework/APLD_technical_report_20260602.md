# APLD Technical Analysis Sample

Generated: 2026-06-02 16:57:52
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (93/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APLD_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APLD_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $47.86             |
| SMA20             | $44.31             |
| SMA50             | $35.24             |
| SMA200            | $29.57             |
| RSI14             | 60.7               |
| MACD / Signal     | 3.55 / 3.47        |
| ADX14 / +DI / -DI | 29.9 / 25.5 / 16.0 |
| ATR14             | $3.95 (8.26%)      |
| 63-day range      | $20.00 - $50.72    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 47.86 vs 44.31               |
| Trend        | Close above SMA50                         | 8      | 8   | 47.86 vs 35.24               |
| Trend        | Close above SMA200                        | 8      | 8   | 47.86 vs 29.57               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 44.31 vs 35.24               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 35.24 vs 29.57               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 6.65                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 60.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | 3.55 vs 3.47                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.08               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 34.33%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.71x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1664049017 vs 1652495981     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.13x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 29.9, +DI 25.5, -DI 16.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 51.68               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.26%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 5.65%                        |

## Support And Resistance

- Support levels: $27.62, $31.41, $35.95, $38.83, $43.86
- Resistance levels: $47.79, $50.96

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $42.33 - $45.30 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $31.29 | $68.87   | $81.40   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $50.72 - $52.70 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $44.31 | $66.52   | $73.93   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
