# CRDO Technical Analysis Sample

Generated: 2026-06-03 19:37:43
Data source: yfinance adjusted daily OHLCV through 2026-06-03.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (88/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRDO_technical_chart_20260603.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRDO_technical_chart_20260603.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $214.60            |
| SMA20             | $201.05            |
| SMA50             | $166.14            |
| SMA200            | $146.80            |
| RSI14             | 57.7               |
| MACD / Signal     | 15.84 / 14.63      |
| ADX14 / +DI / -DI | 32.4 / 25.7 / 16.0 |
| ATR14             | $19.31 (9.00%)     |
| 63-day range      | $86.49 - $245.95   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 214.60 vs 201.05             |
| Trend        | Close above SMA50                         | 8      | 8   | 214.60 vs 166.14             |
| Trend        | Close above SMA200                        | 8      | 8   | 214.60 vs 146.80             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 201.05 vs 166.14             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 166.14 vs 146.80             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 35.99                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 57.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | 15.84 vs 14.63               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.70              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 10.86%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.24x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 209973179 vs 194412909       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.28x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 32.4, +DI 25.7, -DI 16.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 245.73              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 9.00%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 12.75%                       |

## Support And Resistance

- Support levels: $136.32, $152.66, $165.47, $182.80, $202.42
- Resistance levels: $245.89

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $192.77 - $207.25 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $146.83 | $306.37  | $359.55  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $245.89 - $255.55 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $202.42 | $347.32  | $395.62  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
