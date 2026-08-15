# CHAT Technical Analysis Sample

Generated: 2026-06-04 19:39:16
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (92/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CHAT_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CHAT_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $100.23            |
| SMA20             | $91.41             |
| SMA50             | $79.75             |
| SMA200            | $65.14             |
| RSI14             | 71.0               |
| MACD / Signal     | 6.26 / 5.46        |
| ADX14 / +DI / -DI | 35.7 / 40.0 / 22.2 |
| ATR14             | $3.11 (3.11%)      |
| 63-day range      | $58.52 - $104.21   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 100.23 vs 91.41              |
| Trend        | Close above SMA50                         | 8      | 8   | 100.23 vs 79.75              |
| Trend        | Close above SMA200                        | 8      | 8   | 100.23 vs 65.14              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 91.41 vs 79.75               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 79.75 vs 65.14               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.02                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 71.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 6.26 vs 5.46                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.24               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 16.72%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.98x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 21977748 vs 19870432         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.91x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 35.7, +DI 40.0, -DI 22.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 105.25              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.11%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 3.82%                        |

## Support And Resistance

- Support levels: $74.70, $77.57, $80.92, $91.70, $96.80
- Resistance levels: $104.47

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $95.24 - $97.58   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $76.64 | $135.95  | $155.72  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $104.21 - $105.77 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $96.80 | $121.36  | $129.55  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
