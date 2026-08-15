# SHLD Technical Analysis Sample

Generated: 2026-06-08 21:13:28
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (23/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SHLD_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SHLD_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $63.07             |
| SMA20             | $64.64             |
| SMA50             | $68.25             |
| SMA200            | $68.77             |
| RSI14             | 38.7               |
| MACD / Signal     | -1.13 / -1.13      |
| ADX14 / +DI / -DI | 29.4 / 18.7 / 34.6 |
| ATR14             | $1.36 (2.15%)      |
| 63-day range      | $62.21 - $77.73    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 63.07 vs 64.64               |
| Trend        | Close above SMA50                         | 0      | 8   | 63.07 vs 68.25               |
| Trend        | Close above SMA200                        | 0      | 8   | 63.07 vs 68.77               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 64.64 vs 68.25               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 68.25 vs 68.77               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.33                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 38.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | -1.13 vs -1.13               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.55              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -3.34%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.59x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 32630186 vs 32784314         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.14x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 29.4, +DI 18.7, -DI 34.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 67.47               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.15%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 18.86%                       |

## Support And Resistance

- Support levels: $62.26
- Resistance levels: $65.06, $66.46, $67.89, $69.03, $75.05

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $68.25 - $68.93 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $66.21 | $72.32   | $75.04   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $61.58 - $62.60 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $60.90 | $65.06   | $66.17   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $65.06 - $65.74 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $62.26 | $71.69   | $74.83   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
