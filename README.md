# TrendSpider Strategy Lab

This workspace is for iterating stock trading strategies from TrendSpider backtests.

## Workflow

1. Build or adjust the strategy in TrendSpider.
2. Run the backtest.
3. Export results as CSV and place the file in `data/trendspider_exports/`.
4. Create or update a strategy config in `strategies/`.
5. Run the local analysis scripts to calculate comparable metrics.
6. Review results in `reports/`, then adjust entry rules, exit rules, or indicator parameters.

## Current Structure

- `data/trendspider_exports/` - raw CSV exports from TrendSpider.
- `strategies/` - strategy assumptions and parameter sets.
- `reports/` - generated summaries and comparison tables.
- `src/strategy_lab/` - reusable Python analysis code.

## Analyze An Export

```powershell
python -m src.strategy_lab.analyze data/trendspider_exports/example.csv
```

The analyzer expects a trade-level CSV with at least one profit/loss column. It tries common column names such as `Profit`, `P/L`, `Net Profit`, `Return`, and `Return %`.

## Compare Multiple Exports

```powershell
python -m src.strategy_lab.analyze `
  data/trendspider_exports/baseline.csv `
  data/trendspider_exports/variant_fast_exit.csv
```

When more than one CSV is provided, the framework writes:

- `reports/backtest_comparison.csv`
- `reports/backtest_comparison.md`

## Run The Local S&P 500 Top-5 Momentum Backtest

```powershell
python -m src.strategy_lab.sp500_top5 `
  --start 2026-04-12 `
  --end 2026-05-12 `
  --lookback-days 126 `
  --max-positions 5 `
  --refresh
```

This workflow downloads current S&P 500 constituents and Yahoo Finance adjusted open/close prices to `data/sp500_top5/`. Signals are generated from closing prices and entries/exits execute at the next trading day's open. It then writes:

- `reports/sp500_top5_momentum_backtest.md`
- `reports/sp500_top5_equity.csv`
- `reports/sp500_top5_trades.csv`

## First Strategy Checklist

For the first strategy, capture these before tuning:

- Symbol or universe
- Timeframe
- Entry conditions
- Exit conditions
- Indicator parameters
- Risk controls, including stop loss, target, and position sizing
- Baseline TrendSpider export CSV

Then change only one major thing at a time: entry condition, exit condition, or one indicator parameter. That keeps the comparison readable.

## Access Notes

TrendSpider login should stay in the browser session. For most iteration work, the local framework only needs exported backtest CSV files and a short description of the strategy rules.

## Stock Alerts

The project also includes a local stock alert runner for conditions such as `QQQ` closing below SMA 50. See `docs/stock_alerts.md`.

```powershell
python scripts/run_stock_alerts.py --config configs/stock_alerts.example.json --dry-run
```

## Interactive Brokers Paper Connection

IBKR API authentication happens in TWS or IB Gateway, not through API keys in this repo. Start Trader Workstation in paper trading mode, then enable API socket clients:

- TWS paper default: `127.0.0.1:7497`
- IB Gateway paper default: `127.0.0.1:4002`

In TWS, open `Configure > API > Settings`, enable socket clients, and confirm the socket port. Then run:

```powershell
python scripts/check_ibkr_paper_connection.py
```

For paper IB Gateway:

```powershell
python scripts/check_ibkr_paper_connection.py --port 4002
```
