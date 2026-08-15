# RKLB Technical Analysis Sample

Generated: 2026-06-05 16:40:44
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (56/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKLB_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKLB_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $110.08            |
| SMA20             | $127.56            |
| SMA50             | $96.14             |
| SMA200            | $71.00             |
| RSI14             | 46.6               |
| MACD / Signal     | 7.17 / 11.58       |
| ADX14 / +DI / -DI | 32.8 / 22.1 / 24.2 |
| ATR14             | $11.15 (10.13%)    |
| 63-day range      | $56.13 - $151.00   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 110.08 vs 127.56             |
| Trend        | Close above SMA50                         | 8      | 8   | 110.08 vs 96.14              |
| Trend        | Close above SMA200                        | 8      | 8   | 110.08 vs 71.00              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 127.56 vs 96.14              |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 96.14 vs 71.00               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 22.83                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | 7.17 vs 11.58                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -6.19              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 40.09%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.66x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1908954490 vs 1918188424     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.54x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 32.8, +DI 22.1, -DI 24.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 152.14              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 10.13%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 27.10%                       |

## Support And Resistance

- Support levels: $54.98, $65.49, $77.00, $96.14, $104.85
- Resistance levels: $138.38, $151.29

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $99.28 - $107.64  | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $84.99  | $140.40  | $158.87  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $138.38 - $143.95 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $104.85 | $213.80  | $250.11  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
