# SMH Technical Analysis Sample

Generated: 2026-06-10 20:55:16
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (60/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SMH_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SMH_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $570.91            |
| SMA20             | $586.89            |
| SMA50             | $519.79            |
| SMA200            | $400.71            |
| RSI14             | 50.3               |
| MACD / Signal     | 20.58 / 27.50      |
| ADX14 / +DI / -DI | 30.0 / 19.5 / 26.2 |
| ATR14             | $26.68 (4.67%)     |
| 63-day range      | $359.86 - $642.77  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 570.91 vs 586.89             |
| Trend        | Close above SMA50                         | 8      | 8   | 570.91 vs 519.79             |
| Trend        | Close above SMA200                        | 8      | 8   | 570.91 vs 400.71             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 586.89 vs 519.79             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 519.79 vs 400.71             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 78.74                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 50.3                   |
| Momentum     | MACD above signal                         | 0      | 7   | 20.58 vs 27.50               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -9.38              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 1.72%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.14x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 283531923 vs 309146346       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.75x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 30.0, +DI 19.5, -DI 26.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 640.68              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.67%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 11.18%                       |

## Support And Resistance

- Support levels: $337.01, $369.27, $391.92, $526.92, $554.66
- Resistance levels: $581.17, $642.25

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $541.32 - $561.33 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $493.11 | $667.75  | $725.96  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $581.17 - $594.51 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $554.66 | $654.20  | $687.38  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
