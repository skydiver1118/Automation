# CHAT Technical Analysis Sample

Generated: 2026-06-02 16:57:25
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (83/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CHAT_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CHAT_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $103.45            |
| SMA20             | $89.67             |
| SMA50             | $78.25             |
| SMA200            | $64.66             |
| RSI14             | 80.5               |
| MACD / Signal     | 6.13 / 4.98        |
| ADX14 / +DI / -DI | 35.2 / 50.8 / 13.7 |
| ATR14             | $2.85 (2.75%)      |
| 63-day range      | $58.52 - $103.77   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 103.45 vs 89.67              |
| Trend        | Close above SMA50                         | 8      | 8   | 103.45 vs 78.25              |
| Trend        | Close above SMA200                        | 8      | 8   | 103.45 vs 64.66              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 89.67 vs 78.25               |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 78.25 vs 64.66               |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 10.29                        |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 80.5                   |
| Momentum     | MACD above signal                         | 7      | 7   | 6.13 vs 4.98                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.95               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 28.62%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.90x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 23589056 vs 19496148         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.39x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 35.2, +DI 50.8, -DI 13.7 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 102.28              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.75%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.31%                        |

## Support And Resistance

- Support levels: $62.69, $74.70, $77.65, $81.50, $89.84
- Resistance levels: $103.40

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop   | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------ | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $88.58 - $90.71   | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $75.40 | $118.14  | $132.39  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $103.77 - $105.19 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $97.76 | $117.93  | $124.66  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
