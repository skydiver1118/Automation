# AMD Technical Analysis Sample

Generated: 2026-06-08 21:13:37
Data source: yfinance adjusted daily OHLCV through 2026-06-08.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (68/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AMD_technical_chart_20260608.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AMD_technical_chart_20260608.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $490.33            |
| SMA20             | $475.69            |
| SMA50             | $364.45            |
| SMA200            | $247.60            |
| RSI14             | 58.8               |
| MACD / Signal     | 40.09 / 46.09      |
| ADX14 / +DI / -DI | 40.9 / 27.9 / 22.8 |
| ATR14             | $29.36 (5.99%)     |
| 63-day range      | $192.27 - $546.44  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 490.33 vs 475.69             |
| Trend        | Close above SMA50                         | 8      | 8   | 490.33 vs 364.45             |
| Trend        | Close above SMA200                        | 8      | 8   | 490.33 vs 247.60             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 475.69 vs 364.45             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 364.45 vs 247.60             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 109.94                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 58.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | 40.09 vs 46.09               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -8.05              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 7.72%                        |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.77x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1214590965 vs 1222669278     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.82x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 40.9, +DI 27.9, -DI 22.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 553.22              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.99%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.27%                       |

## Support And Resistance

- Support levels: $194.48, $216.24, $364.45, $395.76, $468.66
- Resistance levels: $527.20, $548.13

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $461.01 - $483.03 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $335.10 | $745.87  | $882.79  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $527.20 - $541.88 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $475.69 | $652.23  | $711.08  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
