# SOFI Technical Analysis Sample

Generated: 2026-06-02 16:57:42
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (69/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SOFI_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SOFI_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $17.74             |
| SMA20             | $16.24             |
| SMA50             | $16.76             |
| SMA200            | $23.16             |
| RSI14             | 57.9               |
| MACD / Signal     | 0.17 / -0.18       |
| ADX14 / +DI / -DI | 22.1 / 30.4 / 14.0 |
| ATR14             | $0.91 (5.15%)      |
| 63-day range      | $14.92 - $20.13    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 17.74 vs 16.24               |
| Trend        | Close above SMA50                         | 8      | 8   | 17.74 vs 16.76               |
| Trend        | Close above SMA200                        | 0      | 8   | 17.74 vs 23.16               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 16.24 vs 16.76               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 16.76 vs 23.16               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.79                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 57.9                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.17 vs -0.18                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.32               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 9.51%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.08x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1395670030 vs 1159513556     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.45x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 22.1, +DI 30.4, -DI 14.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 18.09               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.15%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.87%                       |

## Support And Resistance

- Support levels: $14.87, $15.50, $16.60, $17.76
- Resistance levels: $17.97, $18.80, $19.55, $20.13, $22.00

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $16.30 - $16.99 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $15.84 | $18.47   | $19.38   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $17.97 - $18.43 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $16.76 | $21.09   | $22.53   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
