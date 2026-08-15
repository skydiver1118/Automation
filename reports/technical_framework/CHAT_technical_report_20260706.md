# CHAT Technical Analysis Sample

Generated: 2026-07-06 16:40:13
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (55/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CHAT_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CHAT_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $91.00             |
| SMA20             | $94.85             |
| SMA50             | $90.36             |
| SMA200            | $69.29             |
| RSI14             | 46.7               |
| MACD / Signal     | 0.61 / 1.90        |
| ADX14 / +DI / -DI | 16.2 / 23.1 / 35.5 |
| ATR14             | $4.48 (4.93%)      |
| 63-day range      | $62.78 - $105.20   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 91.00 vs 94.85               |
| Trend        | Close above SMA50                         | 8      | 8   | 91.00 vs 90.36               |
| Trend        | Close above SMA200                        | 8      | 8   | 91.00 vs 69.29               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 94.85 vs 90.36               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 90.36 vs 69.29               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 10.61                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | 0.61 vs 1.90                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.58              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -9.21%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.41x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 19729883 vs 19880894         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.05x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 16.2, +DI 23.1, -DI 35.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 103.26              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.93%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.50%                       |

## Support And Resistance

- Support levels: $62.71, $74.70, $81.50, $86.67, $90.36
- Resistance levels: $104.61

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $88.12 - $91.48   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $85.88 | $104.61  | $103.25  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $104.61 - $106.85 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $90.36 | $136.48  | $151.85  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
