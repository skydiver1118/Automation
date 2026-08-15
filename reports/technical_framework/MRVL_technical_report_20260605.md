# MRVL Technical Analysis Sample

Generated: 2026-06-05 16:40:58
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (93/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MRVL_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MRVL_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $263.47            |
| SMA20             | $208.52            |
| SMA50             | $165.34            |
| SMA200            | $103.42            |
| RSI14             | 65.0               |
| MACD / Signal     | 33.51 / 24.41      |
| ADX14 / +DI / -DI | 51.2 / 40.5 / 14.0 |
| ATR14             | $23.07 (8.76%)     |
| 63-day range      | $84.16 - $324.20   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 263.47 vs 208.52             |
| Trend        | Close above SMA50                         | 8      | 8   | 263.47 vs 165.34             |
| Trend        | Close above SMA200                        | 8      | 8   | 263.47 vs 103.42             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 208.52 vs 165.34             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 165.34 vs 103.42             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 48.57                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 65.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 33.51 vs 24.41               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 7.98               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 64.66%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.94x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1090497146 vs 795417517      |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 3.13x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 51.2, +DI 40.5, -DI 14.0 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 301.81              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.76%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 18.73%                       |

## Support And Resistance

- Support levels: $80.48, $121.83, $158.25, $213.49
- Resistance levels: $301.81, $324.20

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $206.92 - $224.22 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $142.26 | $362.19  | $435.51  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $301.81 - $313.34 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $218.46 | $485.81  | $574.93  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
