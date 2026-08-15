# CHAT Technical Analysis Sample

Generated: 2026-06-28 17:42:19
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (50/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CHAT_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CHAT_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $93.61             |
| SMA20             | $96.81             |
| SMA50             | $88.60             |
| SMA200            | $68.38             |
| RSI14             | 49.6               |
| MACD / Signal     | 2.35 / 3.06        |
| ADX14 / +DI / -DI | 17.5 / 27.4 / 30.6 |
| ATR14             | $4.44 (4.74%)      |
| 63-day range      | $58.52 - $105.20   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 93.61 vs 96.81               |
| Trend        | Close above SMA50                         | 8      | 8   | 93.61 vs 88.60               |
| Trend        | Close above SMA200                        | 8      | 8   | 93.61 vs 68.38               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 96.81 vs 88.60               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 88.60 vs 68.38               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 12.55                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | 2.35 vs 3.06                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.53              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -3.36%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.72x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 20268000 vs 20781095         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.87x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.5, +DI 27.4, -DI 30.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 106.20              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.74%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.02%                       |

## Support And Resistance

- Support levels: $62.69, $74.70, $81.50, $87.36, $93.97
- Resistance levels: $105.20

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $86.38 - $89.71   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $84.16 | $105.20  | $101.37  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $105.20 - $107.42 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $88.60 | $141.73  | $159.45  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
