# SMH Technical Analysis Sample

Generated: 2026-06-05 16:40:48
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (67/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SMH_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SMH_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $569.69            |
| SMA20             | $584.09            |
| SMA50             | $506.94            |
| SMA200            | $396.25            |
| RSI14             | 51.1               |
| MACD / Signal     | 28.85 / 31.35      |
| ADX14 / +DI / -DI | 34.5 / 28.3 / 25.8 |
| ATR14             | $22.90 (4.02%)     |
| 63-day range      | $359.86 - $642.77  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 569.69 vs 584.09             |
| Trend        | Close above SMA50                         | 8      | 8   | 569.69 vs 506.94             |
| Trend        | Close above SMA200                        | 8      | 8   | 569.69 vs 396.25             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 584.09 vs 506.94             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 506.94 vs 396.25             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 75.47                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 51.1                   |
| Momentum     | MACD above signal                         | 0      | 7   | 28.85 vs 31.35               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.56              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 5.48%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 2.01x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 298042233 vs 305915497       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.95x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 34.5, +DI 28.3, -DI 25.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 639.09              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.02%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.37%                       |

## Support And Resistance

- Support levels: $359.57, $378.24, $397.77, $506.94, $528.48
- Resistance levels: $581.17, $641.85

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $517.03 - $534.20 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $484.04 | $608.77  | $650.35  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $581.17 - $592.62 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $528.48 | $703.73  | $762.15  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
