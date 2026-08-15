from __future__ import annotations

from datetime import date, timedelta
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import yfinance as yf


IS_START = date(2010, 1, 1)
IS_END = date(2019, 12, 31)
OOS_START = date(2020, 1, 1)
OOS_END = date(2026, 5, 24)
PRICE_START = date(2008, 12, 1)

REPORT_DIR = Path("reports")
DATA_DIR = Path("data/smh_components")

HOLDING_URLS = {
    "SMH": "https://stockanalysis.com/etf/smh/holdings/",
    "SOXX": "https://stockanalysis.com/etf/soxx/holdings/",
}


def pct(value: float) -> str:
    return "" if pd.isna(value) else f"{value:.2%}"


def fetch_holdings() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for source, url in HOLDING_URLS.items():
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=30)
        response.raise_for_status()
        table = pd.read_html(StringIO(response.text))[0]
        table["source"] = source
        frames.append(table)
    holdings = pd.concat(frames, ignore_index=True)
    holdings["Symbol"] = holdings["Symbol"].astype(str).str.replace(".", "-", regex=False)
    holdings = holdings.drop_duplicates(["source", "Symbol"])
    return holdings


def fetch_prices(tickers: list[str], start: date, end: date) -> pd.DataFrame:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / f"adjusted_open_close_{start.isoformat()}_{end.isoformat()}.csv"
    if path.exists():
        return pd.read_csv(path, index_col=0, header=[0, 1], parse_dates=True).sort_index()

    raw = yf.download(
        tickers=sorted(tickers),
        start=start.isoformat(),
        end=(end + timedelta(days=1)).isoformat(),
        auto_adjust=True,
        progress=False,
        threads=True,
    )
    if raw.empty:
        raise RuntimeError("No price data downloaded")
    prices = pd.concat(
        [
            raw["Open"].rename_axis(columns=None).pipe(lambda frame: pd.concat({"Open": frame}, axis=1)),
            raw["Close"].rename_axis(columns=None).pipe(lambda frame: pd.concat({"Close": frame}, axis=1)),
        ],
        axis=1,
    ).sort_index()
    prices.to_csv(path)
    return prices


def month_boundaries(trading_days: pd.DatetimeIndex, start: date, end: date) -> list[tuple[str, pd.Timestamp, pd.Timestamp]]:
    bounds: list[tuple[str, pd.Timestamp, pd.Timestamp]] = []
    for period in pd.Series(trading_days).dt.to_period("M").unique():
        days = trading_days[trading_days.to_period("M") == period]
        if not len(days):
            continue
        trade_date = days[0]
        prior = trading_days[trading_days < trade_date]
        if not len(prior):
            continue
        signal_date = prior[-1]
        if pd.Timestamp(start) <= trade_date <= pd.Timestamp(end):
            bounds.append((str(period), signal_date, trade_date))
    return bounds


def metrics(monthly_returns: pd.Series, start: date, end: date) -> dict[str, float]:
    clean = monthly_returns.dropna()
    if clean.empty:
        return {"return": np.nan, "cagr": np.nan, "max_drawdown": np.nan, "sharpe": np.nan}
    equity = (1.0 + clean).cumprod()
    total_return = float(equity.iloc[-1] - 1.0)
    years = (end - start).days / 365.25
    cagr = float(equity.iloc[-1] ** (1.0 / years) - 1.0) if years > 0 and equity.iloc[-1] > 0 else np.nan
    curve = pd.concat([pd.Series([1.0]), equity.reset_index(drop=True)], ignore_index=True)
    drawdown = curve / curve.cummax() - 1.0
    max_dd = float(drawdown.min())
    std = clean.std(ddof=1)
    sharpe = float((clean.mean() / std) * np.sqrt(12)) if pd.notna(std) and std > 0 else np.nan
    return {"return": total_return, "cagr": cagr, "max_drawdown": max_dd, "sharpe": sharpe}


