# CRDO Technical Analysis Sample

Generated: 2026-06-26 06:53:42
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (88/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRDO_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRDO_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $268.03            |
| SMA20             | $244.68            |
| SMA50             | $209.13            |
| SMA200            | $156.43            |
| RSI14             | 59.3               |
| MACD / Signal     | 20.73 / 19.59      |
| ADX14 / +DI / -DI | 38.6 / 25.0 / 11.7 |
| ATR14             | $25.92 (9.67%)     |
| 63-day range      | $86.49 - $308.67   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 268.03 vs 244.68             |
| Trend        | Close above SMA50                         | 8      | 8   | 268.03 vs 209.13             |
| Trend        | Close above SMA200                        | 8      | 8   | 268.03 vs 156.43             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 244.68 vs 209.13             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 209.13 vs 156.43             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 55.13                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 59.3                   |
| Momentum     | MACD above signal                         | 7      | 7   | 20.73 vs 19.59               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.33               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 21.15%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.81x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 242935200 vs 231949335       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.45x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 38.6, +DI 25.0, -DI 11.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 294.03              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.67%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.17%                       |

## Support And Resistance

- Support levels: $164.80, $192.71, $209.13, $242.94, $259.00
- Resistance levels: $270.21, $305.01

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $246.04 - $265.48 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $183.21 | $400.85  | $473.40  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $270.21 - $283.17 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $259.00 | $328.53  | $354.45  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
