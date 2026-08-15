# QTUM Technical Analysis Sample

Generated: 2026-06-02 16:57:36
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (88/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [QTUM_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/QTUM_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $168.76            |
| SMA20             | $149.74            |
| SMA50             | $132.03            |
| SMA200            | $114.76            |
| RSI14             | 79.4               |
| MACD / Signal     | 8.68 / 7.45        |
| ADX14 / +DI / -DI | 36.7 / 45.3 / 13.8 |
| ATR14             | $4.28 (2.54%)      |
| 63-day range      | $101.41 - $168.97  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 168.76 vs 149.74             |
| Trend        | Close above SMA50                         | 8      | 8   | 168.76 vs 132.03             |
| Trend        | Close above SMA200                        | 8      | 8   | 168.76 vs 114.76             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 149.74 vs 132.03             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 132.03 vs 114.76             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 14.85                        |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 79.4                   |
| Momentum     | MACD above signal                         | 7      | 7   | 8.68 vs 7.45                 |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.70               |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 24.37%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 1.53x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 25015174 vs 19186899         |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 2.83x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 36.7, +DI 45.3, -DI 13.8 |
| Risk/context | Not dangerously overextended              | 0      | 4   | BB upper 166.67              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 2.54%                  |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 0.12%                        |

## Support And Resistance

- Support levels: $114.63, $127.52, $132.42, $137.66, $149.74
- Resistance levels: $168.39

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $147.60 - $150.81 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $127.75 | $192.11  | $213.57  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $168.97 - $171.11 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $160.20 | $189.72  | $199.57  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
