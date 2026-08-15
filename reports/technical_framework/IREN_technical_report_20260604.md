# IREN Technical Analysis Sample

Generated: 2026-06-04 19:39:43
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (78/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [IREN_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/IREN_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $61.86             |
| SMA20             | $58.83             |
| SMA50             | $49.63             |
| SMA200            | $46.60             |
| RSI14             | 56.0               |
| MACD / Signal     | 4.18 / 3.90        |
| ADX14 / +DI / -DI | 27.9 / 31.9 / 19.3 |
| ATR14             | $5.19 (8.39%)      |
| 63-day range      | $30.76 - $70.71    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 61.86 vs 58.83               |
| Trend        | Close above SMA50                         | 8      | 8   | 61.86 vs 49.63               |
| Trend        | Close above SMA200                        | 8      | 8   | 61.86 vs 46.60               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 58.83 vs 49.63               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 49.63 vs 46.60               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 6.96                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 56.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 4.18 vs 3.90                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.49              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 1.44%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.79x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 848273176 vs 856338949       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.08x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 27.9, +DI 31.9, -DI 19.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 70.06               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.39%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 12.51%                       |

## Support And Resistance

- Support levels: $38.10, $43.92, $48.68, $52.36, $59.11
- Resistance levels: $64.60, $70.06

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $56.51 - $60.40 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $44.44 | $86.50   | $100.51  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $64.60 - $67.20 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $59.11 | $79.48   | $86.28   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
