from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PNL_COLUMNS = (
    "profit",
    "p/l",
    "pl",
    "net profit",
    "net p/l",
    "return",
    "return %",
    "percent return",
    "gain/loss",
    "gain loss",
)


@dataclass(frozen=True)
class BacktestRun:
    label: str
    source_path: Path
    pnl_column: str
    pnls: list[float]


def _normalize_name(name: str) -> str:
    return " ".join(name.strip().lower().replace("_", " ").replace("-", " ").split())


def parse_number(value: str) -> float:
    cleaned = (
        value.strip()
        .replace("$", "")
        .replace(",", "")
        .replace("%", "")
        .replace("(", "-")
        .replace(")", "")
    )
    if not cleaned:
        raise ValueError("empty numeric value")
    return float(cleaned)


def find_pnl_column(fieldnames: Iterable[str]) -> str:
    normalized = {_normalize_name(name): name for name in fieldnames}
    for candidate in PNL_COLUMNS:
        if candidate in normalized:
            return normalized[candidate]
    available = ", ".join(fieldnames)
    expected = ", ".join(PNL_COLUMNS)
    raise ValueError(f"Could not find a P/L column. Expected one of: {expected}. Available: {available}")


def load_backtest_run(path: Path, label: str | None = None) -> BacktestRun:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"{path} has no CSV header row")

        pnl_column = find_pnl_column(reader.fieldnames)
        pnls: list[float] = []
        for row_number, row in enumerate(reader, start=2):
            raw_value = row.get(pnl_column, "")
            try:
                pnls.append(parse_number(raw_value))
            except ValueError as exc:
                raise ValueError(f"Could not parse {pnl_column!r} on row {row_number}: {raw_value!r}") from exc

    if not pnls:
        raise ValueError(f"{path} contains no trades")

    return BacktestRun(
        label=label or path.stem,
        source_path=path,
        pnl_column=pnl_column,
        pnls=pnls,
    )


def load_trade_pnls(path: Path) -> list[float]:
    return load_backtest_run(path).pnls

