# IREN Technical Analysis Sample

Generated: 2026-06-02 16:57:51
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (93/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [IREN_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/IREN_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $66.60             |
| SMA20             | $58.25             |
| SMA50             | $48.75             |
| SMA200            | $46.16             |
| RSI14             | 63.1               |
| MACD / Signal     | 4.46 / 3.66        |
| ADX14 / +DI / -DI | 27.0 / 36.3 / 15.2 |
| ATR14             | $5.06 (7.60%)      |
| 63-day range      | $30.76 - $69.57    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 66.60 vs 58.25               |
| Trend        | Close above SMA50                         | 8      | 8   | 66.60 vs 48.75               |
| Trend        | Close above SMA200                        | 8      | 8   | 66.60 vs 46.16               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 58.25 vs 48.75               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 48.75 vs 46.16               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 6.64                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 63.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | 4.46 vs 3.66                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.80               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 34.60%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.72x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 988869656 vs 897564303       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.24x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 27.0, +DI 36.3, -DI 15.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 69.11               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.60%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 4.27%                        |

## Support And Resistance

- Support levels: $38.10, $43.92, $48.32, $52.36, $58.03
- Resistance levels: $69.19

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $55.72 - $59.51 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $43.69 | $85.47   | $99.39   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $69.19 - $71.72 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $58.25 | $94.87   | $107.07  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
