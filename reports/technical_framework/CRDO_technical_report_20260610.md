# CRDO Technical Analysis Sample

Generated: 2026-06-10 20:55:30
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (88/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRDO_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRDO_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $237.68            |
| SMA20             | $207.79            |
| SMA50             | $178.84            |
| SMA200            | $149.62            |
| RSI14             | 63.7               |
| MACD / Signal     | 14.46 / 14.19      |
| ADX14 / +DI / -DI | 31.9 / 26.1 / 10.1 |
| ATR14             | $23.29 (9.80%)     |
| 63-day range      | $86.49 - $261.38   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 237.68 vs 207.79             |
| Trend        | Close above SMA50                         | 8      | 8   | 237.68 vs 178.84             |
| Trend        | Close above SMA200                        | 8      | 8   | 237.68 vs 149.62             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 207.79 vs 178.84             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 178.84 vs 149.62             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 40.72                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 63.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | 14.46 vs 14.19               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.95              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 19.70%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.51x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 232974877 vs 194417404       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.86x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 31.9, +DI 26.1, -DI 10.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 256.69              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.80%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 9.07%                        |

## Support And Resistance

- Support levels: $123.85, $144.41, $161.84, $180.82, $206.22
- Resistance levels: $257.36

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $199.22 - $216.69 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $155.55 | $312.78  | $365.19  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $257.36 - $269.00 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $210.87 | $367.80  | $420.11  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
