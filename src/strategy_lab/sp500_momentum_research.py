from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
import yfinance as yf

from src.strategy_lab.benchmark import benchmark_return
from src.strategy_lab.sp500_top5 import (
    calculate_summary,
    load_or_fetch_prices,
    load_sp500_constituents,
    run_top_n_backtest,
    save_constituents,
)


@dataclass(frozen=True)
class Variant:
    name: str
    lookback_days: int
    score_mode: str = "raw"
    skip_days: int = 0
    volatility_days: int | None = None
    sma_filter_days: int | None = None
    sma_filter_mode: str = "top_n"
    market_sma_days: int | None = None
    rebalance_frequency: str = "daily"


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def format_pct(value: float) -> str:
    return f"{value:.2%}"


def load_market_prices(symbol: str, start: date, end: date) -> pd.Series:
    data = yf.download(
        symbol,
        start=start.isoformat(),
        end=(end + timedelta(days=1)).isoformat(),
        auto_adjust=True,
        progress=False,
    )
    close = data["Close"].dropna()
    if hasattr(close, "columns"):
        close = close.iloc[:, 0].dropna()
    close.index = pd.to_datetime(close.index)
    return close.sort_index()


def default_variants() -> list[Variant]:
    return [
        Variant("126 raw baseline", 126, sma_filter_days=None),
        Variant("126 raw + SMA50 topN", 126, sma_filter_days=50),
        Variant("126 raw + SMA100 topN", 126, sma_filter_days=100),
        Variant("126 raw + SPY SMA200", 126, market_sma_days=200, sma_filter_days=None),
        Variant("126 raw + SMA50 topN + SPY SMA200", 126, sma_filter_days=50, market_sma_days=200),
        Variant("126 risk-adjusted", 126, score_mode="risk_adjusted", volatility_days=126, sma_filter_days=None),
        Variant("126 risk-adjusted + SMA50 topN", 126, score_mode="risk_adjusted", volatility_days=126, sma_filter_days=50),
        Variant("126 skip21", 126, score_mode="skip", skip_days=21, sma_filter_days=None),
        Variant("126 skip21 monthly", 126, score_mode="skip", skip_days=21, sma_filter_days=None, rebalance_frequency="monthly"),
        Variant("126 skip21 + SMA50 topN", 126, score_mode="skip", skip_days=21, sma_filter_days=50),
        Variant("252 skip21", 252, score_mode="skip", skip_days=21, sma_filter_days=None),
        Variant("252 skip21 + SMA50 topN", 252, score_mode="skip", skip_days=21, sma_filter_days=50),
        Variant(
            "252 risk-adjusted skip21",
            252,
            score_mode="risk_adjusted_skip",
            skip_days=21,
            volatility_days=252,
            sma_filter_days=None,
        ),
        Variant(
            "252 risk-adjusted skip21 + SMA50 topN",
            252,
            score_mode="risk_adjusted_skip",
            skip_days=21,
            volatility_days=252,
            sma_filter_days=50,
        ),
        Variant(
            "252 risk-adjusted skip21 + SMA50 topN + SPY SMA200",
            252,
            score_mode="risk_adjusted_skip",
            skip_days=21,
            volatility_days=252,
            sma_filter_days=50,
            market_sma_days=200,
        ),
    ]


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "variant",
        "total_return",
        "excess_vs_spmo",
        "cagr",
        "max_drawdown",
        "sharpe",
        "buy_trades",
        "sell_trades",
        "final_holdings",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, object]], spmo_return: float, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# S&P 500 Momentum Research Grid",
        "",
        f"Benchmark: SPMO total return = {format_pct(spmo_return)}.",
        "",
        "| Rank | Variant | Return | Excess vs SPMO | CAGR | Max DD | Sharpe | Buys | Final Holdings |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for rank, row in enumerate(rows, start=1):
        sharpe = row["sharpe"]
        sharpe_text = "" if sharpe == "" else f"{float(sharpe):.2f}"
        lines.append(
            "| "
            f"{rank} | "
            f"{row['variant']} | "
            f"{format_pct(float(row['total_return']))} | "
            f"{format_pct(float(row['excess_vs_spmo']))} | "
            f"{format_pct(float(row['cagr']))} | "
            f"{format_pct(float(row['max_drawdown']))} | "
            f"{sharpe_text} | "
            f"{row['buy_trades']} | "
            f"{row['final_holdings']} |"
        )
    lines.extend(
        [
            "",
            "Research ideas tested: SPMO-like 12-1 momentum, volatility-adjusted momentum, SMA50/SMA100 top-N gates, and a SPY SMA200 market regime filter.",
            "Data note: this uses the currently fetched S&P 500 constituent list rather than point-in-time membership, so multi-year tests may contain survivorship bias.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a small research grid for S&P 500 momentum variants.")
    parser.add_argument("--start", type=parse_date, default=date(2020, 1, 1))
    parser.add_argument("--end", type=parse_date, default=date(2025, 12, 31))
    parser.add_argument("--max-positions", type=int, default=5)
    parser.add_argument("--transaction-cost-bps", type=float, default=0.0)
    parser.add_argument("--data-start", type=parse_date, default=date(2018, 12, 19))
    parser.add_argument("--data-dir", type=Path, default=Path("data/sp500_top5"))
    parser.add_argument("--report-dir", type=Path, default=Path("reports"))
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    constituents_path = args.data_dir / "sp500_constituents.csv"
    prices_path = args.data_dir / f"adjusted_open_close_{args.data_start.isoformat()}_{args.end.isoformat()}.csv"
    if constituents_path.exists() and not args.refresh:
        constituents = pd.read_csv(constituents_path)
    else:
        constituents = load_sp500_constituents()
        save_constituents(constituents, constituents_path)

    tickers = constituents["Yahoo Symbol"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(prices_path, tickers, args.data_start, args.end, args.refresh)
    spy = load_market_prices("SPY", args.data_start, args.end)
    _, _, spmo_total_return = benchmark_return("SPMO", args.start, args.end)

    rows: list[dict[str, object]] = []
    for variant in default_variants():
        result = run_top_n_backtest(
            prices=prices,
            start=args.start,
            end=args.end,
            lookback_days=variant.lookback_days,
            max_positions=args.max_positions,
            transaction_cost_bps=args.transaction_cost_bps,
            sma_filter_days=variant.sma_filter_days,
            sma_filter_mode=variant.sma_filter_mode,
            score_mode=variant.score_mode,
            skip_days=variant.skip_days,
            volatility_days=variant.volatility_days,
            market_prices=spy if variant.market_sma_days is not None else None,
            market_sma_days=variant.market_sma_days,
            rebalance_frequency=variant.rebalance_frequency,
        )
        summary = calculate_summary(result)
        row = {
            "variant": variant.name,
            "total_return": summary["total_return"],
            "excess_vs_spmo": float(summary["total_return"]) - spmo_total_return,
            "cagr": summary["cagr"],
            "max_drawdown": summary["max_drawdown"],
            "sharpe": summary["sharpe"],
            "buy_trades": summary["buy_trades"],
            "sell_trades": summary["sell_trades"],
            "final_holdings": summary["final_holdings"],
        }
        rows.append(row)
        print(
            f"{variant.name}: return={format_pct(float(row['total_return']))}, "
            f"excess_vs_spmo={format_pct(float(row['excess_vs_spmo']))}, "
            f"max_dd={format_pct(float(row['max_drawdown']))}"
        )

    rows.sort(key=lambda row: float(row["total_return"]), reverse=True)
    output_stem = f"sp500_momentum_research_{args.start.isoformat()}_{args.end.isoformat()}"
    write_csv(rows, args.report_dir / f"{output_stem}.csv")
    write_markdown(rows, spmo_total_return, args.report_dir / f"{output_stem}.md")
    print(f"SPMO: return={format_pct(spmo_total_return)}")
    print(f"Saved reports: {args.report_dir / f'{output_stem}.md'}")


if __name__ == "__main__":
    main()
