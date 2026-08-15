# HOOD Technical Analysis Sample

Generated: 2026-06-10 20:55:05
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (74/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [HOOD_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/HOOD_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $86.36             |
| SMA20             | $81.42             |
| SMA50             | $79.32             |
| SMA200            | $102.96            |
| RSI14             | 55.2               |
| MACD / Signal     | 2.09 / 1.79        |
| ADX14 / +DI / -DI | 21.1 / 24.8 / 17.3 |
| ATR14             | $5.73 (6.64%)      |
| 63-day range      | $63.51 - $94.40    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 86.36 vs 81.42               |
| Trend        | Close above SMA50                         | 8      | 8   | 86.36 vs 79.32               |
| Trend        | Close above SMA200                        | 0      | 8   | 86.36 vs 102.96              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 81.42 vs 79.32               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 79.32 vs 102.96              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 2.76                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 55.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 2.09 vs 1.79                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.88              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 10.34%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.47x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1381261045 vs 1339319197     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.50x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 21.1, +DI 24.8, -DI 17.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 93.72               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.64%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 8.52%                        |

## Support And Resistance

- Support levels: $63.51, $70.73, $74.25, $80.57
- Resistance levels: $92.90, $111.46, $120.88, $124.35, $139.75

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $79.73 - $84.03 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $73.59 | $98.47   | $106.76  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $92.90 - $95.77 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $82.60 | $117.80  | $129.54  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
