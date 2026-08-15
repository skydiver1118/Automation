from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.compare_universe_topn_monthly import is_month_end_signal
from src.strategy_lab.nasdaq100_top1_point_in_time_membership import (
    annualized_sharpe,
    build_current_member_add_dates,
    load_or_fetch_nasdaq100_changes,
    max_drawdown,
    pct,
)
from src.strategy_lab.sp500_top5 import load_or_fetch_prices, momentum_scores


def select_top_eligible(
    scores: pd.Series,
    purchase_date: date,
    top_n: int,
    date_added_by_ticker: dict[str, date],
    enforce_membership_date: bool,
) -> tuple[pd.Series, int, str]:
    selected: dict[str, float] = {}
    skipped: list[str] = []
    for ticker, score in scores.items():
        if len(selected) >= top_n:
            break

        if enforce_membership_date:
            date_added = date_added_by_ticker.get(str(ticker))
            if date_added is not None and date_added > purchase_date:
                skipped.append(str(ticker))
                continue

        selected[str(ticker)] = float(score)

    return pd.Series(selected, dtype=float), len(skipped), ", ".join(skipped[:20])


def run_topn(
    prices: pd.DataFrame,
    members: pd.DataFrame,
    start: date,
    end: date,
    top_n: int,
    enforce_membership_date: bool,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, object]]:
    close = prices["Close"].dropna(axis=1, thresh=128).sort_index()
    open_prices = prices["Open"].reindex(columns=close.columns).sort_index()
    close = close.loc[(close.index.date >= start) | (close.index < pd.Timestamp(start))]
    close = close.loc[close.index.date <= end]
    open_prices = open_prices.reindex(index=close.index)

    date_added_by_ticker = {
        str(row.ticker): row.nasdaq100_date_added
        for row in members.itertuples(index=False)
        if pd.notna(row.ticker) and pd.notna(row.nasdaq100_date_added)
    }
    company_by_ticker = {
        str(row.ticker): row.Company for row in members.itertuples(index=False) if pd.notna(row.ticker)
    }
    date_added_text_by_ticker = {
        str(row.ticker): row.nasdaq100_date_added
        for row in members.itertuples(index=False)
        if pd.notna(row.ticker) and pd.notna(row.nasdaq100_date_added)
    }
    source_by_ticker = {
        str(row.ticker): row.date_source for row in members.itertuples(index=False) if pd.notna(row.ticker)
    }

    strategy = (
        f"Nasdaq-100 Top{top_n} PIT membership"
        if enforce_membership_date
        else f"Nasdaq-100 Top{top_n} current-member baseline"
    )
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
                enforce_membership_date,
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
                        "top_n": top_n,
                        "signal_date": signal_date.isoformat(),
                        "trade_date": trade_date.isoformat(),
                        "action": "SELL",
                        "ticker": ticker,
                        "company": company_by_ticker.get(ticker, ""),
                        "nasdaq100_date_added": date_added_text_by_ticker.get(ticker, ""),
                        "date_source": source_by_ticker.get(ticker, ""),
                        "price": float(open_prices.iloc[entry_index][ticker]),
                        "old_weight": float(holdings[ticker]),
                        "new_weight": 0.0,
                        "rank": "",
                        "score": "",
                        "skipped_not_yet_nasdaq100_before_buy": "",
                        "equity_before_trade": equity,
                    }
                )

            for rank, ticker in enumerate(selected_scores.index, start=1):
                if ticker in old:
                    continue
                trade_rows.append(
                    {
                        "strategy": strategy,
                        "top_n": top_n,
                        "signal_date": signal_date.isoformat(),
                        "trade_date": trade_date.isoformat(),
                        "action": "BUY",
                        "ticker": ticker,
                        "company": company_by_ticker.get(ticker, ""),
                        "nasdaq100_date_added": date_added_text_by_ticker.get(ticker, ""),
                        "date_source": source_by_ticker.get(ticker, ""),
                        "price": float(open_prices.iloc[entry_index][ticker]),
                        "old_weight": 0.0,
                        "new_weight": float(next_holdings[ticker]),
                        "rank": rank,
                        "score": float(selected_scores[ticker]),
                        "skipped_not_yet_nasdaq100_before_buy": skipped_count,
                        "equity_before_trade": equity,
                    }
                )

            rebalance_rows.append(
                {
                    "strategy": strategy,
                    "top_n": top_n,
                    "signal_date": signal_date.isoformat(),
                    "trade_date": trade_date.isoformat(),
                    "selected": ", ".join(selected_scores.index) if len(selected_scores) else "CASH",
                    "skipped_not_yet_nasdaq100_count": skipped_count,
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

    violations = 0
    known_date_buys = 0
    assumed_prewindow_buys = 0
    buys = trades[trades["action"] == "BUY"] if not trades.empty else pd.DataFrame()
    for row in buys.itertuples(index=False):
        trade_day = pd.to_datetime(row.trade_date).date()
        date_added = date_added_by_ticker.get(str(row.ticker))
        if date_added is None:
            assumed_prewindow_buys += 1
            continue
        known_date_buys += 1
        if enforce_membership_date and trade_day < date_added:
            violations += 1

    summary = {
        "strategy": strategy,
        "top_n": top_n,
        "membership_filter": "Nasdaq-100 changes date" if enforce_membership_date else "Current members only",
        "strategy_return": equity - 1.0,
        "max_drawdown": max_drawdown(equity_curve["equity"]),
        "sharpe_ratio": annualized_sharpe(equity_curve["daily_return"]),
        "trade_count": len(trades),
        "buy_count": int((trades["action"] == "BUY").sum()) if not trades.empty else 0,
        "sell_count": int((trades["action"] == "SELL").sum()) if not trades.empty else 0,
        "rebalance_count": len(rebalances),
        "skipped_not_yet_nasdaq100": skipped_not_yet_index,
        "membership_violations": violations,
        "known_date_buys": known_date_buys,
        "assumed_prewindow_buys": assumed_prewindow_buys,
        "final_holdings": ", ".join(holdings.index) if len(holdings) else "CASH",
    }
    return trades, rebalances, equity_curve, summary


def main() -> None:
    start = date(2020, 1, 1)
    end = date(2026, 5, 17)
    data_start = date(2018, 12, 19)
    data_dir = Path("data/nasdaq100_topn_monthly")
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    changes = load_or_fetch_nasdaq100_changes(data_dir / "nasdaq100_changes_wikipedia.csv")
    current_members = pd.read_csv(data_dir / "nasdaq100_constituents.csv")
    members = build_current_member_add_dates(current_members, changes)
    members.to_csv(data_dir / "nasdaq100_constituents_with_add_dates.csv", index=False)

    tickers = members["ticker"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(
        data_dir / f"adjusted_open_close_{data_start.isoformat()}_{end.isoformat()}.csv",
        tickers,
        data_start,
        end,
        False,
    )

    _, _, qqq_return = benchmark_return("QQQ", start, end)
    _, _, vgt_return = benchmark_return("VGT", start, end)

    summaries: list[dict[str, object]] = []
    all_trades: list[pd.DataFrame] = []
    all_rebalances: list[pd.DataFrame] = []
    all_equity: list[pd.DataFrame] = []

    for top_n in [1, 2, 3]:
        for enforce_membership_date in [False, True]:
            trades, rebalances, equity_curve, summary = run_topn(
                prices,
                members,
                start,
                end,
                top_n,
                enforce_membership_date,
            )
            summary["qqq_return"] = qqq_return
            summary["vgt_return"] = vgt_return
            summary["excess_vs_qqq"] = float(summary["strategy_return"]) - qqq_return
            summary["excess_vs_vgt"] = float(summary["strategy_return"]) - vgt_return
            summaries.append(summary)
            all_trades.append(trades)
            all_rebalances.append(rebalances)
            all_equity.append(equity_curve)

    summary_frame = pd.DataFrame(summaries)
    trades_frame = pd.concat(all_trades, ignore_index=True)
    rebalances_frame = pd.concat(all_rebalances, ignore_index=True)
    equity_frame = pd.concat(all_equity, ignore_index=True)
    add_dates_frame = members[
        ["ticker", "Company", "nasdaq100_date_added", "date_source", "nasdaq100_added_security"]
    ].sort_values(["nasdaq100_date_added", "ticker"], na_position="first")

    base = "nasdaq100_top1_top2_top3_point_in_time_membership_2020_2026ytd"
    xlsx_path = report_dir / f"{base}.xlsx"
    md_path = report_dir / f"{base}.md"
    summary_csv_path = report_dir / f"{base}_summary.csv"
    trades_csv_path = report_dir / f"{base}_trades.csv"
    rebalances_csv_path = report_dir / f"{base}_monthly_decisions.csv"
    equity_csv_path = report_dir / f"{base}_equity_curve.csv"

    summary_frame.to_csv(summary_csv_path, index=False)
    trades_frame.to_csv(trades_csv_path, index=False)
    rebalances_frame.to_csv(rebalances_csv_path, index=False)
    equity_frame.to_csv(equity_csv_path, index=False)

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        summary_frame.to_excel(writer, sheet_name="Summary", index=False)
        trades_frame.to_excel(writer, sheet_name="Trades", index=False)
        rebalances_frame.to_excel(writer, sheet_name="Monthly decisions", index=False)
        equity_frame.to_excel(writer, sheet_name="Equity curve", index=False)
        add_dates_frame.to_excel(writer, sheet_name="Add date cache", index=False)

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
        "# Nasdaq-100 Top1/Top2/Top3 Point-in-Time Membership Backtest",
        "",
        f"Period: {start.isoformat()} through {end.isoformat()}.",
        "Execution: monthly signal after month-end close, trade next trading day's open, hold open-to-open.",
        "Ranking: 126 trading-day momentum, skipping the latest 21 trading days.",
        "Point-in-time rule: fill each Top N slot by walking down the rank list and skipping stocks with known Nasdaq-100 add dates after the purchase date.",
        "Add-date source: Wikipedia Nasdaq-100 changes table, cached locally.",
        "",
        "| Top N | Strategy | Return | Max DD | Sharpe | Trades | Buys | Skipped Future Members | Violations | Known-Date Buys | Assumed Pre-window Buys | QQQ | VGT | Final Holdings |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in summaries:
        lines.append(
            "| "
            f"{row['top_n']} | {row['membership_filter']} | {pct(float(row['strategy_return']))} | "
            f"{pct(float(row['max_drawdown']))} | {float(row['sharpe_ratio']):.2f} | "
            f"{row['trade_count']} | {row['buy_count']} | {row['skipped_not_yet_nasdaq100']} | "
            f"{row['membership_violations']} | {row['known_date_buys']} | {row['assumed_prewindow_buys']} | "
            f"{pct(qqq_return)} | {pct(vgt_return)} | {row['final_holdings']} |"
        )
    lines.extend(
        [
            "",
            "Important limitation: this uses today's Nasdaq-100 constituents plus the changes table to prevent buying known future additions. It still does not add historical members that were later removed.",
            "",
            "## Output Files",
            "",
            f"- Excel workbook: `{xlsx_path}`",
            f"- Summary CSV: `{summary_csv_path}`",
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
            f"Top{row['top_n']} {row['membership_filter']}: return={pct(float(row['strategy_return']))}, "
            f"max_dd={pct(float(row['max_drawdown']))}, sharpe={float(row['sharpe_ratio']):.2f}, "
            f"trades={row['trade_count']}, skipped={row['skipped_not_yet_nasdaq100']}, "
            f"violations={row['membership_violations']}"
        )


if __name__ == "__main__":
    main()
