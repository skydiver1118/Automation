# QTUM Technical Analysis Sample

Generated: 2026-06-28 17:42:28
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (55/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QTUM_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QTUM_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $155.97            |
| SMA20             | $161.34            |
| SMA50             | $148.43            |
| SMA200            | $120.32            |
| RSI14             | 49.0               |
| MACD / Signal     | 3.54 / 4.98        |
| ADX14 / +DI / -DI | 18.8 / 19.3 / 27.1 |
| ATR14             | $5.91 (3.79%)      |
| 63-day range      | $101.24 - $169.72  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 155.97 vs 161.34             |
| Trend        | Close above SMA50                         | 8      | 8   | 155.97 vs 148.43             |
| Trend        | Close above SMA200                        | 8      | 8   | 155.97 vs 120.32             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 161.34 vs 148.43             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 148.43 vs 120.32             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 19.84                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | 3.54 vs 4.98                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.10              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -1.78%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.03x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 21392100 vs 22223895         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.87x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.8, +DI 19.3, -DI 27.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 172.01              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.79%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 8.10%                        |

## Support And Resistance

- Support levels: $114.44, $127.31, $137.43, $148.79, $155.03
- Resistance levels: $169.83

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $152.08 - $156.51 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $142.52 | $177.83  | $189.60  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $169.72 - $172.67 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $155.03 | $203.53  | $219.69  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
