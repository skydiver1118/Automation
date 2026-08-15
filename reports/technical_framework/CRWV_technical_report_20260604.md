# CRWV Technical Analysis Sample

Generated: 2026-06-04 19:39:18
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (60/100).**

Not bullish yet under the framework; classify as Neutral because close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWV_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWV_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $108.03            |
| SMA20             | $110.29            |
| SMA50             | $106.48            |
| SMA200            | $99.89             |
| RSI14             | 48.4               |
| MACD / Signal     | 0.82 / 0.75        |
| ADX14 / +DI / -DI | 13.9 / 29.8 / 28.6 |
| ATR14             | $8.96 (8.29%)      |
| 63-day range      | $67.15 - $138.25   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 108.03 vs 110.29             |
| Trend        | Close above SMA50                         | 8      | 8   | 108.03 vs 106.48             |
| Trend        | Close above SMA200                        | 8      | 8   | 108.03 vs 99.89              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 110.29 vs 106.48             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 106.48 vs 99.89              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.63                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 48.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.82 vs 0.75                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.59               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -21.71%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.82x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 506573168 vs 512508448       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.87x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 13.9, +DI 29.8, -DI 28.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 125.08              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.29%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 21.86%                       |

## Support And Resistance

- Support levels: $69.62, $77.58, $85.78, $98.82, $108.63
- Resistance levels: $114.45, $124.06, $132.87, $138.25

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $102.00 - $108.72 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $97.52  | $123.28  | $132.23  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $114.45 - $118.93 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $106.48 | $137.11  | $147.32  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
