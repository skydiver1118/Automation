# MSFT Technical Analysis Sample

Generated: 2026-05-31 20:26:12
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (67/100).**

Not bullish yet under the framework; classify as Neutral because confirmation is mixed.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MSFT_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MSFT_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $450.24            |
| SMA20             | $416.97            |
| SMA50             | $402.06            |
| SMA200            | $456.42            |
| RSI14             | 70.1               |
| MACD / Signal     | 6.04 / 4.26        |
| ADX14 / +DI / -DI | 18.9 / 41.9 / 17.5 |
| ATR14             | $11.74 (2.61%)     |
| 63-day range      | $355.51 - $450.33  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 450.24 vs 416.97             |
| Trend        | Close above SMA50                         | 8      | 8   | 450.24 vs 402.06             |
| Trend        | Close above SMA200                        | 0      | 8   | 450.24 vs 456.42             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 416.97 vs 402.06             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 402.06 vs 456.42             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 7.13                         |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 70.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | 6.04 vs 4.26                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.03               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 10.65%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 2.28x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 138230400 vs 90890400        |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.98x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.9, +DI 41.9, -DI 17.5 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 436.19              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.61%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.02%                        |

## Support And Resistance

- Support levels: $380.89, $396.72, $408.69, $417.65, $436.74
- Resistance levels: $450.33, $487.58

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $430.86 - $439.67 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $390.32 | $525.15  | $570.10  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $450.33 - $456.20 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $436.74 | $486.32  | $502.85  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
