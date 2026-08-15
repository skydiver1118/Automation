# CRWV Technical Analysis Sample

Generated: 2026-05-31 20:25:44
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (63/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWV_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWV_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $109.53            |
| SMA20             | $112.65            |
| SMA50             | $103.76            |
| SMA200            | $99.65             |
| RSI14             | 51.1               |
| MACD / Signal     | -0.69 / 0.34       |
| ADX14 / +DI / -DI | 14.0 / 23.7 / 27.4 |
| ATR14             | $7.95 (7.26%)      |
| 63-day range      | $67.15 - $138.25   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 109.53 vs 112.65             |
| Trend        | Close above SMA50                         | 8      | 8   | 109.53 vs 103.76             |
| Trend        | Close above SMA200                        | 8      | 8   | 109.53 vs 99.65              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 112.65 vs 103.76             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 103.76 vs 99.65              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.58                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 51.1                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.69 vs 0.34                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.75               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -1.85%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.98x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 534199100 vs 511760725       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.13x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.0, +DI 23.7, -DI 27.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 133.23              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.26%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 20.77%                       |

## Support And Resistance

- Support levels: $68.42, $75.79, $85.78, $93.45, $101.88
- Resistance levels: $112.39, $123.55, $133.23, $138.25

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $104.77 - $110.74 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $95.81  | $131.65  | $143.59  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $112.39 - $116.37 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $108.75 | $130.28  | $138.23  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
