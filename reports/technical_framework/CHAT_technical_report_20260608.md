# CHAT Technical Analysis Sample

Generated: 2026-06-08 21:13:15
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (78/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CHAT_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CHAT_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $93.60             |
| SMA20             | $92.12             |
| SMA50             | $80.91             |
| SMA200            | $65.56             |
| RSI14             | 55.5               |
| MACD / Signal     | 4.81 / 5.31        |
| ADX14 / +DI / -DI | 31.2 / 29.5 / 28.0 |
| ATR14             | $3.65 (3.90%)      |
| 63-day range      | $58.52 - $104.21   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 93.60 vs 92.12               |
| Trend        | Close above SMA50                         | 8      | 8   | 93.60 vs 80.91               |
| Trend        | Close above SMA200                        | 8      | 8   | 93.60 vs 65.56               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 92.12 vs 80.91               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 80.91 vs 65.56               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.38                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 55.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | 4.81 vs 5.31                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.49              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 8.61%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.94x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 21078594 vs 20199110         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.34x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 31.2, +DI 29.5, -DI 28.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 105.27              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.90%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.18%                       |

## Support And Resistance

- Support levels: $59.12, $62.69, $74.70, $80.72, $91.52
- Resistance levels: $104.47

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $90.29 - $93.03   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $77.27 | $120.45  | $134.85  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $104.21 - $106.03 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $92.12 | $131.13  | $144.13  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
