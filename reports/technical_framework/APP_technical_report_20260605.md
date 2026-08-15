# APP Technical Analysis Sample

Generated: 2026-06-05 16:40:30
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (82/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APP_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APP_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $557.20            |
| SMA20             | $524.89            |
| SMA50             | $471.77            |
| SMA200            | $540.05            |
| RSI14             | 58.1               |
| MACD / Signal     | 31.40 / 28.78      |
| ADX14 / +DI / -DI | 29.4 / 27.0 / 13.7 |
| ATR14             | $34.99 (6.28%)     |
| 63-day range      | $364.64 - $622.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 557.20 vs 524.89             |
| Trend        | Close above SMA50                         | 8      | 8   | 557.20 vs 471.77             |
| Trend        | Close above SMA200                        | 8      | 8   | 557.20 vs 540.05             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 524.89 vs 471.77             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 471.77 vs 540.05             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 26.40                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 58.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | 31.40 vs 28.78               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -10.09             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 11.69%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.11x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 399935960 vs 394094948       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.72x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 29.4, +DI 27.0, -DI 13.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 633.84              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.28%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.42%                       |

## Support And Resistance

- Support levels: $363.62, $417.07, $458.59, $522.58, $548.78
- Resistance levels: $569.92, $624.96, $679.69, $732.42

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $531.28 - $557.53 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $436.78 | $759.67  | $867.30  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $569.92 - $587.42 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $548.78 | $648.65  | $683.64  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
