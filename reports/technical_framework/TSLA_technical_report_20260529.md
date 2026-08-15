# TSLA Technical Analysis Sample

Generated: 2026-05-31 20:26:06
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (89/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [TSLA_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/TSLA_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $435.79            |
| SMA20             | $421.39            |
| SMA50             | $391.80            |
| SMA200            | $412.13            |
| RSI14             | 60.0               |
| MACD / Signal     | 12.07 / 11.37      |
| ADX14 / +DI / -DI | 21.3 / 31.4 / 22.2 |
| ATR14             | $14.98 (3.44%)     |
| 63-day range      | $337.24 - $453.40  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 435.79 vs 421.39             |
| Trend        | Close above SMA50                         | 8      | 8   | 435.79 vs 391.80             |
| Trend        | Close above SMA200                        | 8      | 8   | 435.79 vs 412.13             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 421.39 vs 391.80             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 391.80 vs 412.13             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 7.66                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 60.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 12.07 vs 11.37               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.56               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 14.19%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.86x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 3815615100 vs 3700287975     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.81x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 21.3, +DI 31.4, -DI 22.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 459.30              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.44%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 3.88%                        |

## Support And Resistance

- Support levels: $352.14, $364.24, $388.40, $400.51, $419.87
- Resistance levels: $436.35, $453.84, $498.83

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $413.90 - $425.14 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $376.81 | $504.94  | $547.64  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $436.35 - $443.84 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $421.39 | $477.50  | $496.20  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
