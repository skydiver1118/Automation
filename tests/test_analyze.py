from pathlib import Path

from src.strategy_lab.analyze import calculate_metrics, load_trade_pnls
from src.strategy_lab.reporting import analyze_run
from src.strategy_lab.trendspider import load_backtest_run


def test_load_trade_pnls() -> None:
    pnls = load_trade_pnls(Path("tests/fixtures/sample_trades.csv"))

    assert pnls == [100.0, -40.0, 60.0]


def test_calculate_metrics() -> None:
    metrics = calculate_metrics([100.0, -40.0, 60.0])

    assert metrics.trades == 3
    assert metrics.wins == 2
    assert metrics.losses == 1
    assert metrics.win_rate == 2 / 3
    assert metrics.total_pnl == 120.0
    assert metrics.average_pnl == 40.0
    assert metrics.profit_factor == 4.0
    assert metrics.max_drawdown == -40.0
    assert metrics.expectancy == 40.0


def test_load_backtest_run_uses_file_stem_as_label() -> None:
    run = load_backtest_run(Path("tests/fixtures/sample_trades.csv"))

    assert run.label == "sample_trades"
    assert run.pnl_column == "Profit"
    assert run.pnls == [100.0, -40.0, 60.0]


def test_analyze_run() -> None:
    run = load_backtest_run(Path("tests/fixtures/sample_trades.csv"), label="baseline")
    analyzed = analyze_run(run)

    assert analyzed.run.label == "baseline"
    assert analyzed.metrics.total_pnl == 120.0
