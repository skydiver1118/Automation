# OPEN Technical Analysis Sample

Generated: 2026-06-28 17:42:25
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (24/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [OPEN_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/OPEN_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value             |
| ----------------- | ----------------- |
| Close             | $4.37             |
| SMA20             | $4.59             |
| SMA50             | $4.84             |
| SMA200            | $6.07             |
| RSI14             | 44.4              |
| MACD / Signal     | -0.14 / -0.12     |
| ADX14 / +DI / -DI | 9.7 / 20.4 / 19.5 |
| ATR14             | $0.34 (7.67%)     |
| 63-day range      | $4.08 - $6.00     |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                    |
| ------------ | ----------------------------------------- | ------ | --- | --------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 4.37 vs 4.59                |
| Trend        | Close above SMA50                         | 0      | 8   | 4.37 vs 4.84                |
| Trend        | Close above SMA200                        | 0      | 8   | 4.37 vs 6.07                |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 4.59 vs 4.84                |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 4.84 vs 6.07                |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.07                       |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 44.4                  |
| Momentum     | MACD above signal                         | 0      | 7   | -0.14 vs -0.12              |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.01             |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -13.81%                     |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 3.74x                       |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 6169829900 vs 5947704190    |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.16x                       |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 9.7, +DI 20.4, -DI 19.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 5.29               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.67%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 27.17%                      |

## Support And Resistance

- Support levels: $4.11
- Resistance levels: $4.51, $5.02, $5.55, $6.00, $6.30

## Entry Plans

| Plan           | Entry zone    | Trigger                                                                                                      | Stop  | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ------------- | ------------------------------------------------------------------------------------------------------------ | ----- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $4.84 - $5.01 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $4.34 | $5.85    | $6.52    | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $3.94 - $4.19 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $3.77 | $4.74    | $5.07    | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $4.51 - $4.68 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $4.11 | $5.57    | $6.05    | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
