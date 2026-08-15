# AMD Technical Analysis Sample

Generated: 2026-07-08 16:40:33
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (70/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AMD_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AMD_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $517.41            |
| SMA20             | $522.12            |
| SMA50             | $472.96            |
| SMA200            | $283.73            |
| RSI14             | 51.4               |
| MACD / Signal     | 17.58 / 23.39      |
| ADX14 / +DI / -DI | 22.5 / 27.1 / 22.3 |
| ATR14             | $37.10 (7.17%)     |
| 63-day range      | $227.09 - $584.73  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 517.41 vs 522.12             |
| Trend        | Close above SMA50                         | 8      | 8   | 517.41 vs 472.96             |
| Trend        | Close above SMA200                        | 8      | 8   | 517.41 vs 283.73             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 522.12 vs 472.96             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 472.96 vs 283.73             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 108.51                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 51.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | 17.58 vs 23.39               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -5.51              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 5.52%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.73x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1328156731 vs 1312706837     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.33x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 22.5, +DI 27.1, -DI 22.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 579.30              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.17%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.51%                       |

## Support And Resistance

- Support levels: $393.36, $437.23, $468.95, $496.75, $520.64
- Resistance levels: $548.75, $583.37

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $478.20 - $506.03 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $435.86 | $604.62  | $660.88  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $548.75 - $567.30 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $496.75 | $680.58  | $741.85  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
