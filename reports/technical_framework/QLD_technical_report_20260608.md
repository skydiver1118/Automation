# QLD Technical Analysis Sample

Generated: 2026-06-08 21:13:24
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (70/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QLD_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QLD_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $92.25             |
| SMA20             | $94.35             |
| SMA50             | $82.19             |
| SMA200            | $72.25             |
| RSI14             | 52.1               |
| MACD / Signal     | 3.58 / 4.67        |
| ADX14 / +DI / -DI | 35.0 / 24.4 / 28.2 |
| ATR14             | $3.15 (3.41%)      |
| 63-day range      | $56.60 - $101.19   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 92.25 vs 94.35               |
| Trend        | Close above SMA50                         | 8      | 8   | 92.25 vs 82.19               |
| Trend        | Close above SMA200                        | 8      | 8   | 92.25 vs 72.25               |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 94.35 vs 82.19               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 82.19 vs 72.25               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.45                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 52.1                   |
| Momentum     | MACD above signal                         | 0      | 7   | 3.58 vs 4.67                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.23              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 0.58%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.24x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 275167959 vs 271146598       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.10x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 35.0, +DI 24.4, -DI 28.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 101.91              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.41%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 8.83%                        |

## Support And Resistance

- Support levels: $64.99, $68.38, $82.19, $87.16, $89.28
- Resistance levels: $94.48, $101.37

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $87.71 - $90.07 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $79.04 | $108.57  | $118.41  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $94.48 - $96.05 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $89.28 | $107.24  | $113.23  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
