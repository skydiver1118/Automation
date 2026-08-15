from __future__ import annotations

import textwrap
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


TITLE = "Nasdaq-100 Top 2 Monthly Skip-Momentum Strategy"


SECTIONS = [
    (
        "1. Strategy Summary",
        [
            "Universe: Nasdaq-100 stocks.",
            "Position count: top 2 stocks.",
            "Portfolio weight: 50% in each selected stock.",
            "Rebalance: monthly.",
            "Signal timing: after month-end close.",
            "Execution: next trading day open.",
            "Return method: open-to-open for completed months.",
            "Ranking score: Close[t - 21 trading days] / Close[t - 126 trading days] - 1.",
        ],
    ),
    (
        "2. Ranking Rule",
        [
            "At each month-end close, calculate the momentum score for every stock in the Nasdaq-100 universe.",
            "Momentum Score = Close[t - 21 trading days] / Close[t - 126 trading days] - 1.",
            "The 126-day lookback is roughly six trading months.",
            "The 21-day skip window excludes the most recent trading month.",
            "Rank all stocks from highest score to lowest and select the top two stocks.",
        ],
    ),
    (
        "3. Monthly Trading Rule",
        [
            "At each rebalance, hold the top 2 ranked stocks at 50% weight each.",
            "If a selected stock remains in the top 2, keep holding it.",
            "If a selected stock drops out of the top 2, sell it at the next monthly trade open.",
            "Buy any new top-2 stock at the same open.",
            "Record monthly decisions even when one or both holdings do not change.",
        ],
    ),
    (
        "4. Execution Timing",
        [
            "The strategy avoids same-day lookahead.",
            "Month-end close signal -> next trading day open trade.",
            "The ranking signal uses only data known as of the month-end close.",
            "Positions are entered and exited at the next available open.",
        ],
    ),
    (
        "5. Return Calculation",
        [
            "For completed months, returns are open-to-open.",
            "Each selected stock contributes according to its target weight.",
            "Monthly Portfolio Return = 0.5 * Stock1 Open-to-Open Return + 0.5 * Stock2 Open-to-Open Return.",
            "Total Return = PRODUCT(1 + Monthly Portfolio Return) - 1.",
        ],
    ),
    (
        "6. Pseudocode",
        [
            "for each month:",
            "    signal_date = last trading day before month start",
            "    trade_date = first trading day of month",
            "    for ticker in Nasdaq-100 universe:",
            "        score[ticker] = close[ticker][signal_date - 21 trading days] / close[ticker][signal_date - 126 trading days] - 1",
            "    selected = top 2 tickers by score",
            "    target weights = 50% each",
            "    sell holdings not in selected at trade_date open",
            "    buy new selected stocks at trade_date open",
            "    hold unchanged selected stocks",
            "    monthly_return = weighted open-to-open return of selected holdings",
        ],
    ),
    (
        "7. Latest Annual Reset Validation",
        [
            "Validation universe: current Nasdaq-100 constituents.",
            "Benchmark: QQQ.",
            "Test period: 2020 through 2026 YTD.",
            "Important caveat: this uses current Nasdaq-100 membership for past years, so point-in-time membership validation is still needed.",
            "",
            "2020: Strategy 148.61%, QQQ close 45.97%, excess +102.64%, max DD -39.54%, trades 26.",
            "2021: Strategy 38.94%, QQQ close 29.24%, excess +9.70%, max DD -50.12%, trades 18.",
            "2022: Strategy -14.29%, QQQ close -33.22%, excess +18.93%, max DD -39.88%, trades 28.",
            "2023: Strategy 90.50%, QQQ close 55.91%, excess +34.60%, max DD -25.98%, trades 22.",
            "2024: Strategy 44.89%, QQQ close 27.74%, excess +17.15%, max DD -38.09%, trades 20.",
            "2025: Strategy 145.92%, QQQ close 21.01%, excess +124.91%, max DD -52.49%, trades 18.",
            "2026 YTD: Strategy 235.72%, QQQ close 15.77%, excess +219.95%, max DD -25.62%, trades 6.",
        ],
    ),
    (
        "8. Compounded Reset Return",
        [
            "2020-2026 YTD compounded reset return:",
            "Strategy: 6647.15%.",
            "QQQ adjusted-close benchmark: 251.51%.",
            "QQQ open-to-open benchmark: 241.34%.",
        ],
    ),
    (
        "9. Generated Validation File",
        [
            r"Validation report: C:\Users\skydiver1118\Documents\New project\reports\nasdaq100_top2_skip21_monthly_o2o_validation_2020_2026ytd.md",
            r"Validation CSV: C:\Users\skydiver1118\Documents\New project\reports\nasdaq100_top2_skip21_monthly_o2o_validation_2020_2026ytd.csv",
        ],
    ),
    (
        "10. Critical Caveats",
        [
            "Survivorship/index-membership bias: the test uses the current Nasdaq-100 constituent list for past dates.",
            "A cleaner historical backtest should use point-in-time Nasdaq-100 membership.",
            "Yahoo Finance adjusted open/close data can be noisy around corporate actions.",
            "No slippage, bid/ask spread, commission, market impact, or tax impact is included.",
            "The strategy holds only two stocks, so concentration risk is high.",
        ],
    ),
    (
        "11. Replication Checklist",
        [
            "Use daily adjusted open and adjusted close prices.",
            "Prefer point-in-time Nasdaq-100 membership.",
            "Compute the score only after month-end close.",
            "Trade only at the next trading day open.",
            "Select the top 2 ranked stocks.",
            "Weight both selected stocks at 50%.",
            "Calculate completed-month returns open-to-open.",
            "Compound monthly returns to reconcile total return.",
            "Compare against QQQ adjusted-close and/or QQQ open-to-open benchmark returns.",
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
            family = "monospace" if raw_line.startswith("    ") else "sans-serif"
            ax.text(0.1, y, line, fontsize=10.5, va="top", family=family)
            y -= 0.026
        y -= 0.01

    pdf.savefig(fig)
    plt.close(fig)


def main() -> None:
    output = Path("reports/nasdaq100_top2_monthly_skip_momentum_strategy_package.pdf")
    output.parent.mkdir(parents=True, exist_ok=True)

    with PdfPages(output) as pdf:
        draw_page(
            pdf,
            TITLE,
            [
                "Structured strategy package for replication in other AI/backtesting tools.",
                "This version trades the top 2 stocks, not top 1.",
                "Includes rules, timing, return calculation, validation summary, caveats, and replication checklist.",
            ],
        )
        for title, lines in SECTIONS:
            draw_page(pdf, title, lines)

    print(output)


if __name__ == "__main__":
    main()
