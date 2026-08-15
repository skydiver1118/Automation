# QTUM Technical Analysis Sample

Generated: 2026-06-08 21:13:25
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (88/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QTUM_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QTUM_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $157.74            |
| SMA20             | $153.53            |
| SMA50             | $136.12            |
| SMA200            | $116.14            |
| RSI14             | 58.2               |
| MACD / Signal     | 7.29 / 7.85        |
| ADX14 / +DI / -DI | 33.8 / 28.7 / 24.9 |
| ATR14             | $5.23 (3.32%)      |
| 63-day range      | $101.41 - $170.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 157.74 vs 153.53             |
| Trend        | Close above SMA50                         | 8      | 8   | 157.74 vs 136.12             |
| Trend        | Close above SMA200                        | 8      | 8   | 157.74 vs 116.14             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 153.53 vs 136.12             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 136.12 vs 116.14             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 16.90                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 58.2                   |
| Momentum     | MACD above signal                         | 0      | 7   | 7.29 vs 7.85                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.46              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 8.85%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.03x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 22433434 vs 20346137         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.56x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 33.8, +DI 28.7, -DI 24.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 171.34              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.32%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 7.21%                        |

## Support And Resistance

- Support levels: $108.02, $114.04, $127.52, $136.50, $153.01
- Resistance levels: $170.33

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $150.92 - $154.84 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $130.89 | $196.87  | $218.86  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $170.00 - $172.62 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $153.53 | $206.86  | $224.63  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
