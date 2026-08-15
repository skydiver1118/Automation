# MSFT Technical Analysis Sample

Generated: 2026-06-05 16:40:56
Data source: yfinance adjusted daily OHLCV through 2026-06-05.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (41/100).**

Not bullish under the framework; classify as Bearish because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MSFT_technical_chart_20260605.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MSFT_technical_chart_20260605.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $416.67            |
| SMA20             | $422.18            |
| SMA50             | $407.67            |
| SMA200            | $454.44            |
| RSI14             | 47.7               |
| MACD / Signal     | 5.78 / 6.40        |
| ADX14 / +DI / -DI | 18.6 / 32.9 / 33.4 |
| ATR14             | $12.88 (3.09%)     |
| 63-day range      | $355.51 - $466.32  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 416.67 vs 422.18             |
| Trend        | Close above SMA50                         | 8      | 8   | 416.67 vs 407.67             |
| Trend        | Close above SMA200                        | 0      | 8   | 416.67 vs 454.44             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 422.18 vs 407.67             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 407.67 vs 454.44             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 10.65                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 47.7                   |
| Momentum     | MACD above signal                         | 0      | 7   | 5.78 vs 6.40                 |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -2.39              |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -0.76%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.87x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 33967911 vs 18417576         |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.97x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 18.6, +DI 32.9, -DI 33.4 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 450.60              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.09%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 10.65%                       |

## Support And Resistance

- Support levels: $355.51, $380.89, $394.86, $409.47
- Resistance levels: $428.48, $450.60, $466.32, $486.84

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $422.18 - $428.62 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $402.86 | $460.82  | $486.58  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $403.03 - $412.69 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $394.79 | $434.00  | $447.07  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $428.48 - $434.92 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $409.47 | $476.15  | $498.37  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
