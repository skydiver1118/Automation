# MU Technical Analysis Sample

Generated: 2026-06-26 06:53:16
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (98/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MU_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MU_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $1,213.56           |
| SMA20             | $1,024.97           |
| SMA50             | $788.62             |
| SMA200            | $420.72             |
| RSI14             | 64.5                |
| MACD / Signal     | 96.50 / 93.93       |
| ADX14 / +DI / -DI | 24.7 / 35.0 / 22.6  |
| ATR14             | $95.41 (7.86%)      |
| 63-day range      | $311.49 - $1,255.00 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 1213.56 vs 1024.97           |
| Trend        | Close above SMA50                         | 8      | 8   | 1213.56 vs 788.62            |
| Trend        | Close above SMA200                        | 8      | 8   | 1213.56 vs 420.72            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1024.97 vs 788.62            |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 788.62 vs 420.72             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 250.51                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 64.5                   |
| Momentum     | MACD above signal                         | 7      | 7   | 96.50 vs 93.93               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 7.30               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 30.71%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.46x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1193149700 vs 1149905535     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.26x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 24.7, +DI 35.0, -DI 22.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 1212.18             |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.86%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 3.30%                        |

## Support And Resistance

- Support levels: $360.63, $435.90, $652.21, $826.91, $1,006.90
- Resistance levels: $1,244.29

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop      | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | --------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $977.27 - $1,048.82   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $693.21   | $1,652.71 | $1,972.54 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,244.29 - $1,292.00 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $1,024.97 | $1,754.50 | $1,997.68 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