def precompute_months(open_prices: pd.DataFrame, close_prices: pd.DataFrame, universe: list[str]) -> list[dict[str, object]]:
    trading_days = close_prices.index
    bounds = month_boundaries(trading_days, IS_START, OOS_END)
    months: list[dict[str, object]] = []
    universe = [ticker for ticker in universe if ticker in close_prices.columns]

    for month_index, (month, signal_date, trade_date) in enumerate(bounds):
        signal_index = trading_days.get_loc(signal_date)
        next_trade = bounds[month_index + 1][2] if month_index < len(bounds) - 1 else None
        if next_trade is None:
            exit_prices = close_prices.loc[close_prices.index >= trade_date].ffill().iloc[-1]
        else:
            exit_prices = open_prices.loc[next_trade]
        entry_prices = open_prices.loc[trade_date]
        return_by_ticker = ((exit_prices / entry_prices - 1.0).replace([np.inf, -np.inf], np.nan)).dropna().to_dict()

        smh_sma100 = False
        smh_sma200 = False
        if "SMH" in close_prices.columns:
            if signal_index >= 99:
                smh_sma100 = bool(close_prices.loc[signal_date, "SMH"] > close_prices["SMH"].iloc[signal_index - 99 : signal_index + 1].mean())
            if signal_index >= 199:
                smh_sma200 = bool(close_prices.loc[signal_date, "SMH"] > close_prices["SMH"].iloc[signal_index - 199 : signal_index + 1].mean())

        sma200_ok = pd.Series(False, index=close_prices.columns)
        if signal_index >= 199:
            sma200 = close_prices.iloc[signal_index - 199 : signal_index + 1].mean()
            sma200_ok = close_prices.loc[signal_date] > sma200

        ranks: dict[tuple[int, int, str], list[str]] = {}
        for lookback in [63, 126, 252]:
            for skip in [0, 21]:
                skip_index = signal_index - skip
                lookback_index = signal_index - lookback
                if skip_index < 0 or lookback_index < 0:
                    ranks[(lookback, skip, "none")] = []
                    ranks[(lookback, skip, "sma200")] = []
                    continue
                scores = (close_prices.iloc[skip_index] / close_prices.iloc[lookback_index] - 1.0).replace(
                    [np.inf, -np.inf], np.nan
                )
                eligible = [ticker for ticker in universe if pd.notna(scores.get(ticker))]
                ranked = scores.loc[eligible].sort_values(ascending=False)
                ranks[(lookback, skip, "none")] = [str(ticker) for ticker in ranked.index]
                ranks[(lookback, skip, "sma200")] = [
                    str(ticker) for ticker in ranked.index if bool(sma200_ok.get(ticker, False))
                ]

        months.append(
            {
                "month": month,
                "trade_date": trade_date.date(),
                "period": "IS" if trade_date.date() < OOS_START else "OOS",
                "smh_sma100": smh_sma100,
                "smh_sma200": smh_sma200,
                "returns": {str(k): float(v) for k, v in return_by_ticker.items()},
                "ranks": ranks,
            }
        )
    return months


def run_strategy(config: dict[str, object], months: list[dict[str, object]]) -> pd.DataFrame:
    exposure = 0.0
    equity = 1.0
    rows: list[dict[str, object]] = []
    for info in months:
        use_sma_rank = config["cash_filter"] == "both_sma200"
        ranks = info["ranks"][(config["lookback"], config["skip"], "sma200" if use_sma_rank else "none")]
        risk_on = True
        if config["cash_filter"] == "smh_sma100":
            risk_on = bool(info["smh_sma100"])
        elif config["cash_filter"] == "smh_sma200":
            risk_on = bool(info["smh_sma200"])
        elif config["cash_filter"] == "both_sma200":
            risk_on = bool(info["smh_sma200"])

        selected = ranks[: int(config["top_n"])] if risk_on else []
        if not selected:
            exposure = 0.0
        elif int(config["dca_steps"]) <= 1:
            exposure = 1.0
        else:
            exposure = min(1.0, exposure + 1.0 / int(config["dca_steps"]))

        selected_returns = [info["returns"].get(ticker) for ticker in selected if ticker in info["returns"]]
        risky_return = float(np.mean(selected_returns)) if selected_returns else 0.0
        monthly_return = exposure * risky_return
        equity *= 1.0 + monthly_return
        rows.append(
            {
                **config,
                "strategy": strategy_name(config),
                "month": info["month"],
                "trade_date": info["trade_date"].isoformat(),
                "period": info["period"],
                "monthly_return": monthly_return,
                "equity": equity,
                "exposure": exposure,
                "tickers": ", ".join(selected) if selected else "CASH",
            }
        )
    return pd.DataFrame(rows)


