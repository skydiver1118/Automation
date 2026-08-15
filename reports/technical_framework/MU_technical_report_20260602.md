# MU Technical Analysis Sample

Generated: 2026-06-02 16:57:30
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (83/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MU_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MU_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $1,064.10           |
| SMA20             | $800.51             |
| SMA50             | $582.19             |
| SMA200            | $347.85             |
| RSI14             | 81.8                |
| MACD / Signal     | 119.83 / 96.45      |
| ADX14 / +DI / -DI | 41.0 / 48.4 / 11.6  |
| ATR14             | $57.55 (5.41%)      |
| 63-day range      | $311.49 - $1,076.52 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 1064.10 vs 800.51            |
| Trend        | Close above SMA50                         | 8      | 8   | 1064.10 vs 582.19            |
| Trend        | Close above SMA200                        | 8      | 8   | 1064.10 vs 347.85            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 800.51 vs 582.19             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 582.19 vs 347.85             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 153.65                       |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 81.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | 119.83 vs 96.45              |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 18.23              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 84.60%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.82x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1306890766 vs 1082875288     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.96x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 41.0, +DI 48.4, -DI 11.6 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 1054.00             |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.41%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 1.15%                        |

## Support And Resistance

- Support levels: $435.90, $547.02, $582.19, $652.21, $801.78
- Resistance levels: $1,070.89

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop    | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $774.27 - $817.43     | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $524.64 | $1,338.27 | $1,609.47 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,070.89 - $1,099.66 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $949.01 | $1,357.82 | $1,494.09 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
