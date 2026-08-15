# MU Technical Analysis Sample

Generated: 2026-05-31 20:25:49
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (88/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MU_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MU_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $971.00            |
| SMA20             | $751.46            |
| SMA50             | $557.54            |
| SMA200            | $338.60            |
| RSI14             | 78.0               |
| MACD / Signal     | 101.83 / 85.42     |
| ADX14 / +DI / -DI | 37.9 / 44.2 / 13.8 |
| ATR14             | $55.99 (5.77%)     |
| 63-day range      | $311.49 - $981.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 971.00 vs 751.46             |
| Trend        | Close above SMA50                         | 8      | 8   | 971.00 vs 557.54             |
| Trend        | Close above SMA200                        | 8      | 8   | 971.00 vs 338.60             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 751.46 vs 557.54             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 557.54 vs 338.60             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 134.46                       |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 78.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 101.83 vs 85.42              |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 17.93              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 87.76%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.08x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1205840600 vs 1034000725     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.01x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 37.9, +DI 44.2, -DI 13.8 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 980.57              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.77%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 1.02%                        |

## Support And Resistance

- Support levels: $435.90, $522.35, $557.54, $652.21, $751.27
- Resistance levels: $980.89

## Entry Plans

| Plan           | Entry zone          | Trigger                                                                                                      | Stop    | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | ------------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $723.47 - $765.46   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $501.55 | $1,230.30 | $1,473.22 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $980.89 - $1,008.89 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $859.02 | $1,266.63 | $1,402.50 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
