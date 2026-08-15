# CRWD Technical Analysis Sample

Generated: 2026-07-07 16:40:13
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (95/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWD_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWD_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value             |
| ----------------- | ----------------- |
| Close             | $194.62           |
| SMA20             | $176.32           |
| SMA50             | $158.47           |
| SMA200            | $126.50           |
| RSI14             | 68.4              |
| MACD / Signal     | 9.65 / 8.22       |
| ADX14 / +DI / -DI | 36.0 / 34.7 / 9.2 |
| ATR14             | $9.19 (4.72%)     |
| 63-day range      | $91.12 - $209.50  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                    |
| ------------ | ----------------------------------------- | ------ | --- | --------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 194.62 vs 176.32            |
| Trend        | Close above SMA50                         | 8      | 8   | 194.62 vs 158.47            |
| Trend        | Close above SMA200                        | 8      | 8   | 194.62 vs 126.50            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 176.32 vs 158.47            |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 158.47 vs 126.50            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 29.55                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 68.4                  |
| Momentum     | MACD above signal                         | 7      | 7   | 9.65 vs 8.22                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.21              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 16.01%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.76x                       |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 98179316 vs 32739756        |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.63x                       |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 36.0, +DI 34.7, -DI 9.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 200.10             |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.72%                 |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 7.10%                       |

## Support And Resistance

- Support levels: $90.40, $109.91, $155.93, $165.23, $177.65
- Resistance levels: $198.26, $209.50

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $174.38 - $181.27 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $149.29 | $234.89  | $263.42  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $198.26 - $202.85 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $178.97 | $243.72  | $265.31  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
