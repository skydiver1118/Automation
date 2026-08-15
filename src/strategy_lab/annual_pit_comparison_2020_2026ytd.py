from __future__ import annotations

import io
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import yfinance as yf


START = date(2020, 1, 1)
END = date(2026, 5, 17)
PRICE_START = date(2019, 6, 1)
SP500_BASE_URL = "https://raw.githubusercontent.com/fja05680/sp500/master/"
SP500_HIST_FILE = "S%26P%20500%20Historical%20Components%20%26%20Changes.csv"
SP500_SINCE_FILE = "sp500_changes_since_2019.csv"
BENCHMARKS = ["SPMO", "VGT", "SMH", "QLD", "TQQQ", "SOXL"]
YEARS = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
YEAR_LABELS = {2026: "2026 YTD"}


def pct(value: float) -> str:
    return "" if pd.isna(value) else f"{value:.2%}"


def yahoo_symbol(symbol: str) -> str:
    return symbol.replace(".", "-")


def download_csv(url: str) -> pd.DataFrame:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text))


def load_sp500_timeline() -> list[tuple[date, frozenset[str]]]:
    hist_df = download_csv(SP500_BASE_URL + SP500_HIST_FILE)
    since_df = download_csv(SP500_BASE_URL + SP500_SINCE_FILE)
    hist_df.columns = [column.strip() for column in hist_df.columns]
    since_df.columns = [column.strip() for column in since_df.columns]

    date_col = hist_df.columns[0]
    ticker_col = hist_df.columns[1] if len(hist_df.columns) > 1 else hist_df.columns[0]
    snapshots: dict[date, set[str]] = {}
    for _, row in hist_df.iterrows():
        try:
            snapshot_date = pd.to_datetime(str(row[date_col])).date()
            tickers = {yahoo_symbol(t.strip()) for t in str(row[ticker_col]).split(",") if t.strip()}
            snapshots[snapshot_date] = tickers
        except Exception:
            continue

    add_col = [column for column in since_df.columns if "add" in column.lower()]
    rem_col = [column for column in since_df.columns if "remov" in column.lower() or "delet" in column.lower()]
    date_col2 = since_df.columns[0]
    additions: dict[date, set[str]] = {}
    removals: dict[date, set[str]] = {}
    for _, row in since_df.iterrows():
        try:
            change_date = pd.to_datetime(str(row[date_col2])).date()
            if add_col:
                additions.setdefault(change_date, set()).update(
                    yahoo_symbol(t.strip())
                    for t in str(row[add_col[0]]).split(",")
                    if t.strip() and t.strip() != "nan"
                )
            if rem_col:
                removals.setdefault(change_date, set()).update(
                    yahoo_symbol(t.strip())
                    for t in str(row[rem_col[0]]).split(",")
                    if t.strip() and t.strip() != "nan"
                )
        except Exception:
            continue

    base_date = max(snapshot_date for snapshot_date in snapshots if snapshot_date <= date(2019, 1, 1))
    current_members = set(snapshots[base_date])
    timeline = [(base_date, frozenset(current_members))]
    for change_date in sorted(set(additions) | set(removals)):
        if change_date < base_date:
            continue
        current_members = set(current_members)
        current_members |= additions.get(change_date, set())
        current_members -= removals.get(change_date, set())
        timeline.append((change_date, frozenset(current_members)))
    return timeline


def members_on(timeline: list[tuple[date, frozenset[str]]], query_date: pd.Timestamp) -> set[str]:
    query = query_date.date()
    members = set()
    for event_date, event_members in timeline:
        if event_date <= query:
            members = set(event_members)
        else:
            break
    return members


def month_boundaries(trading_days: pd.DatetimeIndex, start: date, end: date) -> list[tuple[str, pd.Timestamp, pd.Timestamp]]:
    out: list[tuple[str, pd.Timestamp, pd.Timestamp]] = []
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
            out.append((str(period), signal_date, trade_date))
    return out


def fetch_prices(tickers: list[str], start: date, end: date) -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = yf.download(
        tickers=sorted(tickers),
        start=start.isoformat(),
        end=(end + timedelta(days=1)).isoformat(),
        auto_adjust=True,
        progress=False,
        threads=True,
    )
    if raw.empty:
        raise RuntimeError("No prices downloaded")
    return raw["Open"].sort_index(), raw["Close"].sort_index()


