# QTUM Technical Analysis Sample

Generated: 2026-06-05 16:40:43
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (77/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QTUM_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QTUM_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $152.78            |
| SMA20             | $152.89            |
| SMA50             | $135.12            |
| SMA200            | $115.81            |
| RSI14             | 53.6               |
| MACD / Signal     | 7.89 / 7.99        |
| ADX14 / +DI / -DI | 35.8 / 31.7 / 27.5 |
| ATR14             | $5.10 (3.34%)      |
| 63-day range      | $101.41 - $170.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 152.78 vs 152.89             |
| Trend        | Close above SMA50                         | 8      | 8   | 152.78 vs 135.12             |
| Trend        | Close above SMA200                        | 8      | 8   | 152.78 vs 115.81             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 152.89 vs 135.12             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 135.12 vs 115.81             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 16.45                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.6                   |
| Momentum     | MACD above signal                         | 0      | 7   | 7.89 vs 7.99                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.88              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 8.25%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.79x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 21414221 vs 20096241         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.53x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 35.8, +DI 31.7, -DI 27.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 170.98              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.34%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.13%                       |

## Support And Resistance

- Support levels: $108.43, $114.63, $127.52, $135.86, $152.65
- Resistance levels: $170.25

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $150.20 - $154.03 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $130.02 | $196.31  | $218.41  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $170.00 - $172.55 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $152.76 | $208.32  | $226.84  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
