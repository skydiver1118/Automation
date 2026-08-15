# MSFT Technical Analysis Sample

Generated: 2026-06-04 19:39:39
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (64/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MSFT_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MSFT_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $428.05            |
| SMA20             | $422.34            |
| SMA50             | $406.74            |
| SMA200            | $454.88            |
| RSI14             | 53.1               |
| MACD / Signal     | 7.36 / 6.55        |
| ADX14 / +DI / -DI | 20.0 / 36.0 / 29.1 |
| ATR14             | $12.71 (2.97%)     |
| 63-day range      | $355.51 - $466.32  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 428.05 vs 422.34             |
| Trend        | Close above SMA50                         | 8      | 8   | 428.05 vs 406.74             |
| Trend        | Close above SMA200                        | 0      | 8   | 428.05 vs 454.88             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 422.34 vs 406.74             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 406.74 vs 454.88             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 10.13                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | 7.36 vs 6.55                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.93               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 3.63%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.71x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 80159588 vs 35533829         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.96x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 20.0, +DI 36.0, -DI 29.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 450.66              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.97%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 8.21%                        |

## Support And Resistance

- Support levels: $355.51, $380.89, $394.91, $408.30, $423.72
- Resistance levels: $428.48, $450.66, $466.32, $486.84

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $418.21 - $427.74 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $394.03 | $480.87  | $509.82  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $428.48 - $434.83 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $424.57 | $457.08  | $469.79  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
