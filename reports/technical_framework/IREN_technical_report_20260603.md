# IREN Technical Analysis Sample

Generated: 2026-06-03 19:37:33
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (93/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [IREN_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/IREN_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $65.48             |
| SMA20             | $58.78             |
| SMA50             | $49.21             |
| SMA200            | $46.39             |
| RSI14             | 61.4               |
| MACD / Signal     | 4.49 / 3.83        |
| ADX14 / +DI / -DI | 28.2 / 34.9 / 13.9 |
| ATR14             | $5.12 (7.82%)      |
| 63-day range      | $30.76 - $70.71    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 65.48 vs 58.78               |
| Trend        | Close above SMA50                         | 8      | 8   | 65.48 vs 49.21               |
| Trend        | Close above SMA200                        | 8      | 8   | 65.48 vs 46.39               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 58.78 vs 49.21               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 49.21 vs 46.39               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 6.86                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 61.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 4.49 vs 3.83                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.00               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 19.62%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.97x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 914667813 vs 876751421       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.02x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 28.2, +DI 34.9, -DI 13.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 69.97               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.82%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 7.39%                        |

## Support And Resistance

- Support levels: $38.10, $43.92, $48.55, $52.36, $58.64
- Resistance levels: $70.04

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $56.22 - $60.06 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $44.09 | $86.24   | $100.29  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $70.04 - $72.60 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $58.78 | $96.40   | $108.94  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
