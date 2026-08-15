from __future__ import annotations

import csv
import json
import site
import textwrap
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for extra in ("vendor", ".deps", ".localdeps"):
    site.addsitedir(str(ROOT / extra))

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


OUT = ROOT / "reports" / "SOXL_TQQQ_Rotation_Cash_Verification_Packet_20260530.pdf"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def fmt_pct(value: str | float, decimals: int = 2) -> str:
    try:
        return f"{float(value):,.{decimals}f}%"
    except Exception:
        return str(value)


def pick(rows: list[dict[str, str]], key: str, value: str) -> dict[str, str]:
    for row in rows:
        if row.get(key) == value:
            return row
    raise KeyError(value)


def page(title: str):
    fig = plt.figure(figsize=(8.5, 11))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")
    fig.text(0.08, 0.94, title, fontsize=18, fontweight="bold", color="#1f3b57")
    fig.text(0.08, 0.915, "SOXL/TQQQ Rotation with cash daily scanner", fontsize=9, color="#5c6670")
    fig.lines.append(plt.Line2D([0.08, 0.92], [0.895, 0.895], color="#b7c3cc", linewidth=1))
    return fig, ax


def add_wrapped(fig, x: float, y: float, text: str, width: int = 96, size: int = 9.5, color: str = "#1c242b", line: float = 0.022) -> float:
    for para in text.split("\n"):
        if not para.strip():
            y -= line
            continue
        for wrapped in textwrap.wrap(para, width=width):
            fig.text(x, y, wrapped, fontsize=size, color=color)
            y -= line
    return y


def add_bullets(fig, x: float, y: float, items: list[str], width: int = 95, size: int = 9.2) -> float:
    for item in items:
        lines = textwrap.wrap(item, width=width)
        if not lines:
            continue
        fig.text(x, y, "- " + lines[0], fontsize=size, color="#1c242b")
        y -= 0.021
        for cont in lines[1:]:
            fig.text(x + 0.018, y, cont, fontsize=size, color="#1c242b")
            y -= 0.021
        y -= 0.006
    return y


def add_table(fig, ax, rows: list[list[str]], columns: list[str], bbox: list[float], font_size: int = 7.5, header_color: str = "#1f3b57"):
    table = ax.table(cellText=rows, colLabels=columns, cellLoc="center", colLoc="center", bbox=bbox)
    table.auto_set_font_size(False)
    table.set_fontsize(font_size)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#d6dde3")
        cell.set_linewidth(0.5)
        if r == 0:
            cell.set_facecolor(header_color)
            cell.get_text().set_color("white")
            cell.get_text().set_weight("bold")
        elif r % 2 == 0:
            cell.set_facecolor("#f5f7f9")
        else:
            cell.set_facecolor("white")
    return table


