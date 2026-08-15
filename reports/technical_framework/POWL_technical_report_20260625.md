# POWL Technical Analysis Sample

Generated: 2026-06-26 06:53:34
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (91/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [POWL_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/POWL_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $309.20            |
| SMA20             | $293.02            |
| SMA50             | $281.44            |
| SMA200            | $173.38            |
| RSI14             | 58.0               |
| MACD / Signal     | 6.17 / 6.04        |
| ADX14 / +DI / -DI | 15.3 / 18.9 / 17.4 |
| ATR14             | $20.15 (6.52%)     |
| 63-day range      | $165.20 - $327.89  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 309.20 vs 293.02             |
| Trend        | Close above SMA50                         | 8      | 8   | 309.20 vs 281.44             |
| Trend        | Close above SMA200                        | 8      | 8   | 309.20 vs 173.38             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 293.02 vs 281.44             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 281.44 vs 173.38             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 40.19                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 58.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 6.17 vs 6.04                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 1.05               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 4.48%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.21x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 38411400 vs 36054340         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.85x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.3, +DI 18.9, -DI 17.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 313.37              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.52%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 5.70%                        |

## Support And Resistance

- Support levels: $165.20, $223.92, $254.90, $276.28, $292.84
- Resistance levels: $310.41, $327.89

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $282.94 - $298.05 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $261.29 | $348.91  | $378.12  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $310.41 - $320.48 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $293.02 | $360.30  | $382.73  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
