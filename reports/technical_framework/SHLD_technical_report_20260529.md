# SHLD Technical Analysis Sample

Generated: 2026-05-31 20:26:00
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (57/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SHLD_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SHLD_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $67.53             |
| SMA20             | $65.56             |
| SMA50             | $69.35             |
| SMA200            | $68.69             |
| RSI14             | 53.1               |
| MACD / Signal     | -0.85 / -1.50      |
| ADX14 / +DI / -DI | 32.5 / 28.5 / 26.0 |
| ATR14             | $1.32 (1.96%)      |
| 63-day range      | $62.21 - $78.45    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 67.53 vs 65.56               |
| Trend        | Close above SMA50                         | 0      | 8   | 67.53 vs 69.35               |
| Trend        | Close above SMA200                        | 0      | 8   | 67.53 vs 68.69               |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 65.56 vs 69.35               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 69.35 vs 68.69               |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.15                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | -0.85 vs -1.50               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.57               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -1.00%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 1.00x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 38546800 vs 34030675         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.08x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 32.5, +DI 28.5, -DI 26.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 69.03               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 1.96%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.92%                       |

## Support And Resistance

- Support levels: $60.49, $62.27, $65.16, $66.35, $67.96
- Resistance levels: $68.10, $69.03, $75.05, $76.79, $78.27

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $65.69 - $66.68 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $65.03 | $68.83   | $70.15   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $68.10 - $68.76 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $66.35 | $72.59   | $74.66   | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
