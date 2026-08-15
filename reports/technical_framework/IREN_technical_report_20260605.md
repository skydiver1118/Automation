# IREN Technical Analysis Sample

Generated: 2026-06-05 16:41:02
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (51/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [IREN_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/IREN_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $54.35             |
| SMA20             | $58.70             |
| SMA50             | $49.89             |
| SMA200            | $46.77             |
| RSI14             | 46.9               |
| MACD / Signal     | 3.29 / 3.78        |
| ADX14 / +DI / -DI | 25.9 / 27.5 / 27.7 |
| ATR14             | $5.59 (10.29%)     |
| 63-day range      | $30.76 - $70.71    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 54.35 vs 58.70               |
| Trend        | Close above SMA50                         | 8      | 8   | 54.35 vs 49.89               |
| Trend        | Close above SMA200                        | 8      | 8   | 54.35 vs 46.77               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 58.70 vs 49.89               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 49.89 vs 46.77               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 6.97                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | 3.29 vs 3.78                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.23              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -4.40%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.08x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 763456789 vs 833752389       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.78x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 25.9, +DI 27.5, -DI 27.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 70.08               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.29%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 23.13%                       |

## Support And Resistance

- Support levels: $31.62, $37.79, $43.64, $49.89
- Resistance levels: $54.14, $58.75, $64.60, $70.07

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $47.09 - $51.29 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $44.29 | $60.38   | $65.97   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $58.75 - $61.55 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $49.89 | $80.67   | $90.93   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
