# SNDK Technical Analysis Sample

Generated: 2026-06-02 16:57:41
Data source: yfinance adjusted daily OHLCV through 2026-06-02.

This is technical strategy research, not investment advice.

## Decision

**Framework classification: Bullish (90/100).**

Bullish under the framework, but still buy only at a defined pullback or breakout trigger.

The classification requires price trend, momentum, volume confirmation, and risk context to agree. A bullish label is not an unconditional buy; the entry must still occur at a defined zone with a stop and acceptable reward/risk.

Chart: [SNDK_technical_chart_20260602.png](C:/Users/skydiver1118/Documents/New project/reports/technical_framework/SNDK_technical_chart_20260602.png)

## Key Indicators

| Metric            | Value               |
| ----------------- | ------------------- |
| Close             | $1,716.36           |
| SMA20             | $1,503.97           |
| SMA50             | $1,118.53           |
| SMA200            | $505.17             |
| RSI14             | 70.3                |
| MACD / Signal     | 162.83 / 152.62     |
| ADX14 / +DI / -DI | 44.5 / 34.0 / 9.3   |
| ATR14             | $106.57 (6.21%)     |
| 63-day range      | $517.00 - $1,804.00 |

## Score Breakdown

| Category     | Rule                                      | Points | Max | Evidence                    |
| ------------ | ----------------------------------------- | ------ | --- | --------------------------- |
| Trend        | Close above SMA20                         | 6      | 6   | 1716.36 vs 1503.97          |
| Trend        | Close above SMA50                         | 8      | 8   | 1716.36 vs 1118.53          |
| Trend        | Close above SMA200                        | 8      | 8   | 1716.36 vs 505.17           |
| Trend        | SMA20 above SMA50                         | 6      | 6   | 1503.97 vs 1118.53          |
| Trend        | SMA50 above SMA200                        | 6      | 6   | 1118.53 vs 505.17           |
| Trend        | SMA50 rising over 20 sessions             | 6      | 6   | 343.51                      |
| Momentum     | RSI in constructive range                 | 5      | 8   | RSI14 70.3                  |
| Momentum     | MACD above signal                         | 7      | 7   | 162.83 vs 152.62            |
| Momentum     | MACD histogram improving                  | 5      | 5   | 5d change 14.15             |
| Momentum     | 20-day rate of change positive            | 5      | 5   | 36.67%                      |
| Confirmation | Current volume above 20-day average       | 0      | 5   | 0.50x                       |
| Confirmation | OBV above 20-day average                  | 5      | 5   | 540876649 vs 505757622      |
| Confirmation | 20-day up-volume beats down-volume        | 5      | 5   | 1.39x                       |
| Risk/context | ADX confirms bullish directional pressure | 7      | 7   | ADX 44.5, +DI 34.0, -DI 9.3 |
| Risk/context | Not dangerously overextended              | 4      | 4   | BB upper 1763.66            |
| Risk/context | ATR volatility is tradable                | 2      | 4   | ATR14 6.21%                 |
| Risk/context | Close is within 8% of 63-day high         | 5      | 5   | 4.86%                       |

## Support And Resistance

- Support levels: $207.48, $541.44, $1,118.53, $1,260.81, $1,487.46
- Resistance levels: $1,793.92

## Entry Plans

| Plan           | Entry zone            | Trigger                                                                                                      | Stop      | Target 1  | Target 2  | Notes                                                                                                                     |
| -------------- | --------------------- | ------------------------------------------------------------------------------------------------------------ | --------- | --------- | --------- | ------------------------------------------------------------------------------------------------------------------------- |
| Pullback entry | $1,450.69 - $1,530.61 | Buy only after price holds the zone and closes back above the prior day's high or EMA8.                      | $1,011.96 | $2,448.04 | $2,926.73 | Best used when the stock is already bullish or neutral-bullish; skip if price slices through support on expanding volume. |
| Breakout entry | $1,793.92 - $1,847.20 | Buy only on a daily close above resistance with volume above the 20-day average and MACD histogram positive. | $1,503.97 | $2,453.73 | $2,770.31 | Avoid chasing if the close is more than 1 ATR above the breakout level or RSI is above 78.                                |

## Source Research Used

- GitHub: https://github.com/bukosabino/ta and https://ta-lib.org/index.html for the common indicator stack.
- Reddit: https://www.reddit.com/r/technicalanalysis/comments/1rr9v2e/technical_analysis_how_to_read_charts_and_make/ for practitioner emphasis on support, resistance, validation, and position sizing.
- X/Twitter: public X search/Grok-indexed examples were used as sentiment and workflow samples only; direct public post text is limited without login. Example: https://x.com/i/grok/share/DR88yKZT1Hd3IQjQH3k7I6Xxj.
- Book reference: John J. Murphy, Technical Analysis of the Financial Markets, table of contents/source listing: https://windsorpublishing.com/product/technical-analysis-of-the-financial-markets/.
