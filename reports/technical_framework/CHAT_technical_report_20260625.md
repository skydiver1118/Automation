# CHAT Technical Analysis Sample

Generated: 2026-06-26 06:53:09
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (86/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CHAT_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CHAT_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $97.78             |
| SMA20             | $96.97             |
| SMA50             | $88.19             |
| SMA200            | $68.19             |
| RSI14             | 55.1               |
| MACD / Signal     | 2.83 / 3.24        |
| ADX14 / +DI / -DI | 18.4 / 29.8 / 28.4 |
| ATR14             | $4.40 (4.50%)      |
| 63-day range      | $58.52 - $105.20   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 97.78 vs 96.97               |
| Trend        | Close above SMA50                         | 8      | 8   | 97.78 vs 88.19               |
| Trend        | Close above SMA200                        | 8      | 8   | 97.78 vs 68.19               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 96.97 vs 88.19               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 88.19 vs 68.19               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 12.77                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 55.1                   |
| Momentum     | MACD above signal                         | 0      | 7   | 2.83 vs 3.24                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.21               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 4.24%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.01x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 20893200 vs 20836335         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.06x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.4, +DI 29.8, -DI 28.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 106.24              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.50%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 7.05%                        |

## Support And Resistance

- Support levels: $62.69, $74.70, $81.50, $87.32, $95.39
- Resistance levels: $105.21

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $94.77 - $98.07   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $83.79 | $121.69  | $134.33  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $105.20 - $107.40 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $96.97 | $124.95  | $134.28  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
