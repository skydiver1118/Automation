# IREN Technical Analysis Sample

Generated: 2026-06-08 21:13:39
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (66/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [IREN_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/IREN_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $59.19             |
| SMA20             | $58.60             |
| SMA50             | $50.32             |
| SMA200            | $46.97             |
| RSI14             | 52.3               |
| MACD / Signal     | 2.94 / 3.61        |
| ADX14 / +DI / -DI | 24.1 / 26.1 / 25.8 |
| ATR14             | $5.57 (9.42%)      |
| 63-day range      | $30.76 - $70.71    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 59.19 vs 58.60               |
| Trend        | Close above SMA50                         | 8      | 8   | 59.19 vs 50.32               |
| Trend        | Close above SMA200                        | 8      | 8   | 59.19 vs 46.97               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 58.60 vs 50.32               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 50.32 vs 46.97               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 7.06                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 52.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | 2.94 vs 3.61                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.44              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -3.28%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.75x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 794656477 vs 820275829       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.05x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 24.1, +DI 26.1, -DI 25.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 69.92               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.42%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 16.29%                       |

## Support And Resistance

- Support levels: $31.62, $37.79, $43.92, $49.97, $58.54
- Resistance levels: $58.75, $64.60, $70.03

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $55.82 - $60.00 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $44.75 | $84.22   | $97.38   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $64.60 - $67.39 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $58.60 | $80.78   | $88.17   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
