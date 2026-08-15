# SMH Technical Analysis Sample

Generated: 2026-05-31 20:26:01
Data source: yfinance adjusted daily OHLCV through 2026-05-29.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (92/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SMH_technical_chart_20260529.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SMH_technical_chart_20260529.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $598.93            |
| SMA20             | $561.79            |
| SMA50             | $484.73            |
| SMA200            | $388.28            |
| RSI14             | 70.9               |
| MACD / Signal     | 30.48 / 30.42      |
| ADX14 / +DI / -DI | 35.3 / 36.9 / 14.9 |
| ATR14             | $18.69 (3.12%)     |
| 63-day range      | $359.86 - $612.30  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 598.93 vs 561.79             |
| Trend        | Close above SMA50                         | 8      | 8   | 598.93 vs 484.73             |
| Trend        | Close above SMA200                        | 8      | 8   | 598.93 vs 388.28             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 561.79 vs 484.73             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 484.73 vs 388.28             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 64.18                        |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 70.9                   |
| Momentum     | MACD above signal                         | 7      | 7   | 30.48 vs 30.42               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.63               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 18.20%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.75x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 291997400 vs 289049120       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.15x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 35.3, +DI 36.9, -DI 14.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 617.85              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.12%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 2.18%                        |

## Support And Resistance

- Support levels: $397.77, $484.73, $505.72, $527.87, $559.28
- Resistance levels: $613.69

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $552.44 - $566.46 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $466.04 | $746.29  | $839.70  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $612.30 - $621.65 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $561.79 | $727.34  | $782.53  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
