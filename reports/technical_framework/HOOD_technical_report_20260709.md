# HOOD Technical Analysis Sample

Generated: 2026-07-09 16:40:25
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (89/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [HOOD_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/HOOD_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $115.11            |
| SMA20             | $103.04            |
| SMA50             | $88.95             |
| SMA200            | $102.26            |
| RSI14             | 65.6               |
| MACD / Signal     | 7.25 / 6.34        |
| ADX14 / +DI / -DI | 28.9 / 32.7 / 14.8 |
| ATR14             | $6.61 (5.74%)      |
| 63-day range      | $67.80 - $120.05   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 115.11 vs 103.04             |
| Trend        | Close above SMA50                         | 8      | 8   | 115.11 vs 88.95              |
| Trend        | Close above SMA200                        | 8      | 8   | 115.11 vs 102.26             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 103.04 vs 88.95              |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 88.95 vs 102.26              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 10.06                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 65.6                   |
| Momentum     | MACD above signal                         | 7      | 7   | 7.25 vs 6.34                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.65               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 37.41%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.57x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1603140464 vs 1509267393     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.12x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 28.9, +DI 32.7, -DI 14.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 120.44              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.74%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 4.11%                        |

## Support And Resistance

- Support levels: $87.30, $92.80, $103.51, $108.89, $113.87
- Resistance levels: $120.26

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $110.57 - $115.52 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $82.35  | $174.44  | $205.14  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $120.05 - $123.35 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $113.87 | $137.37  | $145.20  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
