# RKLB Technical Analysis Sample

Generated: 2026-07-07 16:40:23
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (32/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKLB_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKLB_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $83.41             |
| SMA20             | $99.80             |
| SMA50             | $106.97            |
| SMA200            | $76.28             |
| RSI14             | 38.5               |
| MACD / Signal     | -5.46 / -4.49      |
| ADX14 / +DI / -DI | 23.1 / 18.4 / 30.0 |
| ATR14             | $9.89 (11.86%)     |
| 63-day range      | $63.96 - $151.00   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 83.41 vs 99.80               |
| Trend        | Close above SMA50                         | 0      | 8   | 83.41 vs 106.97              |
| Trend        | Close above SMA200                        | 8      | 8   | 83.41 vs 76.28               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 99.80 vs 106.97              |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 106.97 vs 76.28              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 10.83                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 38.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | -5.46 vs -4.49               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.90               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -24.23%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.86x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1743176095 vs 1792555120     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.58x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 23.1, +DI 18.4, -DI 30.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 119.82              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 11.86%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 44.76%                       |

## Support And Resistance

- Support levels: $56.13, $64.91, $72.65, $80.66
- Resistance levels: $91.49, $99.58, $107.60, $119.81, $138.38

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $106.97 - $111.91 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $92.13 | $136.65  | $156.43  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $75.71 - $83.13   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $70.77 | $99.21   | $109.10  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $91.49 - $96.43   | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $80.66 | $120.56  | $133.86  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
