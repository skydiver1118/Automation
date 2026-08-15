from __future__ import annotations

from dataclasses import asdict

import numpy as np
import pandas as pd

from src.strategy_lab.momentum_is_oos_research import (
    DATA_DIR,
    IS_END,
    IS_START,
    OOS_END,
    OOS_START,
    PRICE_START,
    REPORT_DIR,
    StrategyConfig,
    fetch_prices,
    load_nasdaq100_current_and_changes,
    load_sp500_timeline,
    members_from_timeline,
    month_boundaries,
    nasdaq_members_on,
    pct,
    strategy_metrics,
    universe_tickers_from_membership,
)


LOOKBACKS = [63, 126, 252]
SKIPS = [0, 21]
TOP_NS = [1, 2, 3, 5]
CASH_FILTERS = ["none", "benchmark_sma200", "benchmark_sma100", "both_sma200"]
DCA_STEPS = [1, 3]
UNIVERSES = ["SP500", "NASDAQ100"]


def benchmark_for_universe(universe: str) -> str:
    return "SPY" if universe == "SP500" else "QQQ"


def precompute_months(
    open_prices: pd.DataFrame,
    close_prices: pd.DataFrame,
    sp500_timeline,
    nasdaq_current,
    nasdaq_changes,
) -> list[dict[str, object]]:
    trading_days = close_prices.index
    bounds = month_boundaries(trading_days, IS_START, OOS_END)
    months: list[dict[str, object]] = []

    for month_index, (month, signal_date, trade_date) in enumerate(bounds):
        signal_index = trading_days.get_loc(signal_date)
        next_trade = bounds[month_index + 1][2] if month_index < len(bounds) - 1 else None
        universe_members = {
            "SP500": set(close_prices.columns.astype(str)).intersection(members_from_timeline(sp500_timeline, signal_date)),
            "NASDAQ100": set(close_prices.columns.astype(str)).intersection(
                nasdaq_members_on(nasdaq_current, nasdaq_changes, signal_date)
            ),
        }

        if next_trade is None:
            exit_prices = close_prices.loc[close_prices.index >= trade_date].ffill().iloc[-1]
        else:
            exit_prices = open_prices.loc[next_trade]
        entry_prices = open_prices.loc[trade_date]
        return_series = (exit_prices / entry_prices - 1.0).replace([np.inf, -np.inf], np.nan).dropna()
        return_by_ticker = {str(ticker): float(value) for ticker, value in return_series.items()}

        risk: dict[tuple[str, int], bool] = {}
        for benchmark in ["SPY", "QQQ"]:
            risk[(benchmark, 100)] = False
            risk[(benchmark, 200)] = False
            if benchmark in close_prices.columns:
                if signal_index >= 99:
                    risk[(benchmark, 100)] = bool(
                        close_prices.loc[signal_date, benchmark]
                        > close_prices[benchmark].iloc[signal_index - 99 : signal_index + 1].mean()
                    )
                if signal_index >= 199:
                    risk[(benchmark, 200)] = bool(
                        close_prices.loc[signal_date, benchmark]
                        > close_prices[benchmark].iloc[signal_index - 199 : signal_index + 1].mean()
                    )

        sma200_ok = pd.Series(False, index=close_prices.columns)
        if signal_index >= 199:
            sma200 = close_prices.iloc[signal_index - 199 : signal_index + 1].mean()
            sma200_ok = close_prices.loc[signal_date] > sma200

        ranks: dict[tuple[str, int, int, str], list[str]] = {}
        for universe in UNIVERSES:
            members = universe_members[universe]
            for lookback in LOOKBACKS:
                for skip in SKIPS:
                    skip_index = signal_index - skip
                    lookback_index = signal_index - lookback
                    if skip_index < 0 or lookback_index < 0:
                        ranks[(universe, lookback, skip, "none")] = []
                        ranks[(universe, lookback, skip, "sma200")] = []
                        continue
                    scores = (close_prices.iloc[skip_index] / close_prices.iloc[lookback_index] - 1.0).replace(
                        [np.inf, -np.inf], np.nan
                    )
                    eligible = [
                        ticker
                        for ticker in scores.dropna().index.astype(str)
                        if ticker in members and ticker not in {"SPY", "QQQ"}
                    ]
                    ranked = scores.loc[eligible].dropna().sort_values(ascending=False)
                    ranks[(universe, lookback, skip, "none")] = [str(ticker) for ticker in ranked.index]
                    ranks[(universe, lookback, skip, "sma200")] = [
                        str(ticker) for ticker in ranked.index if bool(sma200_ok.get(ticker, False))
                    ]

        months.append(
            {
                "month": month,
                "trade_date": trade_date.date(),
                "period": "IS" if trade_date.date() < OOS_START else "OOS",
                "risk": risk,
                "returns": return_by_ticker,
                "ranks": ranks,
            }
        )
    return months


