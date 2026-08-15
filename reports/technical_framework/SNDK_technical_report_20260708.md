# SNDK Technical Analysis Sample

Generated: 2026-07-08 16:40:26
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (51/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SNDK_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SNDK_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $1,727.18           |
| SMA20             | $1,958.12           |
| SMA50             | $1,654.21           |
| SMA200            | $727.38             |
| RSI14             | 47.0                |
| MACD / Signal     | 42.21 / 115.64      |
| ADX14 / +DI / -DI | 29.6 / 27.5 / 31.8  |
| ATR14             | $203.81 (11.80%)    |
| 63-day range      | $758.19 - $2,354.39 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 1727.18 vs 1958.12           |
| Trend        | Close above SMA50                         | 8      | 8   | 1727.18 vs 1654.21           |
| Trend        | Close above SMA200                        | 8      | 8   | 1727.18 vs 727.38            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1958.12 vs 1654.21           |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 1654.21 vs 727.38            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 453.56                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 47.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | 42.21 vs 115.64              |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -75.32             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 5.19%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.94x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 515450852 vs 552046568       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.72x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 29.6, +DI 27.5, -DI 31.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 2396.44             |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 11.80%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 26.64%                       |

## Support And Resistance

- Support levels: $547.56, $758.19, $1,277.33, $1,506.40, $1,654.21
- Resistance levels: $1,861.00, $2,364.90

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop      | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | --------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $1,552.30 - $1,705.16 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $1,450.40 | $2,036.36 | $2,240.17 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,861.00 - $1,962.91 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $1,654.21 | $2,427.44 | $2,685.18 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
