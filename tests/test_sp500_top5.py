from __future__ import annotations

import pandas as pd

from src.strategy_lab.sp500_top5 import calculate_summary, run_top_n_backtest


def test_top_n_backtest_keeps_only_max_positions() -> None:
    dates = pd.date_range("2026-01-01", periods=10, freq="B")
    prices = pd.DataFrame(
        {
            "AAA": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            "BBB": [10, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            "CCC": [10, 10, 10, 11, 12, 13, 14, 15, 16, 17],
            "DDD": [10, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        },
        index=dates,
    )

    result = run_top_n_backtest(
        prices=prices,
        start=dates[3].date(),
        end=dates[-1].date(),
        lookback_days=2,
        max_positions=2,
    )

    assert result.snapshots
    assert all(len(snapshot.holdings) <= 2 for snapshot in result.snapshots)
    assert result.snapshots[-1].holdings == ("BBB", "CCC")


def test_summary_contains_portfolio_metrics() -> None:
    dates = pd.date_range("2026-01-01", periods=10, freq="B")
    prices = pd.DataFrame(
        {
            "AAA": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            "BBB": [10, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            "CCC": [10, 9, 9, 9, 9, 9, 9, 9, 9, 9],
        },
        index=dates,
    )

    result = run_top_n_backtest(
        prices=prices,
        start=dates[3].date(),
        end=dates[-1].date(),
        lookback_days=2,
        max_positions=2,
    )
    summary = calculate_summary(result)

    assert summary["trading_days"] == len(result.snapshots)
    assert summary["ticker_count"] == 3
    assert "AAA" in summary["final_holdings"]


def test_trades_execute_next_open_after_signal_day() -> None:
    dates = pd.date_range("2026-01-01", periods=8, freq="B")
    close_prices = pd.DataFrame(
        {
            "AAA": [10, 11, 12, 13, 14, 15, 16, 17],
            "BBB": [10, 10, 11, 12, 13, 14, 15, 16],
        },
        index=dates,
    )
    open_prices = close_prices * 0.99
    prices = pd.concat({"Open": open_prices, "Close": close_prices}, axis=1)

    result = run_top_n_backtest(
        prices=prices,
        start=dates[3].date(),
        end=dates[-1].date(),
        lookback_days=2,
        max_positions=1,
    )

    assert result.trades
    assert result.trades[0].date == dates[4]
    assert result.trades[0].action == "BUY"


def test_sma_filter_excludes_stock_below_average() -> None:
    dates = pd.date_range("2026-01-01", periods=8, freq="B")
    close_prices = pd.DataFrame(
        {
            "AAA": [10, 20, 30, 40, 50, 40, 30, 20],
            "BBB": [10, 11, 12, 13, 14, 15, 16, 17],
        },
        index=dates,
    )
    open_prices = close_prices
    prices = pd.concat({"Open": open_prices, "Close": close_prices}, axis=1)

    result = run_top_n_backtest(
        prices=prices,
        start=dates[4].date(),
        end=dates[-1].date(),
        lookback_days=2,
        max_positions=1,
        sma_filter_days=3,
    )

    assert result.snapshots[-1].selected == ("BBB",)


def test_top_n_sma_filter_does_not_fill_from_lower_ranks() -> None:
    dates = pd.date_range("2026-01-01", periods=8, freq="B")
    close_prices = pd.DataFrame(
        {
            "AAA": [10, 10, 10, 10, 10, 10, 100, 20],
            "BBB": [10, 11, 12, 13, 14, 15, 16, 17],
            "CCC": [10, 10, 10, 10, 10, 11, 12, 13],
        },
        index=dates,
    )
    prices = pd.concat({"Open": close_prices, "Close": close_prices}, axis=1)

    result = run_top_n_backtest(
        prices=prices,
        start=dates[4].date(),
        end=dates[-1].date(),
        lookback_days=2,
        max_positions=1,
        sma_filter_days=3,
        sma_filter_mode="top_n",
    )

    assert result.snapshots[-1].selected == ()


def test_future_prices_do_not_change_prior_skip_momentum_results() -> None:
    dates = pd.date_range("2026-01-01", periods=12, freq="B")
    close_prices = pd.DataFrame(
        {
            "AAA": [10, 10, 11, 12, 13, 14, 15, 16, 50, 60, 70, 80],
            "BBB": [10, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
            "CCC": [10, 10, 10, 10, 11, 12, 13, 14, 15, 16, 17, 18],
        },
        index=dates,
    )
    base_prices = pd.concat({"Open": close_prices, "Close": close_prices}, axis=1)
    changed_future = base_prices.copy()
    changed_future.loc[dates[9]:, ("Close", "AAA")] = 1000
    changed_future.loc[dates[9]:, ("Open", "AAA")] = 1000

    base_result = run_top_n_backtest(
        prices=base_prices,
        start=dates[4].date(),
        end=dates[-1].date(),
        lookback_days=4,
        max_positions=2,
        score_mode="skip",
        skip_days=1,
    )
    changed_result = run_top_n_backtest(
        prices=changed_future,
        start=dates[4].date(),
        end=dates[-1].date(),
        lookback_days=4,
        max_positions=2,
        score_mode="skip",
        skip_days=1,
    )

    base_prior = [snapshot for snapshot in base_result.snapshots if snapshot.date < dates[9]]
    changed_prior = [snapshot for snapshot in changed_result.snapshots if snapshot.date < dates[9]]
    assert [(s.date, s.holdings, s.selected, s.equity) for s in base_prior] == [
        (s.date, s.holdings, s.selected, s.equity) for s in changed_prior
    ]
    assert [(trade.date, trade.action, trade.ticker) for trade in base_result.trades if trade.date < dates[9]] == [
        (trade.date, trade.action, trade.ticker) for trade in changed_result.trades if trade.date < dates[9]
    ]
