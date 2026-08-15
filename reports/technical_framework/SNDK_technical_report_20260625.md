# SNDK Technical Analysis Sample

Generated: 2026-06-26 06:53:28
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (93/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SNDK_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SNDK_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $2,335.00           |
| SMA20             | $1,874.40           |
| SMA50             | $1,497.59           |
| SMA200            | $654.42             |
| RSI14             | 66.4                |
| MACD / Signal     | 191.29 / 177.75     |
| ADX14 / +DI / -DI | 42.7 / 39.0 / 19.2  |
| ATR14             | $184.16 (7.89%)     |
| 63-day range      | $558.58 - $2,354.39 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 2335.00 vs 1874.40           |
| Trend        | Close above SMA50                         | 8      | 8   | 2335.00 vs 1497.59           |
| Trend        | Close above SMA200                        | 8      | 8   | 2335.00 vs 654.42            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1874.40 vs 1497.59           |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 1497.59 vs 654.42            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 456.24                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 66.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 191.29 vs 177.75             |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.24              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 46.86%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.35x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 572430300 vs 554454505       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.52x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 42.7, +DI 39.0, -DI 19.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 2324.39             |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.89%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.82%                        |

## Support And Resistance

- Support levels: $234.62, $549.76, $1,277.33, $1,478.79, $1,870.93
- Resistance levels: $2,346.89

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop      | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | --------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $1,785.30 - $1,923.42 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $1,313.42 | $2,936.23 | $3,477.16 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $2,346.89 - $2,438.97 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $1,966.67 | $3,245.45 | $3,671.70 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
