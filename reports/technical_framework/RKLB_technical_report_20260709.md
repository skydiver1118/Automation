# RKLB Technical Analysis Sample

Generated: 2026-07-09 16:40:33
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (27/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKLB_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKLB_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $82.55             |
| SMA20             | $97.00             |
| SMA50             | $107.05            |
| SMA200            | $76.64             |
| RSI14             | 38.1               |
| MACD / Signal     | -6.51 / -5.15      |
| ADX14 / +DI / -DI | 23.5 / 17.1 / 29.2 |
| ATR14             | $9.17 (11.11%)     |
| 63-day range      | $66.34 - $151.00   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 82.55 vs 97.00               |
| Trend        | Close above SMA50                         | 0      | 8   | 82.55 vs 107.05              |
| Trend        | Close above SMA200                        | 8      | 8   | 82.55 vs 76.64               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 97.00 vs 107.05              |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 107.05 vs 76.64              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 9.01                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 38.1                   |
| Momentum     | MACD above signal                         | 0      | 7   | -6.51 vs -5.15               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.44              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -23.73%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.57x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1696376580 vs 1765461304     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.58x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 23.5, +DI 17.1, -DI 29.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 117.79              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 11.11%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 45.33%                       |

## Support And Resistance

- Support levels: $56.13, $65.39, $78.84
- Resistance levels: $91.49, $99.58, $107.60, $118.08, $138.38

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $107.05 - $111.63 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $93.29 | $134.56  | $152.91  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $74.26 - $81.14   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $69.67 | $96.04   | $105.21  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $91.49 - $96.07   | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $78.84 | $123.65  | $138.58  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
