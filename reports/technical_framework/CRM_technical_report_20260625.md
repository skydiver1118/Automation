# CRM Technical Analysis Sample

Generated: 2026-06-26 06:53:38
Data source: yfinance adjusted daily OHLCV through 2026-06-25.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (13/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50; MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRM_technical_chart_20260625.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRM_technical_chart_20260625.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $150.19            |
| SMA20             | $171.93            |
| SMA50             | $176.26            |
| SMA200            | $213.29            |
| RSI14             | 31.9               |
| MACD / Signal     | -8.20 / -5.74      |
| ADX14 / +DI / -DI | 20.7 / 18.3 / 34.6 |
| ATR14             | $7.48 (4.98%)      |
| 63-day range      | $146.32 - $210.80  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 150.19 vs 171.93             |
| Trend        | Close above SMA50                         | 0      | 8   | 150.19 vs 176.26             |
| Trend        | Close above SMA200                        | 0      | 8   | 150.19 vs 213.29             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 171.93 vs 176.26             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 176.26 vs 213.29             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -4.38                        |
| Momentum     | RSI in constructive range                 | 0      | 8   | RSI14 31.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | -8.20 vs -5.74               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 0.78               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -15.17%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.59x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | -202449700 vs -65265745      |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.29x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 20.7, +DI 18.3, -DI 34.6 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 207.50              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.98%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 28.75%                       |

## Support And Resistance

- Support levels: $136.36, $146.32
- Resistance levels: $157.06, $188.27, $193.06, $202.41, $209.97

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $176.26 - $180.00 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $165.03 | $198.71  | $213.68  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $142.58 - $148.19 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $138.84 | $160.35  | $167.83  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $157.06 - $160.80 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $146.32 | $184.15  | $196.76  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
