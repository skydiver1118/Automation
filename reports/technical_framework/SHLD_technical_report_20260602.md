# SHLD Technical Analysis Sample

Generated: 2026-06-02 16:57:38
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (34/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SHLD_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SHLD_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $64.86             |
| SMA20             | $65.28             |
| SMA50             | $68.98             |
| SMA200            | $68.72             |
| RSI14             | 42.7               |
| MACD / Signal     | -0.83 / -1.26      |
| ADX14 / +DI / -DI | 30.0 / 23.6 / 33.5 |
| ATR14             | $1.37 (2.12%)      |
| 63-day range      | $62.21 - $78.45    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 64.86 vs 65.28               |
| Trend        | Close above SMA50                         | 0      | 8   | 64.86 vs 68.98               |
| Trend        | Close above SMA200                        | 0      | 8   | 64.86 vs 68.72               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 65.28 vs 68.98               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 68.98 vs 68.72               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.22                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 42.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.83 vs -1.26               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.08               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -4.73%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.98x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 34169954 vs 33781678         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.87x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 30.0, +DI 23.6, -DI 33.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 68.33               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.12%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.32%                       |

## Support And Resistance

- Support levels: $60.49, $62.31, $64.85
- Resistance levels: $65.06, $66.46, $68.56, $75.05, $76.79

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $68.98 - $69.67 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $66.92 | $73.10   | $75.85   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $64.16 - $65.19 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $63.47 | $67.42   | $68.80   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $65.06 - $65.75 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $64.85 | $68.16   | $69.53   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
