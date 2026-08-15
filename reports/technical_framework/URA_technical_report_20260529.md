# URA Technical Analysis Sample

Generated: 2026-05-31 20:26:07
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (52/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [URA_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/URA_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $50.76             |
| SMA20             | $52.30             |
| SMA50             | $51.83             |
| SMA200            | $48.44             |
| RSI14             | 46.9               |
| MACD / Signal     | -0.99 / -0.82      |
| ADX14 / +DI / -DI | 15.0 / 20.1 / 23.6 |
| ATR14             | $2.19 (4.32%)      |
| 63-day range      | $44.76 - $58.97    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 50.76 vs 52.30               |
| Trend        | Close above SMA50                         | 0      | 8   | 50.76 vs 51.83               |
| Trend        | Close above SMA200                        | 8      | 8   | 50.76 vs 48.44               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 52.30 vs 51.83               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 51.83 vs 48.44               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.01                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.99 vs -0.82               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.82               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -10.03%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.98x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 152925000 vs 151203475       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.70x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.0, +DI 20.1, -DI 23.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 58.93               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.32%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.92%                       |

## Support And Resistance

- Support levels: $41.72, $45.24, $47.01, $49.49
- Resistance levels: $50.71, $53.25, $55.06, $56.67, $58.83

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $52.30 - $53.40 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $49.02 | $58.88   | $63.26   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $48.39 - $50.04 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $47.30 | $53.60   | $55.79   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $53.25 - $54.35 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $49.49 | $62.41   | $66.72   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
