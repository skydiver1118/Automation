# CRWD Technical Analysis Sample

Generated: 2026-06-04 19:39:17
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (85/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWD_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWD_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $719.09            |
| SMA20             | $639.64            |
| SMA50             | $510.00            |
| SMA200            | $476.77            |
| RSI14             | 68.8               |
| MACD / Signal     | 70.26 / 63.94      |
| ADX14 / +DI / -DI | 52.8 / 39.4 / 20.3 |
| ATR14             | $34.03 (4.73%)     |
| 63-day range      | $361.81 - $785.66  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 719.09 vs 639.64             |
| Trend        | Close above SMA50                         | 8      | 8   | 719.09 vs 510.00             |
| Trend        | Close above SMA200                        | 8      | 8   | 719.09 vs 476.77             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 639.64 vs 510.00             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 510.00 vs 476.77             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 90.10                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 68.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | 70.26 vs 63.94               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.78              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 53.63%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.90x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | -25508052 vs -23744583       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.68x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 52.8, +DI 39.4, -DI 20.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 803.37              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.73%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 8.47%                        |

## Support And Resistance

- Support levels: $439.18, $475.68, $510.00, $638.88, $671.22
- Resistance levels: $790.09

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $654.21 - $679.73 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $475.97 | $1,048.95 | $1,239.95 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $785.66 - $802.67 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $671.22 | $1,040.06 | $1,163.01 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
