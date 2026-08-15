# MAG7 Momentum Rotation TrendSpider Results

Run date: 2026-05-11

## Setup

- Indicator: `MAG7 Momentum Rotation Leg`
- Strategy: `MAG7 Momentum Rotation Top2`
- Universe: AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA
- Rule: monthly rebalance, top 2 by 135-day average daily return
- Timeframe: Daily
- TrendSpider range used: 300 candles
- Entry: `MAG7 Rot Entry` signal emerged
- Exit: `MAG7 Rot Exit` signal emerged

## Per-Symbol TrendSpider Results

| Symbol | Net Perf | Buy/Hold | Positions | Wins | Max DD | Avg Return | Reward/Risk | Expectancy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| AAPL | 0.0% | 22.4% | 5 | 40% | -4.4% | 0.03% | 1.56 | 0.0 |
| MSFT | 0.5% | 6.3% | 7 | 57% | -10.5% | 0.08% | 0.83 | 0.0 |
| GOOGL | 48.5% | 135.5% | 2 | 100% | -20.4% | 23.16% | - | - |
| AMZN | 21.4% | 29.9% | 3 | 67% | -4.2% | 6.92% | 4.18 | 2.5 |
| NVDA | 8.4% | 80.5% | 7 | 57% | -16.0% | 1.37% | 1.33 | 0.3 |
| META | -1.8% | -6.6% | 5 | 40% | -30.2% | 0.33% | 1.61 | 0.0 |
| TSLA | -28.0% | 49.4% | 5 | 20% | -31.6% | -6.13% | 0.45 | -0.7 |

## Approximate Combined Result

Because the rule holds the top 2 names, each selected leg would be 50% weighted in a portfolio approximation.

- Sum of full-size leg net performance: 49.0%
- Approximate top-2 weighted portfolio net performance: 24.5%
- Equal-weight MAG7 buy-and-hold average over the same per-symbol windows: 45.3%
- Total per-symbol positions: 34
- Position-weighted average trade return: 1.42%
- Position-weighted win rate: 50.0%

## Caveat

TrendSpider Strategy Tester reports each symbol independently. The combined result above is an approximation from per-leg Strategy Tester output, not a true synchronized portfolio equity curve with exact month-by-month allocations and drawdown.
