# CRWV Technical Analysis Sample

Generated: 2026-07-06 16:40:14
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (21/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWV_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWV_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $86.46             |
| SMA20             | $100.61            |
| SMA50             | $107.98            |
| SMA200            | $100.00            |
| RSI14             | 38.3               |
| MACD / Signal     | -5.25 / -2.90      |
| ADX14 / +DI / -DI | 15.8 / 17.4 / 33.7 |
| ATR14             | $8.55 (9.89%)      |
| 63-day range      | $79.56 - $138.25   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 86.46 vs 100.61              |
| Trend        | Close above SMA50                         | 0      | 8   | 86.46 vs 107.98              |
| Trend        | Close above SMA200                        | 0      | 8   | 86.46 vs 100.00              |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 100.61 vs 107.98             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 107.98 vs 100.00             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 1.51                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 38.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | -5.25 vs -2.90               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.40              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -19.97%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.70x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 391536767 vs 493403283       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.76x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.8, +DI 17.4, -DI 33.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 120.31              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.89%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 37.46%                       |

## Support And Resistance

- Support levels: $71.08, $80.62
- Resistance levels: $87.18, $101.26, $114.45, $122.28, $132.15

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $107.98 - $112.26 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $95.16 | $133.63  | $150.73  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $76.35 - $82.76   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $72.07 | $96.65   | $105.20  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $87.18 - $91.46   | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $80.62 | $106.72  | $115.42  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
