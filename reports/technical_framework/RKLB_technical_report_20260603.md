# RKLB Technical Analysis Sample

Generated: 2026-06-03 19:37:09
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (70/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKLB_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKLB_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $114.70            |
| SMA20             | $124.22            |
| SMA50             | $94.32             |
| SMA200            | $70.27             |
| RSI14             | 49.0               |
| MACD / Signal     | 10.57 / 13.56      |
| ADX14 / +DI / -DI | 37.6 / 26.3 / 23.6 |
| ATR14             | $10.89 (9.50%)     |
| 63-day range      | $56.13 - $151.00   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 114.70 vs 124.22             |
| Trend        | Close above SMA50                         | 8      | 8   | 114.70 vs 94.32              |
| Trend        | Close above SMA200                        | 8      | 8   | 114.70 vs 70.27              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 124.22 vs 94.32              |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 94.32 vs 70.27               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 21.47                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | 10.57 vs 13.56               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -5.72              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 45.63%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.67x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1907154772 vs 1900029734     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.78x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 37.6, +DI 26.3, -DI 23.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 161.28              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.50%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 24.04%                       |

## Support And Resistance

- Support levels: $65.49, $77.00, $87.16, $94.32, $114.45
- Resistance levels: $138.38, $151.00, $161.28

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $109.00 - $117.17 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $83.42  | $172.40  | $202.07  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $138.38 - $143.83 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $114.45 | $194.42  | $221.08  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
