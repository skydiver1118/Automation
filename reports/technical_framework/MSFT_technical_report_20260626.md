# MSFT Technical Analysis Sample

Generated: 2026-06-28 17:42:38
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (32/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MSFT_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MSFT_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $372.97            |
| SMA20             | $400.11            |
| SMA50             | $410.52            |
| SMA200            | $446.27            |
| RSI14             | 40.5               |
| MACD / Signal     | -13.75 / -9.66     |
| ADX14 / +DI / -DI | 24.3 / 21.1 / 39.1 |
| ATR14             | $13.20 (3.54%)     |
| 63-day range      | $349.20 - $466.32  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 372.97 vs 400.11             |
| Trend        | Close above SMA50                         | 0      | 8   | 372.97 vs 410.52             |
| Trend        | Close above SMA200                        | 0      | 8   | 372.97 vs 446.27             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 400.11 vs 410.52             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 410.52 vs 446.27             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 9.64                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 40.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | -13.75 vs -9.66              |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.96               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -12.65%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 3.72x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | -108248000 vs -150621295     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.89x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 24.3, +DI 21.1, -DI 39.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 459.65              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.54%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 20.02%                       |

## Support And Resistance

- Support levels: $340.56, $351.30
- Resistance levels: $373.18, $384.17, $409.38, $428.48, $464.65

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $410.52 - $417.12 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $390.71 | $450.14  | $476.55  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $344.70 - $354.60 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $338.10 | $376.06  | $389.27  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $373.18 - $379.78 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $351.30 | $426.84  | $452.02  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