def strategy_name(config: dict[str, object]) -> str:
    return (
        f"SMH_UNION Top{config['top_n']} L{config['lookback']} S{config['skip']} "
        f"{config['cash_filter']} DCA{config['dca_steps']}"
    )


def benchmark_monthly(open_prices: pd.DataFrame, close_prices: pd.DataFrame, symbol: str) -> pd.DataFrame:
    bounds = month_boundaries(close_prices.index, IS_START, OOS_END)
    equity = 1.0
    rows = []
    for month_index, (month, _, trade_date) in enumerate(bounds):
        next_trade = bounds[month_index + 1][2] if month_index < len(bounds) - 1 else None
        entry = open_prices.loc[trade_date, symbol]
        if next_trade is None:
            exit_price = close_prices.loc[close_prices.index >= trade_date, symbol].dropna().iloc[-1]
        else:
            exit_price = open_prices.loc[next_trade, symbol]
        monthly_return = float(exit_price) / float(entry) - 1.0
        equity *= 1.0 + monthly_return
        rows.append(
            {
                "strategy": symbol,
                "month": month,
                "trade_date": trade_date.date().isoformat(),
                "period": "IS" if trade_date.date() < OOS_START else "OOS",
                "monthly_return": monthly_return,
                "equity": equity,
            }
        )
    return pd.DataFrame(rows)


