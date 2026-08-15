from __future__ import annotations

import argparse
import csv
import math
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path

import pandas as pd


EXPECTED_MONTHLY_SEQUENCE = [
    ("2025-01", "APP", "BUY"),
    ("2025-02", "APP", "HOLD"),
    ("2025-03", "APP", "HOLD"),
    ("2025-04", "APP", "HOLD"),
    ("2025-05", "PLTR", "SWITCH"),
    ("2025-06", "PLTR", "HOLD"),
    ("2025-07", "PLTR", "HOLD"),
    ("2025-08", "PLTR", "HOLD"),
    ("2025-09", "PLTR", "HOLD"),
    ("2025-10", "WDC", "SWITCH"),
    ("2025-11", "SNDK", "SWITCH"),
    ("2025-12", "SNDK", "HOLD"),
    ("2026-01", "SNDK", "HOLD"),
    ("2026-02", "SNDK", "HOLD"),
    ("2026-03", "SNDK", "HOLD"),
    ("2026-04", "SNDK", "HOLD"),
    ("2026-05", "SNDK", "HOLD"),
]


@dataclass(frozen=True)
class DecisionRow:
    month: str
    signal_date: str
    trade_date: str
    previous_ticker: str
    selected_ticker: str
    action: str
    score_close_date: str
    lookback_close_date: str
    score: float
    entry_price: float
    exit_or_valuation_date: str
    exit_or_valuation_price: float
    monthly_return: float
    cumulative_equity: float
    no_lookahead_check: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Independent replication of the Nasdaq-100 top-1 monthly skip-momentum strategy."
    )
    parser.add_argument("--start", default="2025-01-01")
    parser.add_argument("--end", default="2026-05-15")
    parser.add_argument(
        "--prices",
        default="data/nasdaq100_top1_monthly/adjusted_open_close_2018-12-19_2026-05-15.csv",
        help="CSV with MultiIndex columns: first level Open/Close, second level ticker.",
    )
    parser.add_argument(
        "--output-prefix",
        default="reports/independent_nasdaq100_top1_skip21_monthly_o2o_validation",
    )
    return parser.parse_args()


