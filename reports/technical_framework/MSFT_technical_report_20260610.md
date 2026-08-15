# MSFT Technical Analysis Sample

Generated: 2026-06-10 20:55:23
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (23/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MSFT_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MSFT_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $397.36            |
| SMA20             | $421.16            |
| SMA50             | $410.33            |
| SMA200            | $452.97            |
| RSI14             | 39.6               |
| MACD / Signal     | -0.06 / 4.12       |
| ADX14 / +DI / -DI | 17.2 / 27.6 / 37.1 |
| ATR14             | $12.30 (3.10%)     |
| 63-day range      | $355.51 - $466.32  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 397.36 vs 421.16             |
| Trend        | Close above SMA50                         | 0      | 8   | 397.36 vs 410.33             |
| Trend        | Close above SMA200                        | 0      | 8   | 397.36 vs 452.97             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 421.16 vs 410.33             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 410.33 vs 452.97             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 12.47                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 39.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.06 vs 4.12                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -5.93              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -2.34%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.83x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | -81307735 vs -3263487        |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.97x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.2, +DI 27.6, -DI 37.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 451.89              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.10%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 14.79%                       |

## Support And Resistance

- Support levels: $355.51, $380.89, $394.69
- Resistance levels: $409.38, $428.48, $451.89, $466.32, $486.80

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $421.16 - $427.31 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $402.71 | $458.06  | $482.66  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $388.54 - $397.76 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $382.39 | $417.75  | $430.05  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $409.38 - $415.53 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $394.69 | $448.00  | $465.77  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
