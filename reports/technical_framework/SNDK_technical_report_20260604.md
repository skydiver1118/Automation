# SNDK Technical Analysis Sample

Generated: 2026-06-04 19:39:33
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (93/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SNDK_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SNDK_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $1,759.68           |
| SMA20             | $1,542.72           |
| SMA50             | $1,162.25           |
| SMA200            | $522.67             |
| RSI14             | 68.2                |
| MACD / Signal     | 169.57 / 158.94     |
| ADX14 / +DI / -DI | 47.0 / 33.9 / 7.8   |
| ATR14             | $109.58 (6.23%)     |
| 63-day range      | $517.00 - $1,861.00 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                    |
| ------------ | ----------------------------------------- | ------ | --- | --------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 1759.68 vs 1542.72          |
| Trend        | Close above SMA50                         | 8      | 8   | 1759.68 vs 1162.25          |
| Trend        | Close above SMA200                        | 8      | 8   | 1759.68 vs 522.67           |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1542.72 vs 1162.25          |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 1162.25 vs 522.67           |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 357.01                      |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 68.2                  |
| Momentum     | MACD above signal                         | 7      | 7   | 169.57 vs 158.94            |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 8.32              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 24.80%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.83x                       |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 542050052 vs 509380293      |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.38x                       |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 47.0, +DI 33.9, -DI 7.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 1848.66            |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.23%                 |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 5.44%                       |

## Support And Resistance

- Support levels: $207.48, $541.44, $1,162.25, $1,257.05, $1,534.85
- Resistance levels: $1,857.91

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop      | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | --------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $1,487.93 - $1,570.11 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $1,052.67 | $2,481.71 | $2,958.06 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,857.91 - $1,912.70 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $1,542.72 | $2,570.50 | $2,913.09 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