def read_prices(path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    prices = pd.read_csv(path, index_col=0, header=[0, 1], parse_dates=True)
    prices = prices.sort_index()
    if "Open" not in prices.columns.get_level_values(0) or "Close" not in prices.columns.get_level_values(0):
        raise ValueError("Price file must contain Open and Close column groups")

    open_prices = prices["Open"].apply(pd.to_numeric, errors="coerce")
    close_prices = prices["Close"].apply(pd.to_numeric, errors="coerce")
    usable = close_prices.columns[close_prices.notna().sum() >= 128]
    open_prices = open_prices.reindex(columns=usable)
    close_prices = close_prices.reindex(columns=usable)
    return open_prices, close_prices


def first_trading_day_on_or_after(dates: pd.DatetimeIndex, target: pd.Timestamp) -> pd.Timestamp:
    candidates = dates[dates >= target]
    if candidates.empty:
        raise ValueError(f"No trading day on or after {target.date()}")
    return candidates[0]


def last_trading_day_before(dates: pd.DatetimeIndex, target: pd.Timestamp) -> pd.Timestamp:
    candidates = dates[dates < target]
    if candidates.empty:
        raise ValueError(f"No trading day before {target.date()}")
    return candidates[-1]


def month_starts(start: date, end: date) -> list[pd.Timestamp]:
    return [period.to_timestamp() for period in pd.period_range(start=start, end=end, freq="M")]


def score_universe(close_prices: pd.DataFrame, signal_index: int, lookback_days: int, skip_days: int) -> pd.Series:
    if signal_index < lookback_days:
        return pd.Series(dtype=float)
    if skip_days >= lookback_days:
        raise ValueError("skip_days must be smaller than lookback_days")

    score_index = signal_index - skip_days
    scores = close_prices.iloc[score_index] / close_prices.iloc[signal_index - lookback_days] - 1.0
    scores = scores.replace([math.inf, -math.inf], pd.NA).dropna()
    return scores.sort_values(ascending=False)


def no_lookahead_status(
    signal_date: pd.Timestamp,
    trade_date: pd.Timestamp,
    score_close_date: pd.Timestamp,
    lookback_close_date: pd.Timestamp,
) -> str:
    checks = [
        signal_date < trade_date,
        score_close_date <= signal_date,
        lookback_close_date <= signal_date,
        lookback_close_date < score_close_date,
    ]
    return "OK" if all(checks) else "ERROR"


def run_strategy(
    open_prices: pd.DataFrame,
    close_prices: pd.DataFrame,
    start: date,
    end: date,
    lookback_days: int = 126,
    skip_days: int = 21,
) -> pd.DataFrame:
    close_prices = close_prices.loc[close_prices.index.date <= end].copy()
    open_prices = open_prices.reindex(index=close_prices.index, columns=close_prices.columns)

    rows: list[DecisionRow] = []
    previous_ticker = ""
    cumulative_equity = 1.0
    starts = month_starts(start, end)

    for month_offset, month_start in enumerate(starts):
        trade_date = first_trading_day_on_or_after(close_prices.index, month_start)
        signal_date = last_trading_day_before(close_prices.index, trade_date)
        signal_index = close_prices.index.get_loc(signal_date)
        scores = score_universe(close_prices, signal_index, lookback_days, skip_days)
        if scores.empty:
            continue

        selected_ticker = str(scores.index[0])
        entry_price = float(open_prices.loc[trade_date, selected_ticker])
        if not math.isfinite(entry_price):
            raise ValueError(f"Missing entry open for {selected_ticker} on {trade_date.date()}")

        if month_offset + 1 < len(starts):
            exit_date = first_trading_day_on_or_after(close_prices.index, starts[month_offset + 1])
            exit_or_valuation_price = float(open_prices.loc[exit_date, selected_ticker])
        else:
            available = close_prices.index[(close_prices.index >= trade_date) & (close_prices.index.date <= end)]
            exit_date = available[-1]
            exit_or_valuation_price = float(close_prices.loc[exit_date, selected_ticker])

        monthly_return = exit_or_valuation_price / entry_price - 1.0
        cumulative_equity *= 1.0 + monthly_return
        action = "BUY" if not previous_ticker else "HOLD" if previous_ticker == selected_ticker else "SWITCH"

        score_close_date = close_prices.index[signal_index - skip_days]
        lookback_close_date = close_prices.index[signal_index - lookback_days]
        rows.append(
            DecisionRow(
                month=month_start.strftime("%Y-%m"),
                signal_date=signal_date.date().isoformat(),
                trade_date=trade_date.date().isoformat(),
                previous_ticker=previous_ticker,
                selected_ticker=selected_ticker,
                action=action,
                score_close_date=score_close_date.date().isoformat(),
                lookback_close_date=lookback_close_date.date().isoformat(),
                score=float(scores.iloc[0]),
                entry_price=entry_price,
                exit_or_valuation_date=exit_date.date().isoformat(),
                exit_or_valuation_price=exit_or_valuation_price,
                monthly_return=monthly_return,
                cumulative_equity=cumulative_equity,
                no_lookahead_check=no_lookahead_status(signal_date, trade_date, score_close_date, lookback_close_date),
            )
        )
        previous_ticker = selected_ticker

    return pd.DataFrame([asdict(row) for row in rows])


def write_reports(decisions: pd.DataFrame, output_prefix: Path, start: date, end: date) -> None:
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    csv_path = output_prefix.with_suffix(".csv")
    summary_path = output_prefix.with_name(output_prefix.name + "_summary.csv")
    md_path = output_prefix.with_suffix(".md")

    decisions.to_csv(csv_path, index=False)
    total_return = float(decisions["cumulative_equity"].iloc[-1] - 1.0)
    compounded = float((1.0 + decisions["monthly_return"]).prod() - 1.0)
    expected_frame = pd.DataFrame(EXPECTED_MONTHLY_SEQUENCE, columns=["month", "selected_ticker", "action"])
    compare_frame = decisions[["month", "selected_ticker", "action"]].merge(
        expected_frame,
        on="month",
        suffixes=("_actual", "_expected"),
        how="outer",
    )
    sequence_matches = bool(
        (
            (compare_frame["selected_ticker_actual"] == compare_frame["selected_ticker_expected"])
            & (compare_frame["action_actual"] == compare_frame["action_expected"])
        ).all()
    )

    summary = {
        "start": start.isoformat(),
        "end": end.isoformat(),
        "row_count": len(decisions),
        "buy_rows": int((decisions["action"] == "BUY").sum()),
        "hold_rows": int((decisions["action"] == "HOLD").sum()),
        "switch_rows": int((decisions["action"] == "SWITCH").sum()),
        "total_return": total_return,
        "final_equity": float(decisions["cumulative_equity"].iloc[-1]),
        "compounded_from_monthly_returns": compounded,
        "reconciliation_difference": total_return - compounded,
        "all_no_lookahead_checks_ok": bool((decisions["no_lookahead_check"] == "OK").all()),
        "pdf_sequence_matches": sequence_matches,
    }
    with summary_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

    lines = [
        "# Independent Nasdaq-100 Top-1 Monthly Skip-Momentum Validation",
        "",
        "Rules replicated: current Nasdaq-100 price file, top 1 stock, monthly rebalance, score = Close[t-21 trading days] / Close[t-126 trading days] - 1, signal after the prior month-end close, execute at the next trading day open.",
        "",
        "No-lookahead guard: every row requires the signal close, skipped score close, and lookback close to be dated before the trade open. Completed months are measured open-to-open; the final partial month is valued from entry open to the latest available close.",
        "",
        f"- Window: {start.isoformat()} through {end.isoformat()}",
        f"- Rows: {summary['row_count']}",
        f"- Actions: BUY {summary['buy_rows']}, SWITCH {summary['switch_rows']}, HOLD {summary['hold_rows']}",
        f"- Total return: {total_return:.2%}",
        f"- Final equity: {summary['final_equity']:.6f}x",
        f"- Reconciliation difference: {summary['reconciliation_difference']:.12f}",
        f"- No-lookahead checks: {'OK' if summary['all_no_lookahead_checks_ok'] else 'FAILED'}",
        f"- PDF decision sequence match: {'YES' if sequence_matches else 'NO'}",
        "",
        "| Month | Signal | Trade | Selected | Action | Score Close | Lookback Close | Return | Equity |",
        "| --- | --- | --- | --- | --- | --- | --- | ---: | ---: |",
    ]
    for row in decisions.itertuples(index=False):
        lines.append(
            f"| {row.month} | {row.signal_date} | {row.trade_date} | {row.selected_ticker} | "
            f"{row.action} | {row.score_close_date} | {row.lookback_close_date} | "
            f"{row.monthly_return:.2%} | {row.cumulative_equity:.6f} |"
        )
    lines.extend(
        [
            "",
            "Caveat: this validates the price-timing logic and reproduced PDF numbers, but it still uses the current Nasdaq-100 constituent list for historical dates. A stricter investment-grade test needs point-in-time index membership and independent corporate-action verification.",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    start = date.fromisoformat(args.start)
    end = date.fromisoformat(args.end)
    open_prices, close_prices = read_prices(Path(args.prices))
    decisions = run_strategy(open_prices, close_prices, start, end)
    write_reports(decisions, Path(args.output_prefix), start, end)
    print(f"rows={len(decisions)}")
    print(f"total_return={decisions['cumulative_equity'].iloc[-1] - 1.0:.10f}")
    print(f"final_equity={decisions['cumulative_equity'].iloc[-1]:.10f}")
    print(f"all_no_lookahead_checks_ok={(decisions['no_lookahead_check'] == 'OK').all()}")


if __name__ == "__main__":
    main()