def main() -> None:
    OUT.parent.mkdir(exist_ok=True)

    is_oos_rows = read_csv(ROOT / "SOXL_TQQQ_InSample_Top10_OutSample_Rank.csv")
    latest_oos = read_csv(ROOT / "reports" / "soxl_tqqq_rotation_cash_oos_performance_summary_metrics.csv")
    annual = read_csv(ROOT / "reports" / "soxl_tqqq_rotation_cash_oos_performance_annual_return_drawdown.csv")
    status_path = ROOT / "reports" / "soxl_tqqq_cash_run_status.json"
    status = json.loads(status_path.read_text(encoding="utf-8")) if status_path.exists() else {}

    selected_names = ["New cash balanced strategy", "SOXL buy-and-hold", "TQQQ buy-and-hold"]
    selection_rows = [pick(is_oos_rows, "Strategy", name) for name in selected_names]
    latest_rows = [r for r in latest_oos if r.get("strategy") in {"SOXL/TQQQ Rotation with cash daily scanner", "SOXL buy-and-hold", "TQQQ buy-and-hold"}]

    with PdfPages(OUT) as pdf:
        fig, ax = page("Verification Packet")
        y = 0.84
        y = add_wrapped(
            fig,
            0.08,
            y,
            "Purpose: document the scanner trading rules and the available in-sample/out-of-sample performance evidence so a third-party model can verify the setup and numbers.",
            width=98,
            size=10,
        )
        y -= 0.02
        fig.text(0.08, y, "Current run/status artifact", fontsize=12, fontweight="bold", color="#1f3b57")
        y -= 0.035
        status_rows = [
            ["Generated", status.get("generated_at", "n/a")],
            ["Mode", status.get("mode", "n/a")],
            ["Can trade live", str(status.get("can_trade_live", "n/a"))],
            ["Executed trade", str(status.get("executed_trade", "n/a"))],
            ["Status reason", textwrap.shorten(str(status.get("stale_reason", "")), width=90, placeholder="...")],
        ]
        add_table(fig, ax, status_rows, ["Field", "Value"], [0.08, 0.55, 0.84, 0.22], font_size=8)
        fig.text(0.08, 0.49, "Primary source files", fontsize=12, fontweight="bold", color="#1f3b57")
        add_bullets(
            fig,
            0.08,
            0.455,
            [
                "Rules: scripts/soxl_tqqq_cash_signal_scanner.py and scripts/soxl_tqqq_cash_signal_scanner_stdlib.py.",
                "IS/OOS selection table: SOXL_TQQQ_InSample_Top10_OutSample_Rank.csv.",
                "Latest OOS metrics: reports/soxl_tqqq_rotation_cash_oos_performance_summary_metrics.csv.",
                "Annual OOS return/drawdown: reports/soxl_tqqq_rotation_cash_oos_performance_annual_return_drawdown.csv.",
                "Operational status: reports/soxl_tqqq_cash_run_status.json.",
            ],
            width=92,
        )
        fig.text(0.08, 0.12, f"Generated: {datetime.now().astimezone().isoformat(timespec='seconds')}", fontsize=8, color="#5c6670")
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = page("Trading Rules")
        y = 0.84
        fig.text(0.08, y, "Universe and data", fontsize=12, fontweight="bold", color="#1f3b57")
        y -= 0.032
        y = add_bullets(
            fig,
            0.08,
            y,
            [
                "Tradable symbols: SOXL and TQQQ. Context trend symbol: QQQ.",
                "Scanner timeframe: daily bars, evaluated after the daily close.",
                "Price data: adjusted daily close history for SOXL, TQQQ, and QQQ.",
                "Target output is exactly one of SOXL, TQQQ, or CASH.",
            ],
        )
        y -= 0.01
        fig.text(0.08, y, "Base rotation", fontsize=12, fontweight="bold", color="#1f3b57")
        y -= 0.032
        y = add_bullets(
            fig,
            0.08,
            y,
            [
                "Compute each ETF's relative momentum score as 63-trading-day return minus 0.5 times annualized realized volatility.",
                "Skip the most recent 10 trading days in both the return and volatility inputs.",
                "Initial raw choice is SOXL when SOXL score is greater than or equal to TQQQ score; otherwise TQQQ.",
                "Trend preference: if the selected ETF is below SMA50 and the alternate ETF is above SMA50, choose the alternate ETF.",
                "Hysteresis: switch the selected ETF only when the absolute score spread is at least 5 percentage points.",
                "Rebalance cadence: monthly. The chosen target is only refreshed on the first trading day of a new calendar month, then forward-filled.",
            ],
        )
        y -= 0.01
        fig.text(0.08, y, "Cash filter", fontsize=12, fontweight="bold", color="#1f3b57")
        y -= 0.032
        y = add_bullets(
            fig,
            0.08,
            y,
            [
                "Cash SMA window: 150 trading days for the currently selected ETF and QQQ.",
                "Exit to CASH when both the selected ETF and QQQ close below their SMA150 levels.",
                "Re-enter risk-on when either the selected ETF or QQQ closes at or above SMA150 plus 1%.",
                "The selected ETF itself has no exit buffer; re-entry buffer is 1%.",
            ],
        )
        y -= 0.01
        fig.text(0.08, y, "Execution logic", fontsize=12, fontweight="bold", color="#1f3b57")
        y -= 0.032
        add_bullets(
            fig,
            0.08,
            y,
            [
                "If target is CASH, sell any open SOXL/TQQQ positions.",
                "If target is SOXL or TQQQ, sell the non-target ETF first, then buy the target ETF if it is not already held.",
                "Default position size in the automation command is 1 share.",
                "Extended-hours execution uses Alpaca DAY limit orders with extended_hours=True and limit offset 0%.",
                "Default Alpaca mode is paper trading unless --live is supplied.",
                "Fallback mode: if live data or Alpaca is unavailable, write a stale_fallback status and skip trading.",
            ],
        )
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = page("IS/OOS Selection Audit")
        fig.text(0.08, 0.84, "Apples-to-apples comparison from SOXL_TQQQ_InSample_Top10_OutSample_Rank.csv", fontsize=10, color="#1c242b")
        comp_rows = []
        for row in selection_rows:
            comp_rows.append(
                [
                    row["Strategy"].replace("New cash balanced strategy", "Scanner cash strategy"),
                    row["In-sample actual range"],
                    fmt_pct(row["In-sample cumulative return %"]),
                    fmt_pct(row["In-sample max drawdown %"]),
                    row["Out-of-sample actual range"],
                    fmt_pct(row["Out-of-sample cumulative return %"]),
                    fmt_pct(row["Out-of-sample max drawdown %"]),
                    row["Out-of-sample Sharpe"],
                ]
            )
        add_table(
            fig,
            ax,
            comp_rows,
            ["Strategy", "IS period", "IS return", "IS DD", "OOS period", "OOS return", "OOS DD", "OOS Sharpe"],
            [0.04, 0.55, 0.92, 0.23],
            font_size=6.5,
        )
        fig.text(0.08, 0.49, "Interpretation", fontsize=12, fontweight="bold", color="#1f3b57")
        add_bullets(
            fig,
            0.08,
            0.455,
            [
                "The scanner cash strategy had lower IS drawdown than SOXL buy-and-hold and slightly lower IS drawdown than TQQQ buy-and-hold in this selection audit.",
                "The same selection-audit OOS slice shows substantially higher cumulative return and lower drawdown than both SOXL and TQQQ buy-and-hold.",
                "These values are selection-audit values through 2026-05-20; the latest scanner OOS refresh through 2026-05-22 is shown on the next page.",
            ],
            width=96,
        )
        pdf.savefig(fig)
        plt.close(fig)

        fig, ax = page("Latest OOS Refresh")
        latest_table = []
        for row in latest_rows:
            latest_table.append(
                [
                    row["strategy"].replace("SOXL/TQQQ Rotation with cash daily scanner", "Scanner cash strategy"),
                    row["period"],
                    fmt_pct(row["cumulative_return_pct"]),
                    fmt_pct(row["cagr_pct"]),
                    fmt_pct(row["max_drawdown_pct"]),
                    row["sharpe"],
                    row["sortino"],
                    row["calmar"],
                ]
            )
        add_table(
            fig,
            ax,
            latest_table,
            ["Strategy", "OOS period", "Return", "CAGR", "Max DD", "Sharpe", "Sortino", "Calmar"],
            [0.05, 0.70, 0.90, 0.17],
            font_size=6.7,
        )
        fig.text(0.08, 0.64, "Annual OOS return / drawdown", fontsize=12, fontweight="bold", color="#1f3b57")
        ann_rows = []
        for year in sorted({r["year"] for r in annual}):
            year_rows = {r["strategy"]: r for r in annual if r["year"] == year}
            ann_rows.append(
                [
                    year,
                    fmt_pct(year_rows["SOXL/TQQQ Rotation with cash daily scanner"]["return_pct"]),
                    fmt_pct(year_rows["SOXL/TQQQ Rotation with cash daily scanner"]["max_drawdown_pct"]),
                    fmt_pct(year_rows["SOXL buy-and-hold"]["return_pct"]),
                    fmt_pct(year_rows["SOXL buy-and-hold"]["max_drawdown_pct"]),
                    fmt_pct(year_rows["TQQQ buy-and-hold"]["return_pct"]),
                    fmt_pct(year_rows["TQQQ buy-and-hold"]["max_drawdown_pct"]),
                ]
            )
        add_table(
            fig,
            ax,
            ann_rows,
            ["Year", "Scanner ret", "Scanner DD", "SOXL ret", "SOXL DD", "TQQQ ret", "TQQQ DD"],
            [0.08, 0.19, 0.84, 0.40],
            font_size=7.1,
        )
        fig.text(0.08, 0.12, "Latest OOS source period ends 2026-05-22. Annual 2026 values are year-to-date in the source file.", fontsize=8, color="#5c6670")
        pdf.savefig(fig)
        plt.close(fig)

        chart = ROOT / "reports" / "soxl_tqqq_rotation_cash_oos_performance_curves.png"
        if chart.exists():
            fig, ax = page("OOS Curves")
            img = mpimg.imread(chart)
            img_ax = fig.add_axes([0.08, 0.17, 0.84, 0.68])
            img_ax.imshow(img)
            img_ax.axis("off")
            fig.text(0.08, 0.12, "Source: reports/soxl_tqqq_rotation_cash_oos_performance_curves.png", fontsize=8, color="#5c6670")
            pdf.savefig(fig)
            plt.close(fig)

        fig, ax = page("Verification Notes")
        y = 0.84
        fig.text(0.08, y, "Assumptions and caveats", fontsize=12, fontweight="bold", color="#1f3b57")
        y -= 0.035
        y = add_bullets(
            fig,
            0.08,
            y,
            [
                "Backtest metrics are based on local generated artifacts; no new market data was downloaded for this packet.",
                "The strategy reports use adjusted daily prices and zero explicit trading cost unless stated otherwise.",
                "The strategy is a daily scanner whose base SOXL/TQQQ rotation updates monthly; those statements are not contradictory.",
                "The active runner uses a dependency-free scanner for operational robustness, but it implements the same rule set as the pandas/yfinance scanner.",
                "If run_status mode is stale_fallback, the scanner did not place trades during that run; it intentionally reused the prior signal and wrote the blocker reason.",
            ],
            width=98,
        )
        y -= 0.01
        fig.text(0.08, y, "Recommended Claude checks", fontsize=12, fontweight="bold", color="#1f3b57")
        y -= 0.035
        add_bullets(
            fig,
            0.08,
            y,
            [
                "Confirm StrategyConfig values: 63 lookback, 10 skip, SMA50 trend, 5% hysteresis, SMA150 cash filter, 1% re-entry buffer.",
                "Confirm monthly rebalance is applied after daily score calculation and before cash filtering.",
                "Confirm execution path sells non-target exposure before buying the target, and does not trade in stale_fallback mode.",
                "Compare the IS/OOS table values against the listed CSV sources rather than mixing files with different OOS end dates.",
            ],
            width=98,
        )
        pdf.savefig(fig)
        plt.close(fig)

    print(OUT)


if __name__ == "__main__":
    main()
