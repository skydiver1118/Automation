# CRWV Technical Analysis Sample

Generated: 2026-06-26 06:53:12
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (26/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWV_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWV_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $98.76             |
| SMA20             | $107.30            |
| SMA50             | $111.28            |
| SMA200            | $100.68            |
| RSI14             | 43.1               |
| MACD / Signal     | -0.91 / -0.43      |
| ADX14 / +DI / -DI | 11.3 / 24.9 / 28.0 |
| ATR14             | $8.84 (8.95%)      |
| 63-day range      | $67.15 - $138.25   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 98.76 vs 107.30              |
| Trend        | Close above SMA50                         | 0      | 8   | 98.76 vs 111.28              |
| Trend        | Close above SMA200                        | 0      | 8   | 98.76 vs 100.68              |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 107.30 vs 111.28             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 111.28 vs 100.68             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 8.55                         |
| Momentum     | RSI in constructive range                 | 3      | 8   | RSI14 43.1                   |
| Momentum     | MACD above signal                         | 0      | 7   | -0.91 vs -0.43               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.41              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -5.28%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.71x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 514380900 vs 527815130       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.03x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 11.3, +DI 24.9, -DI 28.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 124.09              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.95%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 28.56%                       |

## Support And Resistance

- Support levels: $69.97, $77.58, $88.28, $99.37
- Resistance levels: $101.26, $114.45, $123.30, $132.15, $138.25

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $111.28 - $115.70 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $98.02 | $137.79  | $155.47  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $83.86 - $90.49   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $79.44 | $104.85  | $113.68  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $101.26 - $105.68 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $88.28 | $133.86  | $149.06  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
