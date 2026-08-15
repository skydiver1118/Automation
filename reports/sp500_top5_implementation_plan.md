# S&P 500 Top-5 Momentum Backtest Plan

## Goal

Each trading day, rank all S&P 500 stocks, hold only the top 5 momentum names, keep at most 5 open positions, and only open new positions when the portfolio has fewer than 5 names.

## Detailed Steps

1. Define the strategy rules.
   - Universe: current S&P 500 constituents.
   - Ranking signal: trailing adjusted-close momentum.
   - Default lookback: 126 trading days.
   - Max open positions: 5.
   - Position sizing: 20% per slot, cash idle if fewer than 5 names are held.

2. Fetch the universe.
   - Pull current S&P 500 constituents from Wikipedia.
   - Convert dot tickers to Yahoo tickers, e.g. `BRK.B` to `BRK-B`.
   - Save the constituent file locally in `data/sp500_top5/sp500_constituents.csv`.

3. Fetch historical prices.
   - Use `yfinance.download()` in batches.
   - Use `auto_adjust=True`, so `Open` and `Close` are adjusted for splits and dividends.
   - Fetch extra lookback history before the backtest start date so the first test day has enough ranking data.
   - Save adjusted close data locally under `data/sp500_top5/`.

4. Simulate portfolio state.
   - At each close, rank all usable tickers by trailing momentum.
   - Queue sells for held tickers no longer in the top 5.
   - Queue buys from the ranked list until 5 names will be held.
   - Execute queued exits and entries at the next trading day's open.
   - Apply open-to-close returns for currently held names.

5. Write outputs.
   - Equity snapshots: `reports/sp500_top5_equity.csv`.
   - Trade log: `reports/sp500_top5_trades.csv`.
   - Markdown summary: `reports/sp500_top5_momentum_backtest.md`.

6. Validate.
   - Unit-test the max-position behavior on synthetic data.
   - Run the live data workflow for the most recent month.

## Similar Projects And Borrowed Ideas

- GitHub topic `sp500` contains many S&P 500 data/backtest projects, including historical constituent datasets. This is useful for future survivorship-bias cleanup.
- `Quantitaive-Momentum-Strategy` demonstrates selecting high-momentum S&P 500 stocks and equal-weighting the selected names.
- Daniel Griffiths' S&P 500 momentum project uses daily S&P 500 data, multi-timeframe momentum ranking, and equal-weight portfolio construction.
- `sp500-rsi-backtest` is not a momentum strategy, but it shows the pattern of running a strategy across all S&P 500 symbols and collecting per-symbol metrics.

## Data Source Choice

For the first one-month local test, the implementation uses:

- Current S&P 500 constituents from Wikipedia.
- Yahoo Finance adjusted close prices through `yfinance`.

This is a practical first pass. For multi-year research-grade tests, replace current constituents with point-in-time S&P 500 membership to avoid survivorship bias.
