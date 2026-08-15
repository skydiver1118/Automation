from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.compare_universe_topn_monthly import is_month_end_signal
from src.strategy_lab.sp500_top5 import load_or_fetch_prices, momentum_scores


@dataclass(frozen=True)
class StrategySummary:
    name: str
    strategy_return: float
    max_drawdown: float
    trade_count: int
    buy_count: int
    sell_count: int
    rebalance_count: int
    skipped_not_yet_sp500: int
    membership_violations: int
    final_holding: str
    spmo_return: float
    excess_vs_spmo: float


def pct(value: float) -> str:
    return f"{value:.2%}"


def load_membership(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame["Date added parsed"] = pd.to_datetime(frame["Date added"], errors="coerce").dt.date
    return frame.rename(
        columns={
            "Yahoo Symbol": "ticker",
            "Security": "security",
            "GICS Sector": "sector",
            "Date added": "sp500_date_added",
            "Date added parsed": "sp500_date_added_parsed",
        }
    )


def eligible_on_purchase_date(
    ticker: str,
    purchase_date: date,
    date_added_by_ticker: dict[str, date],
    enforce_membership_date: bool,
) -> bool:
    if not enforce_membership_date:
        return True
    date_added = date_added_by_ticker.get(ticker)
    return date_added is not None and date_added <= purchase_date


def pick_top_eligible(
    scores: pd.Series,
    purchase_date: date,
    date_added_by_ticker: dict[str, date],
    enforce_membership_date: bool,
) -> tuple[str | None, float | None, int, str]:
    skipped: list[str] = []
    for ticker, score in scores.items():
        if eligible_on_purchase_date(ticker, purchase_date, date_added_by_ticker, enforce_membership_date):
            return ticker, float(score), len(skipped), ", ".join(skipped[:10])
        skipped.append(ticker)
    return None, None, len(skipped), ", ".join(skipped[:10])


def run_top1_monthly_o2o(
    prices: pd.DataFrame,
    membership: pd.DataFrame,
    start: date,
    end: date,
    enforce_membership_date: bool,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, StrategySummary]:
    close = prices["Close"].dropna(axis=1, thresh=128).sort_index()
    open_prices = prices["Open"].reindex(columns=close.columns).sort_index()
    close = close.loc[(close.index.date >= start) | (close.index < pd.Timestamp(start))]
    close = close.loc[close.index.date <= end]
    open_prices = open_prices.reindex(index=close.index)

    date_added_by_ticker = {
        str(row.ticker): row.sp500_date_added_parsed
        for row in membership.itertuples(index=False)
        if pd.notna(row.ticker) and pd.notna(row.sp500_date_added_parsed)
    }
    security_by_ticker = {
        str(row.ticker): row.security for row in membership.itertuples(index=False) if pd.notna(row.ticker)
    }
    date_added_text_by_ticker = {
        str(row.ticker): row.sp500_date_added for row in membership.itertuples(index=False) if pd.notna(row.ticker)
    }

    strategy_name = "Top1 PIT S&P membership" if enforce_membership_date else "Top1 current-member baseline"
    holding: str | None = None
    equity = 1.0
    peak = 1.0
    max_drawdown = 0.0
    trade_rows: list[dict[str, object]] = []
    rebalance_rows: list[dict[str, object]] = []
    equity_rows: list[dict[str, object]] = []
    skipped_not_yet_sp500 = 0

    for signal_index in range(126, len(close) - 2):
        entry_index = signal_index + 1
        exit_index = signal_index + 2
        signal_date = close.index[signal_index].date()
        purchase_date = close.index[entry_index].date()
        exit_date = close.index[exit_index].date()
        if purchase_date < start or purchase_date > end:
            continue

        if is_month_end_signal(signal_index, close.index, pd.Series(dtype=float) if holding is None else pd.Series([1.0], index=[holding])):
            scores = momentum_scores(close, signal_index, 126, score_mode="skip", skip_days=21)
            selected, selected_score, skipped_count, skipped_tickers = pick_top_eligible(
                scores,
                purchase_date,
                date_added_by_ticker,
                enforce_membership_date,
            )
            skipped_not_yet_sp500 += skipped_count

            rebalance_rows.append(
                {
                    "strategy": strategy_name,
                    "signal_date": signal_date.isoformat(),
                    "purchase_date": purchase_date.isoformat(),
                    "selected_ticker": selected or "CASH",
                    "selected_security": security_by_ticker.get(selected or "", ""),
                    "selected_score": selected_score if selected_score is not None else "",
                    "selected_sp500_date_added": date_added_text_by_ticker.get(selected or "", ""),
                    "skipped_not_yet_sp500_count": skipped_count,
                    "first_skipped_tickers": skipped_tickers,
                    "prior_holding": holding or "CASH",
                    "equity_before_rebalance": equity,
                }
            )

            if holding != selected:
                if holding is not None:
                    trade_rows.append(
                        {
                            "strategy": strategy_name,
                            "signal_date": signal_date.isoformat(),
                            "trade_date": purchase_date.isoformat(),
                            "action": "SELL",
                            "ticker": holding,
                            "security": security_by_ticker.get(holding, ""),
                            "sp500_date_added": date_added_text_by_ticker.get(holding, ""),
                            "price": float(open_prices.iloc[entry_index][holding]),
                            "score": "",
                            "skipped_not_yet_sp500_before_buy": "",
                            "equity_before_trade": equity,
                        }
                    )
                if selected is not None:
                    trade_rows.append(
                        {
                            "strategy": strategy_name,
                            "signal_date": signal_date.isoformat(),
                            "trade_date": purchase_date.isoformat(),
                            "action": "BUY",
                            "ticker": selected,
                            "security": security_by_ticker.get(selected, ""),
                            "sp500_date_added": date_added_text_by_ticker.get(selected, ""),
                            "price": float(open_prices.iloc[entry_index][selected]),
                            "score": selected_score,
                            "skipped_not_yet_sp500_before_buy": skipped_count,
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
        peak = max(peak, equity)
        max_drawdown = min(max_drawdown, equity / peak - 1.0)
        equity_rows.append(
            {
                "strategy": strategy_name,
                "date": exit_date.isoformat(),
                "equity": equity,
                "daily_return": daily_return,
                "holding": holding or "CASH",
            }
        )

    trades = pd.DataFrame(trade_rows)
    rebalances = pd.DataFrame(rebalance_rows)
    equity_curve = pd.DataFrame(equity_rows)

    buys = trades[trades["action"] == "BUY"] if not trades.empty else pd.DataFrame()
    membership_violations = 0
    if not buys.empty:
        buy_dates = pd.to_datetime(buys["trade_date"]).dt.date
        for ticker, buy_date in zip(buys["ticker"], buy_dates):
            date_added = date_added_by_ticker.get(str(ticker))
            if date_added is None or buy_date < date_added:
                membership_violations += 1

    _, _, spmo_return = benchmark_return("SPMO", start, end)
    summary = StrategySummary(
        name=strategy_name,
        strategy_return=equity - 1.0,
        max_drawdown=max_drawdown,
        trade_count=len(trades),
        buy_count=int((trades["action"] == "BUY").sum()) if not trades.empty else 0,
        sell_count=int((trades["action"] == "SELL").sum()) if not trades.empty else 0,
        rebalance_count=len(rebalances),
        skipped_not_yet_sp500=skipped_not_yet_sp500,
        membership_violations=membership_violations,
        final_holding=holding or "CASH",
        spmo_return=spmo_return,
        excess_vs_spmo=equity - 1.0 - spmo_return,
    )
    return trades, rebalances, equity_curve, summary


def main() -> None:
    start = date(2020, 1, 1)
    end = date(2026, 5, 17)
    data_start = date(2018, 12, 19)
    data_dir = Path("data/sp500_top5")
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    membership = load_membership(data_dir / "sp500_constituents.csv")
    tickers = membership["ticker"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(
        data_dir / f"adjusted_open_close_{data_start.isoformat()}_{end.isoformat()}.csv",
        tickers,
        data_start,
        end,
        False,
    )

    baseline_trades, baseline_rebalances, baseline_equity, baseline_summary = run_top1_monthly_o2o(
        prices,
        membership,
        start,
        end,
        enforce_membership_date=False,
    )
    pit_trades, pit_rebalances, pit_equity, pit_summary = run_top1_monthly_o2o(
        prices,
        membership,
        start,
        end,
        enforce_membership_date=True,
    )

    summary_frame = pd.DataFrame([baseline_summary.__dict__, pit_summary.__dict__])
    base = "sp500_top1_point_in_time_membership_2020_2026ytd"
    xlsx_path = report_dir / f"{base}.xlsx"
    csv_path = report_dir / f"{base}_summary.csv"
    md_path = report_dir / f"{base}.md"
    trades_csv_path = report_dir / f"{base}_trades.csv"
    rebalances_csv_path = report_dir / f"{base}_monthly_rebalances.csv"
    equity_csv_path = report_dir / f"{base}_equity_curve.csv"

    all_trades = pd.concat([baseline_trades, pit_trades], ignore_index=True)
    all_rebalances = pd.concat([baseline_rebalances, pit_rebalances], ignore_index=True)
    all_equity = pd.concat([baseline_equity, pit_equity], ignore_index=True)

    summary_frame.to_csv(csv_path, index=False)
    all_trades.to_csv(trades_csv_path, index=False)
    all_rebalances.to_csv(rebalances_csv_path, index=False)
    all_equity.to_csv(equity_csv_path, index=False)

    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        summary_frame.to_excel(writer, sheet_name="Summary", index=False)
        all_trades.to_excel(writer, sheet_name="Trades", index=False)
        all_rebalances.to_excel(writer, sheet_name="Monthly decisions", index=False)
        all_equity.to_excel(writer, sheet_name="Equity curve", index=False)

        workbook = writer.book
        for worksheet in workbook.worksheets:
            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions
            for column in worksheet.columns:
                max_length = 0
                letter = column[0].column_letter
                for cell in column:
                    value = "" if cell.value is None else str(cell.value)
                    max_length = max(max_length, min(len(value), 42))
                worksheet.column_dimensions[letter].width = max(10, max_length + 2)

    lines = [
        "# S&P 500 Top1 Point-in-Time Membership Backtest",
        "",
        f"Period: {start.isoformat()} through {end.isoformat()}.",
        "Execution: monthly signal after month-end close, buy/sell at next trading day's open, hold open-to-open.",
        "Ranking: 126 trading-day momentum, skipping the latest 21 trading days.",
        "Point-in-time rule: walk down the momentum ranking and skip any ticker whose S&P 500 `Date added` is after the purchase date.",
        "",
        "| Strategy | Return | Max DD | Trades | Buys | Rebalances | Skipped future members | Membership violations | Final holding | SPMO return | Excess vs SPMO |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |",
    ]
    for row in [baseline_summary, pit_summary]:
        lines.append(
            "| "
            f"{row.name} | {pct(row.strategy_return)} | {pct(row.max_drawdown)} | "
            f"{row.trade_count} | {row.buy_count} | {row.rebalance_count} | "
            f"{row.skipped_not_yet_sp500} | {row.membership_violations} | "
            f"{row.final_holding} | {pct(row.spmo_return)} | {pct(row.excess_vs_spmo)} |"
        )
    lines.extend(
        [
            "",
            "The filtered strategy removes buys before each stock's available S&P 500 `Date added` value.",
            "Important limitation: this is still based on today's S&P 500 constituent list plus each member's `Date added`. It prevents buying future additions, but it does not include stocks that were historical S&P 500 members and have since been removed.",
            "",
            "## Output Files",
            "",
            f"- Excel workbook: `{xlsx_path}`",
            f"- Summary CSV: `{csv_path}`",
            f"- Trade CSV: `{trades_csv_path}`",
            f"- Monthly decisions CSV: `{rebalances_csv_path}`",
            f"- Equity curve CSV: `{equity_csv_path}`",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(md_path)
    for row in [baseline_summary, pit_summary]:
        print(
            f"{row.name}: return={pct(row.strategy_return)}, max_dd={pct(row.max_drawdown)}, "
            f"trades={row.trade_count}, buys={row.buy_count}, skipped_future_members={row.skipped_not_yet_sp500}, "
            f"violations={row.membership_violations}, excess_vs_spmo={pct(row.excess_vs_spmo)}"
        )


if __name__ == "__main__":
    main()
