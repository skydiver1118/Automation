from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.nasdaq100_top1_point_in_time_membership import (
    build_current_member_add_dates,
    load_or_fetch_nasdaq100_changes,
    pct,
)
from src.strategy_lab.nasdaq100_topn_point_in_time_membership import run_topn
from src.strategy_lab.sp500_top5 import load_or_fetch_prices


def main() -> None:
    start = date(2020, 1, 1)
    end = date(2024, 12, 31)
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
        data_dir / "adjusted_open_close_2018-12-19_2026-05-17.csv",
        tickers,
        data_start,
        date(2026, 5, 17),
        False,
    )

    _, _, qqq_return = benchmark_return("QQQ", start, end)
    _, _, vgt_return = benchmark_return("VGT", start, end)

    summaries: list[dict[str, object]] = []
    all_trades: list[pd.DataFrame] = []
    all_rebalances: list[pd.DataFrame] = []
    all_equity: list[pd.DataFrame] = []

    for top_n in [1, 2, 3]:
        trades, rebalances, equity_curve, summary = run_topn(
            prices,
            members,
            start,
            end,
            top_n,
            enforce_membership_date=True,
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

    base = "nasdaq100_top1_top2_top3_pit_2020_2024"
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
        "# Nasdaq-100 Top1/Top2/Top3 Point-in-Time Filter Only",
        "",
        f"Period: {start.isoformat()} through {end.isoformat()}.",
        "Execution: monthly signal after month-end close, trade next trading day's open, hold open-to-open.",
        "Ranking: 126 trading-day momentum, skipping the latest 21 trading days.",
        "Point-in-time rule: fill each Top N slot by walking down the rank list and skipping stocks with known Nasdaq-100 add dates after the purchase date.",
        "",
        "| Top N | Return | Max DD | Sharpe | Trades | Buys | Skipped Future Members | Violations | QQQ | VGT | Final Holdings |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in summaries:
        lines.append(
            "| "
            f"{row['top_n']} | {pct(float(row['strategy_return']))} | "
            f"{pct(float(row['max_drawdown']))} | {float(row['sharpe_ratio']):.2f} | "
            f"{row['trade_count']} | {row['buy_count']} | {row['skipped_not_yet_nasdaq100']} | "
            f"{row['membership_violations']} | {pct(qqq_return)} | {pct(vgt_return)} | "
            f"{row['final_holdings']} |"
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
            f"Top{row['top_n']} PIT: return={pct(float(row['strategy_return']))}, "
            f"max_dd={pct(float(row['max_drawdown']))}, sharpe={float(row['sharpe_ratio']):.2f}, "
            f"trades={row['trade_count']}, skipped={row['skipped_not_yet_nasdaq100']}, "
            f"violations={row['membership_violations']}"
        )


if __name__ == "__main__":
    main()
