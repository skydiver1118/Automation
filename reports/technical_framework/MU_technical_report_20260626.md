# MU Technical Analysis Sample

Generated: 2026-06-28 17:42:23
Data source: yfinance adjusted daily OHLCV through 2026-06-26.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (78/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MU_technical_chart_20260626.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MU_technical_chart_20260626.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $1,132.33           |
| SMA20             | $1,035.41           |
| SMA50             | $802.14             |
| SMA200            | $425.71             |
| RSI14             | 59.0                |
| MACD / Signal     | 94.53 / 94.05       |
| ADX14 / +DI / -DI | 24.3 / 32.6 / 22.1  |
| ATR14             | $95.18 (8.41%)      |
| 63-day range      | $311.49 - $1,255.00 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 1132.33 vs 1035.41           |
| Trend        | Close above SMA50                         | 8      | 8   | 1132.33 vs 802.14            |
| Trend        | Close above SMA200                        | 8      | 8   | 1132.33 vs 425.71            |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1035.41 vs 802.14            |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 802.14 vs 425.71             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 254.79                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 59.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 94.53 vs 94.05               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -0.27              |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 22.61%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.48x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1175207400 vs 1219908740     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.96x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 24.3, +DI 32.6, -DI 22.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 1222.09             |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 8.41%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 9.77%                        |

## Support And Resistance

- Support levels: $360.63, $435.90, $652.21, $835.07, $1,014.25
- Resistance levels: $1,246.77

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop      | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | --------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $987.82 - $1,059.20   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $706.96   | $1,656.61 | $1,973.17 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,246.77 - $1,294.36 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $1,035.41 | $1,740.88 | $1,976.04 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
