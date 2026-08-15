# VRSN Technical Analysis Sample

Generated: 2026-06-04 19:39:37
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (72/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [VRSN_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/VRSN_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $293.79            |
| SMA20             | $295.71            |
| SMA50             | $278.07            |
| SMA200            | $256.83            |
| RSI14             | 53.8               |
| MACD / Signal     | 5.62 / 7.49        |
| ADX14 / +DI / -DI | 23.5 / 22.2 / 19.6 |
| ATR14             | $8.49 (2.89%)      |
| 63-day range      | $233.58 - $312.48  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 293.79 vs 295.71             |
| Trend        | Close above SMA50                         | 8      | 8   | 293.79 vs 278.07             |
| Trend        | Close above SMA200                        | 8      | 8   | 293.79 vs 256.83             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 295.71 vs 278.07             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 278.07 vs 256.83             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 23.98                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | 5.62 vs 7.49                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.43              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 6.82%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.50x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 23132752 vs 23195283         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.06x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 23.5, +DI 22.2, -DI 19.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 312.56              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.89%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 5.98%                        |

## Support And Resistance

- Support levels: $243.10, $252.84, $258.09, $279.64, $294.13
- Resistance levels: $302.97, $312.50

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $288.30 - $294.66 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $269.58 | $335.28  | $357.18  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $302.97 - $307.22 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $292.54 | $330.20  | $342.75  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
