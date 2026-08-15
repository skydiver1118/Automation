from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.compare_universe_topn_monthly import is_month_end_signal
from src.strategy_lab.sp500_top5 import load_or_fetch_prices, momentum_scores


@dataclass(frozen=True)
class Universe:
    name: str
    data_dir: Path
    constituents_file: str
    date_added_column: str | None
    security_column: str
    sector_column: str | None


def pct(value: float) -> str:
    return f"{value:.2%}"


def load_universe_members(universe: Universe) -> pd.DataFrame:
    frame = pd.read_csv(universe.data_dir / universe.constituents_file)
    frame = frame.rename(columns={"Yahoo Symbol": "ticker", universe.security_column: "security"})
    if universe.sector_column and universe.sector_column in frame.columns:
        frame = frame.rename(columns={universe.sector_column: "sector"})
    else:
        frame["sector"] = ""

    if universe.date_added_column and universe.date_added_column in frame.columns:
        frame = frame.rename(columns={universe.date_added_column: "index_date_added"})
        frame["index_date_added_parsed"] = pd.to_datetime(frame["index_date_added"], errors="coerce").dt.date
    else:
        frame["index_date_added"] = ""
        frame["index_date_added_parsed"] = pd.NaT

    return frame[["ticker", "security", "sector", "index_date_added", "index_date_added_parsed"]]


def select_top_eligible(
    scores: pd.Series,
    purchase_date: date,
    top_n: int,
    date_added_by_ticker: dict[str, date],
    enforce_date_added: bool,
) -> tuple[pd.Series, int, str]:
    selected: dict[str, float] = {}
    skipped: list[str] = []

    for ticker, score in scores.items():
        if len(selected) >= top_n:
            break

        if enforce_date_added:
            date_added = date_added_by_ticker.get(str(ticker))
            if date_added is None or date_added > purchase_date:
                skipped.append(str(ticker))
                continue

        selected[str(ticker)] = float(score)

    return pd.Series(selected, dtype=float), len(skipped), ", ".join(skipped[:20])


def max_drawdown(equity: pd.Series) -> float:
    if equity.empty:
        return 0.0
    curve = pd.concat([pd.Series([1.0]), equity.reset_index(drop=True)], ignore_index=True)
    peaks = curve.cummax()
    return float((curve / peaks - 1.0).min())


