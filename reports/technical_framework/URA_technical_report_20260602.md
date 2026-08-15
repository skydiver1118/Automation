# URA Technical Analysis Sample

Generated: 2026-06-02 16:57:44
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (72/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [URA_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/URA_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $53.42             |
| SMA20             | $51.97             |
| SMA50             | $52.02             |
| SMA200            | $48.58             |
| RSI14             | 54.8               |
| MACD / Signal     | -0.65 / -0.80      |
| ADX14 / +DI / -DI | 14.2 / 23.7 / 20.4 |
| ATR14             | $2.29 (4.30%)      |
| 63-day range      | $44.76 - $58.97    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 53.42 vs 51.97               |
| Trend        | Close above SMA50                         | 8      | 8   | 53.42 vs 52.02               |
| Trend        | Close above SMA200                        | 8      | 8   | 53.42 vs 48.58               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 51.97 vs 52.02               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 52.02 vs 48.58               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.15                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 54.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.65 vs -0.80               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.77               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -2.46%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.66x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 156341406 vs 149714155       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.91x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 14.2, +DI 23.7, -DI 20.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 58.33               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.30%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 9.41%                        |

## Support And Resistance

- Support levels: $45.49, $47.45, $49.49, $52.06, $53.66
- Resistance levels: $53.33, $55.06, $56.67, $58.71, $62.28

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $50.91 - $52.63 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $49.72 | $56.36   | $58.66   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $55.06 - $56.21 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $52.06 | $62.78   | $66.35   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
