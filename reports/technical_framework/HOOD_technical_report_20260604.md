# HOOD Technical Analysis Sample

Generated: 2026-06-04 19:39:20
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (86/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [HOOD_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/HOOD_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $88.33             |
| SMA20             | $80.16             |
| SMA50             | $78.05             |
| SMA200            | $103.42            |
| RSI14             | 58.2               |
| MACD / Signal     | 2.49 / 1.31        |
| ADX14 / +DI / -DI | 22.2 / 30.4 / 14.1 |
| ATR14             | $5.22 (5.90%)      |
| 63-day range      | $63.51 - $94.40    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 88.33 vs 80.16               |
| Trend        | Close above SMA50                         | 8      | 8   | 88.33 vs 78.05               |
| Trend        | Close above SMA200                        | 0      | 8   | 88.33 vs 103.42              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 80.16 vs 78.05               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 78.05 vs 103.42              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 1.51                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 58.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 2.49 vs 1.31                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.84               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 11.74%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.20x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1404687448 vs 1343404412     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.67x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 22.2, +DI 30.4, -DI 14.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 92.28               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.90%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 6.43%                        |

## Support And Resistance

- Support levels: $63.51, $70.61, $74.25, $80.58
- Resistance levels: $88.60, $93.76, $111.46, $120.88, $124.35

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $79.09 - $83.00 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $72.84 | $97.48   | $105.69  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $88.60 - $91.21 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $81.70 | $106.31  | $114.51  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
