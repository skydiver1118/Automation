# CRWD Technical Analysis Sample

Generated: 2026-07-06 16:40:13
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (92/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWD_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWD_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value             |
| ----------------- | ----------------- |
| Close             | $199.38           |
| SMA20             | $174.98           |
| SMA50             | $156.81           |
| SMA200            | $126.08           |
| RSI14             | 74.6              |
| MACD / Signal     | 9.48 / 7.86       |
| ADX14 / +DI / -DI | 34.3 / 37.3 / 9.9 |
| ATR14             | $9.19 (4.61%)     |
| 63-day range      | $91.12 - $209.49  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                    |
| ------------ | ----------------------------------------- | ------ | --- | --------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 199.38 vs 174.98            |
| Trend        | Close above SMA50                         | 8      | 8   | 199.38 vs 156.81            |
| Trend        | Close above SMA200                        | 8      | 8   | 199.38 vs 126.08            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 174.98 vs 156.81            |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 156.81 vs 126.08            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 29.31                       |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 74.6                  |
| Momentum     | MACD above signal                         | 7      | 7   | 9.48 vs 7.86                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.40              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 10.91%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.77x                       |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 106878941 vs 28266782       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.46x                       |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 34.3, +DI 37.3, -DI 9.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 197.40             |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.61%                 |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 4.83%                       |

## Support And Resistance

- Support levels: $90.40, $109.80, $155.52, $165.23, $176.19
- Resistance levels: $209.49

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $172.81 - $179.70 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $147.62 | $233.53  | $262.16  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $209.49 - $214.08 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $181.00 | $273.36  | $304.15  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