def run_sp500_topn() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    timeline = load_sp500_timeline()
    tickers: set[str] = set(BENCHMARKS)
    for _, members in timeline:
        tickers.update(members)
    open_df, close_df = fetch_prices(list(tickers), PRICE_START, END)
    trading_days = close_df.index
    bounds = month_boundaries(trading_days, START, END)

    monthly_rows: list[dict[str, object]] = []
    equity_rows: list[dict[str, object]] = []
    equity_by_top = {1: 1.0, 2: 1.0, 3: 1.0}

    for month_index, (month, signal_date, trade_date) in enumerate(bounds):
        signal_index = trading_days.get_loc(signal_date)
        skip_index = signal_index - 21
        lookback_index = signal_index - 126
        if skip_index < 0 or lookback_index < 0:
            continue
        skip_date = trading_days[skip_index]
        lookback_date = trading_days[lookback_index]
        sp500_members = members_on(timeline, signal_date)
        next_trade = bounds[month_index + 1][2] if month_index < len(bounds) - 1 else None

        scores: dict[str, float] = {}
        for ticker in close_df.columns:
            if ticker in BENCHMARKS or ticker not in sp500_members:
                continue
            current = close_df.loc[skip_date, ticker]
            prior = close_df.loc[lookback_date, ticker]
            if pd.notna(current) and pd.notna(prior) and current > 0 and prior > 0:
                scores[str(ticker)] = float(current) / float(prior) - 1.0
        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)

        for top_n in [1, 2, 3]:
            selected = [ticker for ticker, _ in ranked[:top_n]]
            returns: list[float] = []
            for ticker in selected:
                entry = open_df.loc[trade_date, ticker] if ticker in open_df.columns else np.nan
                if next_trade is None:
                    available = close_df.loc[close_df.index >= trade_date, ticker].dropna()
                    exit_price = float(available.iloc[-1]) if len(available) else np.nan
                else:
                    exit_price = open_df.loc[next_trade, ticker] if ticker in open_df.columns else np.nan
                if pd.notna(entry) and pd.notna(exit_price) and entry > 0:
                    returns.append(float(exit_price) / float(entry) - 1.0)
            monthly_return = float(np.mean(returns)) if returns else np.nan
            if pd.notna(monthly_return):
                equity_by_top[top_n] *= 1.0 + monthly_return
            monthly_rows.append(
                {
                    "strategy": f"S&P 500 Top{top_n} PIT",
                    "top_n": top_n,
                    "month": month,
                    "trade_date": trade_date.date().isoformat(),
                    "tickers": ", ".join(selected),
                    "monthly_return": monthly_return,
                    "equity": equity_by_top[top_n],
                }
            )
            equity_rows.append(
                {
                    "strategy": f"S&P 500 Top{top_n} PIT",
                    "top_n": top_n,
                    "date": trade_date.date().isoformat(),
                    "equity": equity_by_top[top_n],
                    "period_return": monthly_return,
                }
            )

    monthly = pd.DataFrame(monthly_rows)
    annual = (
        monthly.assign(year=lambda frame: frame["month"].str[:4].astype(int))
        .groupby(["strategy", "top_n", "year"])["monthly_return"]
        .apply(lambda values: (1.0 + values.dropna()).prod() - 1.0)
        .reset_index(name="annual_return")
    )
    return annual, monthly, pd.DataFrame(equity_rows)


def annual_from_nasdaq_equity(path: Path) -> pd.DataFrame:
    equity = pd.read_csv(path)
    rows: list[dict[str, object]] = []
    for top_n in [1, 2, 3]:
        strategy = f"Nasdaq-100 Top{top_n} PIT membership"
        frame = equity[(equity["strategy"] == strategy) & (equity["top_n"] == top_n)].copy()
        frame["date"] = pd.to_datetime(frame["date"])
        frame = frame[(frame["date"].dt.date >= START) & (frame["date"].dt.date <= END)]
        frame["year"] = frame["date"].dt.year
        annual = frame.groupby("year")["daily_return"].apply(lambda values: (1.0 + values).prod() - 1.0)
        for year, annual_return in annual.items():
            rows.append(
                {
                    "strategy": f"Nasdaq-100 Top{top_n} PIT",
                    "top_n": top_n,
                    "year": int(year),
                    "annual_return": float(annual_return),
                }
            )
    return pd.DataFrame(rows)


