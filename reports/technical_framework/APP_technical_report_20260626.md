# APP Technical Analysis Sample

Generated: 2026-06-28 17:42:17
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (31/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APP_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APP_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $477.08            |
| SMA20             | $519.09            |
| SMA50             | $496.68            |
| SMA200            | $540.95            |
| RSI14             | 45.2               |
| MACD / Signal     | -12.81 / -4.12     |
| ADX14 / +DI / -DI | 20.7 / 21.2 / 29.7 |
| ATR14             | $33.02 (6.92%)     |
| 63-day range      | $364.64 - $622.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 477.08 vs 519.09             |
| Trend        | Close above SMA50                         | 0      | 8   | 477.08 vs 496.68             |
| Trend        | Close above SMA200                        | 0      | 8   | 477.08 vs 540.95             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 519.09 vs 496.68             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 496.68 vs 540.95             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 42.16                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 45.2                   |
| Momentum     | MACD above signal                         | 0      | 7   | -12.81 vs -4.12              |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.15               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -20.47%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.64x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 373110500 vs 404444600       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.31x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 20.7, +DI 21.2, -DI 29.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 626.75              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.92%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 23.30%                       |

## Support And Resistance

- Support levels: $363.62, $416.45, $452.00, $472.00
- Resistance levels: $482.58, $519.75, $569.92, $623.19, $679.69

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $519.09 - $535.60 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $469.56 | $618.15  | $684.18  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $455.49 - $480.25 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $438.98 | $533.91  | $566.93  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $482.58 - $499.09 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $472.00 | $556.87  | $589.89  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
