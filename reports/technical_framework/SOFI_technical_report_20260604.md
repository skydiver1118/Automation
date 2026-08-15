# SOFI Technical Analysis Sample

Generated: 2026-06-04 19:39:34
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (64/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SOFI_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SOFI_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $17.15             |
| SMA20             | $16.31             |
| SMA50             | $16.76             |
| SMA200            | $23.09             |
| RSI14             | 52.9               |
| MACD / Signal     | 0.15 / -0.06       |
| ADX14 / +DI / -DI | 21.5 / 26.3 / 18.5 |
| ATR14             | $0.91 (5.31%)      |
| 63-day range      | $14.92 - $20.13    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 17.15 vs 16.31               |
| Trend        | Close above SMA50                         | 8      | 8   | 17.15 vs 16.76               |
| Trend        | Close above SMA200                        | 0      | 8   | 17.15 vs 23.09               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 16.31 vs 16.76               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 16.76 vs 23.09               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.70                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 52.9                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.15 vs -0.06                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.07               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 5.21%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.88x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1374182231 vs 1171236817     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.41x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 21.5, +DI 26.3, -DI 18.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 18.22               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.31%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 14.80%                       |

## Support And Resistance

- Support levels: $14.88, $15.50, $16.61
- Resistance levels: $18.03, $18.80, $19.55, $20.13, $22.00

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $16.30 - $16.98 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $15.85 | $18.46   | $19.38   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $18.03 - $18.49 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $16.76 | $21.27   | $22.77   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
