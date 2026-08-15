# SMH Technical Analysis Sample

Generated: 2026-06-08 21:13:29
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (83/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SMH_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SMH_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $598.16            |
| SMA20             | $585.67            |
| SMA50             | $511.29            |
| SMA200            | $397.80            |
| RSI14             | 57.7               |
| MACD / Signal     | 26.84 / 30.45      |
| ADX14 / +DI / -DI | 32.4 / 25.2 / 23.0 |
| ATR14             | $23.88 (3.99%)     |
| 63-day range      | $359.86 - $642.77  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 598.16 vs 585.67             |
| Trend        | Close above SMA50                         | 8      | 8   | 598.16 vs 511.29             |
| Trend        | Close above SMA200                        | 8      | 8   | 598.16 vs 397.80             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 585.67 vs 511.29             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 511.29 vs 397.80             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 76.73                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 57.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | 26.84 vs 30.45               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -3.84              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 5.58%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.25x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 310380013 vs 305320706       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.95x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 32.4, +DI 25.2, -DI 23.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 640.37              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.99%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 6.94%                        |

## Support And Resistance

- Support levels: $368.42, $391.92, $511.29, $529.42, $578.46
- Resistance levels: $642.17

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $573.73 - $591.64 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $487.41 | $773.23  | $868.50  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $642.17 - $654.11 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $585.67 | $773.07  | $835.54  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
