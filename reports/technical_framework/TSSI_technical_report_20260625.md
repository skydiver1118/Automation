# TSSI Technical Analysis Sample

Generated: 2026-06-26 06:53:41
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (26/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSSI_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSSI_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $11.65             |
| SMA20             | $13.36             |
| SMA50             | $13.57             |
| SMA200            | $12.53             |
| RSI14             | 42.3               |
| MACD / Signal     | -0.26 / -0.13      |
| ADX14 / +DI / -DI | 13.4 / 20.2 / 27.7 |
| ATR14             | $1.15 (9.84%)      |
| 63-day range      | $10.31 - $17.49    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 11.65 vs 13.36               |
| Trend        | Close above SMA50                         | 0      | 8   | 11.65 vs 13.57               |
| Trend        | Close above SMA200                        | 0      | 8   | 11.65 vs 12.53               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 13.36 vs 13.57               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 13.57 vs 12.53               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.27                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 42.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.26 vs -0.13               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.05              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -7.10%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.54x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 21835700 vs 23797380         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.00x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 13.4, +DI 20.2, -DI 27.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 15.90               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.84%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 33.39%                       |

## Support And Resistance

- Support levels: $7.34, $8.65, $10.34, $11.57
- Resistance levels: $12.71, $14.17, $15.90, $17.31

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $13.57 - $14.14 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $11.85 | $17.01   | $19.30   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $11.00 - $11.86 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $10.43 | $13.72   | $14.87   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $12.71 - $13.28 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $11.57 | $15.84   | $17.27   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
