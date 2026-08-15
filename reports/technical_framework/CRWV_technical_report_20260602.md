# CRWV Technical Analysis Sample

Generated: 2026-06-02 16:57:27
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (81/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWV_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWV_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $119.27            |
| SMA20             | $112.64            |
| SMA50             | $105.40            |
| SMA200            | $99.78             |
| RSI14             | 57.0               |
| MACD / Signal     | 1.37 / 0.61        |
| ADX14 / +DI / -DI | 15.1 / 34.4 / 20.8 |
| ATR14             | $9.02 (7.56%)      |
| 63-day range      | $67.15 - $138.25   |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 119.27 vs 112.64             |
| Trend        | Close above SMA50                         | 8      | 8   | 119.27 vs 105.40             |
| Trend        | Close above SMA200                        | 8      | 8   | 119.27 vs 99.78              |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 112.64 vs 105.40             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 105.40 vs 99.78              |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 12.06                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 57.0                   |
| Momentum     | MACD above signal                         | 7      | 7   | 1.37 vs 0.61                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 2.87               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -4.91%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.08x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 559843175 vs 517747729       |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.02x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 15.1, +DI 34.4, -DI 20.8 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 133.16              |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 7.56%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 13.73%                       |

## Support And Resistance

- Support levels: $75.79, $85.78, $93.47, $102.29, $111.42
- Resistance levels: $123.55, $132.64, $138.25

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $108.12 - $114.89 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $96.38  | $141.77  | $156.90  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $123.55 - $128.06 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $112.64 | $152.15  | $165.32  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
