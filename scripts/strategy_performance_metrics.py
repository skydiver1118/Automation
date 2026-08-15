from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.soxl_tqqq_cash_signal_scanner import (  # noqa: E402
    StrategyConfig as SoxlTqqqCashConfig,
    build_base_rotation,
    cash_filtered_targets,
)
from src.strategy_lab.momentum_is_oos_research import (  # noqa: E402
    DATA_DIR as MOMENTUM_DATA_DIR,
    OOS_END as MOMENTUM_OOS_END,
    OOS_START,
    PRICE_START,
    StrategyConfig as MomentumStrategyConfig,
    fetch_prices as fetch_momentum_prices,
    load_nasdaq100_current_and_changes,
    load_sp500_timeline,
    members_from_timeline,
    month_boundaries as momentum_month_boundaries,
    nasdaq_members_on,
    universe_tickers_from_membership,
)
from src.strategy_lab.momentum_is_oos_research_separate import (  # noqa: E402
    precompute_months as precompute_sp500_nasdaq_months,
    run_config as run_sp500_nasdaq_config,
)
from src.strategy_lab.smh_historical_components_momentum_is_oos import (  # noqa: E402
    HOLDINGS_PATH as SMH_HOLDINGS_PATH,
    OOS_END as SMH_OOS_END,
    PRICE_START as SMH_PRICE_START,
    fetch_prices as fetch_smh_prices,
    latest_known_snapshot,
    load_historical_holdings,
    precompute_months as precompute_smh_months,
    price_coverage,
    run_strategy as run_smh_strategy,
    snapshot_tickers_by_public_date,
)


REPORT_DIR = ROOT / "reports"
SOXL_TQQQ_NAME = "SOXL/TQQQ Rotation with cash daily scanner"
STRATEGY_SPECS = {
    "soxl_tqqq_rotation_cash": {
        "display_name": SOXL_TQQQ_NAME,
        "output_stem": "soxl_tqqq_rotation_cash_oos_performance",
    },
    "sp500_top5_l63_s0_none_dca1": {
        "display_name": "SP500 Top5 L63 S0 none DCA1",
        "output_stem": "sp500_top5_l63_s0_none_dca1_oos_performance",
        "benchmark": "SPY",
        "benchmark_name": "SPY buy-and-hold",
    },
    "nasdaq100_top3_l126_s21_none_dca3": {
        "display_name": "NASDAQ100 Top3 L126 S21 none DCA3",
        "output_stem": "nasdaq100_top3_l126_s21_none_dca3_oos_performance",
        "benchmark": "QQQ",
        "benchmark_name": "QQQ buy-and-hold",
    },
    "smh_hist_pit_top2_l252_s0_smh_sma100_dca1": {
        "display_name": "SMH_HIST_PIT Top2 L252 S0 smh_sma100 DCA1",
        "output_stem": "smh_hist_pit_top2_l252_s0_smh_sma100_dca1_oos_performance",
        "benchmark": "SMH",
        "benchmark_name": "SMH buy-and-hold",
    },
}
TRENDSPIDER_STYLE_COLUMNS = [
    "market",
    "trade_cost",
    "net_perf_all",
    "asset_perf",
    "beta_vs_asset",
    "positions",
    "wins",
    "losses",
    "max_drawdown",
    "average_win",
    "average_loss",
    "average_return",
    "reward_risk_ratio",
    "expectancy",
]


@dataclass(frozen=True)
class MetricRow:
    strategy: str
    period: str
    cumulative_return_pct: float
    cagr_pct: float
    max_drawdown_pct: float
    sharpe: float
    sortino: float
    calmar: float
    volatility_pct: float
    best_day_pct: float
    worst_day_pct: float


def fetch_adjusted_close(symbols: list[str], start: str, end: str | None = None) -> pd.DataFrame:
    raw = yf.download(
        symbols,
        start=start,
        end=end,
        interval="1d",
        auto_adjust=True,
        progress=False,
        threads=False,
    )
    if raw.empty:
        raise RuntimeError("No price data returned by yfinance.")
    close = raw["Close"].copy() if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]].copy()
    close = close[symbols].dropna()
    close.index = pd.to_datetime(close.index).tz_localize(None)
    return close


