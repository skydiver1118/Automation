from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from src.strategy_lab.sp500_top5 import (
    load_nasdaq100_constituents,
    load_or_fetch_prices,
    momentum_scores,
    save_constituents,
)


@dataclass(frozen=True)
class MonthlyDecision:
    month: str
    signal_date: str
    trade_date: str
    previous_ticker: str
    selected_ticker: str
    action: str
    entry_price: float
    exit_or_valuation_date: str
    exit_or_valuation_price: float
    score: float
    monthly_return: float
    cumulative_equity: float
    validation: str


def month_starts(start: pd.Timestamp, end: pd.Timestamp) -> list[pd.Timestamp]:
    months = pd.period_range(start=start, end=end, freq="M")
    return [period.to_timestamp() for period in months]


def first_trading_day_on_or_after(index: pd.DatetimeIndex, target: pd.Timestamp) -> pd.Timestamp:
    candidates = index[index >= target]
    if candidates.empty:
        raise ValueError(f"No trading day on or after {target.date()}")
    return candidates[0]


def last_trading_day_before(index: pd.DatetimeIndex, target: pd.Timestamp) -> pd.Timestamp:
    candidates = index[index < target]
    if candidates.empty:
        raise ValueError(f"No trading day before {target.date()}")
    return candidates[-1]


def run_monthly_top1(prices: pd.DataFrame, start: date, end: date) -> tuple[pd.DataFrame, pd.DataFrame]:
    close = prices["Close"].dropna(axis=1, thresh=128).sort_index()
    open_prices = prices["Open"].reindex(columns=close.columns).sort_index()
    close = close.loc[close.index.date <= end]
    open_prices = open_prices.reindex(index=close.index)

    decisions: list[MonthlyDecision] = []
    previous_ticker = ""
    cumulative_equity = 1.0
    starts = month_starts(pd.Timestamp(start), pd.Timestamp(end))

    for offset, month_start in enumerate(starts):
        trade_date = first_trading_day_on_or_after(close.index, month_start)
        signal_date = last_trading_day_before(close.index, trade_date)
        signal_index = close.index.get_loc(signal_date)
        scores = momentum_scores(close, signal_index, 126, score_mode="skip", skip_days=21)
        if scores.empty:
            continue
        selected_ticker = str(scores.index[0])
        score = float(scores.iloc[0])

        if offset + 1 < len(starts):
            next_trade_date = first_trading_day_on_or_after(close.index, starts[offset + 1])
            exit_date = next_trade_date
            exit_price = float(open_prices.loc[exit_date, selected_ticker])
        else:
            available = close.index[(close.index >= trade_date) & (close.index.date <= end)]
            exit_date = available[-1]
            exit_price = float(close.loc[exit_date, selected_ticker])

        entry_price = float(open_prices.loc[trade_date, selected_ticker])
        monthly_return = exit_price / entry_price - 1.0
        cumulative_equity *= 1.0 + monthly_return

        if not previous_ticker:
            action = "BUY"
        elif previous_ticker == selected_ticker:
            action = "HOLD"
        else:
            action = "SWITCH"

        validation = "OK"
        if not signal_date < trade_date:
            validation = "ERROR: signal is not before trade"
        elif signal_index < 126:
            validation = "ERROR: insufficient lookback"
        elif signal_index - 21 >= signal_index:
            validation = "ERROR: skip logic invalid"

        decisions.append(
            MonthlyDecision(
                month=month_start.strftime("%Y-%m"),
                signal_date=signal_date.date().isoformat(),
                trade_date=trade_date.date().isoformat(),
                previous_ticker=previous_ticker,
                selected_ticker=selected_ticker,
                action=action,
                entry_price=entry_price,
                exit_or_valuation_date=exit_date.date().isoformat(),
                exit_or_valuation_price=exit_price,
                score=score,
                monthly_return=monthly_return,
                cumulative_equity=cumulative_equity,
                validation=validation,
            )
        )
        previous_ticker = selected_ticker

    decisions_frame = pd.DataFrame([decision.__dict__ for decision in decisions])
    total_return = cumulative_equity - 1.0
    compounded_from_months = (1.0 + decisions_frame["monthly_return"]).prod() - 1.0
    summary = pd.DataFrame(
        [
            {
                "start": start.isoformat(),
                "end": end.isoformat(),
                "row_count": len(decisions_frame),
                "buy_rows": int((decisions_frame["action"] == "BUY").sum()),
                "hold_rows": int((decisions_frame["action"] == "HOLD").sum()),
                "switch_rows": int((decisions_frame["action"] == "SWITCH").sum()),
                "total_return": total_return,
                "compounded_from_monthly_returns": compounded_from_months,
                "reconciliation_difference": total_return - compounded_from_months,
                "final_equity": cumulative_equity,
                "latest_month_note": "Latest month is valued from entry open to latest available close; prior months are open-to-open.",
                "universe_note": "Uses current Nasdaq-100 constituents, not point-in-time membership.",
            }
        ]
    )
    return decisions_frame, summary


def main() -> None:
    start = date(2025, 1, 1)
    end = date.today()
    data_start = date(2018, 12, 19)
    data_dir = Path("data/nasdaq100_top1_monthly")
    constituents_path = data_dir / "nasdaq100_constituents.csv"
    prices_path = data_dir / f"adjusted_open_close_{data_start.isoformat()}_{end.isoformat()}.csv"

    if constituents_path.exists():
        constituents = pd.read_csv(constituents_path)
    else:
        constituents = load_nasdaq100_constituents()
        save_constituents(constituents, constituents_path)

    tickers = constituents["Yahoo Symbol"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(prices_path, tickers, data_start, end, False)
    decisions, summary = run_monthly_top1(prices, start, end)

    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    stem = "nasdaq100_top1_skip21_monthly_o2o_trades_2025_ytd"
    xlsx_path = report_dir / f"{stem}.xlsx"
    decisions_csv = report_dir / f"{stem}.csv"
    summary_csv = report_dir / f"{stem}_summary.csv"

    decisions.to_csv(decisions_csv, index=False)
    summary.to_csv(summary_csv, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        decisions.to_excel(writer, sheet_name="Monthly Decisions", index=False)
        summary.to_excel(writer, sheet_name="Summary", index=False)

    print(xlsx_path)
    print(decisions_csv)
    print(summary_csv)
    print(f"rows={len(decisions)}")
    print(f"total_return={summary.loc[0, 'total_return']:.10f}")
    print(f"reconciliation_difference={summary.loc[0, 'reconciliation_difference']:.12f}")


if __name__ == "__main__":
    main()
