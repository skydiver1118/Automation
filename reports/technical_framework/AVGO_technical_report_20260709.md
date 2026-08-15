# AVGO Technical Analysis Sample

Generated: 2026-07-09 16:40:20
Data source: yfinance adjusted daily OHLCV through 2026-07-09.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (69/100).**

Not bullish yet under the framework; classify as Neutral because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AVGO_technical_chart_20260709.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AVGO_technical_chart_20260709.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $401.11            |
| SMA20             | $381.16            |
| SMA50             | $405.96            |
| SMA200            | $360.94            |
| RSI14             | 54.1               |
| MACD / Signal     | -6.55 / -9.01      |
| ADX14 / +DI / -DI | 19.7 / 27.8 / 26.8 |
| ATR14             | $18.32 (4.57%)     |
| 63-day range      | $350.94 - $494.22  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 401.11 vs 381.16             |
| Trend        | Close above SMA50                         | 0      | 8   | 401.11 vs 405.96             |
| Trend        | Close above SMA200                        | 8      | 8   | 401.11 vs 360.94             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 381.16 vs 405.96             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 405.96 vs 360.94             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 4.61                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 54.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | -6.55 vs -9.01               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 4.58               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 2.44%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.90x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 926197498 vs 894876415       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.27x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 19.7, +DI 27.8, -DI 26.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 406.02              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.57%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 18.84%                       |

## Support And Resistance

- Support levels: $310.39, $329.29, $354.56, $369.74, $387.16
- Resistance levels: $410.70, $435.76, $494.22

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $378.00 - $391.74 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $368.84 | $421.52  | $439.84  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $410.70 - $419.87 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $387.16 | $471.53  | $499.66  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
