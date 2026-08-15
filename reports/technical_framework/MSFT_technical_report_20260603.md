# MSFT Technical Analysis Sample

Generated: 2026-06-03 19:37:26
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (71/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MSFT_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MSFT_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $427.34            |
| SMA20             | $421.59            |
| SMA50             | $405.62            |
| SMA200            | $455.31            |
| RSI14             | 52.8               |
| MACD / Signal     | 8.11 / 6.35        |
| ADX14 / +DI / -DI | 20.7 / 38.0 / 30.8 |
| ATR14             | $12.94 (3.03%)     |
| 63-day range      | $355.51 - $466.32  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 427.34 vs 421.59             |
| Trend        | Close above SMA50                         | 8      | 8   | 427.34 vs 405.62             |
| Trend        | Close above SMA200                        | 0      | 8   | 427.34 vs 455.31             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 421.59 vs 405.62             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 405.62 vs 455.31             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 9.50                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 52.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | 8.11 vs 6.35                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.58               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 4.10%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.97x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 74140841 vs 51657782         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.99x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 20.7, +DI 38.0, -DI 30.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 450.07              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.03%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 8.36%                        |

## Support And Resistance

- Support levels: $355.51, $380.89, $394.73, $408.07, $423.35
- Resistance levels: $428.48, $450.07, $466.32, $487.58

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $417.75 - $427.45 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $392.68 | $482.44  | $512.36  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $428.48 - $434.95 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $424.22 | $457.59  | $470.53  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
