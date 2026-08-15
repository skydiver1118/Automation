# Profit Taking And Loss Taking Strategy Sub-Module

Date: 2026-05-24

Source brief: attached image `IMG_2773.JPG`. Core principle: first recover risk, then follow the trend, then exit hard only when structure breaks.

## Online Alignment

- CME Group emphasizes that position size should be calculated from the stop location and the dollar or percentage account risk before placing the trade: https://www.cmegroup.com/education/courses/trade-and-risk-management/proper-position-size
- StockCharts describes Chandelier Exit as an ATR-based trailing stop developed by Charles Le Beau and featured by Alexander Elder: https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/chandelier-exit
- TradingView describes Chandelier Exit as a volatility-based stop using local price extremes and ATR: https://www.tradingview.com/support/solutions/43000773013-chandelier-exit/
- Recent systematic trend-following research continues to use adaptive trailing stops and volatility-aware risk controls as core exit machinery: https://arxiv.org/abs/2602.11708

## Top 3 Profit-Taking Profiles

### 1. Risk-First Trend Runner

Best default for momentum and leveraged ETF systems.

- Define initial risk as 1R: entry price minus invalidation stop.
- At +1R, sell one third and raise the stop to breakeven.
- At +2R, sell one third and raise the stop to +1R.
- Hold the final third with a 22-period, 3 ATR Chandelier stop.
- Final exit requires trend damage, not just a scary candle.

Why it made rank 1: it matches the image directly. It converts the trade from risk state to safer state early, but keeps enough exposure for unusually large trend legs.

### 2. Volatility Ladder

Best for noisy high-beta names where fixed stops get shaken out.

- At +1.5R, sell 25% and raise the stop to breakeven.
- At +3R, sell 25% and trail the rest by highest close minus 2.5 ATR.
- If volatility expands, prefer ATR-based distance over a fixed percentage.
- Never lower a trailing stop after it ratchets upward.

Why it made rank 2: it gives wider breathing room than a fixed profit target and adapts better to SOXL/TQQQ-style volatility.

### 3. Structure Ladder

Best for swing trades with visible support/resistance.

- At prior resistance or +2R, sell 30%.
- Trail under higher lows with at least a 1 ATR floor.
- Stay long while higher highs and higher lows continue.
- Exit the runner on failed breakout, lower high, and close below EMA20.

Why it made rank 3: it is intuitive and trader-friendly, but harder to automate consistently than R and ATR rules.

## Top 3 Loss-Taking Profiles

### 1. One-R Invalidation Stop

Best default for every strategy.

- Put the stop where the trade thesis is wrong.
- Use position size so that stop equals the chosen account risk.
- Use at least a 1 ATR floor so ordinary noise does not trigger the stop.
- Exit fully if the active stop is touched or breached.

Why it made rank 1: the loss is known before entry and can be tested cleanly.

### 2. Trend Structure Break

Best for trend-following and momentum rotation.

- Cut exposure when price closes below EMA20 after a failed reclaim.
- Confirm with lower highs/lower lows, RSI below 50, or expanding down-volume.
- For leveraged ETFs, let the benchmark trend break act as a portfolio-level exit.
- Re-entry requires a fresh signal.

Why it made rank 2: it avoids waiting for the full 1R loss when the trend thesis has already failed.

### 3. Time And Volatility Failure

Best for breakouts and fast momentum trades.

- If price cannot reach +0.5R inside the confirmation window, exit or halve.
- If ATR expands against the position while price goes nowhere, reduce risk.
- If price gaps through the initial stop, exit at the first executable price and log slippage.
- Treat this as a secondary protection layer, not a replacement for the hard stop.

Why it made rank 3: it prevents dead-money trades from absorbing attention and capital, but it is less appropriate for monthly rotation systems.

## Implemented Files

- `src/strategy_lab/exit_profiles.py`: reusable catalog, ATR helper, markdown renderer, and long-position exit simulator.
- `tests/test_exit_profiles.py`: coverage for catalog shape, ATR math, scale-outs, stop movement, time failure, and markdown output.

## Current Recommendation

Use `Risk-First Trend Runner` plus `One-R Invalidation Stop` as the default pair for the next backtest iteration. Add `Trend Structure Break` as a portfolio-level override when the traded symbol and benchmark both lose trend.
