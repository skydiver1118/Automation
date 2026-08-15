# S&P 500 Cup-And-Handle Pattern In Force Scan

Generated from weekly OHLCV data through latest available weekly bar `2026-05-25`.
Latest broad-market daily close check: SPY close date `2026-05-29`.
Universe source: `https://en.wikipedia.org/wiki/List_of_S%26P_500_companies`.
Universe size: 503; tickers with usable yfinance weekly data: 503.
Lookback: `2y`. Minimum selected score: `45.0`. Kept top `10` scores only.

This is technical-pattern research, not investment advice.

## Summary

| Metric | Value |
| --- | ---: |
| Pattern in Force selections before top-N filter | 38 |
| Pattern in Force selections kept | 10 |
| Scanned tickers with data | 503 |
| Failed/no-data tickers | 0 |

## Score Meaning

| Score band | Meaning |
| --- | --- |
| 75-100 | Strong: clean geometry and stronger confirmation traits. |
| 60-74 | Good watchlist: pattern is usable but still needs confirmation. |
| 45-59 | Speculative watchlist: recognizable shape, but quality issues remain. |
| Below 45 | Weak: too many geometry/confirmation problems. |

Score is pattern quality, not a probability forecast. It rewards cup symmetry, reasonable depth, rim alignment, handle quality, proximity to breakout, and healthier volume behavior.

## Refined Textbook Filters Used

- Minimum cup width is 20 weekly bars, matching TradingView's documented auto-pattern minimum.
- Cup low must sit near the middle of the cup, and the cup must pass a rounded U-shape fit check.
- Cup depth must be moderate: 12%-45% in this scanner, with higher scores near the 20%-30% textbook zone.
- Cup rims must be close: rim deviation is measured against cup height, not only raw price percentage.
- Handle must be shorter than the cup, stay in the upper half, and retrace no more than 45% of cup depth.
- Pattern bucket is kept as `Cup and Handle Pattern in Force`, meaning active/formed and waiting for breakout.
- Rule references used: TradingView Cup and Handle auto-pattern docs, TrendSpider chart-pattern recognition docs, and classic O'Neil-style guidance on U-shaped cups and upper-half handles.

## Ranked Pattern In Force Selections

| Rank | Symbol | Company | Sector | Score | ScoreBand | LatestClose | BreakoutLevel | BreakoutGainPct | MeasuredTarget | TargetGainPct | TargetReturnPct | HandleLow | HandleRiskPct | CupDepthPct | HandleDepthPctOfCup | CupWidthWeeks | HandleWidthWeeks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | BMY | Bristol Myers Squibb | Health Care | 82.88 | Strong | 57.18 | 60.78 | 6.3 | 78.69 | 37.62 | 29.47 | 55.41 | -3.1 | 29.31 | 29.98 | 65 | 4 |
| 2 | WST | West Pharmaceutical Services | Health Care | 80.7 | Strong | 322.81 | 330.88 | 2.5 | 437.93 | 35.66 | 32.35 | 295.9 | -8.34 | 32.35 | 32.68 | 29 | 2 |
| 3 | LYV | Live Nation Entertainment | Communication Services | 80.34 | Strong | 168.41 | 173.12 | 2.8 | 223.03 | 32.43 | 28.83 | 159.71 | -5.17 | 28.48 | 26.87 | 35 | 2 |
| 4 | MO | Altria | Consumer Staples | 79.43 | Strong | 69.58 | 74.56 | 7.16 | 87.79 | 26.17 | 17.74 | 64.08 | -7.9 | 19.48 | 29.1 | 26 | 7 |
| 5 | FTV | Fortive | Industrials | 78.74 | Strong | 58.32 | 62.81 | 7.7 | 79.07 | 35.58 | 25.89 | 57.38 | -1.61 | 25.9 | 33.35 | 65 | 4 |
| 6 | IEX | IDEX Corporation | Industrials | 77.69 | Strong | 210.83 | 223.85 | 6.18 | 291.71 | 38.36 | 30.31 | 203.45 | -3.5 | 30.02 | 30.06 | 65 | 4 |
| 7 | APO | Apollo Global Management | Financials | 77.54 | Strong | 128.71 | 136.58 | 6.11 | 174.05 | 35.23 | 27.43 | 126.08 | -2.04 | 27.34 | 28.02 | 26 | 2 |
| 8 | VZ | Verizon | Communication Services | 77.34 | Strong | 47.81 | 48.96 | 2.41 | 59.22 | 23.87 | 20.96 | 45.81 | -4.18 | 21.09 | 27.68 | 59 | 4 |
| 9 | AMZN | Amazon | Consumer Discretionary | 73.98 | Good watchlist | 270.64 | 278.56 | 2.93 | 361.12 | 33.43 | 29.64 | 255.19 | -5.71 | 29.64 | 28.31 | 26 | 3 |
| 10 | XYZ | Block, Inc. | Financials | 71.68 | Good watchlist | 75.72 | 77.16 | 1.9 | 110.65 | 46.13 | 43.4 | 67.08 | -11.41 | 40.99 | 30.1 | 27 | 3 |

