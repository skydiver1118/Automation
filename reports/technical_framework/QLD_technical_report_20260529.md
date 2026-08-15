# QLD Technical Analysis Sample

Generated: 2026-05-31 20:25:54
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (97/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QLD_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QLD_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $98.46             |
| SMA20             | $91.13             |
| SMA50             | $78.11             |
| SMA200            | $71.25             |
| RSI14             | 76.8               |
| MACD / Signal     | 5.12 / 5.04        |
| ADX14 / +DI / -DI | 37.2 / 40.9 / 14.7 |
| ATR14             | $2.57 (2.61%)      |
| 63-day range      | $56.60 - $99.35    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 98.46 vs 91.13               |
| Trend        | Close above SMA50                         | 8      | 8   | 98.46 vs 78.11               |
| Trend        | Close above SMA200                        | 8      | 8   | 98.46 vs 71.25               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 91.13 vs 78.11               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 78.11 vs 71.25               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 9.52                         |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 76.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | 5.12 vs 5.04                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.35               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 21.48%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.04x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 286125500 vs 275920450       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.30x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 37.2, +DI 40.9, -DI 14.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 100.23              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.61%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.90%                        |

## Support And Resistance

- Support levels: $69.62, $78.11, $82.03, $87.52, $90.73
- Resistance levels: $99.57

## Entry Plans

| Plan           | Entry zone       | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ---------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $89.85 - $91.77  | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $75.54 | $121.35  | $136.62  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $99.35 - $100.63 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $93.33 | $113.32  | $119.98  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
