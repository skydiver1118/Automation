# AMD Technical Analysis Sample

Generated: 2026-07-06 16:40:34
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (86/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AMD_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AMD_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $552.05            |
| SMA20             | $518.28            |
| SMA50             | $465.35            |
| SMA200            | $280.14            |
| RSI14             | 57.4               |
| MACD / Signal     | 23.25 / 26.02      |
| ADX14 / +DI / -DI | 24.4 / 31.3 / 19.8 |
| ATR14             | $37.21 (6.74%)     |
| 63-day range      | $215.38 - $584.73  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 552.05 vs 518.28             |
| Trend        | Close above SMA50                         | 8      | 8   | 552.05 vs 465.35             |
| Trend        | Close above SMA200                        | 8      | 8   | 552.05 vs 280.14             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 518.28 vs 465.35             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 465.35 vs 280.14             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 111.55                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 57.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | 23.25 vs 26.02               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.16               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 5.51%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.92x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1289976290 vs 1264638464     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.29x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 24.4, +DI 31.3, -DI 19.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 582.01              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.74%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 5.59%                        |

## Support And Resistance

- Support levels: $215.38, $393.36, $452.38, $495.35, $518.96
- Resistance levels: $548.75, $584.05

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $501.05 - $528.95 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $428.14 | $688.72  | $775.57  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $584.05 - $602.66 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $519.65 | $740.75  | $814.46  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
