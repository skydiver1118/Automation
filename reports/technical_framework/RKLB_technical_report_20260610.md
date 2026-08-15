# RKLB Technical Analysis Sample

Generated: 2026-06-10 20:55:13
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (41/100).**

Not bullish under the framework; classify as Bearish because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKLB_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKLB_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $105.05            |
| SMA20             | $126.89            |
| SMA50             | $98.99             |
| SMA200            | $72.00             |
| RSI14             | 44.1               |
| MACD / Signal     | 2.72 / 7.90        |
| ADX14 / +DI / -DI | 28.9 / 17.8 / 25.3 |
| ATR14             | $11.08 (10.55%)    |
| 63-day range      | $56.13 - $151.00   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 105.05 vs 126.89             |
| Trend        | Close above SMA50                         | 8      | 8   | 105.05 vs 98.99              |
| Trend        | Close above SMA200                        | 8      | 8   | 105.05 vs 72.00              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 126.89 vs 98.99              |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 98.99 vs 72.00               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 23.13                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 44.1                   |
| Momentum     | MACD above signal                         | 0      | 7   | 2.72 vs 7.90                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.19              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -10.64%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.49x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1867811420 vs 1910003381     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.92x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 28.9, +DI 17.8, -DI 25.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 153.02              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.55%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 30.43%                       |

## Support And Resistance

- Support levels: $53.82, $65.49, $77.00, $100.32
- Resistance levels: $138.38, $151.50

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $126.89 - $132.43 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $110.27 | $160.12  | $182.28  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $94.78 - $103.09  | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $87.91  | $138.38  | $132.17  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $138.38 - $143.92 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $100.32 | $222.82  | $263.65  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
