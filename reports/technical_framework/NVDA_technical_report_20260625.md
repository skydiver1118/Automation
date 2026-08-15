# NVDA Technical Analysis Sample

Generated: 2026-06-26 06:53:17
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (31/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [NVDA_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/NVDA_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $195.74            |
| SMA20             | $208.79            |
| SMA50             | $210.04            |
| SMA200            | $190.32            |
| RSI14             | 39.7               |
| MACD / Signal     | -2.88 / -1.26      |
| ADX14 / +DI / -DI | 15.0 / 17.6 / 30.8 |
| ATR14             | $7.50 (3.83%)      |
| 63-day range      | $164.08 - $236.26  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 195.74 vs 208.79             |
| Trend        | Close above SMA50                         | 0      | 8   | 195.74 vs 210.04             |
| Trend        | Close above SMA200                        | 8      | 8   | 195.74 vs 190.32             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 208.79 vs 210.04             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 210.04 vs 190.32             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 12.18                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 39.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | -2.88 vs -1.26               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.21              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -7.82%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.89x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 2272658200 vs 2713935110     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.58x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.0, +DI 17.6, -DI 30.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 223.84              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.83%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.15%                       |

## Support And Resistance

- Support levels: $164.08, $173.90, $180.46, $194.34
- Resistance levels: $197.39, $214.43, $223.84, $234.14

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $210.04 - $213.79 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $198.79 | $232.54  | $247.54  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $190.59 - $196.22 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $186.84 | $208.41  | $215.91  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $197.39 - $201.14 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $194.34 | $214.27  | $221.77  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
