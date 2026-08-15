# NVDA Technical Analysis Sample

Generated: 2026-05-31 20:25:50
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (72/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [NVDA_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/NVDA_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $211.14            |
| SMA20             | $215.46            |
| SMA50             | $199.35            |
| SMA200            | $187.64            |
| RSI14             | 49.4               |
| MACD / Signal     | 3.81 / 5.97        |
| ADX14 / +DI / -DI | 22.6 / 24.2 / 20.5 |
| ATR14             | $7.13 (3.38%)      |
| 63-day range      | $164.27 - $236.54  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 211.14 vs 215.46             |
| Trend        | Close above SMA50                         | 8      | 8   | 211.14 vs 199.35             |
| Trend        | Close above SMA200                        | 8      | 8   | 211.14 vs 187.64             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 215.46 vs 199.35             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 199.35 vs 187.64             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 12.41                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.4                   |
| Momentum     | MACD above signal                         | 0      | 7   | 3.81 vs 5.97                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.96              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 5.80%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.73x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 2619268200 vs 3124495925     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.00x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 22.6, +DI 24.2, -DI 20.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 235.22              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.38%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.74%                       |

## Support And Resistance

- Support levels: $164.27, $172.81, $178.90, $196.75, $208.78
- Resistance levels: $216.83, $236.21

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $205.21 - $210.56 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $192.21 | $239.24  | $254.91  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $216.83 - $220.40 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $208.78 | $238.28  | $248.11  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