## Pattern Dates

| Symbol | LeftRimDate | LeftRimPrice | CupLowDate | CupLowPrice | RightRimDate | RightRimPrice | HandleLowDate | LatestDate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| BMY | 2025-01-27 | 61.1 | 2025-09-22 | 43.19 | 2026-04-27 | 60.78 | 2026-05-11 | 2026-05-25 |
| WST | 2025-10-20 | 322.34 | 2026-01-26 | 223.83 | 2026-05-11 | 330.88 | 2026-05-11 | 2026-05-25 |
| LYV | 2025-09-08 | 175.25 | 2025-11-24 | 125.34 | 2026-05-11 | 173.12 | 2026-05-18 | 2026-05-25 |
| MO | 2025-10-06 | 67.12 | 2026-01-05 | 54.7 | 2026-04-06 | 67.93 | 2026-04-13 | 2026-05-25 |
| FTV | 2025-01-27 | 62.17 | 2025-09-01 | 46.54 | 2026-04-27 | 62.81 | 2026-05-18 | 2026-05-25 |
| IEX | 2025-01-27 | 226.05 | 2025-09-22 | 158.19 | 2026-04-27 | 223.85 | 2026-04-27 | 2026-05-25 |
| APO | 2025-11-10 | 137.03 | 2026-03-02 | 99.56 | 2026-05-11 | 136.58 | 2026-05-25 | 2026-05-25 |
| VZ | 2025-03-10 | 47.36 | 2025-10-20 | 38.39 | 2026-04-27 | 48.65 | 2026-05-18 | 2026-05-25 |
| AMZN | 2025-11-03 | 258.6 | 2026-02-16 | 196.0 | 2026-05-04 | 278.56 | 2026-05-18 | 2026-05-25 |
| XYZ | 2025-10-27 | 81.7 | 2026-02-09 | 48.21 | 2026-05-04 | 77.16 | 2026-05-18 | 2026-05-25 |

## Notes By Ticker

- **BMY (Bristol Myers Squibb)**: Cup and Handle Pattern in Force; awaiting breakout; breakout `60.78`, target `78.69`. cup has a declining left side, rising right side, and rounded U-shape fit; handle remains in upper half of the cup; right rim is modestly below the left rim; no weekly close above the handle/rim resistance yet
- **WST (West Pharmaceutical Services)**: Cup and Handle Pattern in Force; near breakout; breakout `330.88`, target `437.93`. cup has a declining left side, rising right side, and rounded U-shape fit; handle remains in upper half of the cup; no weekly close above the handle/rim resistance yet
- **LYV (Live Nation Entertainment)**: Cup and Handle Pattern in Force; near breakout; breakout `173.12`, target `223.03`. cup has a declining left side, rising right side, and rounded U-shape fit; handle remains in upper half of the cup; right rim is modestly below the left rim; no weekly close above the handle/rim resistance yet
- **MO (Altria)**: Cup and Handle Pattern in Force; awaiting breakout; breakout `74.56`, target `87.79`. cup has a declining left side, rising right side, and rounded U-shape fit; handle remains in upper half of the cup; no weekly close above the handle/rim resistance yet
- **FTV (Fortive)**: Cup and Handle Pattern in Force; awaiting breakout; breakout `62.81`, target `79.07`. cup has a declining left side, rising right side, and rounded U-shape fit; handle remains in upper half of the cup; no weekly close above the handle/rim resistance yet
- **IEX (IDEX Corporation)**: Cup and Handle Pattern in Force; awaiting breakout; breakout `223.85`, target `291.71`. cup has a declining left side, rising right side, and rounded U-shape fit; handle remains in upper half of the cup; right rim is modestly below the left rim; no weekly close above the handle/rim resistance yet
- **APO (Apollo Global Management)**: Cup and Handle Pattern in Force; awaiting breakout; breakout `136.58`, target `174.05`. cup has a declining left side, rising right side, and rounded U-shape fit; handle remains in upper half of the cup; right rim is modestly below the left rim; no weekly close above the handle/rim resistance yet
- **VZ (Verizon)**: Cup and Handle Pattern in Force; near breakout; breakout `48.96`, target `59.22`. cup has a declining left side, rising right side, and rounded U-shape fit; handle remains in upper half of the cup; no weekly close above the handle/rim resistance yet
- **AMZN (Amazon)**: Cup and Handle Pattern in Force; near breakout; breakout `278.56`, target `361.12`. cup has a declining left side, rising right side, and rounded U-shape fit; handle remains in upper half of the cup; no weekly close above the handle/rim resistance yet
- **XYZ (Block, Inc.)**: Cup and Handle Pattern in Force; near breakout; breakout `77.16`, target `110.65`. cup has a declining left side, rising right side, and rounded U-shape fit; handle remains in upper half of the cup; right rim is modestly below the left rim; no weekly close above the handle/rim resistance yet
