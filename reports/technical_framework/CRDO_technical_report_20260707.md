# CRDO Technical Analysis Sample

Generated: 2026-07-07 16:40:38
Data source: yfinance adjusted daily OHLCV through 2026-07-07.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (58/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRDO_technical_chart_20260707.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRDO_technical_chart_20260707.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $246.40            |
| SMA20             | $255.49            |
| SMA50             | $220.09            |
| SMA200            | $159.63            |
| RSI14             | 50.7               |
| MACD / Signal     | 10.59 / 14.50      |
| ADX14 / +DI / -DI | 27.4 / 19.4 / 19.4 |
| ATR14             | $28.38 (11.52%)    |
| 63-day range      | $101.65 - $308.67  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 246.40 vs 255.49             |
| Trend        | Close above SMA50                         | 8      | 8   | 246.40 vs 220.09             |
| Trend        | Close above SMA200                        | 8      | 8   | 246.40 vs 159.63             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 255.49 vs 220.09             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 220.09 vs 159.63             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 49.55                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 50.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | 10.59 vs 14.50               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.90              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 19.10%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.71x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 194969251 vs 222608193       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.98x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 27.4, +DI 19.4, -DI 19.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 292.31              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 11.52%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 20.17%                       |

## Support And Resistance

- Support levels: $156.87, $182.80, $200.00, $221.47, $247.82
- Resistance levels: $245.95, $281.01, $308.67

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $207.28 - $228.56 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $191.71 | $281.01  | $303.06  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $281.01 - $295.20 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $221.47 | $421.37  | $488.00  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
