# SNDK Technical Analysis Sample

Generated: 2026-07-06 16:40:26
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (46/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SNDK_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SNDK_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $1,744.43           |
| SMA20             | $1,950.95           |
| SMA50             | $1,625.76           |
| SMA200            | $711.62             |
| RSI14             | 46.8                |
| MACD / Signal     | 96.85 / 152.07      |
| ADX14 / +DI / -DI | 32.7 / 27.9 / 28.2  |
| ATR14             | $204.52 (11.72%)    |
| 63-day range      | $687.68 - $2,354.39 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 1744.43 vs 1950.95           |
| Trend        | Close above SMA50                         | 8      | 8   | 1744.43 vs 1625.76           |
| Trend        | Close above SMA200                        | 8      | 8   | 1744.43 vs 711.62            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1950.95 vs 1625.76           |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 1625.76 vs 711.62            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 463.51                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | 96.85 vs 152.07              |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -60.21             |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -0.87%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.73x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 518963597 vs 554370960       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.92x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 32.7, +DI 27.9, -DI 28.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 2410.08             |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 11.72%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 25.91%                       |

## Support And Resistance

- Support levels: $547.56, $687.68, $1,277.33, $1,543.98, $1,693.00
- Resistance levels: $1,861.00, $2,368.31

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop      | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | --------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $1,590.74 - $1,744.13 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $1,421.24 | $2,159.82 | $2,406.01 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,861.00 - $1,963.26 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $1,693.00 | $2,350.39 | $2,569.52 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
