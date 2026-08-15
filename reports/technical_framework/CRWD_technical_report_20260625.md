# CRWD Technical Analysis Sample

Generated: 2026-06-26 06:53:10
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (72/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWD_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWD_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $678.65            |
| SMA20             | $693.24            |
| SMA50             | $588.23            |
| SMA200            | $494.59            |
| RSI14             | 56.0               |
| MACD / Signal     | 21.14 / 30.25      |
| ADX14 / +DI / -DI | 29.0 / 24.0 / 17.7 |
| ATR14             | $32.20 (4.74%)     |
| 63-day range      | $361.81 - $785.66  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 678.65 vs 693.24             |
| Trend        | Close above SMA50                         | 8      | 8   | 678.65 vs 588.23             |
| Trend        | Close above SMA200                        | 8      | 8   | 678.65 vs 494.59             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 693.24 vs 588.23             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 588.23 vs 494.59             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 116.37                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 56.0                   |
| Momentum     | MACD above signal                         | 0      | 7   | 21.14 vs 30.25               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.31               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 5.16%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.83x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 8194900 vs 7454650           |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.79x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 29.0, +DI 24.0, -DI 17.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 768.41              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.74%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.62%                       |

## Support And Resistance

- Support levels: $439.18, $470.67, $588.23, $622.97, $664.49
- Resistance levels: $707.17, $781.35

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $651.97 - $676.12 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $556.03 | $880.07  | $988.09  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $707.17 - $723.28 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $668.07 | $809.54  | $856.70  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
