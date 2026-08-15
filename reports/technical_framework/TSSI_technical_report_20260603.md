# TSSI Technical Analysis Sample

Generated: 2026-06-03 19:37:41
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (70/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSSI_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSSI_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $13.93             |
| SMA20             | $12.97             |
| SMA50             | $13.66             |
| SMA200            | $12.65             |
| RSI14             | 52.2               |
| MACD / Signal     | 0.28 / -0.08       |
| ADX14 / +DI / -DI | 26.3 / 31.6 / 22.6 |
| ATR14             | $1.40 (10.06%)     |
| 63-day range      | $8.65 - $17.49     |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 13.93 vs 12.97               |
| Trend        | Close above SMA50                         | 8      | 8   | 13.93 vs 13.66               |
| Trend        | Close above SMA200                        | 8      | 8   | 13.93 vs 12.65               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 12.97 vs 13.66               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 13.66 vs 12.65               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.96                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 52.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 0.28 vs -0.08                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.38               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -12.39%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.75x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 24449819 vs 21888821         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.82x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 26.3, +DI 31.6, -DI 22.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 17.01               |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.06%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 20.35%                       |

## Support And Resistance

- Support levels: $7.23, $8.74, $10.25, $11.67, $13.68
- Resistance levels: $14.36, $17.26

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $12.98 - $14.03 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $12.26 | $16.30   | $17.71   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $14.36 - $15.06 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $13.68 | $17.51   | $18.91   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
