from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.sp500_top5 import load_or_fetch_prices, momentum_scores


@dataclass(frozen=True)
class Period:
    name: str
    start: date
    end: date


def is_month_end_signal(index: int, dates: pd.DatetimeIndex, holdings: pd.Series) -> bool:
    next_index = min(index + 1, len(dates) - 1)
    return (
        holdings.empty
        or index >= len(dates) - 2
        or dates[next_index].month != dates[index].month
        or dates[next_index].year != dates[index].year
    )


def run_period(prices: pd.DataFrame, period: Period) -> tuple[list[dict[str, object]], dict[str, object]]:
    close = prices["Close"].dropna(axis=1, thresh=128).sort_index()
    open_prices = prices["Open"].reindex(columns=close.columns).sort_index()
    close = close.loc[(close.index.date >= period.start) | (close.index < pd.Timestamp(period.start))]
    close = close.loc[close.index.date <= period.end]
    open_prices = open_prices.reindex(index=close.index)

    holdings = pd.Series(dtype=float)
    equity = 1.0
    peak = 1.0
    max_drawdown = 0.0
    trade_rows: list[dict[str, object]] = []
    first_entry_date = ""
    last_exit_date = ""

    for signal_index in range(126, len(close) - 2):
        entry_index = signal_index + 1
        exit_index = signal_index + 2
        signal_date = close.index[signal_index].date()
        trade_date = close.index[entry_index].date()
        exit_date = close.index[exit_index].date()
        if trade_date < period.start or trade_date > period.end:
            continue

        if is_month_end_signal(signal_index, close.index, holdings):
            scores = momentum_scores(close, signal_index, 126, score_mode="skip", skip_days=21)
            selected = scores.head(2)
            next_holdings = pd.Series(0.5, index=selected.index, dtype=float)
            old = set(holdings.index)
            new = set(next_holdings.index)

            for ticker in sorted(old - new):
                trade_rows.append(
                    {
                        "period": period.name,
                        "signal_date": signal_date.isoformat(),
                        "trade_date": trade_date.isoformat(),
                        "action": "SELL",
                        "ticker": ticker,
                        "price": float(open_prices.loc[close.index[entry_index], ticker]),
                        "old_weight": float(holdings[ticker]),
                        "new_weight": 0.0,
                        "score": "",
                        "rank": "",
                        "equity_before_trade": equity,
                    }
                )
            for rank, ticker in enumerate(selected.index, start=1):
                if ticker in old:
                    continue
                trade_rows.append(
                    {
                        "period": period.name,
                        "signal_date": signal_date.isoformat(),
                        "trade_date": trade_date.isoformat(),
                        "action": "BUY",
                        "ticker": ticker,
                        "price": float(open_prices.loc[close.index[entry_index], ticker]),
                        "old_weight": 0.0,
                        "new_weight": float(next_holdings[ticker]),
                        "score": float(selected[ticker]),
                        "rank": rank,
                        "equity_before_trade": equity,
                    }
                )

            holdings = next_holdings
            if not first_entry_date and not holdings.empty:
                first_entry_date = trade_date.isoformat()

        one_day_returns = open_prices.iloc[exit_index] / open_prices.iloc[entry_index] - 1.0
        daily_return = 0.0
        for ticker, weight in holdings.items():
            value = one_day_returns.get(ticker)
            if pd.notna(value):
                daily_return += float(weight) * float(value)
        equity *= 1.0 + daily_return
        peak = max(peak, equity)
        max_drawdown = min(max_drawdown, equity / peak - 1.0)
        last_exit_date = exit_date.isoformat()

    _, _, spmo_return = benchmark_return("SPMO", period.start, period.end)
    summary = {
        "period": period.name,
        "requested_start": period.start.isoformat(),
        "requested_end": period.end.isoformat(),
        "actual_start": first_entry_date,
        "actual_end": last_exit_date,
        "strategy_return": equity - 1.0,
        "max_drawdown": max_drawdown,
        "trade_count": len(trade_rows),
        "buy_count": len([row for row in trade_rows if row["action"] == "BUY"]),
        "sell_count": len([row for row in trade_rows if row["action"] == "SELL"]),
        "spmo_return": spmo_return,
        "excess_vs_spmo": equity - 1.0 - spmo_return,
        "final_holdings": ", ".join(holdings.index),
    }
    return trade_rows, summary


def main() -> None:
    data_start = date(2018, 12, 19)
    end = date(2026, 5, 15)
    data_dir = Path("data/sp500_top5")
    tickers = pd.read_csv(data_dir / "sp500_constituents.csv")["Yahoo Symbol"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(
        data_dir / f"adjusted_open_close_{data_start.isoformat()}_{end.isoformat()}.csv",
        tickers,
        data_start,
        end,
        False,
    )
    periods = [Period(str(year), date(year, 1, 1), date(year, 12, 31)) for year in range(2020, 2026)]
    periods.append(Period("2026 YTD", date(2026, 1, 1), end))

    trades: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []
    for period in periods:
        period_trades, summary = run_period(prices, period)
        trades.extend(period_trades)
        summaries.append(summary)

    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)
    xlsx_path = report_dir / "top2_skip21_monthly_o2o_trades_2020_2026ytd.xlsx"
    csv_path = report_dir / "top2_skip21_monthly_o2o_trades_2020_2026ytd.csv"
    summary_csv_path = report_dir / "top2_skip21_monthly_o2o_trade_summary_2020_2026ytd.csv"

    trades_frame = pd.DataFrame(trades)
    summary_frame = pd.DataFrame(summaries)
    trades_frame.to_csv(csv_path, index=False)
    summary_frame.to_csv(summary_csv_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        trades_frame.to_excel(writer, sheet_name="Trades", index=False)
        summary_frame.to_excel(writer, sheet_name="Summary", index=False)

    print(xlsx_path)
    print(csv_path)
    print(summary_csv_path)
    print(f"trades={len(trades_frame)}")


if __name__ == "__main__":
    main()
