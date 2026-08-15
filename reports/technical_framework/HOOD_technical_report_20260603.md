# HOOD Technical Analysis Sample

Generated: 2026-06-03 19:36:55
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (74/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [HOOD_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/HOOD_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $82.85             |
| SMA20             | $79.69             |
| SMA50             | $77.67             |
| SMA200            | $103.55            |
| RSI14             | 52.8               |
| MACD / Signal     | 2.20 / 1.02        |
| ADX14 / +DI / -DI | 21.1 / 30.3 / 15.3 |
| ATR14             | $5.17 (6.24%)      |
| 63-day range      | $63.51 - $94.40    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 82.85 vs 79.69               |
| Trend        | Close above SMA50                         | 8      | 8   | 82.85 vs 77.67               |
| Trend        | Close above SMA200                        | 0      | 8   | 82.85 vs 103.55              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 79.69 vs 77.67               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 77.67 vs 103.55              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 1.23                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 52.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | 2.20 vs 1.02                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.52               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 7.56%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.93x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1388320849 vs 1352672462     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.35x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 21.1, +DI 30.3, -DI 15.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 91.20               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.24%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 12.24%                       |

## Support And Resistance

- Support levels: $63.51, $70.63, $74.25, $80.20
- Resistance levels: $83.34, $89.90, $94.13, $111.46, $120.88

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $78.45 - $82.33 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $72.50 | $96.18   | $104.08  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $83.34 - $85.92 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $81.04 | $94.97   | $100.14  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
