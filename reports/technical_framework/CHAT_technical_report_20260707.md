# CHAT Technical Analysis Sample

Generated: 2026-07-07 16:40:12
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (37/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CHAT_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CHAT_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $87.60             |
| SMA20             | $94.70             |
| SMA50             | $90.57             |
| SMA200            | $69.43             |
| RSI14             | 43.1               |
| MACD / Signal     | 0.02 / 1.52        |
| ADX14 / +DI / -DI | 17.1 / 21.2 / 39.2 |
| ATR14             | $4.53 (5.17%)      |
| 63-day range      | $62.78 - $105.20   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 87.60 vs 94.70               |
| Trend        | Close above SMA50                         | 0      | 8   | 87.60 vs 90.57               |
| Trend        | Close above SMA200                        | 8      | 8   | 87.60 vs 69.43               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 94.70 vs 90.57               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 90.57 vs 69.43               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 10.30                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 43.1                   |
| Momentum     | MACD above signal                         | 0      | 7   | 0.02 vs 1.52                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.73              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -3.36%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.88x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 19148290 vs 19868874         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.85x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.1, +DI 21.2, -DI 39.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 103.52              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.17%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 16.73%                       |

## Support And Resistance

- Support levels: $59.07, $62.71, $74.70, $81.50, $85.93
- Resistance levels: $89.07, $104.67

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $94.70 - $96.96 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $87.90 | $108.28  | $117.34  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $83.67 - $87.06 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $81.40 | $94.42   | $98.95   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $89.07 - $91.34 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $85.93 | $99.26   | $103.79  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
