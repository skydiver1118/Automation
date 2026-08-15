# RKLB Technical Analysis Sample

Generated: 2026-07-06 16:40:23
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (32/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKLB_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKLB_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $93.09             |
| SMA20             | $101.13            |
| SMA50             | $106.99            |
| SMA200            | $76.11             |
| RSI14             | 43.5               |
| MACD / Signal     | -4.63 / -4.25      |
| ADX14 / +DI / -DI | 23.0 / 19.8 / 25.0 |
| ATR14             | $9.87 (10.60%)     |
| 63-day range      | $63.96 - $151.00   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 93.09 vs 101.13              |
| Trend        | Close above SMA50                         | 0      | 8   | 93.09 vs 106.99              |
| Trend        | Close above SMA200                        | 8      | 8   | 93.09 vs 76.11               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 101.13 vs 106.99             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 106.99 vs 76.11              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.60                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 43.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | -4.63 vs -4.25               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.71               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -22.39%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.65x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1770189640 vs 1799624892     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.67x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 23.0, +DI 19.8, -DI 25.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 120.08              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.60%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 38.35%                       |

## Support And Resistance

- Support levels: $56.13, $65.24, $73.99, $80.73, $92.30
- Resistance levels: $99.58, $107.60, $119.94, $138.38, $151.00

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $106.99 - $111.92 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $92.19 | $136.59  | $156.32  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $87.37 - $94.77   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $82.43 | $110.80  | $120.67  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $99.58 - $104.51  | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $92.30 | $121.78  | $131.65  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