def markdown_table(frame: pd.DataFrame) -> str:
    cols = list(frame.columns)
    lines = ["| " + " | ".join(cols) + " |", "| " + " | ".join(["---"] * len(cols)) + " |"]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(str(row[col]) for col in cols) + " |")
    return "\n".join(lines)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    holdings = fetch_holdings()
    holdings.to_csv(DATA_DIR / "smh_soxx_current_holdings_union.csv", index=False)
    universe = sorted(set(holdings["Symbol"]) - {"SMH", "SOXX"})
    tickers = sorted(set(universe) | {"SMH", "SOXX"})
    prices = fetch_prices(tickers, PRICE_START, OOS_END)
    open_prices = prices["Open"].sort_index()
    close_prices = prices["Close"].sort_index()
    months = precompute_months(open_prices, close_prices, universe)

    configs = [
        {
            "top_n": top_n,
            "lookback": lookback,
            "skip": skip,
            "cash_filter": cash_filter,
            "dca_steps": dca_steps,
        }
        for top_n in [1, 2, 3, 5]
        for lookback in [63, 126, 252]
        for skip in [0, 21]
        for cash_filter in ["none", "smh_sma100", "smh_sma200", "both_sma200"]
        for dca_steps in [1, 3]
    ]

    summary_rows = []
    monthly_frames = []
    for config in configs:
        monthly = run_strategy(config, months)
        monthly_frames.append(monthly)
        is_metrics = metrics(monthly[monthly["period"] == "IS"]["monthly_return"], IS_START, IS_END)
        oos_metrics = metrics(monthly[monthly["period"] == "OOS"]["monthly_return"], OOS_START, OOS_END)
        summary_rows.append(
            {
                "strategy": strategy_name(config),
                "passed_is_dd_lt_50": is_metrics["max_drawdown"] > -0.50 if pd.notna(is_metrics["max_drawdown"]) else False,
                **config,
                "is_return": is_metrics["return"],
                "is_cagr": is_metrics["cagr"],
                "is_max_drawdown": is_metrics["max_drawdown"],
                "is_sharpe": is_metrics["sharpe"],
                "oos_return": oos_metrics["return"],
                "oos_cagr": oos_metrics["cagr"],
                "oos_max_drawdown": oos_metrics["max_drawdown"],
                "oos_sharpe": oos_metrics["sharpe"],
            }
        )

    summary = pd.DataFrame(summary_rows)
    passed = summary[summary["passed_is_dd_lt_50"]].sort_values(
        ["is_sharpe", "is_return"], ascending=False
    )
    top3 = passed.head(3).copy()
    all_monthly = pd.concat(monthly_frames, ignore_index=True)
    top_monthly = all_monthly[all_monthly["strategy"].isin(top3["strategy"])]

    smh_monthly = benchmark_monthly(open_prices, close_prices, "SMH")
    smh_is = metrics(smh_monthly[smh_monthly["period"] == "IS"]["monthly_return"], IS_START, IS_END)
    smh_oos = metrics(smh_monthly[smh_monthly["period"] == "OOS"]["monthly_return"], OOS_START, OOS_END)
    benchmark = pd.DataFrame(
        [
            {
                "strategy": "SMH buy-and-hold monthly open-to-open",
                "is_return": smh_is["return"],
                "is_cagr": smh_is["cagr"],
                "is_max_drawdown": smh_is["max_drawdown"],
                "is_sharpe": smh_is["sharpe"],
                "oos_return": smh_oos["return"],
                "oos_cagr": smh_oos["cagr"],
                "oos_max_drawdown": smh_oos["max_drawdown"],
                "oos_sharpe": smh_oos["sharpe"],
            }
        ]
    )

    formatted = top3.copy()
    benchmark_formatted = benchmark.copy()
    for frame in [formatted, benchmark_formatted]:
        for col in ["is_return", "is_cagr", "is_max_drawdown", "oos_return", "oos_cagr", "oos_max_drawdown"]:
            frame[col] = frame[col].map(pct)
        for col in ["is_sharpe", "oos_sharpe"]:
            frame[col] = frame[col].map(lambda value: "" if pd.isna(value) else f"{value:.2f}")

    base = "smh_soxx_components_momentum_is2010_2019_oos2020_2026ytd"
    xlsx_path = REPORT_DIR / f"{base}.xlsx"
    csv_path = REPORT_DIR / f"{base}.csv"
    md_path = REPORT_DIR / f"{base}.md"
    summary.to_csv(csv_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="All candidates raw", index=False)
        passed.to_excel(writer, sheet_name="Passed IS DD raw", index=False)
        formatted.to_excel(writer, sheet_name="Top3 formatted", index=False)
        top_monthly.to_excel(writer, sheet_name="Top3 monthly details", index=False)
        benchmark.to_excel(writer, sheet_name="SMH benchmark raw", index=False)
        holdings.to_excel(writer, sheet_name="Holdings source", index=False)
        workbook = writer.book
        for worksheet in workbook.worksheets:
            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions
            for column in worksheet.columns:
                letter = column[0].column_letter
                worksheet.column_dimensions[letter].width = 38 if letter in {"A", "B", "C"} else 16

    display_cols = [
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
        "# SMH/SOXX Components Momentum IS/OOS Search",
        "",
        f"In-sample: {IS_START.isoformat()} to {IS_END.isoformat()}.",
        f"Out-of-sample: {OOS_START.isoformat()} to latest available data through {OOS_END.isoformat()}.",
        "Universe: current SMH holdings union current SOXX holdings, treated as the semiconductor index universe.",
        "Execution: monthly signal after prior month-end close; trade at next month first open; final open position marked to latest close.",
        "Score: Close[t-skip] / Close[t-lookback] - 1.",
        "Cash/DCA tested: no cash filter, SMH SMA100, SMH SMA200, SMH SMA200 plus selected stocks above SMA200; DCA1 and DCA3.",
        f"Holdings count in union: {len(universe)}. Candidates tested: {len(summary)}. Passed IS max drawdown < 50%: {len(passed)}.",
        "",
        "## Top 3 Strategies by IS Sharpe",
        "",
        markdown_table(formatted[display_cols]),
        "",
        "## SMH Benchmark",
        "",
        markdown_table(benchmark_formatted[display_cols]),
        "",
        "## Output Files",
        "",
        f"- Excel workbook: `{xlsx_path}`",
        f"- CSV: `{csv_path}`",
        f"- Markdown report: `{md_path}`",
        "",
        "Important limitation: this uses current SMH/SOXX holdings, not historical holdings, because a clean long-run historical holdings file was not available. This can introduce survivorship/constituent lookahead bias.",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(md_path)
    print(xlsx_path)
    print(f"holdings={len(universe)} candidates={len(summary)} passed={len(passed)}")
    print(formatted[display_cols].to_string(index=False))
    print("SMH benchmark")
    print(benchmark_formatted[display_cols].to_string(index=False))


if __name__ == "__main__":
    main()
