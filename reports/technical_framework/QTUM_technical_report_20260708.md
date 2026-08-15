# QTUM Technical Analysis Sample

Generated: 2026-07-08 16:40:22
Data source: yfinance adjusted daily OHLCV through 2026-07-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (55/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QTUM_technical_chart_20260708.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QTUM_technical_chart_20260708.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $152.47            |
| SMA20             | $159.75            |
| SMA50             | $152.46            |
| SMA200            | $122.35            |
| RSI14             | 45.4               |
| MACD / Signal     | 0.51 / 2.44        |
| ADX14 / +DI / -DI | 17.0 / 18.0 / 30.4 |
| ATR14             | $5.88 (3.86%)      |
| 63-day range      | $114.32 - $169.72  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 152.47 vs 159.75             |
| Trend        | Close above SMA50                         | 8      | 8   | 152.47 vs 152.46             |
| Trend        | Close above SMA200                        | 8      | 8   | 152.47 vs 122.35             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 159.75 vs 152.46             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 152.46 vs 122.35             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 16.56                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 45.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | 0.51 vs 2.44                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.94              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -3.18%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.44x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 21256220 vs 21610716         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.09x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 17.0, +DI 18.0, -DI 30.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 170.35              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.86%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.16%                       |

## Support And Resistance

- Support levels: $114.28, $127.31, $137.43, $148.64, $152.46
- Resistance levels: $169.00

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $149.52 - $153.93 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $146.58 | $169.00  | $169.36  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $169.00 - $171.94 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $152.46 | $206.49  | $224.49  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