def run_topn_monthly_o2o(
    prices: pd.DataFrame,
    members: pd.DataFrame,
    universe_name: str,
    top_n: int,
    start: date,
    end: date,
    enforce_date_added: bool,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, object]]:
    close = prices["Close"].dropna(axis=1, thresh=128).sort_index()
    open_prices = prices["Open"].reindex(columns=close.columns).sort_index()
    close = close.loc[(close.index.date >= start) | (close.index < pd.Timestamp(start))]
    close = close.loc[close.index.date <= end]
    open_prices = open_prices.reindex(index=close.index)

    date_added_by_ticker = {
        str(row.ticker): row.index_date_added_parsed
        for row in members.itertuples(index=False)
        if pd.notna(row.ticker) and pd.notna(row.index_date_added_parsed)
    }
    security_by_ticker = {
        str(row.ticker): row.security for row in members.itertuples(index=False) if pd.notna(row.ticker)
    }
    date_added_text_by_ticker = {
        str(row.ticker): row.index_date_added for row in members.itertuples(index=False) if pd.notna(row.ticker)
    }

    strategy = f"{universe_name} Top{top_n}"
    if enforce_date_added:
        strategy += " PIT membership"
    else:
        strategy += " current constituents"

    holdings = pd.Series(dtype=float)
    equity = 1.0
    trade_rows: list[dict[str, object]] = []
    rebalance_rows: list[dict[str, object]] = []
    equity_rows: list[dict[str, object]] = []
    skipped_not_yet_index = 0

    for signal_index in range(126, len(close) - 2):
        entry_index = signal_index + 1
        exit_index = signal_index + 2
        signal_date = close.index[signal_index].date()
        trade_date = close.index[entry_index].date()
        equity_date = close.index[exit_index].date()
        if trade_date < start or trade_date > end:
            continue

        if is_month_end_signal(signal_index, close.index, holdings):
            scores = momentum_scores(close, signal_index, 126, score_mode="skip", skip_days=21)
            selected_scores, skipped_count, skipped_tickers = select_top_eligible(
                scores,
                trade_date,
                top_n,
                date_added_by_ticker,
                enforce_date_added,
            )
            skipped_not_yet_index += skipped_count
            next_holdings = (
                pd.Series(1.0 / len(selected_scores), index=selected_scores.index, dtype=float)
                if len(selected_scores)
                else pd.Series(dtype=float)
            )

            old = set(holdings.index)
            new = set(next_holdings.index)

            for ticker in sorted(old - new):
                trade_rows.append(
                    {
                        "strategy": strategy,
                        "universe": universe_name,
                        "top_n": top_n,
                        "signal_date": signal_date.isoformat(),
                        "trade_date": trade_date.isoformat(),
                        "action": "SELL",
                        "ticker": ticker,
                        "security": security_by_ticker.get(ticker, ""),
                        "index_date_added": date_added_text_by_ticker.get(ticker, ""),
                        "price": float(open_prices.iloc[entry_index][ticker]),
                        "old_weight": float(holdings[ticker]),
                        "new_weight": 0.0,
                        "rank": "",
                        "score": "",
                        "skipped_not_yet_index_before_buy": "",
                        "equity_before_trade": equity,
                    }
                )

            for rank, ticker in enumerate(selected_scores.index, start=1):
                if ticker in old:
                    continue
                trade_rows.append(
                    {
                        "strategy": strategy,
                        "universe": universe_name,
                        "top_n": top_n,
                        "signal_date": signal_date.isoformat(),
                        "trade_date": trade_date.isoformat(),
                        "action": "BUY",
                        "ticker": ticker,
                        "security": security_by_ticker.get(ticker, ""),
                        "index_date_added": date_added_text_by_ticker.get(ticker, ""),
                        "price": float(open_prices.iloc[entry_index][ticker]),
                        "old_weight": 0.0,
                        "new_weight": float(next_holdings[ticker]),
                        "rank": rank,
                        "score": float(selected_scores[ticker]),
                        "skipped_not_yet_index_before_buy": skipped_count,
                        "equity_before_trade": equity,
                    }
                )

            rebalance_rows.append(
                {
                    "strategy": strategy,
                    "universe": universe_name,
                    "top_n": top_n,
                    "signal_date": signal_date.isoformat(),
                    "trade_date": trade_date.isoformat(),
                    "selected": ", ".join(selected_scores.index) if len(selected_scores) else "CASH",
                    "skipped_not_yet_index_count": skipped_count,
                    "first_skipped_tickers": skipped_tickers,
                    "equity_before_rebalance": equity,
                }
            )
            holdings = next_holdings

        one_day_returns = open_prices.iloc[exit_index] / open_prices.iloc[entry_index] - 1.0
        daily_return = 0.0
        for ticker, weight in holdings.items():
            value = one_day_returns.get(ticker)
            if pd.notna(value):
                daily_return += float(weight) * float(value)
        equity *= 1.0 + daily_return
        equity_rows.append(
            {
                "strategy": strategy,
                "universe": universe_name,
                "top_n": top_n,
                "date": equity_date.isoformat(),
                "equity": equity,
                "daily_return": daily_return,
                "holdings": ", ".join(holdings.index) if len(holdings) else "CASH",
            }
        )

    trades = pd.DataFrame(trade_rows)
    rebalances = pd.DataFrame(rebalance_rows)
    equity_curve = pd.DataFrame(equity_rows)

    membership_violations: int | str = "N/A"
    if enforce_date_added:
        membership_violations = 0
        buys = trades[trades["action"] == "BUY"] if not trades.empty else pd.DataFrame()
        if not buys.empty:
            for row in buys.itertuples(index=False):
                added = date_added_by_ticker.get(str(row.ticker))
                trade_day = pd.to_datetime(row.trade_date).date()
                if added is None or trade_day < added:
                    membership_violations += 1

    summary = {
        "universe": universe_name,
        "top_n": top_n,
        "strategy": strategy,
        "membership_filter": "Date added" if enforce_date_added else "Not available/current constituents",
        "strategy_return": equity - 1.0,
        "max_drawdown": max_drawdown(equity_curve["equity"]) if not equity_curve.empty else 0.0,
        "trade_count": len(trades),
        "buy_count": int((trades["action"] == "BUY").sum()) if not trades.empty else 0,
        "sell_count": int((trades["action"] == "SELL").sum()) if not trades.empty else 0,
        "rebalance_count": len(rebalances),
        "skipped_not_yet_index": skipped_not_yet_index,
        "membership_violations": membership_violations,
        "final_holdings": ", ".join(holdings.index) if len(holdings) else "CASH",
    }
    return trades, rebalances, equity_curve, summary


