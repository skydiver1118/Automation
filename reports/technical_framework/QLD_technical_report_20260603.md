# QLD Technical Analysis Sample

Generated: 2026-06-03 19:37:04
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (92/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QLD_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QLD_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $100.00            |
| SMA20             | $93.68             |
| SMA50             | $80.30             |
| SMA200            | $71.79             |
| RSI14             | 77.0               |
| MACD / Signal     | 5.26 / 5.15        |
| ADX14 / +DI / -DI | 39.9 / 38.6 / 12.2 |
| ATR14             | $2.48 (2.48%)      |
| 63-day range      | $56.60 - $101.19   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 100.00 vs 93.68              |
| Trend        | Close above SMA50                         | 8      | 8   | 100.00 vs 80.30              |
| Trend        | Close above SMA200                        | 8      | 8   | 100.00 vs 71.79              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 93.68 vs 80.30               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 80.30 vs 71.79               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 10.78                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 77.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 5.26 vs 5.15                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.18               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 18.50%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.92x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 282672466 vs 270801243       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.31x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 39.9, +DI 38.6, -DI 12.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 101.71              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.48%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 1.18%                        |

## Support And Resistance

- Support levels: $71.40, $80.30, $85.64, $87.52, $93.21
- Resistance levels: $101.32

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $92.43 - $94.30   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $77.82 | $124.46  | $140.00  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $101.19 - $102.43 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $95.03 | $115.37  | $122.15  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
