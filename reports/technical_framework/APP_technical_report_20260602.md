# APP Technical Analysis Sample

Generated: 2026-06-02 16:57:22
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (86/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APP_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APP_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value             |
| ----------------- | ----------------- |
| Close             | $605.63           |
| SMA20             | $512.83           |
| SMA50             | $464.66           |
| SMA200            | $538.07           |
| RSI14             | 71.4              |
| MACD / Signal     | 37.37 / 24.36     |
| ADX14 / +DI / -DI | 28.5 / 32.9 / 9.2 |
| ATR14             | $33.74 (5.57%)    |
| 63-day range      | $364.64 - $622.00 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                    |
| ------------ | ----------------------------------------- | ------ | --- | --------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 605.63 vs 512.83            |
| Trend        | Close above SMA50                         | 8      | 8   | 605.63 vs 464.66            |
| Trend        | Close above SMA200                        | 8      | 8   | 605.63 vs 538.07            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 512.83 vs 464.66            |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 464.66 vs 538.07            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 24.30                       |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 71.4                  |
| Momentum     | MACD above signal                         | 7      | 7   | 37.37 vs 24.36              |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 11.96             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 27.50%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.47x                       |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 409383300 vs 385339825      |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.99x                       |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 28.5, +DI 32.9, -DI 9.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 620.61             |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.57%                 |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 2.63%                       |

## Support And Resistance

- Support levels: $409.05, $436.62, $462.83, $515.46, $585.76
- Resistance levels: $621.65, $679.69, $732.42

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2  | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $568.88 - $594.19 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $430.92 | $882.78  | $1,033.39 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $621.65 - $638.52 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $585.76 | $718.76  | $763.09   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
