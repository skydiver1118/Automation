# CRDO Technical Analysis Sample

Generated: 2026-07-06 16:40:38
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (69/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRDO_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRDO_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $265.55            |
| SMA20             | $253.51            |
| SMA50             | $218.87            |
| SMA200            | $159.22            |
| RSI14             | 55.6               |
| MACD / Signal     | 12.31 / 15.48      |
| ADX14 / +DI / -DI | 29.5 / 21.0 / 17.6 |
| ATR14             | $28.26 (10.64%)    |
| 63-day range      | $101.30 - $308.67  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 265.55 vs 253.51             |
| Trend        | Close above SMA50                         | 8      | 8   | 265.55 vs 218.87             |
| Trend        | Close above SMA200                        | 8      | 8   | 265.55 vs 159.22             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 253.51 vs 218.87             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 218.87 vs 159.22             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 50.39                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 55.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | 12.31 vs 15.48               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.51              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 22.09%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.66x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 202615269 vs 222290823       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.14x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 29.5, +DI 21.0, -DI 17.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 296.17              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.64%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.97%                       |

## Support And Resistance

- Support levels: $119.40, $156.87, $182.80, $213.85, $247.24
- Resistance levels: $275.36, $305.54

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $239.38 - $260.57 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $190.61 | $368.71  | $428.08  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $275.36 - $289.48 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $253.51 | $340.24  | $369.15  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
