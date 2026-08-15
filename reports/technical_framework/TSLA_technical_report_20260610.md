# TSLA Technical Analysis Sample

Generated: 2026-06-10 20:55:19
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (28/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSLA_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSLA_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $381.59            |
| SMA20             | $419.89            |
| SMA50             | $397.25            |
| SMA200            | $415.16            |
| RSI14             | 39.4               |
| MACD / Signal     | -1.55 / 4.67       |
| ADX14 / +DI / -DI | 18.2 / 17.1 / 28.4 |
| ATR14             | $17.89 (4.69%)     |
| 63-day range      | $337.24 - $453.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 381.59 vs 419.89             |
| Trend        | Close above SMA50                         | 0      | 8   | 381.59 vs 397.25             |
| Trend        | Close above SMA200                        | 0      | 8   | 381.59 vs 415.16             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 419.89 vs 397.25             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 397.25 vs 415.16             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 12.61                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 39.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | -1.55 vs 4.67                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -4.39              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -11.96%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.03x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 3846149983 vs 3969570009     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.64x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.2, +DI 17.1, -DI 28.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 455.30              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.69%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 15.84%                       |

## Support And Resistance

- Support levels: $337.24, $352.14, $364.24
- Resistance levels: $383.14, $396.23, $413.65, $440.98, $453.70

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $419.89 - $428.84 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $393.05 | $473.57  | $509.36  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $355.29 - $368.71 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $346.35 | $397.79  | $415.68  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $383.14 - $392.09 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $364.24 | $434.36  | $457.73  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
