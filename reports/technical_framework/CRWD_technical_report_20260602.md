# CRWD Technical Analysis Sample

Generated: 2026-06-02 16:57:26
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (88/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWD_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWD_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value             |
| ----------------- | ----------------- |
| Close             | $768.95           |
| SMA20             | $613.53           |
| SMA50             | $496.79           |
| SMA200            | $473.71           |
| RSI14             | 82.6              |
| MACD / Signal     | 72.90 / 59.66     |
| ADX14 / +DI / -DI | 52.7 / 50.1 / 6.1 |
| ATR14             | $31.07 (4.04%)    |
| 63-day range      | $361.81 - $785.66 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                    |
| ------------ | ----------------------------------------- | ------ | --- | --------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 768.95 vs 613.53            |
| Trend        | Close above SMA50                         | 8      | 8   | 768.95 vs 496.79            |
| Trend        | Close above SMA200                        | 8      | 8   | 768.95 vs 473.71            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 613.53 vs 496.79            |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 496.79 vs 473.71            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 81.78                       |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 82.6                  |
| Momentum     | MACD above signal                         | 7      | 7   | 72.90 vs 59.66              |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.65              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 63.87%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.12x                       |
| Confirmation | OBV above 20-day average                  | 5      | 5   | -5029515 vs -18778121       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 3.07x                       |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 52.7, +DI 50.1, -DI 6.1 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 792.29             |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.04%                 |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 2.13%                       |

## Support And Resistance

- Support levels: $365.65, $438.30, $475.60, $496.79, $623.97
- Resistance levels: $787.32

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2  | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $609.75 - $633.05 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $465.72 | $932.76  | $1,088.45 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $785.66 - $801.20 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $706.81 | $966.67  | $1,053.28 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
