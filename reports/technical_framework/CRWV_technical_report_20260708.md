# CRWV Technical Analysis Sample

Generated: 2026-07-08 16:40:14
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (15/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWV_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWV_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $90.00             |
| SMA20             | $99.15             |
| SMA50             | $106.90            |
| SMA200            | $99.66             |
| RSI14             | 42.7               |
| MACD / Signal     | -5.69 / -3.93      |
| ADX14 / +DI / -DI | 17.8 / 19.5 / 32.1 |
| ATR14             | $8.36 (9.29%)      |
| 63-day range      | $79.46 - $138.25   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 90.00 vs 99.15               |
| Trend        | Close above SMA50                         | 0      | 8   | 90.00 vs 106.90              |
| Trend        | Close above SMA200                        | 0      | 8   | 90.00 vs 99.66               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 99.15 vs 106.90              |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 106.90 vs 99.66              |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.27                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 42.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | -5.69 vs -3.93               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.66              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -12.08%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.77x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 391805287 vs 483052574       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.77x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.8, +DI 19.5, -DI 32.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 120.68              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.29%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 34.90%                       |

## Support And Resistance

- Support levels: $71.19, $78.53, $85.78
- Resistance levels: $101.26, $114.45, $122.36, $132.15, $138.25

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $106.90 - $111.08 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $94.36 | $131.98  | $148.71  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $81.60 - $87.88   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $77.42 | $101.46  | $109.82  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $101.26 - $105.44 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $85.78 | $138.49  | $156.05  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
