# NVDA Technical Analysis Sample

Generated: 2026-06-04 19:39:23
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (72/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [NVDA_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/NVDA_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $218.66            |
| SMA20             | $219.42            |
| SMA50             | $202.92            |
| SMA200            | $188.41            |
| RSI14             | 54.2               |
| MACD / Signal     | 3.57 / 4.75        |
| ADX14 / +DI / -DI | 21.7 / 26.5 / 22.2 |
| ATR14             | $8.07 (3.69%)      |
| 63-day range      | $164.27 - $236.54  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 218.66 vs 219.42             |
| Trend        | Close above SMA50                         | 8      | 8   | 218.66 vs 202.92             |
| Trend        | Close above SMA200                        | 8      | 8   | 218.66 vs 188.41             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 219.42 vs 202.92             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 202.92 vs 188.41             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 15.19                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 54.2                   |
| Momentum     | MACD above signal                         | 0      | 7   | 3.57 vs 4.75                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.74               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 5.21%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.96x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1887582174 vs 2356407304     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.81x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 21.7, +DI 26.5, -DI 22.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 231.46              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.69%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 7.56%                        |

## Support And Resistance

- Support levels: $172.64, $178.95, $195.98, $207.51, $217.57
- Resistance levels: $216.83, $234.67

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $213.53 - $219.59 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $194.85 | $259.99  | $281.71  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $234.67 - $238.71 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $217.57 | $274.93  | $294.05  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
