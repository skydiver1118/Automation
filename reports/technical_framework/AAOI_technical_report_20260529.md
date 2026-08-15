# AAOI Technical Analysis Sample

Generated: 2026-05-31 20:26:50
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (46/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AAOI_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AAOI_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $158.41            |
| SMA20             | $178.27            |
| SMA50             | $147.97            |
| SMA200            | $65.95             |
| RSI14             | 46.8               |
| MACD / Signal     | 5.85 / 10.21       |
| ADX14 / +DI / -DI | 24.5 / 20.5 / 20.7 |
| ATR14             | $20.91 (13.20%)    |
| 63-day range      | $78.57 - $233.67   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 158.41 vs 178.27             |
| Trend        | Close above SMA50                         | 8      | 8   | 158.41 vs 147.97             |
| Trend        | Close above SMA200                        | 8      | 8   | 158.41 vs 65.95              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 178.27 vs 147.97             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 147.97 vs 65.95              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 36.64                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 46.8                   |
| Momentum     | MACD above signal                         | 0      | 7   | 5.85 vs 10.21                |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -1.13              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -3.62%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.98x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 199965300 vs 225722540       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.64x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 24.5, +DI 20.5, -DI 20.7 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 210.80              |
| Risk/context | ATR volatility is tradable                | 0      | 4   | ATR14 13.20%                 |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 32.21%                       |

## Support And Resistance

- Support levels: $31.30, $80.58, $144.60
- Resistance levels: $173.41, $193.42, $210.80, $233.67

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $137.52 - $153.20 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $127.06 | $187.19  | $208.10  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $173.41 - $183.87 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $147.97 | $239.97  | $270.63  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
