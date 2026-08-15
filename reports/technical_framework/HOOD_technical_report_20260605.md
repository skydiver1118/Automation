# HOOD Technical Analysis Sample

Generated: 2026-06-05 16:40:36
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (74/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [HOOD_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/HOOD_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $82.47             |
| SMA20             | $80.47             |
| SMA50             | $78.25             |
| SMA200            | $103.29            |
| RSI14             | 51.4               |
| MACD / Signal     | 2.21 / 1.49        |
| ADX14 / +DI / -DI | 22.3 / 26.9 / 16.8 |
| ATR14             | $5.47 (6.64%)      |
| 63-day range      | $63.51 - $94.40    |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 82.47 vs 80.47               |
| Trend        | Close above SMA50                         | 8      | 8   | 82.47 vs 78.25               |
| Trend        | Close above SMA200                        | 0      | 8   | 82.47 vs 103.29              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 80.47 vs 78.25               |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 78.25 vs 103.29              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 1.73                         |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 51.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 2.21 vs 1.49                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.63              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 8.11%                        |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.32x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1329403534 vs 1307089667     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.33x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 22.3, +DI 26.9, -DI 16.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 92.49               |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.64%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 12.64%                       |

## Support And Resistance

- Support levels: $63.51, $70.66, $74.25, $79.99
- Resistance levels: $84.75, $88.60, $93.80, $111.46, $120.88

## Entry Plans

| Plan           | Entry zone      | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | --------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $79.03 - $83.14 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $72.77 | $97.71   | $106.02  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $84.75 - $87.49 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $81.77 | $97.07   | $102.54  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
