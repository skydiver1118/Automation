# APP Technical Analysis Sample

Generated: 2026-07-06 16:40:11
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (60/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [APP_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/APP_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $543.79            |
| SMA20             | $503.46            |
| SMA50             | $501.84            |
| SMA200            | $539.61            |
| RSI14             | 56.9               |
| MACD / Signal     | 3.77 / -2.28       |
| ADX14 / +DI / -DI | 18.3 / 29.3 / 21.5 |
| ATR14             | $35.25 (6.48%)     |
| 63-day range      | $364.64 - $622.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 543.79 vs 503.46             |
| Trend        | Close above SMA50                         | 8      | 8   | 543.79 vs 501.84             |
| Trend        | Close above SMA200                        | 8      | 8   | 543.79 vs 539.61             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 503.46 vs 501.84             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 501.84 vs 539.61             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 32.48                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 56.9                   |
| Momentum     | MACD above signal                         | 7      | 7   | 3.77 vs -2.28                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 14.75              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -2.70%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 1.00x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 384640477 vs 389357009       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.63x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.3, +DI 29.3, -DI 21.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 574.25              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.48%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 12.57%                       |

## Support And Resistance

- Support levels: $363.62, $420.69, $458.67, $505.91
- Resistance levels: $573.54, $595.00, $622.00, $681.60

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $491.66 - $518.10 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $466.59 | $581.46  | $619.75  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $573.54 - $591.17 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $509.29 | $728.50  | $801.57  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
