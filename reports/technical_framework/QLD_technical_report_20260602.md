# QLD Technical Analysis Sample

Generated: 2026-06-02 16:57:34
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (83/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QLD_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QLD_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $100.53            |
| SMA20             | $92.90             |
| SMA50             | $79.58             |
| SMA200            | $71.60             |
| RSI14             | 79.2               |
| MACD / Signal     | 5.30 / 5.12        |
| ADX14 / +DI / -DI | 39.0 / 39.2 / 13.0 |
| ATR14             | $2.52 (2.51%)      |
| 63-day range      | $56.60 - $100.60   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 100.53 vs 92.90              |
| Trend        | Close above SMA50                         | 8      | 8   | 100.53 vs 79.58              |
| Trend        | Close above SMA200                        | 8      | 8   | 100.53 vs 71.60              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 92.90 vs 79.58               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 79.58 vs 71.60               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 10.40                        |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 79.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | 5.30 vs 5.12                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.30               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 22.18%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.80x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 290480504 vs 273783315       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.62x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 39.0, +DI 39.2, -DI 13.0 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 101.36              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.51%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.07%                        |

## Support And Resistance

- Support levels: $69.83, $79.58, $84.43, $87.52, $92.46
- Resistance levels: $100.79

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $91.64 - $93.53   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $77.06 | $123.63  | $139.15  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $100.60 - $101.86 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $95.49 | $112.70  | $118.44  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
