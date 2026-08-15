# HOOD Technical Analysis Sample

Generated: 2026-05-31 20:25:46
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (75/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [HOOD_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/HOOD_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $94.30             |
| SMA20             | $77.97             |
| SMA50             | $76.78             |
| SMA200            | $103.91            |
| RSI14             | 69.1               |
| MACD / Signal     | 1.24 / -0.10       |
| ADX14 / +DI / -DI | 15.5 / 40.1 / 13.4 |
| ATR14             | $4.89 (5.18%)      |
| 63-day range      | $63.51 - $94.40    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 94.30 vs 77.97               |
| Trend        | Close above SMA50                         | 8      | 8   | 94.30 vs 76.78               |
| Trend        | Close above SMA200                        | 0      | 8   | 94.30 vs 103.91              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 77.97 vs 76.78               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 76.78 vs 103.91              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 0.42                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 69.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | 1.24 vs -0.10                |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.73               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 29.37%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 2.58x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1458607900 vs 1307917950     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 3.13x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.5, +DI 40.1, -DI 13.4 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 87.36               |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.18%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.11%                        |

## Support And Resistance

- Support levels: $63.51, $70.67, $77.02
- Resistance levels: $94.13, $111.46, $120.88, $124.35, $139.75

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $76.62 - $80.29 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $71.89 | $94.40   | $98.14   | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $94.40 - $96.84 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $84.52 | $117.82  | $128.92  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
