# CRWV Technical Analysis Sample

Generated: 2026-06-03 19:36:53
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (65/100).**

Not bullish yet under the framework; classify as Neutral because close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWV_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWV_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $110.93            |
| SMA20             | $111.79            |
| SMA50             | $105.98            |
| SMA200            | $99.84             |
| RSI14             | 50.5               |
| MACD / Signal     | 1.20 / 0.73        |
| ADX14 / +DI / -DI | 14.8 / 31.3 / 25.4 |
| ATR14             | $9.19 (8.29%)      |
| 63-day range      | $67.15 - $138.25   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 110.93 vs 111.79             |
| Trend        | Close above SMA50                         | 8      | 8   | 110.93 vs 105.98             |
| Trend        | Close above SMA200                        | 8      | 8   | 110.93 vs 99.84              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 111.79 vs 105.98             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 105.98 vs 99.84              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.90                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 50.5                   |
| Momentum     | MACD above signal                         | 7      | 7   | 1.20 vs 0.73                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.38               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -13.26%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.85x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 531798583 vs 516511059       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.83x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.8, +DI 31.3, -DI 25.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 131.02              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.29%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 19.76%                       |

## Support And Resistance

- Support levels: $77.58, $85.78, $93.69, $102.44, $111.14
- Resistance levels: $114.45, $123.55, $131.58, $138.25

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $101.38 - $108.28 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $96.78  | $123.22  | $132.41  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $114.45 - $119.05 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $105.98 | $138.29  | $149.06  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
