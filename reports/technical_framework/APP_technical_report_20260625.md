# APP Technical Analysis Sample

Generated: 2026-06-26 06:53:06
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (21/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APP_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APP_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $445.93            |
| SMA20             | $525.23            |
| SMA50             | $496.43            |
| SMA200            | $541.36            |
| RSI14             | 36.6               |
| MACD / Signal     | -13.08 / -1.94     |
| ADX14 / +DI / -DI | 21.0 / 15.8 / 32.7 |
| ATR14             | $32.26 (7.23%)     |
| 63-day range      | $364.64 - $622.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 445.93 vs 525.23             |
| Trend        | Close above SMA50                         | 0      | 8   | 445.93 vs 496.43             |
| Trend        | Close above SMA200                        | 0      | 8   | 445.93 vs 541.36             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 525.23 vs 496.43             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 496.43 vs 541.36             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 44.73                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 36.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | -13.08 vs -1.94              |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.26              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -21.47%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.76x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 373007300 vs 410110915       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.34x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 21.0, +DI 15.8, -DI 32.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 636.74              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.23%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 28.31%                       |

## Support And Resistance

- Support levels: $363.62, $416.91
- Resistance levels: $442.24, $482.33, $519.75, $569.92, $625.69

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $525.23 - $541.36 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $476.85 | $622.00  | $686.52  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $400.78 - $424.97 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $384.65 | $482.33  | $509.64  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $482.33 - $498.46 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $416.91 | $637.37  | $710.86  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
