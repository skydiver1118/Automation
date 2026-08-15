# AMD Technical Analysis Sample

Generated: 2026-06-02 16:57:49
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (92/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AMD_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AMD_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $521.54            |
| SMA20             | $456.58            |
| SMA50             | $340.65            |
| SMA200            | $240.91            |
| RSI14             | 75.2               |
| MACD / Signal     | 49.54 / 47.85      |
| ADX14 / +DI / -DI | 46.8 / 35.2 / 14.5 |
| ATR14             | $26.00 (4.99%)     |
| 63-day range      | $189.02 - $527.20  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 521.54 vs 456.58             |
| Trend        | Close above SMA50                         | 8      | 8   | 521.54 vs 340.65             |
| Trend        | Close above SMA200                        | 8      | 8   | 521.54 vs 240.91             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 456.58 vs 340.65             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 340.65 vs 240.91             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 102.44                       |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 75.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 49.54 vs 47.85               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.71               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 52.70%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.59x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1271374026 vs 1251345536     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.35x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 46.8, +DI 35.2, -DI 14.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 544.38              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.99%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 1.07%                        |

## Support And Resistance

- Support levels: $210.51, $340.65, $368.79, $393.36, $452.93
- Resistance levels: $527.20, $544.38

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $443.58 - $463.09 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $314.64 | $730.71  | $869.40  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $527.20 - $540.20 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $469.53 | $662.03  | $726.20  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
