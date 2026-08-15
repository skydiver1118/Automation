# AAPL Technical Analysis Sample

Generated: 2026-06-02 16:57:20
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (87/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AAPL_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AAPL_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $315.20            |
| SMA20             | $300.72            |
| SMA50             | $277.61            |
| SMA200            | $263.58            |
| RSI14             | 73.7               |
| MACD / Signal     | 9.97 / 9.87        |
| ADX14 / +DI / -DI | 44.5 / 35.5 / 11.3 |
| ATR14             | $5.92 (1.88%)      |
| 63-day range      | $245.28 - $315.45  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 315.20 vs 300.72             |
| Trend        | Close above SMA50                         | 8      | 8   | 315.20 vs 277.61             |
| Trend        | Close above SMA200                        | 8      | 8   | 315.20 vs 263.58             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 300.72 vs 277.61             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 277.61 vs 263.58             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 16.39                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 73.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | 9.97 vs 9.87                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.78              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 13.97%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.92x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 2255102845 vs 2158996172     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.77x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 44.5, +DI 35.5, -DI 11.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 318.97              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 1.88%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.08%                        |

## Support And Resistance

- Support levels: $265.64, $276.62, $282.46, $300.11, $305.02
- Resistance levels: $316.33

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $302.06 - $306.50 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $271.69 | $369.46  | $402.04  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $315.45 - $318.41 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $305.02 | $340.75  | $352.66  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
