# NVDA Technical Analysis Sample

Generated: 2026-07-06 16:40:18
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (36/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [NVDA_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/NVDA_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $195.55            |
| SMA20             | $202.33            |
| SMA50             | $209.51            |
| SMA200            | $190.92            |
| RSI14             | 42.0               |
| MACD / Signal     | -4.09 / -3.25      |
| ADX14 / +DI / -DI | 18.3 / 16.0 / 25.9 |
| ATR14             | $6.87 (3.51%)      |
| 63-day range      | $173.46 - $236.26  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 195.55 vs 202.33             |
| Trend        | Close above SMA50                         | 0      | 8   | 195.55 vs 209.51             |
| Trend        | Close above SMA200                        | 8      | 8   | 195.55 vs 190.92             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 202.33 vs 209.51             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 209.51 vs 190.92             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 6.82                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 42.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | -4.09 vs -3.25               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.06               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -10.57%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.63x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 2479732306 vs 2771650230     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.74x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.3, +DI 16.0, -DI 25.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 214.32              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.51%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.23%                       |

## Support And Resistance

- Support levels: $164.08, $173.11, $178.70, $190.07, $196.95
- Resistance levels: $197.39, $214.49, $232.01, $236.26

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $209.51 - $212.95 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $199.21 | $230.12  | $243.85  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $186.63 - $191.78 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $183.20 | $202.94  | $209.81  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $197.39 - $200.82 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $190.07 | $217.18  | $226.22  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
