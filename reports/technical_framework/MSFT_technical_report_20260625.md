# MSFT Technical Analysis Sample

Generated: 2026-06-26 06:53:35
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (19/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MSFT_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MSFT_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $352.83            |
| SMA20             | $402.81            |
| SMA50             | $411.27            |
| SMA200            | $446.88            |
| RSI14             | 28.8               |
| MACD / Signal     | -14.11 / -8.64     |
| ADX14 / +DI / -DI | 23.9 / 16.5 / 44.8 |
| ATR14             | $12.39 (3.51%)     |
| 63-day range      | $349.20 - $466.32  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 352.83 vs 402.81             |
| Trend        | Close above SMA50                         | 0      | 8   | 352.83 vs 411.27             |
| Trend        | Close above SMA200                        | 0      | 8   | 352.83 vs 446.88             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 402.81 vs 411.27             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 411.27 vs 446.88             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 10.96                        |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 28.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | -14.11 vs -8.64              |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.44              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -14.50%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.53x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | -279553900 vs -137133710     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.67x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 23.9, +DI 16.5, -DI 44.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 462.07              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.51%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 24.34%                       |

## Support And Resistance

- Support levels: $347.32, $355.51
- Resistance levels: $373.18, $384.17, $409.38, $428.48, $465.26

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $411.27 - $417.46 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $392.68 | $448.44  | $473.23  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $341.12 - $350.41 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $334.92 | $373.18  | $382.94  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $373.18 - $379.38 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $347.32 | $434.21  | $463.17  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
