from __future__ import annotations

import argparse
import csv
import math
from io import StringIO
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable

import pandas as pd
import requests
import yfinance as yf


SP500_WIKI_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
NASDAQ100_WIKI_URL = "https://en.wikipedia.org/wiki/Nasdaq-100"


@dataclass(frozen=True)
class PortfolioSnapshot:
    date: pd.Timestamp
    equity: float
    daily_return: float
    holdings: tuple[str, ...]
    selected: tuple[str, ...]


@dataclass(frozen=True)
class TradeEvent:
    date: pd.Timestamp
    action: str
    ticker: str
    score: float | None
    reason: str


@dataclass(frozen=True)
class BacktestResult:
    snapshots: list[PortfolioSnapshot]
    trades: list[TradeEvent]
    start: pd.Timestamp
    end: pd.Timestamp
    lookback_days: int
    max_positions: int
    tickers: list[str]
    missing_tickers: list[str]


def yahoo_symbol(symbol: str) -> str:
    return symbol.replace(".", "-")


def load_sp500_constituents(source_url: str = SP500_WIKI_URL) -> pd.DataFrame:
    response = requests.get(
        source_url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0 Safari/537.36"
            )
        },
        timeout=30,
    )
    response.raise_for_status()
    tables = pd.read_html(StringIO(response.text))
    if not tables:
        raise RuntimeError("No tables found while reading S&P 500 constituents")

    frame = tables[0].copy()
    if "Symbol" not in frame.columns:
        raise RuntimeError("S&P 500 constituents table did not include a Symbol column")

    frame["Yahoo Symbol"] = frame["Symbol"].map(yahoo_symbol)
    return frame


def load_nasdaq100_constituents(source_url: str = NASDAQ100_WIKI_URL) -> pd.DataFrame:
    response = requests.get(
        source_url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0 Safari/537.36"
            )
        },
        timeout=30,
    )
    response.raise_for_status()
    tables = pd.read_html(StringIO(response.text))
    candidates = [frame.copy() for frame in tables if "Ticker" in frame.columns or "Symbol" in frame.columns]
    if not candidates:
        raise RuntimeError("Nasdaq-100 constituents table did not include a Ticker or Symbol column")

    frame = max(candidates, key=len)
    symbol_column = "Ticker" if "Ticker" in frame.columns else "Symbol"
    frame["Symbol"] = frame[symbol_column].astype(str)
    frame["Yahoo Symbol"] = frame["Symbol"].map(yahoo_symbol)
    return frame


def save_constituents(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, index=False)


