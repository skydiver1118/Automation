from __future__ import annotations

from datetime import date
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.compare_universe_topn_monthly import is_month_end_signal
from src.strategy_lab.sp500_top5 import load_or_fetch_prices, momentum_scores


NASDAQ100_WIKI_URL = "https://en.wikipedia.org/wiki/Nasdaq-100"


def pct(value: float) -> str:
    return f"{value:.2%}"


def annualized_sharpe(daily_returns: pd.Series) -> float:
    returns = daily_returns.dropna()
    if returns.empty:
        return 0.0
    std = returns.std(ddof=1)
    if std == 0 or pd.isna(std):
        return 0.0
    return float((returns.mean() / std) * (252 ** 0.5))


def max_drawdown(equity: pd.Series) -> float:
    if equity.empty:
        return 0.0
    curve = pd.concat([pd.Series([1.0]), equity.reset_index(drop=True)], ignore_index=True)
    peaks = curve.cummax()
    return float((curve / peaks - 1.0).min())


def yahoo_symbol(symbol: str) -> str:
    return symbol.replace(".", "-")


def load_or_fetch_nasdaq100_changes(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)

    response = requests.get(
        NASDAQ100_WIKI_URL,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        timeout=30,
    )
    response.raise_for_status()
    tables = pd.read_html(StringIO(response.text))
    changes = None
    for table in tables:
        flat_columns = [
            " ".join([str(part) for part in column if str(part) != "nan"]).strip()
            if isinstance(column, tuple)
            else str(column)
            for column in table.columns
        ]
        table = table.copy()
        table.columns = flat_columns
        if {"Date Date", "Added Ticker", "Added Security", "Removed Ticker"}.issubset(table.columns):
            changes = table
            break
    if changes is None:
        raise RuntimeError("Could not find Nasdaq-100 changes table on Wikipedia")

    changes = changes.rename(
        columns={
            "Date Date": "date",
            "Added Ticker": "added_ticker",
            "Added Security": "added_security",
            "Removed Ticker": "removed_ticker",
            "Removed Security": "removed_security",
            "Reason Reason": "reason",
        }
    )
    changes["date"] = pd.to_datetime(changes["date"], errors="coerce").dt.date
    changes["added_yahoo_symbol"] = changes["added_ticker"].dropna().astype(str).map(yahoo_symbol)
    path.parent.mkdir(parents=True, exist_ok=True)
    changes.to_csv(path, index=False)
    return changes


def build_current_member_add_dates(current_members: pd.DataFrame, changes: pd.DataFrame) -> pd.DataFrame:
    additions = changes.dropna(subset=["date", "added_yahoo_symbol"]).copy()
    additions["date"] = pd.to_datetime(additions["date"]).dt.date
    additions = additions.sort_values("date", ascending=False)
    latest_add_by_ticker = additions.drop_duplicates("added_yahoo_symbol", keep="first").set_index(
        "added_yahoo_symbol"
    )

    members = current_members.copy()
    members["ticker"] = members["Yahoo Symbol"].astype(str)
    members["nasdaq100_date_added"] = members["ticker"].map(latest_add_by_ticker["date"])
    members["nasdaq100_added_security"] = members["ticker"].map(latest_add_by_ticker["added_security"])
    members["date_source"] = members["nasdaq100_date_added"].apply(
        lambda value: "Wikipedia Nasdaq-100 changes table" if pd.notna(value) else "No add date found; assumed already member before test window"
    )
    return members


def pick_top_eligible(
    scores: pd.Series,
    purchase_date: date,
    date_added_by_ticker: dict[str, date],
) -> tuple[str | None, float | None, int, str]:
    skipped: list[str] = []
    for ticker, score in scores.items():
        date_added = date_added_by_ticker.get(str(ticker))
        if date_added is None or date_added <= purchase_date:
            return str(ticker), float(score), len(skipped), ", ".join(skipped[:20])
        skipped.append(str(ticker))
    return None, None, len(skipped), ", ".join(skipped[:20])


