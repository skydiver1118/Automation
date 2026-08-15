# HOOD Technical Analysis Sample

Generated: 2026-06-28 17:42:21
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (67/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [HOOD_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/HOOD_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $98.69             |
| SMA20             | $93.70             |
| SMA50             | $85.22             |
| SMA200            | $102.58            |
| RSI14             | 57.2               |
| MACD / Signal     | 5.03 / 5.05        |
| ADX14 / +DI / -DI | 24.4 / 23.9 / 20.0 |
| ATR14             | $6.64 (6.72%)      |
| 63-day range      | $63.51 - $112.50   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 98.69 vs 93.70               |
| Trend        | Close above SMA50                         | 8      | 8   | 98.69 vs 85.22               |
| Trend        | Close above SMA200                        | 0      | 8   | 98.69 vs 102.58              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 93.70 vs 85.22               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 85.22 vs 102.58              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 8.83                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 57.2                   |
| Momentum     | MACD above signal                         | 0      | 7   | 5.03 vs 5.05                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.19              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 16.32%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.22x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1490227500 vs 1440398175     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.13x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 24.4, +DI 23.9, -DI 20.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 109.49              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.72%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 12.28%                       |

## Support And Resistance

- Support levels: $63.51, $71.30, $78.42, $85.22, $93.35
- Resistance levels: $111.69, $122.09

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $90.38 - $95.35   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $78.59 | $121.43  | $135.71  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $111.69 - $115.01 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $93.70 | $152.65  | $172.31  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
