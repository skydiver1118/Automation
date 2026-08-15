from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from src.strategy_lab.metrics import BacktestMetrics, calculate_metrics
from src.strategy_lab.trendspider import BacktestRun


@dataclass(frozen=True)
class AnalyzedRun:
    run: BacktestRun
    metrics: BacktestMetrics


def analyze_run(run: BacktestRun) -> AnalyzedRun:
    return AnalyzedRun(run=run, metrics=calculate_metrics(run.pnls))


def format_metrics(metrics: BacktestMetrics) -> str:
    profit_factor = "n/a" if metrics.profit_factor is None else f"{metrics.profit_factor:.2f}"
    return "\n".join(
        (
            f"Trades: {metrics.trades}",
            f"Wins: {metrics.wins}",
            f"Losses: {metrics.losses}",
            f"Win rate: {metrics.win_rate:.2%}",
            f"Total P/L: {metrics.total_pnl:.2f}",
            f"Average P/L: {metrics.average_pnl:.2f}",
            f"Profit factor: {profit_factor}",
            f"Max drawdown: {metrics.max_drawdown:.2f}",
            f"Expectancy: {metrics.expectancy:.2f}",
        )
    )


def write_comparison_csv(runs: list[AnalyzedRun], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "label",
        "source_file",
        "pnl_column",
        "trades",
        "wins",
        "losses",
        "win_rate",
        "total_pnl",
        "average_pnl",
        "profit_factor",
        "max_drawdown",
        "expectancy",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for analyzed in runs:
            row = {
                "label": analyzed.run.label,
                "source_file": str(analyzed.run.source_path),
                "pnl_column": analyzed.run.pnl_column,
            }
            row.update(analyzed.metrics.as_row())
            writer.writerow(row)


def write_markdown_report(runs: list[AnalyzedRun], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Backtest Comparison",
        "",
        "| Run | Trades | Win Rate | Total P/L | Profit Factor | Max Drawdown | Expectancy |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for analyzed in sorted(runs, key=lambda item: item.metrics.total_pnl, reverse=True):
        metrics = analyzed.metrics
        profit_factor = "" if metrics.profit_factor is None else f"{metrics.profit_factor:.2f}"
        lines.append(
            "| "
            f"{analyzed.run.label} | "
            f"{metrics.trades} | "
            f"{metrics.win_rate:.2%} | "
            f"{metrics.total_pnl:.2f} | "
            f"{profit_factor} | "
            f"{metrics.max_drawdown:.2f} | "
            f"{metrics.expectancy:.2f} |"
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")

