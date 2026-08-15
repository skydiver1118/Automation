# CRM Technical Analysis Sample

Generated: 2026-06-10 20:55:26
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (17/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRM_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRM_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $170.92            |
| SMA20             | $181.52            |
| SMA50             | $180.83            |
| SMA200            | $218.43            |
| RSI14             | 41.4               |
| MACD / Signal     | 0.12 / 1.45        |
| ADX14 / +DI / -DI | 13.4 / 23.7 / 29.2 |
| ATR14             | $9.05 (5.29%)      |
| 63-day range      | $163.52 - $211.34  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 170.92 vs 181.52             |
| Trend        | Close above SMA50                         | 0      | 8   | 170.92 vs 180.83             |
| Trend        | Close above SMA200                        | 0      | 8   | 170.92 vs 218.43             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 181.52 vs 180.83             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 180.83 vs 218.43             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.42                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 41.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | 0.12 vs 1.45                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -3.94              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -0.23%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.68x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | -24873591 vs 38328650        |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.67x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 13.4, +DI 23.7, -DI 29.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 202.81              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.29%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 19.13%                       |

## Support And Resistance

- Support levels: $162.90, $171.90
- Resistance levels: $189.95, $202.90, $211.34, $235.15, $267.47

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $181.52 - $186.05 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $167.95 | $208.67  | $226.76  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $158.38 - $165.16 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $153.85 | $189.95  | $188.92  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $189.95 - $194.48 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $162.90 | $250.85  | $280.16  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
