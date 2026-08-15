# APLD Technical Analysis Sample

Generated: 2026-06-28 17:42:43
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (38/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APLD_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APLD_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $39.16             |
| SMA20             | $43.75             |
| SMA50             | $40.98             |
| SMA200            | $31.92             |
| RSI14             | 42.3               |
| MACD / Signal     | 0.20 / 0.94        |
| ADX14 / +DI / -DI | 16.6 / 18.2 / 23.1 |
| ATR14             | $4.02 (10.27%)     |
| 63-day range      | $20.00 - $50.72    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 39.16 vs 43.75               |
| Trend        | Close above SMA50                         | 0      | 8   | 39.16 vs 40.98               |
| Trend        | Close above SMA200                        | 8      | 8   | 39.16 vs 31.92               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 43.75 vs 40.98               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 40.98 vs 31.92               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 7.01                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 42.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | 0.20 vs 0.94                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.67              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -21.13%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 2.27x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1558774100 vs 1618202285     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.72x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 16.6, +DI 18.2, -DI 23.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 49.69               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.27%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 22.80%                       |

## Support And Resistance

- Support levels: $20.00, $24.23, $27.62, $31.41, $37.65
- Resistance levels: $39.34, $42.27, $49.34

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $43.75 - $45.76 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $37.71 | $55.82   | $63.87   | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $35.64 - $38.66 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $33.63 | $45.19   | $49.22   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $39.34 - $41.35 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $37.65 | $48.39   | $52.42   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