def run_top1(
    prices: pd.DataFrame,
    members: pd.DataFrame,
    start: date,
    end: date,
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

    strategy = "Nasdaq-100 Top1 PIT membership" if enforce_membership_date else "Nasdaq-100 Top1 current-member baseline"
    holding: str | None = None
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

        current_holdings = pd.Series(dtype=float) if holding is None else pd.Series([1.0], index=[holding])
        if is_month_end_signal(signal_index, close.index, current_holdings):
            scores = momentum_scores(close, signal_index, 126, score_mode="skip", skip_days=21)
            if enforce_membership_date:
                selected, selected_score, skipped_count, skipped_tickers = pick_top_eligible(
                    scores, trade_date, date_added_by_ticker
                )
            else:
                selected = str(scores.index[0]) if len(scores) else None
                selected_score = float(scores.iloc[0]) if len(scores) else None
                skipped_count = 0
                skipped_tickers = ""
            skipped_not_yet_index += skipped_count

            rebalance_rows.append(
                {
                    "strategy": strategy,
                    "signal_date": signal_date.isoformat(),
                    "trade_date": trade_date.isoformat(),
                    "selected_ticker": selected or "CASH",
                    "selected_company": company_by_ticker.get(selected or "", ""),
                    "selected_score": selected_score if selected_score is not None else "",
                    "nasdaq100_date_added": date_added_text_by_ticker.get(selected or "", ""),
                    "date_source": source_by_ticker.get(selected or "", ""),
                    "skipped_not_yet_nasdaq100_count": skipped_count,
                    "first_skipped_tickers": skipped_tickers,
                    "prior_holding": holding or "CASH",
                    "equity_before_rebalance": equity,
                }
            )

            if holding != selected:
                if holding is not None:
                    trade_rows.append(
                        {
                            "strategy": strategy,
                            "signal_date": signal_date.isoformat(),
                            "trade_date": trade_date.isoformat(),
                            "action": "SELL",
                            "ticker": holding,
                            "company": company_by_ticker.get(holding, ""),
                            "nasdaq100_date_added": date_added_text_by_ticker.get(holding, ""),
                            "date_source": source_by_ticker.get(holding, ""),
                            "price": float(open_prices.iloc[entry_index][holding]),
                            "score": "",
                            "skipped_not_yet_nasdaq100_before_buy": "",
                            "equity_before_trade": equity,
                        }
                    )
                if selected is not None:
                    trade_rows.append(
                        {
                            "strategy": strategy,
                            "signal_date": signal_date.isoformat(),
                            "trade_date": trade_date.isoformat(),
                            "action": "BUY",
                            "ticker": selected,
                            "company": company_by_ticker.get(selected, ""),
                            "nasdaq100_date_added": date_added_text_by_ticker.get(selected, ""),
                            "date_source": source_by_ticker.get(selected, ""),
                            "price": float(open_prices.iloc[entry_index][selected]),
                            "score": selected_score,
                            "skipped_not_yet_nasdaq100_before_buy": skipped_count,
                            "equity_before_trade": equity,
                        }
                    )
                holding = selected

        daily_return = 0.0
        if holding is not None:
            value = open_prices.iloc[exit_index][holding] / open_prices.iloc[entry_index][holding] - 1.0
            if pd.notna(value):
                daily_return = float(value)
        equity *= 1.0 + daily_return
        equity_rows.append(
            {
                "strategy": strategy,
                "date": equity_date.isoformat(),
                "equity": equity,
                "daily_return": daily_return,
                "holding": holding or "CASH",
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
        "final_holding": holding or "CASH",
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

    baseline_trades, baseline_rebalances, baseline_equity, baseline_summary = run_top1(
        prices, members, start, end, enforce_membership_date=False
    )
    pit_trades, pit_rebalances, pit_equity, pit_summary = run_top1(
        prices, members, start, end, enforce_membership_date=True
    )

    _, _, qqq_return = benchmark_return("QQQ", start, end)
    _, _, vgt_return = benchmark_return("VGT", start, end)
    for summary in [baseline_summary, pit_summary]:
        summary["qqq_return"] = qqq_return
        summary["vgt_return"] = vgt_return
        summary["excess_vs_qqq"] = float(summary["strategy_return"]) - qqq_return
        summary["excess_vs_vgt"] = float(summary["strategy_return"]) - vgt_return

    summary_frame = pd.DataFrame([baseline_summary, pit_summary])
    trades_frame = pd.concat([baseline_trades, pit_trades], ignore_index=True)
    rebalances_frame = pd.concat([baseline_rebalances, pit_rebalances], ignore_index=True)
    equity_frame = pd.concat([baseline_equity, pit_equity], ignore_index=True)
    add_dates_frame = members[
        ["ticker", "Company", "nasdaq100_date_added", "date_source", "nasdaq100_added_security"]
    ].sort_values(["nasdaq100_date_added", "ticker"], na_position="first")

    base = "nasdaq100_top1_point_in_time_membership_2020_2026ytd"
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
        "# Nasdaq-100 Top1 Point-in-Time Membership Backtest",
        "",
        f"Period: {start.isoformat()} through {end.isoformat()}.",
        "Execution: monthly signal after month-end close, trade next trading day's open, hold open-to-open.",
        "Ranking: 126 trading-day momentum, skipping the latest 21 trading days.",
        "Point-in-time rule: if the top-ranked stock has a known Nasdaq-100 add date after the purchase date, skip it and choose the next eligible stock.",
        "Add-date source: Wikipedia Nasdaq-100 changes table, cached locally.",
        "",
        "| Strategy | Return | Max DD | Sharpe | Trades | Buys | Skipped Future Members | Violations | Known-Date Buys | Assumed Pre-window Buys | QQQ | VGT | Excess vs QQQ | Excess vs VGT | Final Holding |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in [baseline_summary, pit_summary]:
        lines.append(
            "| "
            f"{row['strategy']} | {pct(float(row['strategy_return']))} | "
            f"{pct(float(row['max_drawdown']))} | {float(row['sharpe_ratio']):.2f} | "
            f"{row['trade_count']} | {row['buy_count']} | {row['skipped_not_yet_nasdaq100']} | "
            f"{row['membership_violations']} | {row['known_date_buys']} | {row['assumed_prewindow_buys']} | "
            f"{pct(qqq_return)} | {pct(vgt_return)} | {pct(float(row['excess_vs_qqq']))} | "
            f"{pct(float(row['excess_vs_vgt']))} | {row['final_holding']} |"
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
    for row in [baseline_summary, pit_summary]:
        print(
            f"{row['strategy']}: return={pct(float(row['strategy_return']))}, "
            f"max_dd={pct(float(row['max_drawdown']))}, sharpe={float(row['sharpe_ratio']):.2f}, "
            f"trades={row['trade_count']}, skipped={row['skipped_not_yet_nasdaq100']}, "
            f"violations={row['membership_violations']}, excess_vs_qqq={pct(float(row['excess_vs_qqq']))}"
        )


if __name__ == "__main__":
    main()
