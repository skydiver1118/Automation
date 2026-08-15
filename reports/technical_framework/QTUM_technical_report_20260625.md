# QTUM Technical Analysis Sample

Generated: 2026-06-26 06:53:23
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (70/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QTUM_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QTUM_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $160.24            |
| SMA20             | $161.48            |
| SMA50             | $147.77            |
| SMA200            | $120.02            |
| RSI14             | 53.6               |
| MACD / Signal     | 4.32 / 5.34        |
| ADX14 / +DI / -DI | 19.0 / 20.6 / 26.6 |
| ATR14             | $5.96 (3.72%)      |
| 63-day range      | $101.24 - $169.72  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 160.24 vs 161.48             |
| Trend        | Close above SMA50                         | 8      | 8   | 160.24 vs 147.77             |
| Trend        | Close above SMA200                        | 8      | 8   | 160.24 vs 120.02             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 161.48 vs 147.77             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 147.77 vs 120.02             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 20.14                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | 4.32 vs 5.34                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.37              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 2.55%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.65x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 22409200 vs 22267290         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.08x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 19.0, +DI 20.6, -DI 26.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 171.93              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.72%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 5.59%                        |

## Support And Resistance

- Support levels: $114.44, $127.31, $137.43, $148.69, $159.14
- Resistance levels: $169.81

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $156.16 - $160.63 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $141.81 | $191.57  | $208.16  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $169.72 - $172.70 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $159.14 | $195.34  | $207.40  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
