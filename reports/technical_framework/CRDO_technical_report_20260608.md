# CRDO Technical Analysis Sample

Generated: 2026-06-08 21:13:42
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (81/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRDO_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRDO_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $222.27            |
| SMA20             | $204.63            |
| SMA50             | $173.06            |
| SMA200            | $148.38            |
| RSI14             | 59.1               |
| MACD / Signal     | 13.19 / 14.20      |
| ADX14 / +DI / -DI | 30.3 / 21.3 / 13.2 |
| ATR14             | $20.73 (9.33%)     |
| 63-day range      | $86.49 - $245.95   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 222.27 vs 204.63             |
| Trend        | Close above SMA50                         | 8      | 8   | 222.27 vs 173.06             |
| Trend        | Close above SMA200                        | 8      | 8   | 222.27 vs 148.38             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 204.63 vs 173.06             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 173.06 vs 148.38             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 38.58                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 59.1                   |
| Momentum     | MACD above signal                         | 0      | 7   | 13.19 vs 14.20               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -3.91              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 17.91%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.04x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 201603215 vs 188883176       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.14x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 30.3, +DI 21.3, -DI 13.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 249.71              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.33%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 9.63%                        |

## Support And Resistance

- Support levels: $119.40, $136.32, $157.76, $177.93, $203.40
- Resistance levels: $246.89

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $195.21 - $210.76 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $152.33 | $304.30  | $354.95  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $245.95 - $256.32 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $205.57 | $342.25  | $387.81  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
