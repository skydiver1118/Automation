# SHLD Technical Analysis Sample

Generated: 2026-06-26 06:53:26
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (13/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SHLD_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SHLD_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $58.20             |
| SMA20             | $63.28             |
| SMA50             | $65.65             |
| SMA200            | $68.78             |
| RSI14             | 29.0               |
| MACD / Signal     | -1.69 / -1.27      |
| ADX14 / +DI / -DI | 28.8 / 15.0 / 41.0 |
| ATR14             | $1.41 (2.43%)      |
| 63-day range      | $58.14 - $75.27    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 58.20 vs 63.28               |
| Trend        | Close above SMA50                         | 0      | 8   | 58.20 vs 65.65               |
| Trend        | Close above SMA200                        | 0      | 8   | 58.20 vs 68.78               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 63.28 vs 65.65               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 65.65 vs 68.78               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.05                        |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 29.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | -1.69 vs -1.27               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.57              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -11.19%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.27x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 18856100 vs 31440090         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.27x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 28.8, +DI 15.0, -DI 41.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 68.20               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.43%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 22.68%                       |

## Support And Resistance

- Support levels: $58.21
- Resistance levels: $65.08, $66.46, $68.13, $69.03, $75.12

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $65.65 - $66.36 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $63.53 | $69.89   | $72.72   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $55.37 - $56.43 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $54.67 | $65.08   | $60.14   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $65.08 - $65.79 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $56.08 | $84.14   | $93.49   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
