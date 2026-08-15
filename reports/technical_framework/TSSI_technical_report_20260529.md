# TSSI Technical Analysis Sample

Generated: 2026-05-31 20:26:21
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (92/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSSI_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSSI_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $16.48             |
| SMA20             | $13.01             |
| SMA50             | $13.45             |
| SMA200            | $12.69             |
| RSI14             | 65.7               |
| MACD / Signal     | -0.04 / -0.39      |
| ADX14 / +DI / -DI | 25.7 / 39.5 / 16.6 |
| ATR14             | $1.40 (8.50%)      |
| 63-day range      | $8.65 - $17.49     |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 16.48 vs 13.01               |
| Trend        | Close above SMA50                         | 8      | 8   | 16.48 vs 13.45               |
| Trend        | Close above SMA200                        | 8      | 8   | 16.48 vs 12.69               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 13.01 vs 13.45               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 13.45 vs 12.69               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 1.20                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 65.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.04 vs -0.39               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.72               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 7.57%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 4.15x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 29865100 vs 21193010         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.24x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 25.7, +DI 39.5, -DI 16.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 17.11               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.50%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 5.77%                        |

## Support And Resistance

- Support levels: $7.23, $8.71, $10.25, $11.67, $13.60
- Resistance levels: $17.28

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $12.90 - $13.95 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $12.05 | $17.28   | $17.63   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $17.28 - $17.98 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $13.68 | $25.53   | $29.48   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
