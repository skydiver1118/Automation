# AVGO Technical Analysis Sample

Generated: 2026-06-04 19:39:15
Data source: yfinance adjusted daily OHLCV through 2026-06-04.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (67/100).**

Not bullish yet under the framework; classify as Neutral because close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [AVGO_technical_chart_20260604.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/AVGO_technical_chart_20260604.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $418.91            |
| SMA20             | $430.36            |
| SMA50             | $397.07            |
| SMA200            | $354.46            |
| RSI14             | 48.1               |
| MACD / Signal     | 14.16 / 13.27      |
| ADX14 / +DI / -DI | 27.1 / 30.0 / 31.1 |
| ATR14             | $21.79 (5.20%)     |
| 63-day range      | $289.96 - $495.00  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 418.91 vs 430.36             |
| Trend        | Close above SMA50                         | 8      | 8   | 418.91 vs 397.07             |
| Trend        | Close above SMA200                        | 8      | 8   | 418.91 vs 354.46             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 430.36 vs 397.07             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 397.07 vs 354.46             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 42.22                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 48.1                   |
| Momentum     | MACD above signal                         | 7      | 7   | 14.16 vs 13.27               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.51               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -1.53%                       |
| Confirmation | Current volume above 20-day average       | 5      | 5   | 3.09x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | 1147521822 vs 1197096046     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.72x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 27.1, +DI 30.0, -DI 31.1 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 472.22              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.20%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 15.37%                       |

## Support And Resistance

- Support levels: $291.53, $312.73, $329.81, $369.17, $400.03
- Resistance levels: $436.45, $472.22, $495.00

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $389.13 - $405.48 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $375.27 | $441.36  | $463.39  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $436.45 - $447.35 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $400.03 | $525.64  | $567.51  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
