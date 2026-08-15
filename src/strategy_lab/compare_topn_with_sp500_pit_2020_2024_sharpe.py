from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.compare_topn_with_sp500_point_in_time_filter import (
    Universe,
    load_universe_members,
    pct,
    run_topn_monthly_o2o,
)
from src.strategy_lab.sp500_top5 import load_or_fetch_prices


def annualized_sharpe(daily_returns: pd.Series) -> float:
    returns = daily_returns.dropna()
    if returns.empty:
        return 0.0
    std = returns.std(ddof=1)
    if std == 0 or pd.isna(std):
        return 0.0
    return float((returns.mean() / std) * (252 ** 0.5))


def main() -> None:
    start = date(2020, 1, 1)
    end = date(2024, 12, 31)
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

    summaries: list[dict[str, object]] = []
    all_trades: list[pd.DataFrame] = []
    all_rebalances: list[pd.DataFrame] = []
    all_equity: list[pd.DataFrame] = []

    for universe in universes:
        members = load_universe_members(universe)
        tickers = members["ticker"].dropna().astype(str).tolist()
        prices = load_or_fetch_prices(
            universe.data_dir / f"adjusted_open_close_{data_start.isoformat()}_2026-05-17.csv",
            tickers,
            data_start,
            date(2026, 5, 17),
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
            summary["sharpe_ratio"] = annualized_sharpe(equity_curve["daily_return"])
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

    base = "top1_top2_top3_sp500_pit_nasdaq100_vs_spmo_vgt_2020_2024_sharpe"
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
        "# Top1/Top2/Top3 Monthly Skip-Momentum Comparison With Sharpe",
        "",
        f"Period: {start.isoformat()} through {end.isoformat()}.",
        "Execution: monthly signal after month-end close, trade at next trading day's open, hold open-to-open.",
        "Ranking: 126 trading-day momentum, skipping the latest 21 trading days.",
        "Sharpe ratio: annualized from daily open-to-open strategy returns, risk-free rate assumed 0%.",
        "S&P 500 rule: skip stocks whose `Date added` is after the purchase date, then choose the next eligible ranked stock.",
        "Nasdaq-100 note: the cached Nasdaq-100 constituent table has no add-date field, so Nasdaq-100 rows use current constituents only.",
        "",
        "| Universe | Top N | Membership Filter | Return | Max DD | Sharpe | Trades | Buys | Skipped Future Members | Violations | SPMO | VGT | Final Holdings |",
        "| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- |",
    ]
    for row in summaries:
        lines.append(
            "| "
            f"{row['universe']} | {row['top_n']} | {row['membership_filter']} | "
            f"{pct(float(row['strategy_return']))} | {pct(float(row['max_drawdown']))} | "
            f"{float(row['sharpe_ratio']):.2f} | {row['trade_count']} | {row['buy_count']} | "
            f"{row['skipped_not_yet_index']} | {row['membership_violations']} | "
            f"{pct(spmo_return)} | {pct(vgt_return)} | {row['final_holdings']} |"
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
            f"max_dd={pct(float(row['max_drawdown']))}, sharpe={float(row['sharpe_ratio']):.2f}, "
            f"trades={row['trade_count']}, skipped={row['skipped_not_yet_index']}, "
            f"violations={row['membership_violations']}"
        )


if __name__ == "__main__":
    main()
