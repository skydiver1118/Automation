# CRWV Technical Analysis Sample

Generated: 2026-06-28 17:42:20
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (26/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWV_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWV_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $96.58             |
| SMA20             | $106.79            |
| SMA50             | $110.84            |
| SMA200            | $100.66            |
| RSI14             | 41.6               |
| MACD / Signal     | -1.61 / -0.66      |
| ADX14 / +DI / -DI | 11.5 / 23.8 / 30.8 |
| ATR14             | $8.58 (8.89%)      |
| 63-day range      | $67.15 - $138.25   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 96.58 vs 106.79              |
| Trend        | Close above SMA50                         | 0      | 8   | 96.58 vs 110.84              |
| Trend        | Close above SMA200                        | 0      | 8   | 96.58 vs 100.66              |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 106.79 vs 110.84             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 110.84 vs 100.66             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 7.61                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 41.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | -1.61 vs -0.66               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.39              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -9.62%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.49x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 466619400 vs 525833940       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.80x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 11.5, +DI 23.8, -DI 30.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 124.25              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.89%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 30.14%                       |

## Support And Resistance

- Support levels: $69.97, $77.58, $87.98, $94.16
- Resistance levels: $101.26, $114.45, $123.34, $132.15, $138.25

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $110.84 - $115.13 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $97.96 | $136.58  | $153.75  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $89.87 - $96.31   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $85.58 | $110.25  | $118.83  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $101.26 - $105.55 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $94.16 | $121.90  | $131.15  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
