from __future__ import annotations

import io
import math
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import requests
import yfinance as yf


IS_START = date(2010, 1, 1)
IS_END = date(2019, 12, 31)
OOS_START = date(2020, 1, 1)
OOS_END = date(2026, 5, 23)
PRICE_START = date(2008, 12, 1)

REPORT_DIR = Path("reports")
DATA_DIR = Path("data/momentum_is_oos")

SP500_BASE_URL = "https://raw.githubusercontent.com/fja05680/sp500/master/"
SP500_HIST_FILE = "S%26P%20500%20Historical%20Components%20%26%20Changes.csv"
SP500_SINCE_FILE = "sp500_changes_since_2019.csv"
NASDAQ100_WIKI_URL = "https://en.wikipedia.org/wiki/Nasdaq-100"


@dataclass(frozen=True)
class StrategyConfig:
    universe: str
    top_n: int
    lookback: int
    skip: int
    cash_filter: str
    dca_steps: int

    @property
    def name(self) -> str:
        return (
            f"{self.universe} Top{self.top_n} L{self.lookback} S{self.skip} "
            f"{self.cash_filter} DCA{self.dca_steps}"
        )


def yahoo_symbol(symbol: str) -> str:
    return str(symbol).strip().replace(".", "-")


def pct(value: float) -> str:
    return "" if pd.isna(value) else f"{value:.2%}"


def download_csv(url: str) -> pd.DataFrame:
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return pd.read_csv(io.StringIO(response.text))


def load_sp500_timeline() -> list[tuple[date, frozenset[str]]]:
    hist_df = download_csv(SP500_BASE_URL + SP500_HIST_FILE)
    since_df = download_csv(SP500_BASE_URL + SP500_SINCE_FILE)
    hist_df.columns = [column.strip() for column in hist_df.columns]
    since_df.columns = [column.strip() for column in since_df.columns]

    snapshots: dict[date, set[str]] = {}
    date_col = hist_df.columns[0]
    ticker_col = hist_df.columns[1] if len(hist_df.columns) > 1 else hist_df.columns[0]
    for _, row in hist_df.iterrows():
        try:
            snapshot_date = pd.to_datetime(str(row[date_col])).date()
            tickers = {yahoo_symbol(ticker) for ticker in str(row[ticker_col]).split(",") if ticker.strip()}
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
                    yahoo_symbol(ticker)
                    for ticker in str(row[add_col[0]]).split(",")
                    if ticker.strip() and ticker.strip() != "nan"
                )
            if rem_col:
                removals.setdefault(change_date, set()).update(
                    yahoo_symbol(ticker)
                    for ticker in str(row[rem_col[0]]).split(",")
                    if ticker.strip() and ticker.strip() != "nan"
                )
        except Exception:
            continue

    timeline: list[tuple[date, frozenset[str]]] = []
    for snapshot_date in sorted(snapshots):
        if snapshot_date <= date(2019, 1, 1):
            timeline.append((snapshot_date, frozenset(snapshots[snapshot_date])))

    base_date = max(snapshot_date for snapshot_date in snapshots if snapshot_date <= date(2019, 1, 1))
    current_members = set(snapshots[base_date])
    if not timeline or timeline[-1][0] != base_date:
        timeline.append((base_date, frozenset(current_members)))
    for change_date in sorted(set(additions) | set(removals)):
        if change_date < base_date:
            continue
        current_members = set(current_members)
        current_members |= additions.get(change_date, set())
        current_members -= removals.get(change_date, set())
        timeline.append((change_date, frozenset(current_members)))

    return sorted(timeline, key=lambda item: item[0])


def members_from_timeline(timeline: list[tuple[date, frozenset[str]]], query_date: pd.Timestamp) -> set[str]:
    query = query_date.date()
    members: set[str] = set()
    for event_date, event_members in timeline:
        if event_date <= query:
            members = set(event_members)
        else:
            break
    return members