def drawdown(equity: pd.Series) -> pd.Series:
    normalized = equity / equity.iloc[0]
    return normalized / normalized.cummax() - 1.0


def metric_row(name: str, equity: pd.Series, *, periods_per_year: int = 252) -> MetricRow:
    equity = equity.dropna()
    normalized = equity / equity.iloc[0]
    returns = normalized.pct_change().dropna()
    years = (normalized.index[-1] - normalized.index[0]).days / 365.25
    cumulative = normalized.iloc[-1] - 1.0
    cagr = normalized.iloc[-1] ** (1.0 / years) - 1.0 if years > 0 else np.nan
    dd = drawdown(normalized)
    vol = returns.std(ddof=0) * math.sqrt(periods_per_year) if len(returns) else np.nan
    sharpe = returns.mean() / returns.std(ddof=0) * math.sqrt(periods_per_year) if returns.std(ddof=0) else np.nan
    downside = returns[returns < 0].std(ddof=0)
    sortino = returns.mean() / downside * math.sqrt(periods_per_year) if downside else np.nan
    max_dd = dd.min()
    calmar = cagr / abs(max_dd) if max_dd < 0 else np.nan
    return MetricRow(
        strategy=name,
        period=f"{normalized.index[0].date()} to {normalized.index[-1].date()}",
        cumulative_return_pct=round(cumulative * 100, 2),
        cagr_pct=round(cagr * 100, 2),
        max_drawdown_pct=round(max_dd * 100, 2),
        sharpe=round(float(sharpe), 3) if pd.notna(sharpe) else np.nan,
        sortino=round(float(sortino), 3) if pd.notna(sortino) else np.nan,
        calmar=round(float(calmar), 3) if pd.notna(calmar) else np.nan,
        volatility_pct=round(float(vol) * 100, 2) if pd.notna(vol) else np.nan,
        best_day_pct=round(float(returns.max()) * 100, 2) if len(returns) else np.nan,
        worst_day_pct=round(float(returns.min()) * 100, 2) if len(returns) else np.nan,
    )


