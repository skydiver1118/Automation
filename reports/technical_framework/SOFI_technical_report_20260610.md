# SOFI Technical Analysis Sample

Generated: 2026-06-10 20:55:18
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (24/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SOFI_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SOFI_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $15.87             |
| SMA20             | $16.36             |
| SMA50             | $16.80             |
| SMA200            | $22.95             |
| RSI14             | 44.6               |
| MACD / Signal     | -0.05 / -0.02      |
| ADX14 / +DI / -DI | 17.1 / 21.5 / 18.4 |
| ATR14             | $0.96 (6.08%)      |
| 63-day range      | $14.92 - $20.13    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 15.87 vs 16.36               |
| Trend        | Close above SMA50                         | 0      | 8   | 15.87 vs 16.80               |
| Trend        | Close above SMA200                        | 0      | 8   | 15.87 vs 22.95               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 16.36 vs 16.80               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 16.80 vs 22.95               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.44                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 44.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.05 vs -0.02               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.28              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -0.19%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.17x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1205736135 vs 1203320907     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.27x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.1, +DI 21.5, -DI 18.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 18.25               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.08%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 21.16%                       |

## Support And Resistance

- Support levels: $14.89, $15.58
- Resistance levels: $16.32, $18.05, $18.80, $19.55, $20.13

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $16.80 - $17.28 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $15.35 | $19.69   | $21.62   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $15.09 - $15.82 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $14.61 | $17.38   | $18.35   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $16.32 - $16.80 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $15.58 | $18.53   | $19.52   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
