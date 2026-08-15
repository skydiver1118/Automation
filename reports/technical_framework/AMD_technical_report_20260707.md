# AMD Technical Analysis Sample

Generated: 2026-07-07 16:40:33
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (65/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AMD_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AMD_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $516.11            |
| SMA20             | $520.76            |
| SMA50             | $469.57            |
| SMA200            | $281.93            |
| RSI14             | 51.2               |
| MACD / Signal     | 20.14 / 24.85      |
| ADX14 / +DI / -DI | 23.5 / 28.4 / 22.4 |
| ATR14             | $38.05 (7.37%)     |
| 63-day range      | $215.38 - $584.73  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 516.11 vs 520.76             |
| Trend        | Close above SMA50                         | 8      | 8   | 516.11 vs 469.57             |
| Trend        | Close above SMA200                        | 8      | 8   | 516.11 vs 281.93             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 520.76 vs 469.57             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 469.57 vs 281.93             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 110.84                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 51.2                   |
| Momentum     | MACD above signal                         | 0      | 7   | 20.14 vs 24.85               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.43              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 10.66%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.92x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1262357213 vs 1267082416     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.08x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 23.5, +DI 28.4, -DI 22.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 579.67              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.37%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.74%                       |

## Support And Resistance

- Support levels: $195.01, $393.36, $437.23, $465.71, $509.64
- Resistance levels: $548.75, $583.46

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $490.61 - $519.15 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $431.52 | $651.61  | $724.97  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $548.75 - $567.77 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $509.64 | $655.51  | $704.13  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
