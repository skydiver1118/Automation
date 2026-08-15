# RKLB Technical Analysis Sample

Generated: 2026-06-08 21:13:26
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (58/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKLB_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKLB_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $113.65            |
| SMA20             | $127.97            |
| SMA50             | $97.09             |
| SMA200            | $71.36             |
| RSI14             | 48.6               |
| MACD / Signal     | 5.81 / 10.43       |
| ADX14 / +DI / -DI | 30.8 / 21.2 / 23.2 |
| ATR14             | $10.79 (9.50%)     |
| 63-day range      | $56.13 - $151.00   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 113.65 vs 127.97             |
| Trend        | Close above SMA50                         | 8      | 8   | 113.65 vs 97.09              |
| Trend        | Close above SMA200                        | 8      | 8   | 113.65 vs 71.36              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 127.97 vs 97.09              |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 97.09 vs 71.36               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 23.13                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 48.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | 5.81 vs 10.43                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -4.38              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 7.76%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.47x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1910794295 vs 1913598465     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.35x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 30.8, +DI 21.2, -DI 23.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 151.24              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.50%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 24.74%                       |

## Support And Resistance

- Support levels: $53.16, $65.49, $77.00, $97.09, $105.71
- Resistance levels: $138.38, $151.06

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $100.32 - $108.41 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $86.30  | $140.49  | $158.56  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $138.38 - $143.78 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $105.71 | $211.81  | $247.18  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
