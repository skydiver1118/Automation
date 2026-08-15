# PLTR Technical Analysis Sample

Generated: 2026-06-28 17:42:26
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (13/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [PLTR_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/PLTR_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $112.93            |
| SMA20             | $132.18            |
| SMA50             | $136.46            |
| SMA200            | $158.85            |
| RSI14             | 34.5               |
| MACD / Signal     | -7.02 / -4.48      |
| ADX14 / +DI / -DI | 22.5 / 15.9 / 37.5 |
| ATR14             | $6.55 (5.80%)      |
| 63-day range      | $106.37 - $163.70  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 112.93 vs 132.18             |
| Trend        | Close above SMA50                         | 0      | 8   | 112.93 vs 136.46             |
| Trend        | Close above SMA200                        | 0      | 8   | 112.93 vs 158.85             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 132.18 vs 136.46             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 136.46 vs 158.85             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -5.26                        |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 34.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | -7.02 vs -4.48               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.47              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -21.22%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.35x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 4011281100 vs 4230105775     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.36x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 22.5, +DI 15.9, -DI 37.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 160.50              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.80%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 31.01%                       |

## Support And Resistance

- Support levels: $105.53
- Resistance levels: $136.10, $140.96, $151.16, $156.51, $162.93

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $136.46 - $139.73 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $126.63 | $156.11  | $169.21  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $102.26 - $107.17 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $98.98  | $136.10  | $124.37  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $136.10 - $139.38 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $105.53 | $202.15  | $234.36  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
