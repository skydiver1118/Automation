# RKLB Technical Analysis Sample

Generated: 2026-06-28 17:42:29
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (38/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKLB_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKLB_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $84.54             |
| SMA20             | $107.66            |
| SMA50             | $105.80            |
| SMA200            | $74.89             |
| RSI14             | 37.2               |
| MACD / Signal     | -6.79 / -2.70      |
| ADX14 / +DI / -DI | 29.6 / 11.6 / 30.9 |
| ATR14             | $9.69 (11.46%)     |
| 63-day range      | $56.13 - $151.00   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 84.54 vs 107.66              |
| Trend        | Close above SMA50                         | 0      | 8   | 84.54 vs 105.80              |
| Trend        | Close above SMA200                        | 8      | 8   | 84.54 vs 74.89               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 107.66 vs 105.80             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 105.80 vs 74.89              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 16.03                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 37.2                   |
| Momentum     | MACD above signal                         | 0      | 7   | -6.79 vs -2.70               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.06              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -42.89%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.16x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1708947400 vs 1826139195     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.46x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 29.6, +DI 11.6, -DI 30.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 136.87              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 11.46%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 44.01%                       |

## Support And Resistance

- Support levels: $56.13, $65.49, $78.11
- Resistance levels: $91.49, $99.58, $137.63, $144.00, $151.00

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $107.66 - $112.50 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $93.12 | $136.73  | $156.11  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $73.27 - $80.53   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $68.42 | $96.28   | $105.97  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $91.49 - $96.33   | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $78.11 | $125.50  | $141.30  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