def run_config(config: StrategyConfig, months: list[dict[str, object]]) -> pd.DataFrame:
    exposure = 0.0
    equity = 1.0
    rows: list[dict[str, object]] = []
    benchmark = benchmark_for_universe(config.universe)

    for info in months:
        use_sma_rank = config.cash_filter == "both_sma200"
        ranks = info["ranks"][(config.universe, config.lookback, config.skip, "sma200" if use_sma_rank else "none")]

        risk_on = True
        if config.cash_filter == "benchmark_sma200":
            risk_on = bool(info["risk"][(benchmark, 200)])
        elif config.cash_filter == "benchmark_sma100":
            risk_on = bool(info["risk"][(benchmark, 100)])
        elif config.cash_filter == "both_sma200":
            risk_on = bool(info["risk"][(benchmark, 200)])

        selected = ranks[: config.top_n] if risk_on else []
        if not selected:
            exposure = 0.0
        elif config.dca_steps <= 1:
            exposure = 1.0
        else:
            exposure = min(1.0, exposure + 1.0 / config.dca_steps)

        returns = [info["returns"].get(ticker) for ticker in selected if ticker in info["returns"]]
        risky_return = float(np.mean(returns)) if returns else 0.0
        monthly_return = exposure * risky_return
        equity *= 1.0 + monthly_return
        rows.append(
            {
                "strategy": config.name,
                "month": info["month"],
                "trade_date": info["trade_date"].isoformat(),
                "period": info["period"],
                "monthly_return": monthly_return,
                "equity": equity,
                **asdict(config),
                "exposure": exposure,
                "tickers": ", ".join(selected) if selected else "CASH",
            }
        )
    return pd.DataFrame(rows)


