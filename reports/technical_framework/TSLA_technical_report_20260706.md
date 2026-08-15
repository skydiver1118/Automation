# TSLA Technical Analysis Sample

Generated: 2026-07-06 16:40:28
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (81/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSLA_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSLA_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $419.77            |
| SMA20             | $399.22            |
| SMA50             | $407.07            |
| SMA200            | $418.60            |
| RSI14             | 54.7               |
| MACD / Signal     | -0.05 / -2.64      |
| ADX14 / +DI / -DI | 15.2 / 23.7 / 25.2 |
| ATR14             | $20.32 (4.84%)     |
| 63-day range      | $337.24 - $453.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 419.77 vs 399.22             |
| Trend        | Close above SMA50                         | 8      | 8   | 419.77 vs 407.07             |
| Trend        | Close above SMA200                        | 8      | 8   | 419.77 vs 418.60             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 399.22 vs 407.07             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 407.07 vs 418.60             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.88                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 54.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.05 vs -2.64               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 6.19               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 0.32%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.03x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 2819202444 vs 2710219482     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.45x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.2, +DI 23.7, -DI 25.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 429.42              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.84%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 7.42%                        |

## Support And Resistance

- Support levels: $337.24, $363.65, $390.20, $409.54
- Resistance levels: $432.87, $452.91

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $399.38 - $414.62 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $386.74 | $447.65  | $467.97  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $432.87 - $443.03 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $409.54 | $494.78  | $523.19  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
