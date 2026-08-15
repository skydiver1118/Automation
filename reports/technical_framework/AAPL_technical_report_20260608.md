# AAPL Technical Analysis Sample

Generated: 2026-06-08 21:13:12
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (77/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AAPL_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AAPL_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $301.54            |
| SMA20             | $304.66            |
| SMA50             | $282.06            |
| SMA200            | $265.14            |
| RSI14             | 53.4               |
| MACD / Signal     | 7.41 / 9.04        |
| ADX14 / +DI / -DI | 43.7 / 24.2 / 16.0 |
| ATR14             | $6.79 (2.25%)      |
| 63-day range      | $245.28 - $317.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 301.54 vs 304.66             |
| Trend        | Close above SMA50                         | 8      | 8   | 301.54 vs 282.06             |
| Trend        | Close above SMA200                        | 8      | 8   | 301.54 vs 265.14             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 304.66 vs 282.06             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 282.06 vs 265.14             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 19.50                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | 7.41 vs 9.04                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.64              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 2.90%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.59x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 2090616095 vs 2171887605     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.18x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 43.7, +DI 24.2, -DI 16.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 317.73              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.25%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 5.00%                        |

## Support And Resistance

- Support levels: $253.90, $265.64, $282.06, $291.60, $303.20
- Resistance levels: $303.20, $317.48

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $288.20 - $293.30 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $275.27 | $321.71  | $337.18  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $303.20 - $306.60 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $291.60 | $331.50  | $344.80  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
