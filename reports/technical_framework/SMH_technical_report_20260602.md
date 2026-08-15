# SMH Technical Analysis Sample

Generated: 2026-06-02 16:57:40
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (92/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SMH_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SMH_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $632.21            |
| SMA20             | $572.96            |
| SMA50             | $493.94            |
| SMA200            | $391.48            |
| RSI14             | 77.1               |
| MACD / Signal     | 32.48 / 30.88      |
| ADX14 / +DI / -DI | 36.3 / 38.0 / 13.8 |
| ATR14             | $19.24 (3.04%)     |
| 63-day range      | $359.86 - $632.57  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 632.21 vs 572.96             |
| Trend        | Close above SMA50                         | 8      | 8   | 632.21 vs 493.94             |
| Trend        | Close above SMA200                        | 8      | 8   | 632.21 vs 391.48             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 572.96 vs 493.94             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 493.94 vs 391.48             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 69.56                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 77.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | 32.48 vs 30.88               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.03               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 24.75%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.76x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 314961896 vs 298461720       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.34x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 36.3, +DI 38.0, -DI 13.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 626.83              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.04%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.06%                        |

## Support And Resistance

- Support levels: $378.24, $397.77, $493.94, $523.48, $570.40
- Resistance levels: $631.14

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $563.34 - $577.77 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $474.70 | $762.26  | $858.12  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $632.57 - $642.19 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $593.74 | $724.67  | $768.31  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
