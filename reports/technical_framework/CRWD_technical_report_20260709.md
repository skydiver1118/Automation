# CRWD Technical Analysis Sample

Generated: 2026-07-09 16:40:22
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (95/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWD_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWD_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $198.40            |
| SMA20             | $179.50            |
| SMA50             | $161.75            |
| SMA200            | $127.19            |
| RSI14             | 68.5               |
| MACD / Signal     | 9.68 / 8.70        |
| ADX14 / +DI / -DI | 36.7 / 31.4 / 12.6 |
| ATR14             | $9.45 (4.76%)      |
| 63-day range      | $91.12 - $209.50   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 198.40 vs 179.50             |
| Trend        | Close above SMA50                         | 8      | 8   | 198.40 vs 161.75             |
| Trend        | Close above SMA200                        | 8      | 8   | 198.40 vs 127.19             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 179.50 vs 161.75             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 161.75 vs 127.19             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 30.12                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 68.5                   |
| Momentum     | MACD above signal                         | 7      | 7   | 9.68 vs 8.70                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.16               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 23.05%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.51x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 130792650 vs 78333602        |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.86x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 36.7, +DI 31.4, -DI 12.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 203.90              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.76%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 5.30%                        |

## Support And Resistance

- Support levels: $90.40, $108.94, $155.94, $163.49, $182.18
- Resistance levels: $208.10

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $177.46 - $184.54 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $152.30 | $238.39  | $267.09  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $208.10 - $212.82 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $182.18 | $267.02  | $295.30  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
