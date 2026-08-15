# SOFI Technical Analysis Sample

Generated: 2026-06-08 21:13:30
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (49/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SOFI_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SOFI_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $16.50             |
| SMA20             | $16.35             |
| SMA50             | $16.76             |
| SMA200            | $23.03             |
| RSI14             | 48.7               |
| MACD / Signal     | 0.04 / -0.02       |
| ADX14 / +DI / -DI | 18.6 / 22.1 / 22.0 |
| ATR14             | $0.93 (5.66%)      |
| 63-day range      | $14.92 - $20.13    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 16.50 vs 16.35               |
| Trend        | Close above SMA50                         | 0      | 8   | 16.50 vs 16.76               |
| Trend        | Close above SMA200                        | 0      | 8   | 16.50 vs 23.03               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 16.35 vs 16.76               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 16.76 vs 23.03               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.56                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 48.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.04 vs -0.02                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.30              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 4.76%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.10x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1351511183 vs 1171599169     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.36x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.6, +DI 22.1, -DI 22.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 18.24               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.66%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 18.03%                       |

## Support And Resistance

- Support levels: $14.89, $15.59, $16.61
- Resistance levels: $18.04, $18.80, $19.55, $20.13, $22.00

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $15.88 - $16.58 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $15.42 | $18.10   | $19.03   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $18.04 - $18.51 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $16.35 | $22.13   | $24.05   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
