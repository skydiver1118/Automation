# CRM Technical Analysis Sample

Generated: 2026-07-06 16:40:35
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (34/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRM_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRM_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $165.65            |
| SMA20             | $162.62            |
| SMA50             | $173.59            |
| SMA200            | $210.86            |
| RSI14             | 49.6               |
| MACD / Signal     | -4.35 / -5.79      |
| ADX14 / +DI / -DI | 16.3 / 27.4 / 26.9 |
| ATR14             | $6.93 (4.19%)      |
| 63-day range      | $146.32 - $210.80  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 165.65 vs 162.62             |
| Trend        | Close above SMA50                         | 0      | 8   | 165.65 vs 173.59             |
| Trend        | Close above SMA200                        | 0      | 8   | 165.65 vs 210.86             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 162.62 vs 173.59             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 173.59 vs 210.86             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -7.08                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 49.6                   |
| Momentum     | MACD above signal                         | 7      | 7   | -4.35 vs -5.79               |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 3.02               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -12.01%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.44x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | -209509228 vs -150007916     |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.26x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 16.3, +DI 27.4, -DI 26.9 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 182.60              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 4.19%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 21.42%                       |

## Support And Resistance

- Support levels: $145.10, $163.44
- Resistance levels: $167.72, $182.60, $189.98, $202.41, $210.80

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $173.59 - $177.06 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $163.19 | $194.39  | $208.26  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $160.68 - $165.88 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $157.22 | $177.15  | $184.08  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $167.72 - $171.19 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $164.15 | $183.32  | $190.25  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
