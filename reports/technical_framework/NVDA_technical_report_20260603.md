# NVDA Technical Analysis Sample

Generated: 2026-06-03 19:37:00
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (67/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [NVDA_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/NVDA_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $214.75            |
| SMA20             | $218.88            |
| SMA50             | $202.05            |
| SMA200            | $188.23            |
| RSI14             | 51.1               |
| MACD / Signal     | 3.76 / 5.04        |
| ADX14 / +DI / -DI | 22.7 / 29.2 / 21.1 |
| ATR14             | $7.88 (3.67%)      |
| 63-day range      | $164.27 - $236.54  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 214.75 vs 218.88             |
| Trend        | Close above SMA50                         | 8      | 8   | 214.75 vs 202.05             |
| Trend        | Close above SMA200                        | 8      | 8   | 214.75 vs 188.23             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 218.88 vs 202.05             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 202.05 vs 188.23             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 14.63                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 51.1                   |
| Momentum     | MACD above signal                         | 0      | 7   | 3.76 vs 5.04                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.50               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 9.29%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.85x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 2259036075 vs 2894087909     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.82x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 22.7, +DI 29.2, -DI 21.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 231.99              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.67%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 9.21%                        |

## Support And Resistance

- Support levels: $172.64, $178.95, $195.98, $203.91, $208.78
- Resistance levels: $216.83, $234.78

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $204.84 - $210.75 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $194.17 | $235.04  | $248.66  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $216.83 - $220.77 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $208.78 | $238.84  | $248.86  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
