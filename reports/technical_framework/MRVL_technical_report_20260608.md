# MRVL Technical Analysis Sample

Generated: 2026-06-08 21:13:36
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (93/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MRVL_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MRVL_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $288.85            |
| SMA20             | $214.46            |
| SMA50             | $169.16            |
| SMA200            | $104.51            |
| RSI14             | 69.2               |
| MACD / Signal     | 34.75 / 26.48      |
| ADX14 / +DI / -DI | 51.1 / 36.8 / 12.3 |
| ATR14             | $24.39 (8.44%)     |
| 63-day range      | $85.09 - $324.20   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 288.85 vs 214.46             |
| Trend        | Close above SMA50                         | 8      | 8   | 288.85 vs 169.16             |
| Trend        | Close above SMA200                        | 8      | 8   | 288.85 vs 104.51             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 214.46 vs 169.16             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 169.16 vs 104.51             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 50.57                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 69.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 34.75 vs 26.48               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 6.50               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 69.78%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.75x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1168193793 vs 821107925      |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 3.32x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 51.1, +DI 36.8, -DI 12.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 312.45              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.44%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.90%                       |

## Support And Resistance

- Support levels: $80.56, $122.45, $159.20, $219.66
- Resistance levels: $321.26

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $212.66 - $230.95 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $144.77 | $375.88  | $452.92  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $321.26 - $333.46 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $240.07 | $501.94  | $589.23  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
