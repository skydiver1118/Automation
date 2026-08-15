# AMD Technical Analysis Sample

Generated: 2026-06-10 20:55:25
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (53/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AMD_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AMD_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $452.40            |
| SMA20             | $476.73            |
| SMA50             | $375.05            |
| SMA200            | $250.58            |
| RSI14             | 50.4               |
| MACD / Signal     | 30.27 / 41.29      |
| ADX14 / +DI / -DI | 36.5 / 22.1 / 26.5 |
| ATR14             | $31.89 (7.05%)     |
| 63-day range      | $192.27 - $546.44  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 452.40 vs 476.73             |
| Trend        | Close above SMA50                         | 8      | 8   | 452.40 vs 375.05             |
| Trend        | Close above SMA200                        | 8      | 8   | 452.40 vs 250.58             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 476.73 vs 375.05             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 375.05 vs 250.58             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 110.38                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 50.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | 30.27 vs 41.29               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -13.28             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 0.92%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.87x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1189775002 vs 1253909350     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.83x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 36.5, +DI 22.1, -DI 26.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 553.55              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.05%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.21%                       |

## Support And Resistance

- Support levels: $194.48, $389.44, $437.23
- Resistance levels: $469.22, $527.20, $548.22

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $421.29 - $445.20 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $343.17 | $613.40  | $703.48  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $469.22 - $485.16 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $437.23 | $557.11  | $597.08  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
