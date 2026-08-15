# NVDA Technical Analysis Sample

Generated: 2026-06-05 16:40:39
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (55/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [NVDA_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/NVDA_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $205.10            |
| SMA20             | $218.87            |
| SMA50             | $203.22            |
| SMA200            | $188.34            |
| RSI14             | 44.0               |
| MACD / Signal     | 2.33 / 4.26        |
| ADX14 / +DI / -DI | 20.5 / 23.3 / 24.9 |
| ATR14             | $8.51 (4.15%)      |
| 63-day range      | $164.08 - $236.26  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 205.10 vs 218.87             |
| Trend        | Close above SMA50                         | 8      | 8   | 205.10 vs 203.22             |
| Trend        | Close above SMA200                        | 8      | 8   | 205.10 vs 188.34             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 218.87 vs 203.22             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 203.22 vs 188.34             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 15.40                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 44.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | 2.33 vs 4.26                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.23               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -2.91%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.21x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 2337942622 vs 2993296231     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.66x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 20.5, +DI 23.3, -DI 24.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 232.01              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.15%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.19%                       |

## Support And Resistance

- Support levels: $164.08, $173.27, $179.48, $195.75, $205.46
- Resistance levels: $216.58, $234.56

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $198.96 - $205.35 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $194.71 | $219.18  | $227.69  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $216.58 - $220.83 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $203.22 | $249.68  | $265.16  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
