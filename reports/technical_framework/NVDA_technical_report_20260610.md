# NVDA Technical Analysis Sample

Generated: 2026-06-10 20:55:08
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (37/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [NVDA_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/NVDA_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $200.42            |
| SMA20             | $217.00            |
| SMA50             | $205.50            |
| SMA200            | $188.79            |
| RSI14             | 41.2               |
| MACD / Signal     | -0.14 / 2.52       |
| ADX14 / +DI / -DI | 18.6 / 18.6 / 25.1 |
| ATR14             | $8.54 (4.26%)      |
| 63-day range      | $164.08 - $236.26  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 200.42 vs 217.00             |
| Trend        | Close above SMA50                         | 0      | 8   | 200.42 vs 205.50             |
| Trend        | Close above SMA200                        | 8      | 8   | 200.42 vs 188.79             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 217.00 vs 205.50             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 205.50 vs 188.79             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 15.46                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 41.2                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.14 vs 2.52                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.37              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -9.12%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.84x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 2463088276 vs 3181092559     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.43x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.6, +DI 18.6, -DI 25.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 233.49              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.26%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 15.17%                       |

## Support And Resistance

- Support levels: $164.08, $173.27, $179.35, $197.84
- Resistance levels: $216.58, $234.86

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $217.00 - $221.27 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $204.20 | $242.61  | $259.69  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $193.57 - $199.97 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $189.30 | $216.58  | $222.38  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $216.58 - $220.85 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $197.84 | $260.46  | $281.33  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
