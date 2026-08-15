# IREN Technical Analysis Sample

Generated: 2026-06-10 20:55:27
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (41/100).**

Not bullish under the framework; classify as Bearish because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [IREN_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/IREN_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $51.52             |
| SMA20             | $58.29             |
| SMA50             | $51.10             |
| SMA200            | $47.29             |
| RSI14             | 44.4               |
| MACD / Signal     | 1.43 / 2.95        |
| ADX14 / +DI / -DI | 22.1 / 21.5 / 25.8 |
| ATR14             | $5.82 (11.31%)     |
| 63-day range      | $30.76 - $70.71    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 51.52 vs 58.29               |
| Trend        | Close above SMA50                         | 8      | 8   | 51.52 vs 51.10               |
| Trend        | Close above SMA200                        | 8      | 8   | 51.52 vs 47.29               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 58.29 vs 51.10               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 51.10 vs 47.29               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 7.25                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 44.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | 1.43 vs 2.95                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.19              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -8.91%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.79x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 669586132 vs 783010082       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.81x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 22.1, +DI 21.5, -DI 25.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 70.10               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 11.31%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 27.14%                       |

## Support And Resistance

- Support levels: $31.62, $37.79, $44.44, $50.83
- Resistance levels: $54.14, $58.75, $64.60, $70.07

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $58.29 - $61.21 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $49.56 | $75.77   | $87.42   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $48.19 - $52.55 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $45.27 | $62.02   | $67.84   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $54.14 - $57.05 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $51.10 | $67.25   | $73.07   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
