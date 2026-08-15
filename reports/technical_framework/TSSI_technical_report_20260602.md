# TSSI Technical Analysis Sample

Generated: 2026-06-02 16:57:53
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (82/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSSI_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSSI_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $15.09             |
| SMA20             | $13.07             |
| SMA50             | $13.63             |
| SMA200            | $12.66             |
| RSI14             | 58.0               |
| MACD / Signal     | 0.29 / -0.16       |
| ADX14 / +DI / -DI | 27.1 / 34.3 / 16.3 |
| ATR14             | $1.39 (9.22%)      |
| 63-day range      | $8.65 - $17.49     |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 15.09 vs 13.07               |
| Trend        | Close above SMA50                         | 8      | 8   | 15.09 vs 13.63               |
| Trend        | Close above SMA200                        | 8      | 8   | 15.09 vs 12.66               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 13.07 vs 13.63               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 13.63 vs 12.66               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 1.10                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 58.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.29 vs -0.16                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.55               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 3.64%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.00x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 26255834 vs 22131597         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.97x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 27.1, +DI 34.3, -DI 16.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 17.30               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.22%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.72%                       |

## Support And Resistance

- Support levels: $7.23, $8.71, $10.25, $11.67, $13.70
- Resistance levels: $17.31

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $13.01 - $14.05 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $12.24 | $17.31   | $17.70   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $17.31 - $18.00 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $13.70 | $25.56   | $29.52   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