def annual_rows(equity_by_name: dict[str, pd.Series]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for name, equity in equity_by_name.items():
        normalized = (equity / equity.iloc[0]).dropna()
        for year, yearly in normalized.groupby(normalized.index.year):
            if yearly.empty:
                continue
            rows.append(
                {
                    "year": int(year),
                    "strategy": name,
                    "return_pct": round((yearly.iloc[-1] / yearly.iloc[0] - 1.0) * 100, 2),
                    "max_drawdown_pct": round(drawdown(yearly).min() * 100, 2),
                }
            )
    return pd.DataFrame(rows)


def annual_wide_tables(annual: pd.DataFrame, ordered_strategies: list[str] | None = None) -> tuple[pd.DataFrame, pd.DataFrame]:
    returns = annual.pivot(index="year", columns="strategy", values="return_pct").reset_index()
    drawdowns = annual.pivot(index="year", columns="strategy", values="max_drawdown_pct").reset_index()
    ordered_columns = ["year", *(ordered_strategies or [column for column in returns.columns if column != "year"])]
    returns = returns[[column for column in ordered_columns if column in returns.columns]]
    drawdowns = drawdowns[[column for column in ordered_columns if column in drawdowns.columns]]
    return returns, drawdowns


def equity_from_monthly(monthly: pd.DataFrame, name: str, final_date: pd.Timestamp | None = None) -> pd.Series:
    frame = monthly.copy()
    frame["trade_date"] = pd.to_datetime(frame["trade_date"])
    frame["oos_equity"] = (1.0 + frame["monthly_return"].astype(float)).cumprod()
    dates = list(frame["trade_date"])
    if final_date is not None and dates:
        dates[-1] = pd.Timestamp(final_date)
    equity = pd.concat(
        [
            pd.Series([1.0], index=[frame["trade_date"].iloc[0] - pd.Timedelta(days=1)]),
            pd.Series(frame["oos_equity"].to_numpy(), index=pd.to_datetime(dates)),
        ]
    )
    equity.name = name
    return equity.sort_index()


def benchmark_monthly_equity(
    open_prices: pd.DataFrame,
    close_prices: pd.DataFrame,
    symbol: str,
    start: Any,
    end: Any,
    name: str,
) -> pd.Series:
    bounds = momentum_month_boundaries(close_prices.index, pd.Timestamp(start).date(), pd.Timestamp(end).date())
    values = [1.0]
    dates = []
    equity = 1.0
    for month_index, (_, _, trade_date) in enumerate(bounds):
        if month_index == 0:
            dates.append(trade_date - pd.Timedelta(days=1))
        next_trade = bounds[month_index + 1][2] if month_index < len(bounds) - 1 else None
        entry = open_prices.loc[trade_date, symbol]
        if next_trade is None:
            final_series = close_prices.loc[close_prices.index >= trade_date, symbol].dropna()
            exit_price = final_series.iloc[-1]
            value_date = final_series.index[-1]
        else:
            exit_price = open_prices.loc[next_trade, symbol]
            value_date = trade_date
        equity *= float(exit_price) / float(entry)
        values.append(equity)
        dates.append(value_date)
    return pd.Series(values, index=pd.to_datetime(dates), name=name).sort_index()


def run_soxl_tqqq_cash(close: pd.DataFrame, start: str) -> tuple[pd.Series, pd.Series]:
    config = SoxlTqqqCashConfig()
    base = build_base_rotation(close, config)
    targets = cash_filtered_targets(close, base, config).reindex(close.index).ffill().fillna("CASH")
    close = close.loc[close.index >= pd.Timestamp(start)].copy()
    targets = targets.reindex(close.index).ffill().fillna("CASH")

    equity = np.ones(len(close), dtype=float)
    held = str(targets.iloc[0])
    for i in range(1, len(close)):
        if held in {"SOXL", "TQQQ"}:
            equity[i] = equity[i - 1] * (float(close[held].iloc[i]) / float(close[held].iloc[i - 1]))
        else:
            equity[i] = equity[i - 1]
        held = str(targets.iloc[i])
    return pd.Series(equity, index=close.index, name=SOXL_TQQQ_NAME), targets


def trade_segments(close: pd.DataFrame, targets: pd.Series) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    active_symbol: str | None = None
    entry_date: pd.Timestamp | None = None
    entry_price: float | None = None

    for ts, target in targets.items():
        target = str(target)
        if active_symbol is None and target in {"SOXL", "TQQQ"}:
            active_symbol = target
            entry_date = pd.Timestamp(ts)
            entry_price = float(close.loc[ts, target])
            continue
        if active_symbol is not None and target != active_symbol:
            exit_date = pd.Timestamp(ts)
            exit_price = float(close.loc[ts, active_symbol])
            trade_return = exit_price / float(entry_price) - 1.0
            rows.append(
                {
                    "entry_date": entry_date.date().isoformat(),
                    "exit_date": exit_date.date().isoformat(),
                    "symbol": active_symbol,
                    "exit_to": target,
                    "entry_price": round(float(entry_price), 4),
                    "exit_price": round(exit_price, 4),
                    "return_pct": round(trade_return * 100, 2),
                    "outcome": "win" if trade_return > 0 else "loss",
                    "holding_calendar_days": int((exit_date - entry_date).days),
                    "holding_trading_days": int(len(close.loc[entry_date:exit_date]) - 1),
                }
            )
            active_symbol = target if target in {"SOXL", "TQQQ"} else None
            entry_date = exit_date if active_symbol is not None else None
            entry_price = float(close.loc[ts, active_symbol]) if active_symbol is not None else None

    if active_symbol is not None and entry_date is not None and entry_price is not None:
        exit_date = pd.Timestamp(targets.index[-1])
        exit_price = float(close.loc[exit_date, active_symbol])
        trade_return = exit_price / float(entry_price) - 1.0
        rows.append(
            {
                "entry_date": entry_date.date().isoformat(),
                "exit_date": exit_date.date().isoformat(),
                "symbol": active_symbol,
                "exit_to": "OPEN",
                "entry_price": round(float(entry_price), 4),
                "exit_price": round(exit_price, 4),
                "return_pct": round(trade_return * 100, 2),
                "outcome": "win" if trade_return > 0 else "loss",
                "holding_calendar_days": int((exit_date - entry_date).days),
                "holding_trading_days": int(len(close.loc[entry_date:exit_date]) - 1),
            }
        )
    return pd.DataFrame(rows)


def parse_tickers(value: Any) -> list[str]:
    text = str(value)
    if text == "CASH" or not text.strip():
        return []
    return [part.strip() for part in text.split(",") if part.strip()]


def monthly_trade_segments(monthly: pd.DataFrame, open_prices: pd.DataFrame, close_prices: pd.DataFrame) -> pd.DataFrame:
    frame = monthly.copy()
    frame["trade_date"] = pd.to_datetime(frame["trade_date"])
    frame = frame.sort_values("trade_date")
    active: dict[str, dict[str, Any]] = {}
    rows: list[dict[str, Any]] = []

    for row in frame.itertuples(index=False):
        trade_date = pd.Timestamp(row.trade_date)
        selected = set(parse_tickers(row.tickers))
        current = set(active)

        for ticker in sorted(current - selected):
            entry = active.pop(ticker)
            exit_price = float(open_prices.loc[trade_date, ticker])
            trade_return = exit_price / float(entry["entry_price"]) - 1.0
            rows.append(
                {
                    "entry_date": entry["entry_date"].date().isoformat(),
                    "exit_date": trade_date.date().isoformat(),
                    "symbol": ticker,
                    "exit_to": "REMOVED",
                    "entry_price": round(float(entry["entry_price"]), 4),
                    "exit_price": round(exit_price, 4),
                    "return_pct": round(trade_return * 100, 2),
                    "outcome": "win" if trade_return > 0 else "loss",
                    "holding_calendar_days": int((trade_date - entry["entry_date"]).days),
                    "holding_trading_days": int(len(close_prices.loc[entry["entry_date"]:trade_date]) - 1),
                }
            )

        for ticker in sorted(selected - current):
            if ticker not in open_prices.columns or pd.isna(open_prices.loc[trade_date, ticker]):
                continue
            active[ticker] = {
                "entry_date": trade_date,
                "entry_price": float(open_prices.loc[trade_date, ticker]),
            }

    final_date = pd.Timestamp(close_prices.index[close_prices.index <= frame["trade_date"].iloc[-1]].max())
    if pd.isna(final_date):
        final_date = pd.Timestamp(close_prices.index[-1])
    for ticker, entry in sorted(active.items()):
        if ticker not in close_prices.columns:
            continue
        exit_candidates = close_prices.index[(close_prices.index >= entry["entry_date"]) & close_prices[ticker].notna()]
        if exit_candidates.empty:
            continue
        exit_date = exit_candidates[-1]
        exit_price = float(close_prices.loc[exit_date, ticker])
        trade_return = exit_price / float(entry["entry_price"]) - 1.0
        rows.append(
            {
                "entry_date": entry["entry_date"].date().isoformat(),
                "exit_date": pd.Timestamp(exit_date).date().isoformat(),
                "symbol": ticker,
                "exit_to": "OPEN",
                "entry_price": round(float(entry["entry_price"]), 4),
                "exit_price": round(exit_price, 4),
                "return_pct": round(trade_return * 100, 2),
                "outcome": "win" if trade_return > 0 else "loss",
                "holding_calendar_days": int((pd.Timestamp(exit_date) - entry["entry_date"]).days),
                "holding_trading_days": int(len(close_prices.loc[entry["entry_date"]:exit_date]) - 1),
            }
        )
    return pd.DataFrame(rows)


def trade_summary(trades: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for outcome, group in trades.groupby("outcome"):
        rows.append(
            {
                "outcome": outcome,
                "trades": len(group),
                "average_return_pct": round(group["return_pct"].mean(), 2),
                "median_return_pct": round(group["return_pct"].median(), 2),
                "average_holding_trading_days": round(group["holding_trading_days"].mean(), 2),
                "median_holding_trading_days": round(group["holding_trading_days"].median(), 2),
                "average_holding_calendar_days": round(group["holding_calendar_days"].mean(), 2),
                "median_holding_calendar_days": round(group["holding_calendar_days"].median(), 2),
            }
        )
    return pd.DataFrame(rows).sort_values("outcome")


def trendspider_style_metrics(
    strategy_equity: pd.Series,
    asset_equity: pd.Series,
    trades: pd.DataFrame,
    *,
    market: str,
    trade_cost: str,
) -> dict[str, Any]:
    strategy_norm = (strategy_equity / strategy_equity.iloc[0]).dropna()
    asset_norm = (asset_equity / asset_equity.iloc[0]).reindex(strategy_norm.index).dropna()
    strategy_norm = strategy_norm.reindex(asset_norm.index).dropna()
    strategy_returns = strategy_norm.pct_change().dropna()
    asset_returns = asset_norm.pct_change().dropna()
    aligned = pd.concat([strategy_returns, asset_returns], axis=1).dropna()
    aligned.columns = ["strategy", "asset"]

    beta = np.nan
    asset_variance = aligned["asset"].var(ddof=0) if len(aligned) else np.nan
    if pd.notna(asset_variance) and asset_variance != 0:
        beta = aligned["strategy"].cov(aligned["asset"]) / asset_variance

    wins = trades[trades["return_pct"] > 0]
    losses = trades[trades["return_pct"] <= 0]
    positions = len(trades)
    win_rate = len(wins) / positions if positions else np.nan
    loss_rate = len(losses) / positions if positions else np.nan
    average_win = wins["return_pct"].mean() if len(wins) else np.nan
    average_loss = losses["return_pct"].mean() if len(losses) else np.nan
    average_return = trades["return_pct"].mean() if positions else np.nan
    reward_risk = average_win / abs(average_loss) if pd.notna(average_win) and pd.notna(average_loss) and average_loss != 0 else np.nan
    expectancy = (win_rate * average_win + loss_rate * average_loss) if positions else np.nan

    return {
        "market": market,
        "trade_cost": trade_cost,
        "net_perf_all": round((strategy_norm.iloc[-1] / strategy_norm.iloc[0] - 1.0) * 100, 2),
        "asset_perf": round((asset_norm.iloc[-1] / asset_norm.iloc[0] - 1.0) * 100, 2),
        "beta_vs_asset": round(float(beta), 3) if pd.notna(beta) else np.nan,
        "positions": positions,
        "wins": round(win_rate * 100, 2) if pd.notna(win_rate) else np.nan,
        "losses": round(loss_rate * 100, 2) if pd.notna(loss_rate) else np.nan,
        "max_drawdown": round(drawdown(strategy_norm).min() * 100, 2),
        "average_win": round(float(average_win), 2) if pd.notna(average_win) else np.nan,
        "average_loss": round(float(average_loss), 2) if pd.notna(average_loss) else np.nan,
        "average_return": round(float(average_return), 2) if pd.notna(average_return) else np.nan,
        "reward_risk_ratio": round(float(reward_risk), 3) if pd.notna(reward_risk) else np.nan,
        "expectancy": round(float(expectancy), 2) if pd.notna(expectancy) else np.nan,
    }


def pct_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return ""
    text = frame.fillna("").astype(str)
    columns = list(text.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for _, row in text.iterrows():
        lines.append("| " + " | ".join(row[column] for column in columns) + " |")
    return "\n".join(lines)


def plot_curves(curves: pd.DataFrame, drawdowns: pd.DataFrame, output: Path) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    curves.plot(ax=axes[0], linewidth=1.5)
    axes[0].set_title("Equity Curve")
    axes[0].set_ylabel("Growth of $1")
    axes[0].grid(True, alpha=0.3)
    drawdowns.mul(100).plot(ax=axes[1], linewidth=1.2)
    axes[1].set_title("Drawdown Curve")
    axes[1].set_ylabel("Drawdown %")
    axes[1].grid(True, alpha=0.3)
    fig.tight_layout()
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=150)
    plt.close(fig)


def write_performance_package(
    *,
    strategy_name: str,
    prefix: Path,
    equity_by_name: dict[str, pd.Series],
    trades: pd.DataFrame,
    benchmark_name: str,
    market: str,
    trade_cost: str = "0%",
    periods_per_year: int = 12,
) -> None:
    curves = pd.DataFrame({name: series / series.iloc[0] for name, series in equity_by_name.items()}).dropna(how="all")
    drawdowns = curves.apply(lambda column: drawdown(column.dropna()).reindex(curves.index))
    metrics = pd.DataFrame(
        [asdict(metric_row(name, series, periods_per_year=periods_per_year)) for name, series in equity_by_name.items()]
    )
    for column in TRENDSPIDER_STYLE_COLUMNS:
        metrics[column] = pd.Series([""] * len(metrics), dtype=object)
    extra_metrics = trendspider_style_metrics(
        strategy_equity=equity_by_name[strategy_name],
        asset_equity=equity_by_name[benchmark_name],
        trades=trades,
        market=market,
        trade_cost=trade_cost,
    )
    strategy_mask = metrics["strategy"] == strategy_name
    for column in TRENDSPIDER_STYLE_COLUMNS:
        metrics.loc[strategy_mask, column] = extra_metrics[column]

    annual = annual_rows(equity_by_name)
    annual_returns, annual_drawdowns = annual_wide_tables(annual, list(equity_by_name))
    trades_summary = trade_summary(trades) if not trades.empty else pd.DataFrame()

    curves_path = prefix.with_name(prefix.name + "_equity_curves.csv")
    drawdown_path = prefix.with_name(prefix.name + "_drawdown_curves.csv")
    metrics_path = prefix.with_name(prefix.name + "_summary_metrics.csv")
    annual_path = prefix.with_name(prefix.name + "_annual_return_drawdown.csv")
    annual_returns_path = prefix.with_name(prefix.name + "_annual_returns.csv")
    annual_drawdowns_path = prefix.with_name(prefix.name + "_annual_drawdowns.csv")
    trades_path = prefix.with_name(prefix.name + "_trades.csv")
    trades_summary_path = prefix.with_name(prefix.name + "_holding_period_by_outcome.csv")
    extra_metrics_path = prefix.with_name(prefix.name + "_trendspider_style_metrics.json")
    plot_path = prefix.with_name(prefix.name + "_curves.png")
    markdown_path = prefix.with_suffix(".md")

    prefix.parent.mkdir(parents=True, exist_ok=True)
    curves.to_csv(curves_path, index_label="date")
    drawdowns.to_csv(drawdown_path, index_label="date")
    metrics.to_csv(metrics_path, index=False)
    annual.to_csv(annual_path, index=False)
    annual_returns.to_csv(annual_returns_path, index=False)
    annual_drawdowns.to_csv(annual_drawdowns_path, index=False)
    trades.to_csv(trades_path, index=False)
    trades_summary.to_csv(trades_summary_path, index=False)
    extra_metrics_path.write_text(json.dumps(extra_metrics, indent=2), encoding="utf-8")
    plot_curves(curves, drawdowns, plot_path)

    lines = [
        f"# {strategy_name} OOS Performance",
        "",
        f"Period: {equity_by_name[strategy_name].index[0].date()} to {equity_by_name[strategy_name].index[-1].date()}.",
        "",
        "## TrendSpider-Style Metrics",
        "",
        "These fields use the metric names implied by the screenshot, but values are calculated from this strategy's OOS data.",
        "",
        pct_table(pd.DataFrame([extra_metrics])),
        "",
        "## OOS Summary Metrics",
        "",
        pct_table(metrics),
        "",
        "## Holding Period By Outcome",
        "",
        pct_table(trades_summary),
        "",
        "## Annual Return",
        "",
        pct_table(annual_returns),
        "",
        "## Annual Drawdown",
        "",
        pct_table(annual_drawdowns),
        "",
        "## Outputs",
        "",
        f"- Summary metrics: `{metrics_path}`",
        f"- Annual return/drawdown long table: `{annual_path}`",
        f"- Annual returns comparison: `{annual_returns_path}`",
        f"- Annual drawdowns comparison: `{annual_drawdowns_path}`",
        f"- Trades and holding periods: `{trades_path}`",
        f"- Holding-period summary: `{trades_summary_path}`",
        f"- Equity curves: `{curves_path}`",
        f"- Drawdown curves: `{drawdown_path}`",
        f"- Curve image: `{plot_path}`",
        f"- TrendSpider-style metrics JSON: `{extra_metrics_path}`",
    ]
    markdown_path.write_text("\n".join(lines), encoding="utf-8")

    print(markdown_path)
    print(metrics.to_string(index=False))
    if not trades_summary.empty:
        print(trades_summary.to_string(index=False))


def load_sp500_nasdaq_package(strategy_key: str) -> tuple[str, dict[str, pd.Series], pd.DataFrame, str, str]:
    specs = {
        "sp500_top5_l63_s0_none_dca1": MomentumStrategyConfig("SP500", 5, 63, 0, "none", 1),
        "nasdaq100_top3_l126_s21_none_dca3": MomentumStrategyConfig("NASDAQ100", 3, 126, 21, "none", 3),
    }
    config = specs[strategy_key]
    sp500_timeline = load_sp500_timeline()
    nasdaq_current, nasdaq_changes = load_nasdaq100_current_and_changes()
    tickers = universe_tickers_from_membership(sp500_timeline, nasdaq_current, nasdaq_changes)
    prices = fetch_momentum_prices(sorted(tickers), PRICE_START, MOMENTUM_OOS_END)
    open_prices = prices["Open"].sort_index()
    close_prices = prices["Close"].sort_index()
    months = precompute_sp500_nasdaq_months(open_prices, close_prices, sp500_timeline, nasdaq_current, nasdaq_changes)
    monthly = run_sp500_nasdaq_config(config, months)
    monthly_oos = monthly[monthly["period"] == "OOS"].copy()
    strategy_name = config.name
    strategy_equity = equity_from_monthly(monthly_oos, strategy_name, final_date=close_prices.index[-1])
    benchmark_symbol = "SPY" if config.universe == "SP500" else "QQQ"
    benchmark_name = f"{benchmark_symbol} buy-and-hold"
    benchmark_equity = benchmark_monthly_equity(
        open_prices,
        close_prices,
        benchmark_symbol,
        monthly_oos["trade_date"].iloc[0],
        monthly_oos["trade_date"].iloc[-1],
        benchmark_name,
    )
    trades = monthly_trade_segments(monthly_oos, open_prices, close_prices)
    return strategy_name, {strategy_name: strategy_equity, benchmark_name: benchmark_equity}, trades, benchmark_name, benchmark_symbol


def load_smh_package() -> tuple[str, dict[str, pd.Series], pd.DataFrame, str, str]:
    holdings = load_historical_holdings()
    snapshots = snapshot_tickers_by_public_date(holdings)
    historical_tickers = sorted(set(holdings["ticker"]))
    prices = fetch_smh_prices(sorted(set(historical_tickers) | {"SMH"}), SMH_PRICE_START, SMH_OOS_END)
    open_prices = prices["Open"].sort_index()
    close_prices = prices["Close"].sort_index()
    coverage = price_coverage(open_prices, close_prices, sorted(set(historical_tickers) | {"SMH"}))
    available_tickers = set(coverage.loc[coverage["available"], "ticker"]) - {"SMH"}
    months = precompute_smh_months(open_prices, close_prices, snapshots, available_tickers)
    config = {"top_n": 2, "lookback": 252, "skip": 0, "cash_filter": "smh_sma100", "dca_steps": 1}
    monthly = run_smh_strategy(config, months)
    monthly_oos = monthly[monthly["period"] == "OOS"].copy()
    strategy_name = "SMH_HIST_PIT Top2 L252 S0 smh_sma100 DCA1"
    strategy_equity = equity_from_monthly(monthly_oos, strategy_name, final_date=close_prices.index[-1])
    benchmark_name = "SMH buy-and-hold"
    benchmark_equity = benchmark_monthly_equity(
        open_prices,
        close_prices,
        "SMH",
        monthly_oos["trade_date"].iloc[0],
        monthly_oos["trade_date"].iloc[-1],
        benchmark_name,
    )
    trades = monthly_trade_segments(monthly_oos, open_prices, close_prices)
    return strategy_name, {strategy_name: strategy_equity, benchmark_name: benchmark_equity}, trades, benchmark_name, "SMH"


def run_soxl_report(args: argparse.Namespace, prefix: Path) -> None:
    close_all = fetch_adjusted_close(["SOXL", "TQQQ", "QQQ"], "2010-03-11", args.end)
    strategy_equity, targets = run_soxl_tqqq_cash(close_all, args.start)
    close = close_all.loc[strategy_equity.index]
    benchmarks = {
        "SOXL buy-and-hold": close["SOXL"] / close["SOXL"].iloc[0],
        "TQQQ buy-and-hold": close["TQQQ"] / close["TQQQ"].iloc[0],
    }
    trades = trade_segments(close, targets)
    write_performance_package(
        strategy_name=SOXL_TQQQ_NAME,
        prefix=prefix,
        equity_by_name={SOXL_TQQQ_NAME: strategy_equity, **benchmarks},
        trades=trades,
        benchmark_name="SOXL buy-and-hold",
        market="SOXL/TQQQ daily rotation",
        periods_per_year=252,
    )


def run_monthly_report(strategy_key: str, prefix: Path) -> None:
    if strategy_key in {"sp500_top5_l63_s0_none_dca1", "nasdaq100_top3_l126_s21_none_dca3"}:
        strategy_name, equity_by_name, trades, benchmark_name, market = load_sp500_nasdaq_package(strategy_key)
    elif strategy_key == "smh_hist_pit_top2_l252_s0_smh_sma100_dca1":
        strategy_name, equity_by_name, trades, benchmark_name, market = load_smh_package()
    else:
        raise ValueError(f"Unsupported monthly strategy: {strategy_key}")
    write_performance_package(
        strategy_name=strategy_name,
        prefix=prefix,
        equity_by_name=equity_by_name,
        trades=trades,
        benchmark_name=benchmark_name,
        market=market,
        periods_per_year=12,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate reusable strategy performance metrics.")
    parser.add_argument("--strategy", default="soxl_tqqq_rotation_cash", choices=sorted(STRATEGY_SPECS))
    parser.add_argument("--start", default="2020-01-02")
    parser.add_argument("--end", default=None)
    parser.add_argument("--output-prefix", default=None)
    args = parser.parse_args()

    default_prefix = REPORT_DIR / STRATEGY_SPECS[args.strategy]["output_stem"]
    prefix = Path(args.output_prefix) if args.output_prefix else default_prefix
    if args.strategy == "soxl_tqqq_rotation_cash":
        run_soxl_report(args, prefix)
    else:
        run_monthly_report(args.strategy, prefix)


if __name__ == "__main__":
    main()