def annual_benchmark_returns(symbols: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    open_df, close_df = fetch_prices(symbols, PRICE_START, END)
    bounds = month_boundaries(close_df.index, START, END)
    rows: list[dict[str, object]] = []
    equity_rows: list[dict[str, object]] = []
    for symbol in symbols:
        equity = 1.0
        for month_index, (month, _, trade_date) in enumerate(bounds):
            next_trade = bounds[month_index + 1][2] if month_index < len(bounds) - 1 else None
            entry = open_df.loc[trade_date, symbol]
            if next_trade is None:
                available = close_df.loc[close_df.index >= trade_date, symbol].dropna()
                exit_price = float(available.iloc[-1]) if len(available) else np.nan
            else:
                exit_price = open_df.loc[next_trade, symbol]
            monthly_return = float(exit_price) / float(entry) - 1.0 if pd.notna(entry) and pd.notna(exit_price) and entry > 0 else np.nan
            if pd.notna(monthly_return):
                equity *= 1.0 + monthly_return
            rows.append(
                {
                    "strategy": symbol,
                    "month": month,
                    "monthly_return": monthly_return,
                    "equity": equity,
                }
            )
            equity_rows.append(
                {
                    "strategy": symbol,
                    "date": trade_date.date().isoformat(),
                    "equity": equity,
                    "period_return": monthly_return,
                }
            )
    monthly = pd.DataFrame(rows)
    annual = (
        monthly.assign(year=lambda frame: frame["month"].str[:4].astype(int))
        .groupby(["strategy", "year"])["monthly_return"]
        .apply(lambda values: (1.0 + values.dropna()).prod() - 1.0)
        .reset_index(name="annual_return")
    )
    return annual, pd.DataFrame(equity_rows)


def drawdown_from_equity(equity: pd.Series) -> float:
    if equity.empty:
        return np.nan
    curve = pd.concat([pd.Series([1.0]), equity.reset_index(drop=True)], ignore_index=True)
    peaks = curve.cummax()
    return float((curve / peaks - 1.0).min())


def sharpe_from_monthly_returns(returns: pd.Series) -> float:
    clean = returns.dropna()
    if clean.empty:
        return np.nan
    std = clean.std(ddof=1)
    if pd.isna(std) or std == 0:
        return np.nan
    return float((clean.mean() / std) * np.sqrt(12))


def build_drawdown_table(sp_equity: pd.DataFrame, nasdaq_equity_path: Path, benchmark_equity: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for strategy, frame in sp_equity.groupby("strategy"):
        rows.append({"strategy": strategy, "max_drawdown": drawdown_from_equity(frame.sort_values("date")["equity"])})

    nasdaq = pd.read_csv(nasdaq_equity_path)
    for top_n in [1, 2, 3]:
        raw_strategy = f"Nasdaq-100 Top{top_n} PIT membership"
        frame = nasdaq[nasdaq["strategy"] == raw_strategy].copy()
        frame["date"] = pd.to_datetime(frame["date"])
        frame = frame[(frame["date"].dt.date >= START) & (frame["date"].dt.date <= END)].sort_values("date")
        rows.append(
            {
                "strategy": f"Nasdaq-100 Top{top_n} PIT",
                "max_drawdown": drawdown_from_equity(frame["equity"]),
            }
        )

    for strategy, frame in benchmark_equity.groupby("strategy"):
        rows.append({"strategy": strategy, "max_drawdown": drawdown_from_equity(frame.sort_values("date")["equity"])})
    return pd.DataFrame(rows)


def build_sharpe_table(sp_monthly: pd.DataFrame, nasdaq_equity_path: Path, benchmark_equity: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for strategy, frame in sp_monthly.groupby("strategy"):
        rows.append({"strategy": strategy, "sharpe_ratio": sharpe_from_monthly_returns(frame["monthly_return"])})

    nasdaq = pd.read_csv(nasdaq_equity_path)
    for top_n in [1, 2, 3]:
        raw_strategy = f"Nasdaq-100 Top{top_n} PIT membership"
        frame = nasdaq[nasdaq["strategy"] == raw_strategy].copy()
        frame["date"] = pd.to_datetime(frame["date"])
        frame = frame[(frame["date"].dt.date >= START) & (frame["date"].dt.date <= END)]
        frame["month"] = frame["date"].dt.to_period("M")
        monthly = frame.groupby("month")["daily_return"].apply(lambda values: (1.0 + values).prod() - 1.0)
        rows.append({"strategy": f"Nasdaq-100 Top{top_n} PIT", "sharpe_ratio": sharpe_from_monthly_returns(monthly)})

    for strategy, frame in benchmark_equity.groupby("strategy"):
        rows.append({"strategy": strategy, "sharpe_ratio": sharpe_from_monthly_returns(frame["period_return"])})
    return pd.DataFrame(rows)


def build_output_table(annual: pd.DataFrame, drawdowns: pd.DataFrame, sharpes: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    order = [
        "S&P 500 Top1 PIT",
        "S&P 500 Top2 PIT",
        "S&P 500 Top3 PIT",
        "Nasdaq-100 Top1 PIT",
        "Nasdaq-100 Top2 PIT",
        "Nasdaq-100 Top3 PIT",
        *BENCHMARKS,
    ]
    drawdown_by_strategy = drawdowns.set_index("strategy")["max_drawdown"].to_dict()
    sharpe_by_strategy = sharpes.set_index("strategy")["sharpe_ratio"].to_dict()
    rows: list[dict[str, object]] = []
    for strategy in order:
        strategy_annual = annual[annual["strategy"] == strategy].set_index("year")["annual_return"]
        row: dict[str, object] = {"Strategy": strategy}
        cumulative = 1.0
        available_years = 0
        for year in YEARS:
            value = strategy_annual.get(year, np.nan)
            label = YEAR_LABELS.get(year, str(year))
            row[label] = value
            if pd.notna(value):
                cumulative *= 1.0 + float(value)
                available_years += 1
        total_return = cumulative - 1.0
        elapsed_years = (END - START).days / 365.25
        row["Cumulative"] = total_return
        row["CAGR"] = cumulative ** (1.0 / elapsed_years) - 1.0 if cumulative > 0 else np.nan
        row["Max Drawdown"] = drawdown_by_strategy.get(strategy, np.nan)
        row["Sharpe Ratio"] = sharpe_by_strategy.get(strategy, np.nan)
        rows.append(row)

    raw = pd.DataFrame(rows)
    formatted = raw.copy()
    for column in [str(year) for year in YEARS[:-1]] + ["2026 YTD", "Cumulative", "CAGR", "Max Drawdown"]:
        formatted[column] = formatted[column].map(pct)
    formatted["Sharpe Ratio"] = formatted["Sharpe Ratio"].map(lambda value: "" if pd.isna(value) else f"{value:.2f}")
    return raw, formatted


def markdown_table(frame: pd.DataFrame) -> str:
    columns = list(frame.columns)
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
    for _, row in frame.iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in columns) + " |")
    return "\n".join(lines)


def main() -> None:
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    sp_annual, sp_monthly, sp_equity = run_sp500_topn()
    nasdaq_annual = annual_from_nasdaq_equity(
        report_dir / "nasdaq100_top1_top2_top3_point_in_time_membership_2020_2026ytd_equity_curve.csv"
    )
    benchmark_annual, benchmark_equity = annual_benchmark_returns(BENCHMARKS)
    annual = pd.concat([sp_annual, nasdaq_annual, benchmark_annual], ignore_index=True, sort=False)
    nasdaq_equity_path = report_dir / "nasdaq100_top1_top2_top3_point_in_time_membership_2020_2026ytd_equity_curve.csv"
    drawdowns = build_drawdown_table(sp_equity, nasdaq_equity_path, benchmark_equity)
    sharpes = build_sharpe_table(sp_monthly, nasdaq_equity_path, benchmark_equity)
    raw, formatted = build_output_table(annual, drawdowns, sharpes)

    base = "annual_returns_2020_2026ytd_pit_top123_vs_benchmarks"
    xlsx_path = report_dir / f"{base}.xlsx"
    md_path = report_dir / f"{base}.md"
    csv_path = report_dir / f"{base}.csv"

    raw.to_csv(csv_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        raw.to_excel(writer, sheet_name="Annual returns raw", index=False)
        formatted.to_excel(writer, sheet_name="Annual returns formatted", index=False)
        annual.to_excel(writer, sheet_name="Annual source", index=False)
        drawdowns.to_excel(writer, sheet_name="Drawdown source", index=False)
        sharpes.to_excel(writer, sheet_name="Sharpe source", index=False)
        sp_monthly.to_excel(writer, sheet_name="S&P monthly source", index=False)
        sp_equity.to_excel(writer, sheet_name="S&P equity source", index=False)
        workbook = writer.book
        for worksheet in workbook.worksheets:
            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions
            for column in worksheet.columns:
                letter = column[0].column_letter
                worksheet.column_dimensions[letter].width = 26 if letter == "A" else 14

    lines = [
        "# Annual Returns: PIT Momentum Strategies vs Benchmarks",
        "",
        f"Period: {START.isoformat()} through {END.isoformat()}.",
        "S&P 500 rows use fja05680/sp500 point-in-time constituents.",
        "Nasdaq-100 rows use the Nasdaq-100 changes-table point-in-time filter.",
        "Benchmark rows use adjusted open-to-open monthly returns; 2026 YTD uses latest available close for the unfinished month.",
        "CAGR is annualized across the full elapsed period from 2020-01-01 through 2026-05-17.",
        "",
        markdown_table(formatted),
        "",
        "## Output Files",
        "",
        f"- Excel workbook: `{xlsx_path}`",
        f"- CSV: `{csv_path}`",
        f"- Markdown report: `{md_path}`",
        "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(md_path)
    print(xlsx_path)
    print(formatted.to_string(index=False))


if __name__ == "__main__":
    main()
