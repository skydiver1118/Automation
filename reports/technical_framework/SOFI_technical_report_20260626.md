# SOFI Technical Analysis Sample

Generated: 2026-06-28 17:42:33
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (76/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SOFI_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SOFI_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $17.88             |
| SMA20             | $17.18             |
| SMA50             | $16.95             |
| SMA200            | $22.49             |
| RSI14             | 57.4               |
| MACD / Signal     | 0.24 / 0.16        |
| ADX14 / +DI / -DI | 20.9 / 26.0 / 14.9 |
| ATR14             | $0.96 (5.39%)      |
| 63-day range      | $14.92 - $20.13    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 17.88 vs 17.18               |
| Trend        | Close above SMA50                         | 8      | 8   | 17.88 vs 16.95               |
| Trend        | Close above SMA200                        | 0      | 8   | 17.88 vs 22.49               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 17.18 vs 16.95               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 16.95 vs 22.49               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.26                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 57.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.24 vs 0.16                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.06              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 5.36%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.03x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1579048700 vs 1428871410     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.18x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 20.9, +DI 26.0, -DI 14.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 18.60               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.39%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.18%                       |

## Support And Resistance

- Support levels: $15.27, $16.87, $17.76
- Resistance levels: $17.85, $18.66, $19.55, $20.13, $22.00

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $17.27 - $18.00 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $15.99 | $20.92   | $22.57   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $18.66 - $19.15 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $17.76 | $21.21   | $22.36   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
