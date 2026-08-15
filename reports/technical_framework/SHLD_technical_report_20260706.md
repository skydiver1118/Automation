# SHLD Technical Analysis Sample

Generated: 2026-07-06 16:40:25
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (59/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SHLD_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SHLD_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $64.84             |
| SMA20             | $61.79             |
| SMA50             | $64.09             |
| SMA200            | $68.45             |
| RSI14             | 58.5               |
| MACD / Signal     | -0.82 / -1.35      |
| ADX14 / +DI / -DI | 27.6 / 35.8 / 25.9 |
| ATR14             | $1.48 (2.28%)      |
| 63-day range      | $57.70 - $75.03    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 64.84 vs 61.79               |
| Trend        | Close above SMA50                         | 8      | 8   | 64.84 vs 64.09               |
| Trend        | Close above SMA200                        | 0      | 8   | 64.84 vs 68.45               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 61.79 vs 64.09               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 64.09 vs 68.45               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.32                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 58.5                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.82 vs -1.35               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.97               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 1.15%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.53x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 30706572 vs 30413319         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.86x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 27.6, +DI 35.8, -DI 25.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 66.25               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.28%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.58%                       |

## Support And Resistance

- Support levels: $57.58, $61.88, $64.48
- Resistance levels: $64.97, $66.25, $67.88, $68.81, $74.88

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $63.74 - $64.85 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $62.61 | $67.65   | $69.33   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $64.97 - $65.70 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $64.48 | $68.29   | $69.77   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
