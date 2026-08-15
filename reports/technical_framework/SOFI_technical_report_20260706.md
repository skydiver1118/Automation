# SOFI Technical Analysis Sample

Generated: 2026-07-06 16:40:27
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (81/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SOFI_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SOFI_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $18.61             |
| SMA20             | $17.33             |
| SMA50             | $16.87             |
| SMA200            | $22.29             |
| RSI14             | 61.2               |
| MACD / Signal     | 0.43 / 0.30        |
| ADX14 / +DI / -DI | 26.3 / 26.4 / 10.4 |
| ATR14             | $0.95 (5.11%)      |
| 63-day range      | $14.92 - $20.13    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 18.61 vs 17.33               |
| Trend        | Close above SMA50                         | 8      | 8   | 18.61 vs 16.87               |
| Trend        | Close above SMA200                        | 0      | 8   | 18.61 vs 22.29               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 17.33 vs 16.87               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 16.87 vs 22.29               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.11                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 61.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.43 vs 0.30                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.05               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 8.51%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.94x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1658356752 vs 1467797968     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.44x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 26.3, +DI 26.4, -DI 10.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 18.91               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.11%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 7.55%                        |

## Support And Resistance

- Support levels: $15.27, $16.72, $17.60
- Resistance levels: $18.87, $19.55, $20.13, $22.00, $26.40

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $17.12 - $17.83 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $15.92 | $20.60   | $22.17   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $18.87 - $19.34 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $17.60 | $22.13   | $23.64   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
