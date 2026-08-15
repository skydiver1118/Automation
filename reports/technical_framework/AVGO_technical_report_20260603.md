# AVGO Technical Analysis Sample

Generated: 2026-06-03 19:36:45
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (92/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AVGO_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AVGO_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $479.23            |
| SMA20             | $430.69            |
| SMA50             | $395.06            |
| SMA200            | $353.88            |
| RSI14             | 73.3               |
| MACD / Signal     | 17.46 / 13.05      |
| ADX14 / +DI / -DI | 29.1 / 40.0 / 11.0 |
| ATR14             | $17.61 (3.67%)     |
| 63-day range      | $289.96 - $495.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 479.23 vs 430.69             |
| Trend        | Close above SMA50                         | 8      | 8   | 479.23 vs 395.06             |
| Trend        | Close above SMA200                        | 8      | 8   | 479.23 vs 353.88             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 430.69 vs 395.06             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 395.06 vs 353.88             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 42.22                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 73.3                   |
| Momentum     | MACD above signal                         | 7      | 7   | 17.46 vs 13.05               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 7.66               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 12.14%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.61x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1275021738 vs 1235872537     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.96x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 29.1, +DI 40.0, -DI 11.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 472.27              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.67%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 3.19%                        |

## Support And Resistance

- Support levels: $329.81, $369.17, $392.94, $405.65, $431.51
- Resistance levels: $495.00

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $423.53 - $436.74 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $377.45 | $535.51  | $588.20  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $495.00 - $503.80 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $444.01 | $610.18  | $665.57  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
