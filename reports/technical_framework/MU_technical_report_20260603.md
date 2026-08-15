# MU Technical Analysis Sample

Generated: 2026-06-03 19:36:58
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (83/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MU_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MU_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $1,079.57           |
| SMA20             | $822.48             |
| SMA50             | $595.70             |
| SMA200            | $352.64             |
| RSI14             | 82.4                |
| MACD / Signal     | 126.34 / 102.43     |
| ADX14 / +DI / -DI | 42.5 / 46.9 / 10.9  |
| ATR14             | $57.07 (5.29%)      |
| 63-day range      | $311.49 - $1,089.29 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 1079.57 vs 822.48            |
| Trend        | Close above SMA50                         | 8      | 8   | 1079.57 vs 595.70            |
| Trend        | Close above SMA200                        | 8      | 8   | 1079.57 vs 352.64            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 822.48 vs 595.70             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 595.70 vs 352.64             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 162.77                       |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 82.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 126.34 vs 102.43             |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 12.67              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 68.63%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.71x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1360433880 vs 1115176989     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.92x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 42.5, +DI 46.9, -DI 10.9 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 1093.05             |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.29%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.89%                        |

## Support And Resistance

- Support levels: $435.90, $551.91, $595.70, $652.21, $825.33
- Resistance levels: $1,090.23

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop    | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $799.65 - $842.45     | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $538.63 | $1,385.90 | $1,668.32 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,089.29 - $1,117.83 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $965.43 | $1,379.82 | $1,517.96 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
