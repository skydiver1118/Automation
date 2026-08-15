# MU Technical Analysis Sample

Generated: 2026-06-04 19:39:22
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (88/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MU_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MU_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $996.00             |
| SMA20             | $838.95             |
| SMA50             | $607.71             |
| SMA200            | $357.01             |
| RSI14             | 69.7                |
| MACD / Signal     | 123.33 / 106.61     |
| ADX14 / +DI / -DI | 42.4 / 40.9 / 17.4  |
| ATR14             | $60.70 (6.09%)      |
| 63-day range      | $311.49 - $1,089.29 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 996.00 vs 838.95             |
| Trend        | Close above SMA50                         | 8      | 8   | 996.00 vs 607.71             |
| Trend        | Close above SMA200                        | 8      | 8   | 996.00 vs 357.01             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 838.95 vs 607.71             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 607.71 vs 357.01             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 169.80                       |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 69.7                   |
| Momentum     | MACD above signal                         | 7      | 7   | 123.33 vs 106.61             |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.27               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 49.42%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.98x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 1285528942 vs 1106753772     |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.89x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 42.4, +DI 40.9, -DI 17.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 1109.67             |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.09%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 8.56%                        |

## Support And Resistance

- Support levels: $568.23, $607.71, $652.21, $841.19, $971.68
- Resistance levels: $1,094.39

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop    | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $941.33 - $986.86     | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $547.01 | $1,798.26 | $2,215.34 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,089.29 - $1,119.64 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $971.68 | $1,370.04 | $1,502.82 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
