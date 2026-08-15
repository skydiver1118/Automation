# NVDA Technical Analysis Sample

Generated: 2026-06-08 21:13:21
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (50/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [NVDA_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/NVDA_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $208.64            |
| SMA20             | $218.56            |
| SMA50             | $203.97            |
| SMA200            | $188.51            |
| RSI14             | 46.9               |
| MACD / Signal     | 1.60 / 3.73        |
| ADX14 / +DI / -DI | 19.2 / 22.2 / 23.8 |
| ATR14             | $8.29 (3.97%)      |
| 63-day range      | $164.08 - $236.26  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 208.64 vs 218.56             |
| Trend        | Close above SMA50                         | 8      | 8   | 208.64 vs 203.97             |
| Trend        | Close above SMA200                        | 8      | 8   | 208.64 vs 188.51             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 218.56 vs 203.97             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 203.97 vs 188.51             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 15.54                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | 1.60 vs 3.73                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.71              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -2.94%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.77x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 2571831036 vs 3064157142     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.65x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 19.2, +DI 22.2, -DI 23.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 232.38              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.97%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.69%                       |

## Support And Resistance

- Support levels: $164.08, $173.27, $179.79, $195.75, $205.39
- Resistance levels: $216.58, $234.64

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $201.25 - $207.47 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $195.68 | $221.70  | $230.38  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $216.58 - $220.72 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $205.39 | $245.16  | $258.42  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
