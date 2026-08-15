# PLTR Technical Analysis Sample

Generated: 2026-06-02 16:57:33
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (62/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [PLTR_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/PLTR_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $152.17            |
| SMA20             | $138.94            |
| SMA50             | $141.92            |
| SMA200            | $161.52            |
| RSI14             | 59.6               |
| MACD / Signal     | 2.65 / -0.04       |
| ADX14 / +DI / -DI | 16.7 / 34.4 / 21.2 |
| ATR14             | $6.97 (4.58%)      |
| 63-day range      | $122.68 - $163.70  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 152.17 vs 138.94             |
| Trend        | Close above SMA50                         | 8      | 8   | 152.17 vs 141.92             |
| Trend        | Close above SMA200                        | 0      | 8   | 152.17 vs 161.52             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 138.94 vs 141.92             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 141.92 vs 161.52             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -3.48                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 59.6                   |
| Momentum     | MACD above signal                         | 7      | 7   | 2.65 vs -0.04                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.28               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 4.20%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.95x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 4526242973 vs 4399336864     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.47x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 16.7, +DI 34.4, -DI 21.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 155.13              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.58%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 7.04%                        |

## Support And Resistance

- Support levels: $125.40, $133.44, $141.05, $148.83
- Resistance levels: $154.10, $163.34, $172.00, $182.43, $188.83

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $145.35 - $150.58 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $134.95 | $173.99  | $187.00  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $154.10 - $157.58 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $148.83 | $169.84  | $176.85  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
