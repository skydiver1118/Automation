# AVGO Technical Analysis Sample

Generated: 2026-06-10 20:55:01
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (40/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AVGO_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AVGO_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $372.10            |
| SMA20             | $423.18            |
| SMA50             | $403.55            |
| SMA200            | $356.38            |
| RSI14             | 37.8               |
| MACD / Signal     | -1.91 / 6.97       |
| ADX14 / +DI / -DI | 24.3 / 21.0 / 32.1 |
| ATR14             | $23.15 (6.22%)     |
| 63-day range      | $289.96 - $495.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 372.10 vs 423.18             |
| Trend        | Close above SMA50                         | 0      | 8   | 372.10 vs 403.55             |
| Trend        | Close above SMA200                        | 8      | 8   | 372.10 vs 356.38             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 423.18 vs 403.55             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 403.55 vs 356.38             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 40.70                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 37.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | -1.91 vs 6.97                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -13.30             |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -11.26%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.24x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 995104292 vs 1106475020      |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.62x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 24.3, +DI 21.0, -DI 32.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 479.06              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.22%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 24.83%                       |

## Support And Resistance

- Support levels: $291.53, $312.73, $329.81, $368.81
- Resistance levels: $412.95, $436.45, $479.06, $495.00

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $423.18 - $434.75 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $388.45 | $492.63  | $538.94  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $357.24 - $374.60 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $345.66 | $412.95  | $435.37  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $412.95 - $424.53 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $368.81 | $518.60  | $568.52  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
