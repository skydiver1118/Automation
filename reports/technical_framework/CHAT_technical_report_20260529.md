# CHAT Technical Analysis Sample

Generated: 2026-05-31 20:25:41
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (97/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CHAT_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CHAT_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $98.22             |
| SMA20             | $87.38             |
| SMA50             | $76.69             |
| SMA200            | $64.16             |
| RSI14             | 76.2               |
| MACD / Signal     | 5.17 / 4.45        |
| ADX14 / +DI / -DI | 31.8 / 45.5 / 16.1 |
| ATR14             | $2.80 (2.85%)      |
| 63-day range      | $58.52 - $98.67    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 98.22 vs 87.38               |
| Trend        | Close above SMA50                         | 8      | 8   | 98.22 vs 76.69               |
| Trend        | Close above SMA200                        | 8      | 8   | 98.22 vs 64.16               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 87.38 vs 76.69               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 76.69 vs 64.16               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 9.32                         |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 76.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 5.17 vs 4.45                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.98               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 25.94%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.09x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 21689500 vs 18693850         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.51x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 31.8, +DI 45.5, -DI 16.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 97.65               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.85%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.46%                        |

## Support And Resistance

- Support levels: $62.69, $74.70, $76.90, $81.50, $87.35
- Resistance levels: $98.41

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $85.98 - $88.08 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $73.89 | $113.32  | $126.47  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $98.41 - $99.82 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $92.61 | $112.12  | $118.63  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
