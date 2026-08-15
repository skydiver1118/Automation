# RKLB Technical Analysis Sample

Generated: 2026-07-08 16:40:23
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (32/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKLB_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKLB_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $83.35             |
| SMA20             | $98.28             |
| SMA50             | $107.04            |
| SMA200            | $76.46             |
| RSI14             | 38.5               |
| MACD / Signal     | -6.05 / -4.80      |
| ADX14 / +DI / -DI | 23.3 / 17.6 / 30.1 |
| ATR14             | $9.58 (11.49%)     |
| 63-day range      | $66.34 - $151.00   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 83.35 vs 98.28               |
| Trend        | Close above SMA50                         | 0      | 8   | 83.35 vs 107.04              |
| Trend        | Close above SMA200                        | 8      | 8   | 83.35 vs 76.46               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 98.28 vs 107.04              |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 107.04 vs 76.46              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 9.95                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 38.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | -6.05 vs -4.80               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.44               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -26.66%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.62x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1719254848 vs 1779102872     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.59x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 23.3, +DI 17.6, -DI 30.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 118.48              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 11.49%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 44.80%                       |

## Support And Resistance

- Support levels: $56.13, $65.39, $77.86
- Resistance levels: $91.49, $99.58, $107.60, $119.13, $138.38

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $107.04 - $111.83 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $92.67 | $135.78  | $154.94  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $73.07 - $80.25   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $68.28 | $95.82   | $105.40  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $91.49 - $96.27   | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $77.86 | $125.93  | $141.95  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
