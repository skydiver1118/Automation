# CRWD Technical Analysis Sample

Generated: 2026-07-08 16:40:13
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (90/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWD_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWD_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $191.12            |
| SMA20             | $177.64            |
| SMA50             | $160.06            |
| SMA200            | $126.82            |
| RSI14             | 64.2               |
| MACD / Signal     | 9.40 / 8.46        |
| ADX14 / +DI / -DI | 36.2 / 31.9 / 13.8 |
| ATR14             | $9.27 (4.85%)      |
| 63-day range      | $91.12 - $209.50   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 191.12 vs 177.64             |
| Trend        | Close above SMA50                         | 8      | 8   | 191.12 vs 160.06             |
| Trend        | Close above SMA200                        | 8      | 8   | 191.12 vs 126.82             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 177.64 vs 160.06             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 160.06 vs 126.82             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 29.80                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 64.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 9.40 vs 8.46                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.79               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 16.04%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.64x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 102157079 vs 49313399        |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.97x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 36.2, +DI 31.9, -DI 13.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 201.64              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.85%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 8.77%                        |

## Support And Resistance

- Support levels: $109.91, $156.60, $165.23, $178.86, $185.30
- Resistance levels: $199.03, $209.50

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $180.66 - $187.62 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $150.79 | $250.85  | $284.21  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $199.03 - $203.66 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $185.30 | $233.43  | $249.47  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