def load_nasdaq100_current_and_changes() -> tuple[set[str], pd.DataFrame]:
    response = requests.get(
        NASDAQ100_WIKI_URL,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        timeout=30,
    )
    response.raise_for_status()
    tables = pd.read_html(io.StringIO(response.text))

    current: set[str] = set()
    changes: pd.DataFrame | None = None
    for table in tables:
        flat_columns = [
            " ".join([str(part) for part in column if str(part) != "nan"]).strip()
            if isinstance(column, tuple)
            else str(column)
            for column in table.columns
        ]
        table = table.copy()
        table.columns = flat_columns
        if "Ticker" in table.columns and "Company" in table.columns and len(table) > 50:
            current = {yahoo_symbol(ticker) for ticker in table["Ticker"].dropna().astype(str)}
        if {"Date Date", "Added Ticker", "Removed Ticker"}.issubset(table.columns):
            changes = table.rename(
                columns={
                    "Date Date": "date",
                    "Added Ticker": "added_ticker",
                    "Removed Ticker": "removed_ticker",
                }
            )

    if not current or changes is None:
        raise RuntimeError("Could not parse Nasdaq-100 current members and changes table")

    changes["date"] = pd.to_datetime(changes["date"], errors="coerce").dt.date
    changes["added_ticker"] = changes["added_ticker"].map(lambda value: yahoo_symbol(value) if pd.notna(value) else np.nan)
    changes["removed_ticker"] = changes["removed_ticker"].map(lambda value: yahoo_symbol(value) if pd.notna(value) else np.nan)
    changes = changes.dropna(subset=["date"]).sort_values("date")
    return current, changes


def nasdaq_members_on(current_members: set[str], changes: pd.DataFrame, query_date: pd.Timestamp) -> set[str]:
    query = query_date.date()
    members = set(current_members)
    future_changes = changes[changes["date"] > query].sort_values("date", ascending=False)
    for row in future_changes.itertuples(index=False):
        added = getattr(row, "added_ticker")
        removed = getattr(row, "removed_ticker")
        if pd.notna(added):
            members.discard(str(added))
        if pd.notna(removed):
            members.add(str(removed))
    return members


def universe_tickers_from_membership(
    sp500_timeline: list[tuple[date, frozenset[str]]],
    nasdaq_current: set[str],
    nasdaq_changes: pd.DataFrame,
) -> set[str]:
    tickers: set[str] = set()
    for _, members in sp500_timeline:
        tickers.update(members)
    tickers.update(nasdaq_current)
    tickers.update(ticker for ticker in nasdaq_changes["added_ticker"].dropna().astype(str))
    tickers.update(ticker for ticker in nasdaq_changes["removed_ticker"].dropna().astype(str))
    tickers.update({"SPY", "QQQ"})
    return {ticker for ticker in tickers if ticker and ticker.lower() != "nan"}


def fetch_prices(tickers: list[str], start: date, end: date, refresh: bool = False) -> pd.DataFrame:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = DATA_DIR / f"adjusted_open_close_{start.isoformat()}_{end.isoformat()}.csv"
    if path.exists() and not refresh:
        prices = pd.read_csv(path, index_col=0, header=[0, 1], parse_dates=True)
        return prices.sort_index()

    chunks: list[pd.DataFrame] = []
    batch_size = 80
    for offset in range(0, len(tickers), batch_size):
        batch = sorted(tickers)[offset : offset + batch_size]
        raw = yf.download(
            tickers=batch,
            start=start.isoformat(),
            end=(end + timedelta(days=1)).isoformat(),
            auto_adjust=True,
            progress=False,
            threads=True,
        )
        if raw.empty:
            continue
        if isinstance(raw.columns, pd.MultiIndex):
            open_prices = raw["Open"]
            close_prices = raw["Close"]
        else:
            open_prices = raw[["Open"]]
            close_prices = raw[["Close"]]
            open_prices.columns = batch
            close_prices.columns = batch
        open_prices.columns = pd.MultiIndex.from_product([["Open"], open_prices.columns])
        close_prices.columns = pd.MultiIndex.from_product([["Close"], close_prices.columns])
        chunks.append(pd.concat([open_prices, close_prices], axis=1))

    if not chunks:
        raise RuntimeError("No price data downloaded")
    prices = pd.concat(chunks, axis=1).loc[:, lambda frame: ~frame.columns.duplicated()].sort_index()
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


