# SMH Technical Analysis Sample

Generated: 2026-06-04 19:39:32
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (97/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SMH_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SMH_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $627.53            |
| SMA20             | $582.61            |
| SMA50             | $503.53            |
| SMA200            | $394.85            |
| RSI14             | 72.5               |
| MACD / Signal     | 33.90 / 31.97      |
| ADX14 / +DI / -DI | 36.8 / 34.5 / 18.2 |
| ATR14             | $20.22 (3.22%)     |
| 63-day range      | $359.86 - $642.77  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 627.53 vs 582.61             |
| Trend        | Close above SMA50                         | 8      | 8   | 627.53 vs 503.53             |
| Trend        | Close above SMA200                        | 8      | 8   | 627.53 vs 394.85             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 582.61 vs 503.53             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 503.53 vs 394.85             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 74.34                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 72.5                   |
| Momentum     | MACD above signal                         | 7      | 7   | 33.90 vs 31.97               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.68               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 14.15%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.01x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 309920140 vs 295956342       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.29x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 36.8, +DI 34.5, -DI 18.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 640.74              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.22%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 2.37%                        |

## Support And Resistance

- Support levels: $378.24, $397.77, $503.53, $526.17, $580.83
- Resistance levels: $642.26

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $572.50 - $587.66 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $483.31 | $773.62  | $870.39  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $642.26 - $652.37 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $587.10 | $767.76  | $827.98  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
