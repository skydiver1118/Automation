# OPEN Technical Analysis Sample

Generated: 2026-06-10 20:55:09
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (24/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [OPEN_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/OPEN_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $4.48              |
| SMA20             | $4.65              |
| SMA50             | $4.87              |
| SMA200            | $6.11              |
| RSI14             | 43.7               |
| MACD / Signal     | -0.10 / -0.06      |
| ADX14 / +DI / -DI | 16.0 / 21.3 / 24.4 |
| ATR14             | $0.39 (8.81%)      |
| 63-day range      | $4.08 - $6.00      |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 4.48 vs 4.65                 |
| Trend        | Close above SMA50                         | 0      | 8   | 4.48 vs 4.87                 |
| Trend        | Close above SMA200                        | 0      | 8   | 4.48 vs 6.11                 |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 4.65 vs 4.87                 |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 4.87 vs 6.11                 |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.16                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 43.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.10 vs -0.06               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.12              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -4.88%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.27x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 5945291045 vs 5841651092     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.34x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 16.0, +DI 21.3, -DI 24.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 5.34                |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.81%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 25.33%                       |

## Support And Resistance

- Support levels: $4.11, $4.36
- Resistance levels: $5.01, $5.55, $6.00, $7.85

## Entry Plans

| Plan           | Entry zone    | Trigger                                                                                                      | Stop  | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ------------- | ------------------------------------------------------------------------------------------------------------ | ----- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $4.87 - $5.07 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $4.28 | $6.06    | $6.84    | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $4.16 - $4.46 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $3.97 | $5.10    | $5.50    | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $5.01 - $5.21 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $4.36 | $6.60    | $7.35    | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