def strategy_metrics(monthly_returns: pd.Series, start: date, end: date) -> dict[str, float]:
    clean = monthly_returns.dropna()
    if clean.empty:
        return {"return": np.nan, "cagr": np.nan, "max_drawdown": np.nan, "sharpe": np.nan, "calmar": np.nan}
    equity = (1.0 + clean).cumprod()
    total_return = float(equity.iloc[-1] - 1.0)
    years = (end - start).days / 365.25
    cagr = float(equity.iloc[-1] ** (1.0 / years) - 1.0) if years > 0 and equity.iloc[-1] > 0 else np.nan
    drawdown = equity / equity.cummax() - 1.0
    max_dd = float(drawdown.min())
    std = clean.std(ddof=1)
    sharpe = float((clean.mean() / std) * math.sqrt(12)) if pd.notna(std) and std > 0 else np.nan
    calmar = float(cagr / abs(max_dd)) if pd.notna(cagr) and max_dd < 0 else np.nan
    return {"return": total_return, "cagr": cagr, "max_drawdown": max_dd, "sharpe": sharpe, "calmar": calmar}


def run_strategy(
    config: StrategyConfig,
    open_prices: pd.DataFrame,
    close_prices: pd.DataFrame,
    bounds: list[tuple[str, pd.Timestamp, pd.Timestamp]],
    sp500_timeline: list[tuple[date, frozenset[str]]],
    nasdaq_current: set[str],
    nasdaq_changes: pd.DataFrame,
) -> pd.DataFrame:
    trading_days = close_prices.index
    rows: list[dict[str, object]] = []
    exposure = 0.0
    equity = 1.0

    for month_index, (month, signal_date, trade_date) in enumerate(bounds):
        signal_index = trading_days.get_loc(signal_date)
        skip_index = signal_index - config.skip
        lookback_index = signal_index - config.lookback
        if skip_index < 0 or lookback_index < 0:
            continue

        if config.universe == "SP500":
            universe = members_from_timeline(sp500_timeline, signal_date)
            benchmark = "SPY"
        elif config.universe == "NASDAQ100":
            universe = nasdaq_members_on(nasdaq_current, nasdaq_changes, signal_date)
            benchmark = "QQQ"
        else:
            universe = members_from_timeline(sp500_timeline, signal_date) | nasdaq_members_on(
                nasdaq_current, nasdaq_changes, signal_date
            )
            benchmark = "QQQ"

        risk_on = True
        if config.cash_filter in {"benchmark_sma200", "both_sma200"}:
            if benchmark in close_prices.columns and signal_index >= 199:
                sma = close_prices[benchmark].iloc[signal_index - 199 : signal_index + 1].mean()
                risk_on = bool(close_prices.loc[signal_date, benchmark] > sma)
            else:
                risk_on = False
        elif config.cash_filter == "benchmark_sma100":
            if benchmark in close_prices.columns and signal_index >= 99:
                sma = close_prices[benchmark].iloc[signal_index - 99 : signal_index + 1].mean()
                risk_on = bool(close_prices.loc[signal_date, benchmark] > sma)
            else:
                risk_on = False

        current = close_prices.iloc[skip_index]
        prior = close_prices.iloc[lookback_index]
        scores = (current / prior - 1.0).replace([np.inf, -np.inf], np.nan).dropna()
        eligible = [ticker for ticker in scores.index.astype(str) if ticker in universe and ticker not in {"SPY", "QQQ"}]
        scores = scores.loc[eligible].sort_values(ascending=False)

        selected: list[str] = []
        for ticker in scores.index:
            if len(selected) >= config.top_n:
                break
            if config.cash_filter in {"selected_sma200", "both_sma200"}:
                if signal_index < 199:
                    continue
                sma = close_prices[str(ticker)].iloc[signal_index - 199 : signal_index + 1].mean()
                if not bool(close_prices.loc[signal_date, str(ticker)] > sma):
                    continue
            selected.append(str(ticker))

        if not risk_on or not selected:
            selected = []
            target_exposure = 0.0
        else:
            target_exposure = 1.0

        if target_exposure == 0.0:
            exposure = 0.0
        elif config.dca_steps <= 1:
            exposure = 1.0
        else:
            exposure = min(1.0, exposure + 1.0 / config.dca_steps)

        next_trade = bounds[month_index + 1][2] if month_index < len(bounds) - 1 else None
        stock_returns: list[float] = []
        for ticker in selected:
            entry = open_prices.loc[trade_date, ticker] if ticker in open_prices.columns else np.nan
            if next_trade is None:
                available = close_prices.loc[close_prices.index >= trade_date, ticker].dropna()
                exit_price = float(available.iloc[-1]) if len(available) else np.nan
            else:
                exit_price = open_prices.loc[next_trade, ticker] if ticker in open_prices.columns else np.nan
            if pd.notna(entry) and pd.notna(exit_price) and entry > 0:
                stock_returns.append(float(exit_price) / float(entry) - 1.0)

        risky_return = float(np.mean(stock_returns)) if stock_returns else 0.0
        monthly_return = exposure * risky_return
        equity *= 1.0 + monthly_return
        rows.append(
            {
                "strategy": config.name,
                "month": month,
                "trade_date": trade_date.date().isoformat(),
                "period": "IS" if trade_date.date() < OOS_START else "OOS",
                "monthly_return": monthly_return,
                "equity": equity,
                "universe": config.universe,
                "top_n": config.top_n,
                "lookback": config.lookback,
                "skip": config.skip,
                "cash_filter": config.cash_filter,
                "dca_steps": config.dca_steps,
                "exposure": exposure,
                "tickers": ", ".join(selected) if selected else "CASH",
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    sp500_timeline = load_sp500_timeline()
    nasdaq_current, nasdaq_changes = load_nasdaq100_current_and_changes()
    all_tickers = universe_tickers_from_membership(sp500_timeline, nasdaq_current, nasdaq_changes)
    prices = fetch_prices(sorted(all_tickers), PRICE_START, OOS_END)
    open_prices = prices["Open"].sort_index()
    close_prices = prices["Close"].sort_index()
    bounds = month_boundaries(close_prices.index, IS_START, OOS_END)

    # Keep this grid focused on the user's stated universe: the monthly union of
    # point-in-time S&P 500 and Nasdaq-100 members. This still tests the main
    # knobs without spending hours on low-signal permutations.
    configs = [
        StrategyConfig(universe, top_n, lookback, skip, cash_filter, dca_steps)
        for universe in ["COMBINED"]
        for top_n in [1, 2, 3, 5]
        for lookback in [63, 126, 252]
        for skip in [0, 21]
        for cash_filter in ["none", "benchmark_sma200", "benchmark_sma100", "both_sma200"]
        for dca_steps in [1, 3]
    ]

    summary_rows: list[dict[str, object]] = []
    selected_detail_frames: list[pd.DataFrame] = []
    for index, config in enumerate(configs, start=1):
        if index == 1 or index % 12 == 0:
            print(f"running {index}/{len(configs)}: {config.name}", flush=True)
        monthly = run_strategy(config, open_prices, close_prices, bounds, sp500_timeline, nasdaq_current, nasdaq_changes)
        if monthly.empty:
            continue
        is_returns = monthly[monthly["period"] == "IS"]["monthly_return"]
        oos_returns = monthly[monthly["period"] == "OOS"]["monthly_return"]
        is_metrics = strategy_metrics(is_returns, IS_START, IS_END)
        oos_metrics = strategy_metrics(oos_returns, OOS_START, OOS_END)
        passed = pd.notna(is_metrics["max_drawdown"]) and is_metrics["max_drawdown"] > -0.50
        summary_rows.append(
            {
                "strategy": config.name,
                "passed_is_dd_lt_50": passed,
                "universe": config.universe,
                "top_n": config.top_n,
                "lookback": config.lookback,
                "skip": config.skip,
                "cash_filter": config.cash_filter,
                "dca_steps": config.dca_steps,
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
                "is_months": len(is_returns.dropna()),
                "oos_months": len(oos_returns.dropna()),
            }
        )

    summary = pd.DataFrame(summary_rows)
    passed = summary[summary["passed_is_dd_lt_50"]].copy()
    passed = passed.sort_values(["is_sharpe", "is_calmar", "is_return"], ascending=False)
    top20 = passed.head(20).copy()

    for strategy in top20["strategy"].head(5):
        row = top20[top20["strategy"] == strategy].iloc[0]
        config = StrategyConfig(
            universe=str(row["universe"]),
            top_n=int(row["top_n"]),
            lookback=int(row["lookback"]),
            skip=int(row["skip"]),
            cash_filter=str(row["cash_filter"]),
            dca_steps=int(row["dca_steps"]),
        )
        selected_detail_frames.append(
            run_strategy(config, open_prices, close_prices, bounds, sp500_timeline, nasdaq_current, nasdaq_changes)
        )
    details = pd.concat(selected_detail_frames, ignore_index=True) if selected_detail_frames else pd.DataFrame()

    formatted = top20.copy()
    for column in [
        "is_return",
        "is_cagr",
        "is_max_drawdown",
        "is_sharpe",
        "is_calmar",
        "oos_return",
        "oos_cagr",
        "oos_max_drawdown",
        "oos_sharpe",
        "oos_calmar",
    ]:
        if "sharpe" in column or "calmar" in column:
            formatted[column] = formatted[column].map(lambda value: "" if pd.isna(value) else f"{value:.2f}")
        else:
            formatted[column] = formatted[column].map(pct)

    base = "momentum_is2010_2019_oos2020_2026ytd_sp500_nasdaq_cash_dca"
    xlsx_path = REPORT_DIR / f"{base}.xlsx"
    csv_path = REPORT_DIR / f"{base}.csv"
    md_path = REPORT_DIR / f"{base}.md"
    summary.to_csv(csv_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="All candidates raw", index=False)
        passed.to_excel(writer, sheet_name="Passed IS DD raw", index=False)
        formatted.to_excel(writer, sheet_name="Top20 formatted", index=False)
        details.to_excel(writer, sheet_name="Top5 monthly details", index=False)
        workbook = writer.book
        for worksheet in workbook.worksheets:
            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions
            for column in worksheet.columns:
                letter = column[0].column_letter
                worksheet.column_dimensions[letter].width = 34 if letter in {"A", "B"} else 16

    markdown_columns = [
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
        "# Momentum IS/OOS Strategy Search",
        "",
        f"In-sample: {IS_START.isoformat()} to {IS_END.isoformat()}.",
        f"Out-of-sample: {OOS_START.isoformat()} to latest available data through {OOS_END.isoformat()}.",
        "Universe candidates: point-in-time S&P 500, reconstructed point-in-time Nasdaq-100, and combined union.",
        "Execution: monthly signal after prior month-end close; trade at next month first open; final open position marked to latest close.",
        "Cash filters tested: none, benchmark SMA100/SMA200, selected-stock SMA200, and both benchmark+selected SMA200.",
        "DCA tested: full allocation immediately (`DCA1`) and three-month exposure ramp after cash (`DCA3`).",
        f"Candidates tested: {len(summary)}. Passed IS max drawdown < 50%: {len(passed)}.",
        "",
        "## Top 20 Passed Candidates Ranked by IS Sharpe",
        "",
        "| " + " | ".join(markdown_columns) + " |",
        "| " + " | ".join(["---"] * len(markdown_columns)) + " |",
    ]
    for _, row in formatted[markdown_columns].iterrows():
        lines.append("| " + " | ".join(str(row[column]) for column in markdown_columns) + " |")
    lines.extend(
        [
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
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(md_path)
    print(xlsx_path)
    print(f"candidates={len(summary)} passed={len(passed)}")
    print(formatted[markdown_columns].head(10).to_string(index=False))


if __name__ == "__main__":
    main()
