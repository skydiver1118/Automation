# QTUM Technical Analysis Sample

Generated: 2026-06-04 19:39:27
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (97/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QTUM_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QTUM_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $166.49            |
| SMA20             | $152.31            |
| SMA50             | $134.30            |
| SMA200            | $115.50            |
| RSI14             | 74.7               |
| MACD / Signal     | 9.05 / 8.02        |
| ADX14 / +DI / -DI | 38.0 / 39.5 / 17.3 |
| ATR14             | $4.40 (2.64%)      |
| 63-day range      | $101.41 - $170.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 166.49 vs 152.31             |
| Trend        | Close above SMA50                         | 8      | 8   | 166.49 vs 134.30             |
| Trend        | Close above SMA200                        | 8      | 8   | 166.49 vs 115.50             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 152.31 vs 134.30             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 134.30 vs 115.50             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 16.08                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 74.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | 9.05 vs 8.02                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.27               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 15.89%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.18x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 23142645 vs 19850347         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.09x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 38.0, +DI 39.5, -DI 17.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 171.15              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.64%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 2.06%                        |

## Support And Resistance

- Support levels: $114.63, $127.52, $133.89, $137.66, $152.53
- Resistance levels: $170.29

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $150.55 - $153.85 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $129.90 | $196.81  | $219.12  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $170.00 - $172.20 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $157.68 | $197.93  | $211.35  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