def markdown_table(frame: pd.DataFrame) -> str:
    columns = list(frame.columns)
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("loading point-in-time membership", flush=True)
    sp500_timeline = load_sp500_timeline()
    nasdaq_current, nasdaq_changes = load_nasdaq100_current_and_changes()
    tickers = universe_tickers_from_membership(sp500_timeline, nasdaq_current, nasdaq_changes)

    print("loading prices from cache", flush=True)
    prices = fetch_prices(sorted(tickers), PRICE_START, OOS_END)
    open_prices = prices["Open"].sort_index()
    close_prices = prices["Close"].sort_index()

    print("precomputing monthly ranks and returns", flush=True)
    months = precompute_months(open_prices, close_prices, sp500_timeline, nasdaq_current, nasdaq_changes)

    configs = [
        StrategyConfig(universe, top_n, lookback, skip, cash_filter, dca_steps)
        for universe in UNIVERSES
        for top_n in TOP_NS
        for lookback in LOOKBACKS
        for skip in SKIPS
        for cash_filter in CASH_FILTERS
        for dca_steps in DCA_STEPS
    ]

    summary_rows: list[dict[str, object]] = []
    details: list[pd.DataFrame] = []
    print(f"running {len(configs)} configs", flush=True)
    for config in configs:
        monthly = run_config(config, months)
        is_returns = monthly[monthly["period"] == "IS"]["monthly_return"]
        oos_returns = monthly[monthly["period"] == "OOS"]["monthly_return"]
        is_metrics = strategy_metrics(is_returns, IS_START, IS_END)
        oos_metrics = strategy_metrics(oos_returns, OOS_START, OOS_END)
        passed = pd.notna(is_metrics["max_drawdown"]) and is_metrics["max_drawdown"] > -0.50
        summary_rows.append(
            {
                "strategy": config.name,
                "passed_is_dd_lt_50": passed,
                **asdict(config),
                "is_return": is_metrics["return"],
                "is_cagr": is_metrics["cagr"],
                "is_max_drawdown": is_metrics["max_drawdown"],
                "is_sharpe": is_metrics["sharpe"],
                "is_calmar": is_metrics["calmar"],
                "oos_return": oos_metrics["return"],
                "oos_cagr": oos_metrics["cagr"],
                "oos_max_drawdown": oos_metrics["max_drawdown"],
                "oos_sharpe": oos_metrics["sharpe"],
                "oos_calmar": oos_metrics["calmar"],
            }
        )
        details.append(monthly)

    summary = pd.DataFrame(summary_rows)
    passed = summary[summary["passed_is_dd_lt_50"]].copy()
    top_by_universe = (
        passed.sort_values(["universe", "is_sharpe", "is_calmar", "is_return"], ascending=[True, False, False, False])
        .groupby("universe")
        .head(20)
    )
    selected_strategies = (
        passed.sort_values(["universe", "is_sharpe", "is_calmar"], ascending=[True, False, False])
        .groupby("universe")
        .head(5)["strategy"]
    )
    all_monthly = pd.concat(details, ignore_index=True)
    top_monthly = all_monthly[all_monthly["strategy"].isin(selected_strategies)]

    formatted = top_by_universe.copy()
    for column in [
        "is_return",
        "is_cagr",
        "is_max_drawdown",
        "oos_return",
        "oos_cagr",
        "oos_max_drawdown",
    ]:
        formatted[column] = formatted[column].map(pct)
    for column in ["is_sharpe", "is_calmar", "oos_sharpe", "oos_calmar"]:
        formatted[column] = formatted[column].map(lambda value: "" if pd.isna(value) else f"{value:.2f}")

    base = "momentum_is2010_2019_oos2020_2026ytd_separate_sp500_nasdaq_cash_dca"
    xlsx_path = REPORT_DIR / f"{base}.xlsx"
    csv_path = REPORT_DIR / f"{base}.csv"
    md_path = REPORT_DIR / f"{base}.md"
    summary.to_csv(csv_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="All candidates raw", index=False)
        passed.to_excel(writer, sheet_name="Passed IS DD raw", index=False)
        formatted.to_excel(writer, sheet_name="Top20 each formatted", index=False)
        top_monthly.to_excel(writer, sheet_name="Top5 each monthly", index=False)
        workbook = writer.book
        for worksheet in workbook.worksheets:
            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions
            for column in worksheet.columns:
                letter = column[0].column_letter
                worksheet.column_dimensions[letter].width = 36 if letter in {"A", "B"} else 16

    display_cols = [
        "universe",
        "strategy",
        "is_return",
        "is_cagr",
        "is_max_drawdown",
        "is_sharpe",
        "oos_return",
        "oos_cagr",
        "oos_max_drawdown",
        "oos_sharpe",
    ]
    lines = [
        "# Separate Momentum IS/OOS Strategy Search",
        "",
        f"In-sample: {IS_START.isoformat()} to {IS_END.isoformat()}.",
        f"Out-of-sample: {OOS_START.isoformat()} to latest available data through {OOS_END.isoformat()}.",
        "Universes searched separately: point-in-time S&P 500 and reconstructed point-in-time Nasdaq-100.",
        "Execution: monthly signal after prior month-end close; trade at next month first open; final open position marked to latest close.",
        "Score: Close[t-skip] / Close[t-lookback] - 1.",
        "Cash/DCA tested: no cash filter, universe benchmark SMA100/SMA200, benchmark SMA200 plus selected stocks above SMA200; DCA1 and DCA3.",
        f"Candidates tested: {len(summary)}. Passed IS max drawdown < 50%: {len(passed)}.",
        "",
        "## Top Passed Candidates by Universe Ranked by IS Sharpe",
        "",
        markdown_table(formatted[display_cols]),
        "",
        "## Output Files",
        "",
        f"- Excel workbook: `{xlsx_path}`",
        f"- CSV: `{csv_path}`",
        f"- Markdown report: `{md_path}`",
        "",
        "Important limitations: delisted tickers with no Yahoo price history are skipped implicitly; Nasdaq-100 point-in-time membership is reconstructed from Wikipedia's current members and changes table.",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(md_path)
    print(xlsx_path)
    print(f"candidates={len(summary)} passed={len(passed)}")
    print(formatted[display_cols].groupby("universe").head(5).to_string(index=False))


if __name__ == "__main__":
    main()
