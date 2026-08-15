from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Iterable


@dataclass(frozen=True)
class BacktestMetrics:
    trades: int
    wins: int
    losses: int
    win_rate: float
    total_pnl: float
    average_pnl: float
    profit_factor: float | None
    max_drawdown: float
    expectancy: float

    def as_row(self) -> dict[str, int | float | str]:
        row = asdict(self)
        row["profit_factor"] = "" if self.profit_factor is None else self.profit_factor
        return row


def max_drawdown(values: Iterable[float]) -> float:
    equity = 0.0
    peak = 0.0
    worst = 0.0
    for value in values:
        equity += value
        peak = max(peak, equity)
        worst = min(worst, equity - peak)
    return worst


def calculate_metrics(pnls: list[float]) -> BacktestMetrics:
    if not pnls:
        raise ValueError("Cannot calculate metrics for an empty trade list")

    wins = [value for value in pnls if value > 0]
    losses = [value for value in pnls if value < 0]
    gross_loss = abs(sum(losses))
    profit_factor = None if math.isclose(gross_loss, 0.0) else sum(wins) / gross_loss

    return BacktestMetrics(
        trades=len(pnls),
        wins=len(wins),
        losses=len(losses),
        win_rate=len(wins) / len(pnls),
        total_pnl=sum(pnls),
        average_pnl=sum(pnls) / len(pnls),
        profit_factor=profit_factor,
        max_drawdown=max_drawdown(pnls),
        expectancy=sum(pnls) / len(pnls),
    )

