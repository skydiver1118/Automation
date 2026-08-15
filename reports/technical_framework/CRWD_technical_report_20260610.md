# CRWD Technical Analysis Sample

Generated: 2026-06-10 20:55:03
Data source: yfinance adjusted daily OHLCV through 2026-06-10.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Neutral (62/100).**

Not bullish yet under the framework; classify as Neutral because MACD is not above signal; close is below SMA20, showing near-term pullback pressure.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [CRWD_technical_chart_20260610.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/CRWD_technical_chart_20260610.png)

## Key Indicators

| Metric            | Value              |
| ----------------- | ------------------ |
| Close             | $647.74            |
| SMA20             | $664.67            |
| SMA50             | $531.89            |
| SMA200            | $481.52            |
| RSI14             | 53.9               |
| MACD / Signal     | 42.86 / 56.28      |
| ADX14 / +DI / -DI | 43.4 / 28.4 / 24.5 |
| ATR14             | $35.07 (5.41%)     |
| 63-day range      | $361.81 - $785.66  |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                     |
| ------------ | ----------------------------------------- | ------ | --- | ---------------------------- |
| Trend        | Close above SMA20                         | 0      | 6   | 647.74 vs 664.67             |
| Trend        | Close above SMA50                         | 8      | 8   | 647.74 vs 531.89             |
| Trend        | Close above SMA200                        | 8      | 8   | 647.74 vs 481.52             |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 664.67 vs 531.89             |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 531.89 vs 481.52             |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 99.58                        |
| Momentum     | RSI in constructive range                 | 8      | 8   | RSI14 53.9                   |
| Momentum     | MACD above signal                         | 0      | 7   | 42.86 vs 56.28               |
| Momentum     | MACD histogram improving                  | 0      | 5   | 5d change -24.22             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 18.59%                       |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.65x                        |
| Confirmation | OBV above 20-day average                  | 0      | 5   | -58378466 vs -45960478       |
| Confirmation | 20-day up-volume beats down-volume        | 0      | 5   | 0.88x                        |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 43.4, +DI 28.4, -DI 24.5 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 783.95              |
| Risk/context | ATR volatility is tradable                | 4      | 4   | ATR14 5.41%                  |
| Risk/context | Close is within 8% of 63-day high         | 0      | 5   | 17.55%                       |

## Support And Resistance

- Support levels: $361.06, $439.18, $470.25, $538.63, $625.42
- Resistance levels: $785.23

## Entry Plans

| Plan           | Entry zone        | Trigger                                                                                                      | Stop    | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | ----------------- | ------------------------------------------------------------------------------------------------------------ | ------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $629.79 - $656.09 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $496.82 | $935.18   | $1,081.30 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $785.23 - $802.77 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $647.32 | $1,087.36 | $1,234.04 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
