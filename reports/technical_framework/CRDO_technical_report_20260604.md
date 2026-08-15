# CRDO Technical Analysis Sample

Generated: 2026-06-04 19:39:46
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (83/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRDO_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRDO_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $217.50            |
| SMA20             | $202.01            |
| SMA50             | $168.48            |
| SMA200            | $147.30            |
| RSI14             | 58.6               |
| MACD / Signal     | 15.04 / 14.71      |
| ADX14 / +DI / -DI | 31.4 / 23.1 / 15.9 |
| ATR14             | $19.91 (9.15%)     |
| 63-day range      | $86.49 - $245.95   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 217.50 vs 202.01             |
| Trend        | Close above SMA50                         | 8      | 8   | 217.50 vs 168.48             |
| Trend        | Close above SMA200                        | 8      | 8   | 217.50 vs 147.30             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 202.01 vs 168.48             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 168.48 vs 147.30             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 36.79                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 58.6                   |
| Momentum     | MACD above signal                         | 7      | 7   | 15.04 vs 14.71               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.01              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 9.69%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.96x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 214037966 vs 192522058       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.52x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 31.4, +DI 23.1, -DI 15.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 247.26              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.15%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.57%                       |

## Support And Resistance

- Support levels: $136.32, $152.85, $166.64, $182.80, $201.87
- Resistance levels: $246.28

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $193.65 - $208.58 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $148.57 | $306.21  | $358.75  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $245.95 - $255.90 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $203.61 | $345.57  | $392.89  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
