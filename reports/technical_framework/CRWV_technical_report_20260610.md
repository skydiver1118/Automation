# CRWV Technical Analysis Sample

Generated: 2026-06-10 20:55:04
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (21/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWV_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWV_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $95.61             |
| SMA20             | $106.86            |
| SMA50             | $108.18            |
| SMA200            | $100.03            |
| RSI14             | 40.5               |
| MACD / Signal     | -2.19 / -0.45      |
| ADX14 / +DI / -DI | 13.8 / 22.3 / 31.1 |
| ATR14             | $8.91 (9.31%)      |
| 63-day range      | $67.15 - $138.25   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 95.61 vs 106.86              |
| Trend        | Close above SMA50                         | 0      | 8   | 95.61 vs 108.18              |
| Trend        | Close above SMA200                        | 0      | 8   | 95.61 vs 100.03              |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 106.86 vs 108.18             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 108.18 vs 100.03             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 11.08                        |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 40.5                   |
| Momentum     | MACD above signal                         | 0      | 7   | -2.19 vs -0.45               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.21              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -11.27%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.60x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 451893928 vs 504008756       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.79x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 13.8, +DI 22.3, -DI 31.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 120.89              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.31%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 30.84%                       |

## Support And Resistance

- Support levels: $68.27, $75.79, $85.78, $93.75
- Resistance levels: $101.26, $114.45, $122.66, $132.15, $138.25

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $108.18 - $112.63 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $94.82 | $134.89  | $152.70  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $89.30 - $95.97   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $84.84 | $110.45  | $119.35  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $101.26 - $105.72 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $93.75 | $122.97  | $132.71  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
