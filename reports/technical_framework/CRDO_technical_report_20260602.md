# CRDO Technical Analysis Sample

Generated: 2026-06-02 16:57:54
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (98/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRDO_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRDO_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $229.00            |
| SMA20             | $200.00            |
| SMA50             | $163.95            |
| SMA200            | $146.31            |
| RSI14             | 64.7               |
| MACD / Signal     | 16.92 / 14.33      |
| ADX14 / +DI / -DI | 33.1 / 29.0 / 15.3 |
| ATR14             | $18.41 (8.04%)     |
| 63-day range      | $86.49 - $245.95   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 229.00 vs 200.00             |
| Trend        | Close above SMA50                         | 8      | 8   | 229.00 vs 163.95             |
| Trend        | Close above SMA200                        | 8      | 8   | 229.00 vs 146.31             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 200.00 vs 163.95             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 163.95 vs 146.31             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 35.19                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 64.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | 16.92 vs 14.33               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.59               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 27.18%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 2.14x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 217145951 vs 191186623       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.61x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 33.1, +DI 29.0, -DI 15.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 244.32              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.04%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 6.89%                        |

## Support And Resistance

- Support levels: $136.32, $152.31, $166.63, $182.80, $203.90
- Resistance levels: $245.54

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $194.69 - $208.50 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $145.54 | $313.72  | $369.78  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $245.54 - $254.75 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $203.90 | $342.64  | $388.88  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
