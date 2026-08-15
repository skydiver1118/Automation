# RKLB Technical Analysis Sample

Generated: 2026-06-26 06:53:24
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (30/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKLB_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKLB_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $80.69             |
| SMA20             | $110.83            |
| SMA50             | $105.58            |
| SMA200            | $74.70             |
| RSI14             | 34.2               |
| MACD / Signal     | -5.97 / -1.68      |
| ADX14 / +DI / -DI | 28.3 / 11.9 / 32.2 |
| ATR14             | $10.01 (12.40%)    |
| 63-day range      | $56.13 - $151.00   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 80.69 vs 110.83              |
| Trend        | Close above SMA50                         | 0      | 8   | 80.69 vs 105.58              |
| Trend        | Close above SMA200                        | 8      | 8   | 80.69 vs 74.70               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 110.83 vs 105.58             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 105.58 vs 74.70              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 17.20                        |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 34.2                   |
| Momentum     | MACD above signal                         | 0      | 7   | -5.97 vs -1.68               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.83              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -46.29%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.92x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1678887400 vs 1842217130     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.34x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 28.3, +DI 11.9, -DI 32.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 143.11              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 12.40%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 46.56%                       |

## Support And Resistance

- Support levels: $56.13, $65.49, $78.14
- Resistance levels: $91.49, $99.58, $140.74, $150.94

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $110.83 - $115.84 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $95.82 | $140.85  | $160.86  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $73.14 - $80.64   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $68.13 | $96.90   | $106.91  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $91.49 - $96.49   | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $78.14 | $125.68  | $141.53  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
