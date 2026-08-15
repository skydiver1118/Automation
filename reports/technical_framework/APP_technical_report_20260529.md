# APP Technical Analysis Sample

Generated: 2026-05-31 20:25:39
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (87/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APP_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APP_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $613.09            |
| SMA20             | $498.62            |
| SMA50             | $457.92            |
| SMA200            | $536.37            |
| RSI14             | 73.8               |
| MACD / Signal     | 30.38 / 17.66      |
| ADX14 / +DI / -DI | 24.1 / 36.5 / 10.6 |
| ATR14             | $34.12 (5.57%)     |
| 63-day range      | $364.64 - $616.67  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 613.09 vs 498.62             |
| Trend        | Close above SMA50                         | 8      | 8   | 613.09 vs 457.92             |
| Trend        | Close above SMA200                        | 8      | 8   | 613.09 vs 536.37             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 498.62 vs 457.92             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 457.92 vs 536.37             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 19.64                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 73.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | 30.38 vs 17.66               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 12.93              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 37.36%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.15x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 404707900 vs 378216065       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.23x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 24.1, +DI 36.5, -DI 10.6 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 586.36              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.57%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.58%                        |

## Support And Resistance

- Support levels: $415.81, $453.97, $504.77, $563.50, $595.51
- Resistance levels: $616.67, $679.69, $732.42

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2  | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $578.45 - $604.04 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $423.80 | $926.14  | $1,093.59 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $616.67 - $633.73 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $595.51 | $693.45  | $727.57   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
