from __future__ import annotations

import textwrap
from pathlib import Path

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt


TITLE = "Nasdaq-100 Top 1 Monthly Skip-Momentum Strategy"


SECTIONS = [
    (
        "1. Strategy Summary",
        [
            "Universe: Nasdaq-100 stocks.",
            "Position count: top 1 stock, 100% weight.",
            "Rebalance: monthly.",
            "Signal timing: after month-end close.",
            "Execution: next trading day open.",
            "Return method: open-to-open for completed months; latest incomplete month uses latest available close.",
            "Ranking score: Close[t - 21 trading days] / Close[t - 126 trading days] - 1.",
        ],
    ),
    (
        "2. Ranking Rule",
        [
            "At each month-end close, calculate the momentum score for every stock in the Nasdaq-100 universe.",
            "Momentum Score = Close[t - 21 trading days] / Close[t - 126 trading days] - 1.",
            "The 126-day lookback is roughly six trading months.",
            "The 21-day skip window excludes the most recent trading month to reduce short-term reversal/noise.",
            "Rank all stocks from highest score to lowest and select the top-ranked stock.",
        ],
    ),
    (
        "3. Monthly Trading Rule",
        [
            "If there is no existing holding, buy the selected stock at the first trading day open of the month.",
            "If the selected stock changes, sell the old stock and buy the new stock at the same first trading day open.",
            "If the selected stock is unchanged, keep holding it and still record a HOLD row for that month.",
            "Every month must have exactly one decision row: BUY, SWITCH, or HOLD.",
        ],
    ),
    (
        "4. Return Calculation",
        [
            "For completed months: Monthly Return = Next Month First Trading Day Open / Current Month First Trading Day Open - 1.",
            "For the latest incomplete month: Monthly Return = Latest Available Close / Current Month First Trading Day Open - 1.",
            "Total Return = PRODUCT(1 + Monthly Return) - 1.",
            "The exported workbook reconciles total return exactly from the monthly rows.",
        ],
    ),
    (
        "5. Pseudocode",
        [
            "for each month:",
            "    signal_date = last trading day before month start",
            "    trade_date = first trading day of month",
            "    for ticker in Nasdaq-100 universe:",
            "        score[ticker] = close[ticker][signal_date - 21 trading days] / close[ticker][signal_date - 126 trading days] - 1",
            "    selected = ticker with highest score",
            "    if no current holding: BUY selected",
            "    elif selected != current holding: SWITCH to selected",
            "    else: HOLD selected",
            "    monthly_return = next_month_trade_open / current_trade_open - 1",
        ],
    ),
    (
        "6. Latest Validation Results",
        [
            "Validation window: 2025-01-01 through 2026-05-15.",
            "Monthly rows: 17.",
            "Buy rows: 1.",
            "Switch rows: 3.",
            "Hold rows: 13.",
            "Total return: 1005.28%.",
            "Final equity: 11.0528x.",
            "Reconciliation difference: 0.0.",
            "Validation column: all rows OK.",
        ],
    ),
    (
        "7. Monthly Decision Summary",
        [
            "2025-01: BUY APP, signal 2024-12-31, trade 2025-01-02.",
            "2025-02: HOLD APP.",
            "2025-03: HOLD APP.",
            "2025-04: HOLD APP.",
            "2025-05: SWITCH APP to PLTR.",
            "2025-06: HOLD PLTR.",
            "2025-07: HOLD PLTR.",
            "2025-08: HOLD PLTR.",
            "2025-09: HOLD PLTR.",
            "2025-10: SWITCH PLTR to WDC.",
            "2025-11: SWITCH WDC to SNDK.",
            "2025-12: HOLD SNDK.",
            "2026-01: HOLD SNDK.",
            "2026-02: HOLD SNDK.",
            "2026-03: HOLD SNDK.",
            "2026-04: HOLD SNDK.",
            "2026-05: HOLD SNDK; latest incomplete month.",
        ],
    ),
    (
        "8. Generated Files",
        [
            r"Excel workbook: C:\Users\skydiver1118\Documents\New project\reports\nasdaq100_top1_skip21_monthly_o2o_trades_2025_ytd.xlsx",
            r"Monthly trades CSV: C:\Users\skydiver1118\Documents\New project\reports\nasdaq100_top1_skip21_monthly_o2o_trades_2025_ytd.csv",
            r"Summary CSV: C:\Users\skydiver1118\Documents\New project\reports\nasdaq100_top1_skip21_monthly_o2o_trades_2025_ytd_summary.csv",
        ],
    ),
    (
        "9. Critical Caveats",
        [
            "Survivorship/index-membership bias: the test uses the current Nasdaq-100 constituent list for past dates.",
            "A cleaner historical backtest should use point-in-time Nasdaq-100 membership.",
            "Yahoo Finance adjusted open/close data can be noisy around corporate actions.",
            "No slippage, bid/ask spread, commission, market impact, or borrow constraints are included.",
            "The strategy holds only one stock, so concentration risk is extreme.",
            "The latest month is partial and valued from month-start open to latest available close.",
        ],
    ),
    (
        "10. Replication Checklist",
        [
            "Use daily adjusted open and adjusted close prices.",
            "Prefer point-in-time Nasdaq-100 membership.",
            "Compute the score only after month-end close.",
            "Trade only at the next trading day open.",
            "Record a monthly row even when the ticker does not change.",
            "Calculate completed-month returns open-to-open.",
            "Compound monthly returns to reconcile total return.",
            "Compare against QQQ or another Nasdaq-100 benchmark.",
        ],
    ),
]


def draw_page(pdf: PdfPages, page_title: str, lines: list[str]) -> None:
    fig = plt.figure(figsize=(8.5, 11))
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis("off")

    y = 0.95
    ax.text(0.08, y, page_title, fontsize=16, fontweight="bold", va="top")
    y -= 0.05

    for raw_line in lines:
        wrapped = textwrap.wrap(raw_line, width=88) or [""]
        for line in wrapped:
            if y < 0.08:
                pdf.savefig(fig)
                plt.close(fig)
                fig = plt.figure(figsize=(8.5, 11))
                fig.patch.set_facecolor("white")
                ax = fig.add_axes([0, 0, 1, 1])
                ax.axis("off")
                y = 0.95
                ax.text(0.08, y, page_title + " (continued)", fontsize=16, fontweight="bold", va="top")
                y -= 0.05
            ax.text(0.1, y, line, fontsize=10.5, va="top", family="monospace" if raw_line.startswith("    ") else "sans-serif")
            y -= 0.026
        y -= 0.01

    pdf.savefig(fig)
    plt.close(fig)


def main() -> None:
    output = Path("reports/nasdaq100_top1_monthly_skip_momentum_strategy_package.pdf")
    output.parent.mkdir(parents=True, exist_ok=True)

    with PdfPages(output) as pdf:
        draw_page(
            pdf,
            TITLE,
            [
                "Structured strategy package for replication in other AI/backtesting tools.",
                "Includes rules, timing, return calculation, validation summary, generated files, and caveats.",
                "Prepared from the local validated backtest artifacts.",
            ],
        )
        for title, lines in SECTIONS:
            draw_page(pdf, title, lines)

    print(output)


if __name__ == "__main__":
    main()