def fetch_adjusted_prices(
    tickers: list[str],
    start: date,
    end: date,
    batch_size: int = 80,
) -> pd.DataFrame:
    chunks: list[pd.DataFrame] = []
    for offset in range(0, len(tickers), batch_size):
        batch = tickers[offset : offset + batch_size]
        raw = yf.download(
            tickers=" ".join(batch),
            start=start.isoformat(),
            end=(end + timedelta(days=1)).isoformat(),
            auto_adjust=True,
            group_by="column",
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

        if len(batch) == 1:
            open_prices.columns = batch
            close_prices.columns = batch

        open_prices.columns = pd.MultiIndex.from_product([["Open"], open_prices.columns])
        close_prices.columns = pd.MultiIndex.from_product([["Close"], close_prices.columns])
        chunks.append(pd.concat([open_prices, close_prices], axis=1))

    if not chunks:
        raise RuntimeError("No price data downloaded")

    prices = pd.concat(chunks, axis=1)
    prices = prices.loc[:, ~prices.columns.duplicated()].sort_index()
    return prices.dropna(axis=1, how="all")


def load_or_fetch_prices(
    prices_path: Path,
    tickers: list[str],
    start: date,
    end: date,
    refresh: bool,
) -> pd.DataFrame:
    if prices_path.exists() and not refresh:
        prices = pd.read_csv(prices_path, index_col=0, header=[0, 1], parse_dates=True)
    else:
        prices = fetch_adjusted_prices(tickers, start, end)
        prices_path.parent.mkdir(parents=True, exist_ok=True)
        prices.to_csv(prices_path)

    prices.index = pd.to_datetime(prices.index)
    return prices.sort_index()


def momentum_scores(
    prices: pd.DataFrame,
    asof_index: int,
    lookback_days: int,
    score_mode: str = "raw",
    skip_days: int = 0,
    volatility_days: int | None = None,
) -> pd.Series:
    if asof_index < lookback_days:
        return pd.Series(dtype=float)
    if skip_days < 0:
        raise ValueError("skip_days must be non-negative")
    if skip_days >= lookback_days:
        raise ValueError("skip_days must be smaller than lookback_days")

    score_index = asof_index - skip_days
    current = prices.iloc[score_index]
    prior = prices.iloc[asof_index - lookback_days]
    scores = (current / prior) - 1.0

    if score_mode in {"risk_adjusted", "risk_adjusted_skip"}:
        vol_window = volatility_days or lookback_days
        if score_index < vol_window:
            return pd.Series(dtype=float)
        daily_returns = prices.pct_change()
        volatility = daily_returns.iloc[score_index - vol_window + 1 : score_index + 1].std()
        scores = scores / volatility
    elif score_mode not in {"raw", "skip"}:
        raise ValueError(f"Unsupported score_mode: {score_mode}")

    return scores.replace([math.inf, -math.inf], pd.NA).dropna().sort_values(ascending=False)


def apply_sma_filter(
    scores: pd.Series,
    prices: pd.DataFrame,
    asof_index: int,
    sma_days: int | None,
) -> pd.Series:
    if sma_days is None:
        return scores
    if asof_index + 1 < sma_days:
        return pd.Series(dtype=float)

    sma = prices.iloc[asof_index - sma_days + 1 : asof_index + 1].mean()
    current = prices.iloc[asof_index]
    eligible = current[current > sma].index
    return scores.loc[scores.index.intersection(eligible)]


def apply_recent_return_filter(
    scores: pd.Series,
    prices: pd.DataFrame,
    asof_index: int,
    days: int | None,
) -> pd.Series:
    if days is None:
        return scores
    if asof_index < days:
        return pd.Series(dtype=float)

    recent_return = (prices.iloc[asof_index] / prices.iloc[asof_index - days]) - 1.0
    eligible = recent_return[recent_return > 0].index
    return scores.loc[scores.index.intersection(eligible)]


def run_top_n_backtest(
    prices: pd.DataFrame,
    start: date,
    end: date,
    lookback_days: int = 126,
    max_positions: int = 5,
    transaction_cost_bps: float = 0.0,
    sma_filter_days: int | None = None,
    sma_filter_mode: str = "universe",
    score_mode: str = "raw",
    skip_days: int = 0,
    volatility_days: int | None = None,
    market_prices: pd.Series | None = None,
    market_sma_days: int | None = None,
    rebalance_frequency: str = "daily",
    confirm_recent_days: int | None = None,
) -> BacktestResult:
    if isinstance(prices.columns, pd.MultiIndex):
        close_prices = prices["Close"].copy()
        open_prices = prices["Open"].copy()
    else:
        close_prices = prices.copy()
        open_prices = prices.copy()

    close_prices = close_prices.dropna(axis=1, thresh=lookback_days + 2).sort_index()
    open_prices = open_prices.reindex(columns=close_prices.columns).sort_index()
    close_prices = close_prices.loc[(close_prices.index.date >= start) | (close_prices.index < pd.Timestamp(start))]
    close_prices = close_prices.loc[close_prices.index.date <= end]
    open_prices = open_prices.reindex(index=close_prices.index)
    market_filter = None
    if market_prices is not None and market_sma_days is not None:
        market_filter = market_prices.reindex(close_prices.index).ffill()
    if close_prices.empty:
        raise ValueError("No prices in requested backtest window")

    holdings: list[str] = []
    pending_holdings: list[str] | None = None
    equity = 1.0
    snapshots: list[PortfolioSnapshot] = []
    trades: list[TradeEvent] = []
    cost_rate = transaction_cost_bps / 10_000.0

    for index in range(1, len(close_prices)):
        current_date = close_prices.index[index]
        if current_date.date() < start:
            continue

        if pending_holdings is not None:
            previous_holdings = set(holdings)
            next_holdings = set(pending_holdings)
            scores = momentum_scores(
                close_prices,
                index - 1,
                lookback_days,
                score_mode=score_mode,
                skip_days=skip_days,
                volatility_days=volatility_days,
            )
            if sma_filter_mode == "universe":
                scores = apply_sma_filter(scores, close_prices, index - 1, sma_filter_days)
            for ticker in holdings:
                if ticker not in next_holdings:
                    equity *= 1.0 - cost_rate
                    trades.append(
                        TradeEvent(
                            date=current_date,
                            action="SELL",
                            ticker=ticker,
                            score=float(scores[ticker]) if ticker in scores else None,
                            reason="next_open_left_top_rank",
                        )
                    )
            for ticker in pending_holdings:
                if ticker not in previous_holdings:
                    equity *= 1.0 - cost_rate
                    trades.append(
                        TradeEvent(
                            date=current_date,
                            action="BUY",
                            ticker=ticker,
                            score=float(scores[ticker]) if ticker in scores else None,
                            reason="next_open_fill_open_slot",
                        )
                    )
            holdings = list(pending_holdings)
            pending_holdings = None

        returns = (close_prices.iloc[index] / open_prices.iloc[index]) - 1.0
        daily_return = 0.0
        for ticker in holdings:
            value = returns.get(ticker)
            if pd.notna(value):
                daily_return += (1.0 / max_positions) * float(value)
        equity *= 1.0 + daily_return

        if rebalance_frequency == "daily":
            is_rebalance_day = True
        elif rebalance_frequency == "monthly":
            next_index = min(index + 1, len(close_prices) - 1)
            is_rebalance_day = (
                not holdings
                or index == len(close_prices) - 1
                or close_prices.index[next_index].month != current_date.month
                or close_prices.index[next_index].year != current_date.year
            )
        else:
            raise ValueError(f"Unsupported rebalance_frequency: {rebalance_frequency}")

        if not is_rebalance_day:
            snapshots.append(
                PortfolioSnapshot(
                    date=current_date,
                    equity=equity,
                    daily_return=daily_return,
                    holdings=tuple(holdings),
                    selected=tuple(holdings),
                )
            )
            continue

        scores = momentum_scores(
            close_prices,
            index,
            lookback_days,
            score_mode=score_mode,
            skip_days=skip_days,
            volatility_days=volatility_days,
        )
        if sma_filter_mode == "universe":
            selected_scores = apply_recent_return_filter(scores, close_prices, index, confirm_recent_days)
            selected_scores = apply_sma_filter(selected_scores, close_prices, index, sma_filter_days).head(max_positions)
        elif sma_filter_mode == "top_n":
            selected_scores = apply_recent_return_filter(scores.head(max_positions), close_prices, index, confirm_recent_days)
            selected_scores = apply_sma_filter(selected_scores, close_prices, index, sma_filter_days)
        else:
            raise ValueError(f"Unsupported sma_filter_mode: {sma_filter_mode}")
        if market_filter is not None:
            market_window = market_filter.iloc[index - market_sma_days + 1 : index + 1]
            market_value = market_filter.iloc[index]
            if index + 1 < market_sma_days or pd.isna(market_value) or market_value <= market_window.mean():
                selected_scores = pd.Series(dtype=float)
        selected = list(selected_scores.index)

        next_holdings = [ticker for ticker in holdings if ticker in selected]
        for ticker in selected:
            if len(next_holdings) >= max_positions:
                break
            if ticker not in next_holdings:
                next_holdings.append(ticker)
        pending_holdings = next_holdings

        snapshots.append(
            PortfolioSnapshot(
                date=current_date,
                equity=equity,
                daily_return=daily_return,
                holdings=tuple(holdings),
                selected=tuple(selected),
            )
        )

    missing_tickers = sorted(set(close_prices.columns[close_prices.isna().all()].tolist()))
    return BacktestResult(
        snapshots=snapshots,
        trades=trades,
        start=pd.Timestamp(start),
        end=pd.Timestamp(end),
        lookback_days=lookback_days,
        max_positions=max_positions,
        tickers=list(close_prices.columns),
        missing_tickers=missing_tickers,
    )


def calculate_summary(result: BacktestResult) -> dict[str, str | int | float]:
    if not result.snapshots:
        raise ValueError("No snapshots generated")

    equity = pd.Series(
        [snapshot.equity for snapshot in result.snapshots],
        index=[snapshot.date for snapshot in result.snapshots],
    )
    daily_returns = pd.Series(
        [snapshot.daily_return for snapshot in result.snapshots],
        index=[snapshot.date for snapshot in result.snapshots],
    )
    running_peak = equity.cummax()
    drawdowns = (equity / running_peak) - 1.0
    elapsed_days = max((equity.index[-1] - equity.index[0]).days, 1)
    cagr = equity.iloc[-1] ** (365.25 / elapsed_days) - 1.0
    sharpe = None
    if daily_returns.std(ddof=0) > 0:
        sharpe = (daily_returns.mean() / daily_returns.std(ddof=0)) * math.sqrt(252)

    buys = [trade for trade in result.trades if trade.action == "BUY"]
    sells = [trade for trade in result.trades if trade.action == "SELL"]
    return {
        "start": equity.index[0].date().isoformat(),
        "end": equity.index[-1].date().isoformat(),
        "trading_days": len(equity),
        "ending_equity": float(equity.iloc[-1]),
        "total_return": float(equity.iloc[-1] - 1.0),
        "cagr": float(cagr),
        "max_drawdown": float(drawdowns.min()),
        "sharpe": "" if sharpe is None else float(sharpe),
        "buy_trades": len(buys),
        "sell_trades": len(sells),
        "final_holdings": ", ".join(result.snapshots[-1].holdings),
        "ticker_count": len(result.tickers),
    }


def write_snapshots(snapshots: Iterable[PortfolioSnapshot], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["date", "equity", "daily_return", "holdings", "selected"])
        writer.writeheader()
        for snapshot in snapshots:
            writer.writerow(
                {
                    "date": snapshot.date.date().isoformat(),
                    "equity": f"{snapshot.equity:.10f}",
                    "daily_return": f"{snapshot.daily_return:.10f}",
                    "holdings": " ".join(snapshot.holdings),
                    "selected": " ".join(snapshot.selected),
                }
            )


def write_trades(trades: Iterable[TradeEvent], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["date", "action", "ticker", "score", "reason"])
        writer.writeheader()
        for trade in trades:
            writer.writerow(
                {
                    "date": trade.date.date().isoformat(),
                    "action": trade.action,
                    "ticker": trade.ticker,
                    "score": "" if trade.score is None else f"{trade.score:.10f}",
                    "reason": trade.reason,
                }
            )


def write_markdown(summary: dict[str, str | int | float], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    def pct(value: object) -> str:
        return f"{float(value):.2%}"

    sharpe = summary["sharpe"]
    sharpe_text = "" if sharpe == "" else f"{float(sharpe):.2f}"
    lines = [
        "# S&P 500 Top-5 Momentum Backtest",
        "",
        "## Rules",
        "",
        "- Universe: current S&P 500 constituents from Wikipedia.",
        "- Data: Yahoo Finance adjusted daily close via yfinance.",
        "- Signal: rank by trailing adjusted-close momentum.",
        "- Execution model: rank after the close, then execute exits and entries at the next trading day's open.",
        "- Portfolio model: five 20% slots; cash is idle when fewer than five names are held.",
        "",
        "## Summary",
        "",
        f"- Start: {summary['start']}",
        f"- End: {summary['end']}",
        f"- Trading days: {summary['trading_days']}",
        f"- Ticker count with usable data: {summary['ticker_count']}",
        f"- Total return: {pct(summary['total_return'])}",
        f"- CAGR: {pct(summary['cagr'])}",
        f"- Max drawdown: {pct(summary['max_drawdown'])}",
        f"- Sharpe: {sharpe_text}",
        f"- Buy trades: {summary['buy_trades']}",
        f"- Sell trades: {summary['sell_trades']}",
        f"- Final holdings: {summary['final_holdings']}",
        "",
        "## Notes",
        "",
        "This first pass uses the current S&P 500 membership. That is acceptable for a recent one-month smoke test, but a multi-year research-grade test should use point-in-time constituents to avoid survivorship bias.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def main() -> None:
    parser = argparse.ArgumentParser(description="Backtest daily S&P 500 top-N momentum rotation.")
    parser.add_argument("--start", type=parse_date, default=date.today() - timedelta(days=31))
    parser.add_argument("--end", type=parse_date, default=date.today())
    parser.add_argument("--lookback-days", type=int, default=126)
    parser.add_argument("--max-positions", type=int, default=5)
    parser.add_argument("--transaction-cost-bps", type=float, default=0.0)
    parser.add_argument("--sma-filter-days", type=int, default=None)
    parser.add_argument(
        "--sma-filter-mode",
        choices=["universe", "top_n"],
        default="universe",
        help="universe filters all ranked stocks before taking top N; top_n filters only the raw top N.",
    )
    parser.add_argument(
        "--score-mode",
        choices=["raw", "skip", "risk_adjusted", "risk_adjusted_skip"],
        default="raw",
    )
    parser.add_argument("--skip-days", type=int, default=0)
    parser.add_argument("--volatility-days", type=int, default=None)
    parser.add_argument("--market-sma-days", type=int, default=None)
    parser.add_argument("--rebalance-frequency", choices=["daily", "monthly"], default="daily")
    parser.add_argument("--confirm-recent-days", type=int, default=None)
    parser.add_argument("--data-dir", type=Path, default=Path("data/sp500_top5"))
    parser.add_argument("--report-dir", type=Path, default=Path("reports"))
    parser.add_argument("--refresh", action="store_true", help="Redownload constituents and price data")
    args = parser.parse_args()

    fetch_start = args.start - timedelta(days=max(args.lookback_days * 3, 260))
    constituents_path = args.data_dir / "sp500_constituents.csv"
    prices_path = args.data_dir / f"adjusted_closes_{fetch_start.isoformat()}_{args.end.isoformat()}.csv"

    if constituents_path.exists() and not args.refresh:
        constituents = pd.read_csv(constituents_path)
    else:
        constituents = load_sp500_constituents()
        save_constituents(constituents, constituents_path)

    tickers = constituents["Yahoo Symbol"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(prices_path, tickers, fetch_start, args.end, args.refresh)
    market_prices = None
    if args.market_sma_days is not None:
        market_data = yf.download(
            "SPY",
            start=fetch_start.isoformat(),
            end=(args.end + timedelta(days=1)).isoformat(),
            auto_adjust=True,
            progress=False,
        )
        market_prices = market_data["Close"].dropna()
        if hasattr(market_prices, "columns"):
            market_prices = market_prices.iloc[:, 0].dropna()
    result = run_top_n_backtest(
        prices=prices,
        start=args.start,
        end=args.end,
        lookback_days=args.lookback_days,
        max_positions=args.max_positions,
        transaction_cost_bps=args.transaction_cost_bps,
        sma_filter_days=args.sma_filter_days,
        sma_filter_mode=args.sma_filter_mode,
        score_mode=args.score_mode,
        skip_days=args.skip_days,
        volatility_days=args.volatility_days,
        market_prices=market_prices,
        market_sma_days=args.market_sma_days,
        rebalance_frequency=args.rebalance_frequency,
        confirm_recent_days=args.confirm_recent_days,
    )
    summary = calculate_summary(result)

    write_snapshots(result.snapshots, args.report_dir / "sp500_top5_equity.csv")
    write_trades(result.trades, args.report_dir / "sp500_top5_trades.csv")
    write_markdown(summary, args.report_dir / "sp500_top5_momentum_backtest.md")

    print("S&P 500 top-5 momentum backtest")
    for key, value in summary.items():
        print(f"{key}: {value}")
    print(f"Saved prices: {prices_path}")
    print(f"Saved reports: {args.report_dir}")


if __name__ == "__main__":
    main()
