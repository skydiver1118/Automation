# MSFT Technical Analysis Sample

Generated: 2026-07-06 16:40:32
Data source: yfinance adjusted daily OHLCV through 2026-07-06.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bearish (44/100).**

Not bullish under the framework; classify as Bearish because close is not above SMA50.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [MSFT_technical_chart_20260706.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/MSFT_technical_chart_20260706.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $386.74            |
| SMA20             | $384.89            |
| SMA50             | $406.31            |
| SMA200            | $443.19            |
| RSI14             | 48.2               |
| MACD / Signal     | -8.57 / -10.39     |
| ADX14 / +DI / -DI | 20.9 / 25.4 / 29.2 |
| ATR14             | $12.79 (3.31%)     |
| 63-day range      | $349.20 - $466.32  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 386.74 vs 384.89             |
| Trend        | Close above SMA50                         | 0      | 8   | 386.74 vs 406.31             |
| Trend        | Close above SMA200                        | 0      | 8   | 386.74 vs 443.19             |
| Trend        | SMA20 above SMA50                         | 0      | 6   | 384.89 vs 406.31             |
| Trend        | SMA50 above SMA200                        | 0      | 6   | 406.31 vs 443.19             |
| Trend        | SMA50 rising over 20 sessions             | 0      | 6   | -0.43                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 48.2                   |
| Momentum     | MACD above signal                         | 7      | 7   | -8.57 vs -10.39              |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 5.91               |
| Momentum     | 20-day rate of change positive            | 0      | 5   | -9.65%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.61x                        |
| Confirmation | OBV above 20-day average                  | 5      | 5   | -70537293 vs -176674615      |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.07x                        |
| Risk/context | ADX confirms bullish directional pressure | 0      | 7   | ADX 20.9, +DI 25.4, -DI 29.2 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 417.59              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 3.31%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.07%                       |

## Support And Resistance

- Support levels: $351.53, $387.27
- Resistance levels: $384.17, $392.20, $409.38, $427.06, $466.32

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1 | Target 2 | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | -------- | -------- | ------------------------------------------------------------------------------------------------------------------------- |
| Reclaim entry  | $406.31 - $412.71 | Wait for a daily close back above SMA20/SMA50 with MACD above signal before considering a long.              | $387.12 | $444.69  | $470.28  | The framework does not treat bearish charts as immediate buys; this is a repair trigger.                                  |
| Pullback entry | $378.49 - $388.09 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $372.10 | $408.88  | $421.67  | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $392.20 - $398.60 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $384.89 | $420.98  | $433.78  | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
