# SOFI Technical Analysis Sample

Generated: 2026-05-31 20:26:04
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (58/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SOFI_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SOFI_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $18.22             |
| SMA20             | $16.05             |
| SMA50             | $16.71             |
| SMA200            | $23.21             |
| RSI14             | 64.0               |
| MACD / Signal     | -0.09 / -0.36      |
| ADX14 / +DI / -DI | 19.4 / 34.7 / 14.7 |
| ATR14             | $0.88 (4.84%)      |
| 63-day range      | $14.92 - $20.13    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 18.22 vs 16.05               |
| Trend        | Close above SMA50                         | 8      | 8   | 18.22 vs 16.71               |
| Trend        | Close above SMA200                        | 0      | 8   | 18.22 vs 23.21               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 16.05 vs 16.71               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 16.71 vs 23.21               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.95                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 64.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.09 vs -0.36               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.30               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 13.17%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 2.26x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1311832800 vs 1080734925     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.17x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 19.4, +DI 34.7, -DI 14.7 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 17.35               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.84%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 9.49%                        |

## Support And Resistance

- Support levels: $14.95, $15.50, $16.49, $17.76
- Resistance levels: $18.59, $19.55, $20.13, $22.00, $26.40

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $17.31 - $17.98 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $15.83 | $21.28   | $23.09   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $18.59 - $19.03 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $17.76 | $20.92   | $21.98   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
