# CRWD Technical Analysis Sample

Generated: 2026-06-03 19:36:51
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (97/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWD_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWD_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value             |
| ----------------- | ----------------- |
| Close             | $747.61           |
| SMA20             | $627.09           |
| SMA50             | $503.48           |
| SMA200            | $475.31           |
| RSI14             | 76.3              |
| MACD / Signal     | 73.16 / 62.36     |
| ADX14 / +DI / -DI | 54.4 / 47.0 / 6.5 |
| ATR14             | $30.77 (4.12%)    |
| 63-day range      | $361.81 - $785.66 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                    |
| ------------ | ----------------------------------------- | ------ | --- | --------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 747.61 vs 627.09            |
| Trend        | Close above SMA50                         | 8      | 8   | 747.61 vs 503.48            |
| Trend        | Close above SMA200                        | 8      | 8   | 747.61 vs 475.31            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 627.09 vs 503.48            |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 503.48 vs 475.31            |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 85.94                       |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 76.3                  |
| Momentum     | MACD above signal                         | 7      | 7   | 73.16 vs 62.36              |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.44              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 56.89%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.35x                       |
| Confirmation | OBV above 20-day average                  | 5      | 5   | -1702302 vs -8864110        |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.61x                       |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 54.4, +DI 47.0, -DI 6.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 803.19             |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.12%                 |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 4.84%                       |

## Support And Resistance

- Support levels: $365.65, $441.54, $475.60, $503.48, $632.19
- Resistance levels: $790.04

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $621.02 - $644.10 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $472.71 | $952.26   | $1,112.11 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $785.66 - $801.04 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $686.07 | $1,007.91 | $1,115.18 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
