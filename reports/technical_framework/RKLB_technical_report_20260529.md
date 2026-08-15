# RKLB Technical Analysis Sample

Generated: 2026-05-31 20:25:57
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (93/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [RKLB_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/RKLB_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $143.48            |
| SMA20             | $118.09            |
| SMA50             | $91.25             |
| SMA200            | $69.12             |
| RSI14             | 67.8               |
| MACD / Signal     | 16.54 / 14.76      |
| ADX14 / +DI / -DI | 43.4 / 34.0 / 13.4 |
| ATR14             | $10.52 (7.33%)     |
| 63-day range      | $56.13 - $151.00   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 143.48 vs 118.09             |
| Trend        | Close above SMA50                         | 8      | 8   | 143.48 vs 91.25              |
| Trend        | Close above SMA200                        | 8      | 8   | 143.48 vs 69.12              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 118.09 vs 91.25              |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 91.25 vs 69.12               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 18.81                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 67.8                   |
| Momentum     | MACD above signal                         | 7      | 7   | 16.54 vs 14.76               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.82              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 73.89%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.15x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1943588100 vs 1868566420     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.29x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 43.4, +DI 34.0, -DI 13.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 167.80              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.33%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 4.98%                        |

## Support And Resistance

- Support levels: $65.97, $77.00, $91.25, $118.29, $134.05
- Resistance levels: $151.00, $167.80

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $128.79 - $136.68 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $80.73  | $236.74  | $288.74  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $151.00 - $156.26 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $134.05 | $192.79  | $212.37  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
