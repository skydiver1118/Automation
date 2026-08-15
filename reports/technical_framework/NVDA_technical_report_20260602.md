# NVDA Technical Analysis Sample

Generated: 2026-06-02 16:57:31
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (83/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [NVDA_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/NVDA_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $222.82            |
| SMA20             | $217.97            |
| SMA50             | $201.27            |
| SMA200            | $188.06            |
| RSI14             | 58.8               |
| MACD / Signal     | 4.34 / 5.36        |
| ADX14 / +DI / -DI | 23.2 / 31.6 / 16.1 |
| ATR14             | $7.84 (3.52%)      |
| 63-day range      | $164.27 - $236.54  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 222.82 vs 217.97             |
| Trend        | Close above SMA50                         | 8      | 8   | 222.82 vs 201.27             |
| Trend        | Close above SMA200                        | 8      | 8   | 222.82 vs 188.06             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 217.97 vs 201.27             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 201.27 vs 188.06             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 13.94                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 58.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | 4.34 vs 5.36                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.32               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 12.26%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.96x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 2841010607 vs 3306006955     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.02x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 23.2, +DI 31.6, -DI 16.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 234.41              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.52%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 5.80%                        |

## Support And Resistance

- Support levels: $178.90, $195.98, $201.40, $208.78, $216.73
- Resistance levels: $235.26

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $214.05 - $219.93 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $193.42 | $264.12  | $287.69  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $235.26 - $239.18 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $217.97 | $275.73  | $294.98  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
