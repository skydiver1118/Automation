# SNDK Technical Analysis Sample

Generated: 2026-06-28 17:42:33
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (88/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SNDK_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SNDK_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $2,090.71           |
| SMA20             | $1,896.86           |
| SMA50             | $1,521.57           |
| SMA200            | $664.52             |
| RSI14             | 57.7                |
| MACD / Signal     | 183.98 / 178.99     |
| ADX14 / +DI / -DI | 41.9 / 35.1 / 18.3  |
| ATR14             | $190.43 (9.11%)     |
| 63-day range      | $558.58 - $2,354.39 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 2090.71 vs 1896.86           |
| Trend        | Close above SMA50                         | 8      | 8   | 2090.71 vs 1521.57           |
| Trend        | Close above SMA200                        | 8      | 8   | 2090.71 vs 664.52            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1896.86 vs 1521.57           |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 1521.57 vs 664.52            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 461.79                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 57.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | 183.98 vs 178.99             |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -19.03             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 27.35%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.48x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 555808500 vs 555795065       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.18x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 41.9, +DI 35.1, -DI 18.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 2342.74             |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.11%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.20%                       |

## Support And Resistance

- Support levels: $235.24, $549.76, $1,277.33, $1,495.63, $1,884.88
- Resistance levels: $2,351.48

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop      | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | --------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $1,801.64 - $1,944.46 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $1,331.13 | $2,956.89 | $3,498.81 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $2,351.48 - $2,446.69 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $1,896.86 | $3,403.55 | $3,905.78 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
