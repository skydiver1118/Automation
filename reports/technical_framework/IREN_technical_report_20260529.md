# IREN Technical Analysis Sample

Generated: 2026-05-31 20:26:18
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (93/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [IREN_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/IREN_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $63.54             |
| SMA20             | $56.41             |
| SMA50             | $47.77             |
| SMA200            | $45.69             |
| RSI14             | 60.4               |
| MACD / Signal     | 4.02 / 3.27        |
| ADX14 / +DI / -DI | 25.2 / 35.1 / 18.0 |
| ATR14             | $4.95 (7.79%)      |
| 63-day range      | $30.76 - $68.13    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 63.54 vs 56.41               |
| Trend        | Close above SMA50                         | 8      | 8   | 63.54 vs 47.77               |
| Trend        | Close above SMA200                        | 8      | 8   | 63.54 vs 45.69               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 56.41 vs 47.77               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 47.77 vs 45.69               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 5.90                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 60.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 4.02 vs 3.27                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.18               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 39.62%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.87x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 916141400 vs 906815465       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.22x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 25.2, +DI 35.1, -DI 18.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 67.72               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.79%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 6.73%                        |

## Support And Resistance

- Support levels: $38.10, $44.16, $48.30, $52.36, $56.25
- Resistance levels: $64.60, $68.02

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $53.93 - $57.64 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $42.82 | $81.73   | $94.70   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $64.60 - $67.07 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $56.41 | $84.70   | $94.13   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
