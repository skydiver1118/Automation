# CRWV Technical Analysis Sample

Generated: 2026-06-05 16:40:34
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (45/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWV_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWV_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $100.39            |
| SMA20             | $108.87            |
| SMA50             | $106.74            |
| SMA200            | $99.93             |
| RSI14             | 43.3               |
| MACD / Signal     | -0.09 / 0.58       |
| ADX14 / +DI / -DI | 13.6 / 27.0 / 33.2 |
| ATR14             | $9.21 (9.18%)      |
| 63-day range      | $67.15 - $138.25   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 100.39 vs 108.87             |
| Trend        | Close above SMA50                         | 0      | 8   | 100.39 vs 106.74             |
| Trend        | Close above SMA200                        | 8      | 8   | 100.39 vs 99.93              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 108.87 vs 106.74             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 106.74 vs 99.93              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.27                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 43.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.09 vs 0.58                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.36               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -22.08%                      |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.00x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 474558660 vs 508897048       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.92x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 13.6, +DI 27.0, -DI 33.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 121.46              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.18%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 27.39%                       |

## Support And Resistance

- Support levels: $68.27, $76.48, $85.78, $97.47
- Resistance levels: $101.26, $114.45, $122.85, $132.15, $138.25

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $108.87 - $113.47 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $95.05 | $136.50  | $154.92  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $92.87 - $99.77   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $88.26 | $114.74  | $123.95  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $101.26 - $105.87 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $97.47 | $121.99  | $131.20  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