def main() -> None:
    start = date(2020, 1, 1)
    end = date(2026, 5, 17)
    data_start = date(2018, 12, 19)
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    universes = [
        Universe(
            name="S&P 500",
            data_dir=Path("data/sp500_top5"),
            constituents_file="sp500_constituents.csv",
            date_added_column="Date added",
            security_column="Security",
            sector_column="GICS Sector",
        ),
        Universe(
            name="Nasdaq-100",
            data_dir=Path("data/nasdaq100_topn_monthly"),
            constituents_file="nasdaq100_constituents.csv",
            date_added_column=None,
            security_column="Company",
            sector_column="ICB Industry[14]",
        ),
    ]

    _, _, spmo_return = benchmark_return("SPMO", start, end)
    _, _, vgt_return = benchmark_return("VGT", start, end)

    all_trades: list[pd.DataFrame] = []
    all_rebalances: list[pd.DataFrame] = []
    all_equity: list[pd.DataFrame] = []
    summaries: list[dict[str, object]] = []

    for universe in universes:
        members = load_universe_members(universe)
        tickers = members["ticker"].dropna().astype(str).tolist()
        prices = load_or_fetch_prices(
            universe.data_dir / f"adjusted_open_close_{data_start.isoformat()}_{end.isoformat()}.csv",
            tickers,
            data_start,
            end,
            False,
        )
        enforce_date_added = universe.date_added_column is not None

        for top_n in [1, 2, 3]:
            trades, rebalances, equity_curve, summary = run_topn_monthly_o2o(
                prices,
                members,
                universe.name,
                top_n,
                start,
                end,
                enforce_date_added,
            )
            summary["spmo_return"] = spmo_return
            summary["vgt_return"] = vgt_return
            summary["excess_vs_spmo"] = float(summary["strategy_return"]) - spmo_return
            summary["excess_vs_vgt"] = float(summary["strategy_return"]) - vgt_return
            summaries.append(summary)
            all_trades.append(trades)
            all_rebalances.append(rebalances)
            all_equity.append(equity_curve)

    summary_frame = pd.DataFrame(summaries)
    trades_frame = pd.concat(all_trades, ignore_index=True)
    rebalances_frame = pd.concat(all_rebalances, ignore_index=True)
    equity_frame = pd.concat(all_equity, ignore_index=True)
    benchmark_frame = pd.DataFrame(
        [
            {"benchmark": "SPMO", "return": spmo_return},
            {"benchmark": "VGT", "return": vgt_return},
        ]
    )

    base = "top1_top2_top3_sp500_pit_nasdaq100_vs_spmo_vgt_2020_2026ytd"
    xlsx_path = report_dir / f"{base}.xlsx"
    csv_path = report_dir / f"{base}.csv"
    md_path = report_dir / f"{base}.md"
    trades_csv_path = report_dir / f"{base}_trades.csv"
    rebalances_csv_path = report_dir / f"{base}_monthly_decisions.csv"
    equity_csv_path = report_dir / f"{base}_equity_curve.csv"

    summary_frame.to_csv(csv_path, index=False)
    trades_frame.to_csv(trades_csv_path, index=False)
    rebalances_frame.to_csv(rebalances_csv_path, index=False)
    equity_frame.to_csv(equity_csv_path, index=False)

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        summary_frame.to_excel(writer, sheet_name="Summary", index=False)
        benchmark_frame.to_excel(writer, sheet_name="Benchmarks", index=False)
        trades_frame.to_excel(writer, sheet_name="Trades", index=False)
        rebalances_frame.to_excel(writer, sheet_name="Monthly decisions", index=False)
        equity_frame.to_excel(writer, sheet_name="Equity curve", index=False)

        workbook = writer.book
        for worksheet in workbook.worksheets:
            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions
            for column in worksheet.columns:
                max_length = 0
                letter = column[0].column_letter
                for cell in column:
                    value = "" if cell.value is None else str(cell.value)
                    max_length = max(max_length, min(len(value), 45))
                worksheet.column_dimensions[letter].width = max(10, max_length + 2)

    lines = [
        "# Top1/Top2/Top3 Monthly Skip-Momentum Comparison",
        "",
        f"Period: {start.isoformat()} through {end.isoformat()}.",
        "Execution: monthly signal after month-end close, trade at next trading day's open, hold open-to-open.",
        "Ranking: 126 trading-day momentum, skipping the latest 21 trading days.",
        "S&P 500 rule: skip stocks whose `Date added` is after the purchase date, then choose the next eligible ranked stock.",
        "Nasdaq-100 note: the cached Nasdaq-100 constituent table has no add-date field, so Nasdaq-100 rows use current constituents only.",
        "",
        "| Universe | Top N | Membership Filter | Return | Max DD | Trades | Buys | Skipped Future Members | Violations | SPMO | VGT | Excess vs SPMO | Excess vs VGT | Final Holdings |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in summaries:
        lines.append(
            "| "
            f"{row['universe']} | {row['top_n']} | {row['membership_filter']} | "
            f"{pct(float(row['strategy_return']))} | {pct(float(row['max_drawdown']))} | "
            f"{row['trade_count']} | {row['buy_count']} | {row['skipped_not_yet_index']} | "
            f"{row['membership_violations']} | {pct(spmo_return)} | {pct(vgt_return)} | "
            f"{pct(float(row['excess_vs_spmo']))} | {pct(float(row['excess_vs_vgt']))} | "
            f"{row['final_holdings']} |"
        )
    lines.extend(
        [
            "",
            "## Output Files",
            "",
            f"- Excel workbook: `{xlsx_path}`",
            f"- Summary CSV: `{csv_path}`",
            f"- Trades CSV: `{trades_csv_path}`",
            f"- Monthly decisions CSV: `{rebalances_csv_path}`",
            f"- Equity curve CSV: `{equity_csv_path}`",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(md_path)
    for row in summaries:
        print(
            f"{row['universe']} top{row['top_n']}: return={pct(float(row['strategy_return']))}, "
            f"max_dd={pct(float(row['max_drawdown']))}, trades={row['trade_count']}, "
            f"skipped={row['skipped_not_yet_index']}, violations={row['membership_violations']}, "
            f"excess_vs_spmo={pct(float(row['excess_vs_spmo']))}, excess_vs_vgt={pct(float(row['excess_vs_vgt']))}"
        )


if __name__ == "__main__":
    main()
