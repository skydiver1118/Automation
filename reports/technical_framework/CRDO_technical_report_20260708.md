# CRDO Technical Analysis Sample

Generated: 2026-07-08 16:40:38
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (64/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRDO_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRDO_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $258.69            |
| SMA20             | $257.31            |
| SMA50             | $221.36            |
| SMA200            | $160.07            |
| RSI14             | 53.6               |
| MACD / Signal     | 10.10 / 13.62      |
| ADX14 / +DI / -DI | 25.9 / 20.9 / 18.2 |
| ATR14             | $28.05 (10.84%)    |
| 63-day range      | $106.09 - $308.67  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 258.69 vs 257.31             |
| Trend        | Close above SMA50                         | 8      | 8   | 258.69 vs 221.36             |
| Trend        | Close above SMA200                        | 8      | 8   | 258.69 vs 160.07             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 257.31 vs 221.36             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 221.36 vs 160.07             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 48.30                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | 10.10 vs 13.62               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.33              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 16.39%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.53x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 201886395 vs 224147480       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.88x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 25.9, +DI 20.9, -DI 18.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 290.65              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.84%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 16.19%                       |

## Support And Resistance

- Support levels: $156.87, $182.80, $200.00, $227.49, $253.59
- Resistance levels: $280.46, $308.67

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $243.28 - $264.32 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $193.31 | $374.78  | $435.26  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $280.46 - $294.48 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $257.31 | $347.79  | $377.95  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
