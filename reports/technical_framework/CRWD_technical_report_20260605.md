# CRWD Technical Analysis Sample

Generated: 2026-06-05 16:40:33
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (78/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWD_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWD_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $671.02            |
| SMA20             | $647.90            |
| SMA50             | $515.70            |
| SMA200            | $478.04            |
| RSI14             | 58.3               |
| MACD / Signal     | 63.35 / 63.82      |
| ADX14 / +DI / -DI | 51.3 / 35.5 / 18.5 |
| ATR14             | $35.10 (5.23%)     |
| 63-day range      | $361.81 - $785.66  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 671.02 vs 647.90             |
| Trend        | Close above SMA50                         | 8      | 8   | 671.02 vs 515.70             |
| Trend        | Close above SMA200                        | 8      | 8   | 671.02 vs 478.04             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 647.90 vs 515.70             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 515.70 vs 478.04             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 92.96                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 58.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | 63.35 vs 63.82               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -9.77              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 32.69%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.33x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | -26086842 vs -18408777       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.28x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 51.3, +DI 35.5, -DI 18.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 799.40              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.23%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 14.59%                       |

## Support And Resistance

- Support levels: $439.18, $470.25, $506.05, $642.46, $670.10
- Resistance levels: $789.10

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $652.55 - $678.88 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $480.60 | $1,035.94 | $1,221.05 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $785.66 - $803.21 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $670.10 | $1,043.11 | $1,167.44 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
