# AVGO Technical Analysis Sample

Generated: 2026-06-02 16:57:23
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (93/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AVGO_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AVGO_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $481.57            |
| SMA20             | $428.09            |
| SMA50             | $391.92            |
| SMA200            | $353.01            |
| RSI14             | 74.8               |
| MACD / Signal     | 15.29 / 11.94      |
| ADX14 / +DI / -DI | 26.9 / 41.3 / 12.1 |
| ATR14             | $17.24 (3.58%)     |
| 63-day range      | $289.96 - $488.82  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 481.57 vs 428.09             |
| Trend        | Close above SMA50                         | 8      | 8   | 481.57 vs 391.92             |
| Trend        | Close above SMA200                        | 8      | 8   | 481.57 vs 353.01             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 428.09 vs 391.92             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 391.92 vs 353.01             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 41.04                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 74.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | 15.29 vs 11.94               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 6.99               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 15.62%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.62x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1330810580 vs 1260188454     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.02x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 26.9, +DI 41.3, -DI 12.1 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 462.84              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.58%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 1.48%                        |

## Support And Resistance

- Support levels: $329.81, $369.17, $393.31, $405.65, $427.87
- Resistance levels: $488.82

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $419.47 - $432.40 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $374.68 | $528.45  | $579.71  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $488.82 - $497.44 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $447.08 | $585.22  | $631.27  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
