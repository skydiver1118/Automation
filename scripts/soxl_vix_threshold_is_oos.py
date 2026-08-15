from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import math

import numpy as np
import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"

START = "2010-03-11"
END_EXCLUSIVE = "2026-05-21"
SPLIT_DATE = pd.Timestamp("2020-01-01")

STRATEGY_NAME = "SOXL VIX 35/10 next-open"
OUTPUT_STEM = "soxl_vix_35_10_is_oos"


@dataclass(frozen=True)
class SummaryRow:
    period: str
    date_range: str
    cumulative_return_pct: float
    cagr_pct: float
    max_drawdown_pct: float
    sharpe: float
    volatility_pct: float
    exposure_days_pct: float
    trades: int
    wins: int
    losses: int
    win_rate_pct: float
    average_trade_return_pct: float
    benchmark_return_pct: float
    benchmark_max_drawdown_pct: float


def fetch_inputs() -> pd.DataFrame:
    raw = yf.download(
        ["SOXL", "^VIX"],
        start=START,
        end=END_EXCLUSIVE,
        interval="1d",
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    if raw.empty:
        raise RuntimeError("No yfinance data returned for SOXL and ^VIX.")

    if not isinstance(raw.columns, pd.MultiIndex):
        raise RuntimeError("Expected yfinance multi-symbol OHLC data.")

    frame = pd.DataFrame(
        {
            "SOXL_open": raw["Open"]["SOXL"],
            "SOXL_close": raw["Close"]["SOXL"],
            "VIX_close": raw["Close"]["^VIX"],
        }
    ).dropna()
    frame.index = pd.to_datetime(frame.index).tz_localize(None)
    return frame


def max_drawdown(equity: pd.Series) -> float:
    normalized = equity / equity.iloc[0]
    return float((normalized / normalized.cummax() - 1.0).min() * 100)


def sharpe_ratio(equity: pd.Series) -> float:
    returns = (equity / equity.iloc[0]).pct_change().dropna()
    std = returns.std(ddof=0)
    if not len(returns) or std == 0 or not np.isfinite(std):
        return np.nan
    return float(returns.mean() / std * math.sqrt(252))


def cagr_pct(equity: pd.Series) -> float:
    years = max((equity.index[-1] - equity.index[0]).days, 1) / 365.25
    return float(((equity.iloc[-1] / equity.iloc[0]) ** (1.0 / years) - 1.0) * 100)


def simulate_next_open(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    dates = frame.index
    opens = frame["SOXL_open"].to_numpy(dtype=float)
    closes = frame["SOXL_close"].to_numpy(dtype=float)
    vix = frame["VIX_close"].to_numpy(dtype=float)

    capital = 1.0
    in_position = False
    pending: str | None = None
    entry_date: pd.Timestamp | None = None
    entry_price: float | None = None

    daily_rows: list[dict[str, object]] = []
    trades: list[dict[str, object]] = []

    for i, date in enumerate(dates):
        action = "HOLD"
        execution_price = np.nan

        if i == 0:
            equity = capital
        else:
            previous_close = closes[i - 1]
            open_equity = capital * (opens[i] / previous_close) if in_position else capital

            if pending == "BUY" and not in_position:
                in_position = True
                entry_date = date
                entry_price = float(opens[i])
                execution_price = float(opens[i])
                action = "BUY"
                equity = open_equity * (closes[i] / opens[i])
            elif pending == "SELL" and in_position:
                exit_price = float(opens[i])
                trade_return = exit_price / float(entry_price) - 1.0
                trades.append(
                    {
                        "entry_date": entry_date.date().isoformat(),
                        "exit_date": date.date().isoformat(),
                        "symbol": "SOXL",
                        "exit_to": "CASH",
                        "entry_price": round(float(entry_price), 4),
                        "exit_price": round(exit_price, 4),
                        "return_pct": round(trade_return * 100, 2),
                        "outcome": "win" if trade_return > 0 else "loss",
                        "holding_calendar_days": int((date - entry_date).days),
                        "holding_trading_days": int(len(dates[(dates >= entry_date) & (dates <= date)]) - 1),
                    }
                )
                capital = open_equity
                in_position = False
                entry_date = None
                entry_price = None
                execution_price = exit_price
                action = "SELL"
                equity = capital
            else:
                equity = capital * (closes[i] / previous_close) if in_position else capital

        capital = float(equity)
        pending = None
        signal = "NONE"
        if not in_position and vix[i] > 35:
            pending = "BUY"
            signal = "BUY_NEXT_OPEN"
        elif in_position and vix[i] < 10:
            pending = "SELL"
            signal = "SELL_NEXT_OPEN"

        daily_rows.append(
            {
                "date": date.date().isoformat(),
                "equity": capital,
                "benchmark_soxl_buy_hold": closes[i] / closes[0],
                "target": "SOXL" if in_position else "CASH",
                "action": action,
                "execution_price": execution_price,
                "signal": signal,
                "pending_next_open": pending or "",
                "SOXL_open": opens[i],
                "SOXL_close": closes[i],
                "VIX_close": vix[i],
            }
        )

    if in_position and entry_date is not None and entry_price is not None:
        final_date = dates[-1]
        final_price = float(closes[-1])
        trade_return = final_price / entry_price - 1.0
        trades.append(
            {
                "entry_date": entry_date.date().isoformat(),
                "exit_date": final_date.date().isoformat(),
                "symbol": "SOXL",
                "exit_to": "OPEN",
                "entry_price": round(entry_price, 4),
                "exit_price": round(final_price, 4),
                "return_pct": round(trade_return * 100, 2),
                "outcome": "win" if trade_return > 0 else "loss",
                "holding_calendar_days": int((final_date - entry_date).days),
                "holding_trading_days": int(len(dates[dates >= entry_date]) - 1),
            }
        )

    daily = pd.DataFrame(daily_rows)
    daily["date"] = pd.to_datetime(daily["date"])
    daily = daily.set_index("date")
    return daily, pd.DataFrame(trades)


def period_summary(
    period: str,
    daily: pd.DataFrame,
    trades: pd.DataFrame,
    mask: pd.Series,
) -> SummaryRow:
    sub = daily.loc[mask].copy()
    equity = sub["equity"]
    benchmark = sub["benchmark_soxl_buy_hold"]
    normalized_benchmark = benchmark / benchmark.iloc[0]

    period_trades = trades.copy()
    if not period_trades.empty:
        entries = pd.to_datetime(period_trades["entry_date"])
        period_trades = period_trades[(entries >= sub.index[0]) & (entries <= sub.index[-1])]
    wins = period_trades[period_trades["return_pct"] > 0] if not period_trades.empty else period_trades
    losses = period_trades[period_trades["return_pct"] <= 0] if not period_trades.empty else period_trades
    trade_count = len(period_trades)

    return SummaryRow(
        period=period,
        date_range=f"{sub.index[0].date()} to {sub.index[-1].date()}",
        cumulative_return_pct=round((equity.iloc[-1] / equity.iloc[0] - 1.0) * 100, 2),
        cagr_pct=round(cagr_pct(equity), 2),
        max_drawdown_pct=round(max_drawdown(equity), 2),
        sharpe=round(sharpe_ratio(equity), 3),
        volatility_pct=round((equity / equity.iloc[0]).pct_change().dropna().std(ddof=0) * math.sqrt(252) * 100, 2),
        exposure_days_pct=round((sub["target"].eq("SOXL").mean()) * 100, 2),
        trades=trade_count,
        wins=len(wins),
        losses=len(losses),
        win_rate_pct=round(len(wins) / trade_count * 100, 2) if trade_count else np.nan,
        average_trade_return_pct=round(period_trades["return_pct"].mean(), 2) if trade_count else np.nan,
        benchmark_return_pct=round((normalized_benchmark.iloc[-1] - 1.0) * 100, 2),
        benchmark_max_drawdown_pct=round(max_drawdown(normalized_benchmark), 2),
    )


def annual_rows(daily: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for year, group in daily.groupby(daily.index.year):
        equity = group["equity"]
        benchmark = group["benchmark_soxl_buy_hold"] / group["benchmark_soxl_buy_hold"].iloc[0]
        rows.append(
            {
                "year": int(year),
                "strategy_return_pct": round((equity.iloc[-1] / equity.iloc[0] - 1.0) * 100, 2),
                "strategy_max_drawdown_pct": round(max_drawdown(equity), 2),
                "soxl_buy_hold_return_pct": round((benchmark.iloc[-1] - 1.0) * 100, 2),
                "soxl_buy_hold_max_drawdown_pct": round(max_drawdown(benchmark), 2),
                "exposure_days_pct": round(group["target"].eq("SOXL").mean() * 100, 2),
            }
        )
    return pd.DataFrame(rows)


def markdown_table(frame: pd.DataFrame) -> str:
    text = frame.fillna("").astype(str)
    lines = [
        "| " + " | ".join(text.columns) + " |",
        "| " + " | ".join(["---"] * len(text.columns)) + " |",
    ]
    for _, row in text.iterrows():
        lines.append("| " + " | ".join(row[column] for column in text.columns) + " |")
    return "\n".join(lines)


def write_report(daily: pd.DataFrame, trades: pd.DataFrame, summary: pd.DataFrame, annual: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    daily_path = REPORTS / f"{OUTPUT_STEM}_daily.csv"
    trades_path = REPORTS / f"{OUTPUT_STEM}_trades.csv"
    summary_path = REPORTS / f"{OUTPUT_STEM}_summary.csv"
    annual_path = REPORTS / f"{OUTPUT_STEM}_annual.csv"
    markdown_path = REPORTS / f"{OUTPUT_STEM}.md"

    daily.to_csv(daily_path)
    trades.to_csv(trades_path, index=False)
    summary.to_csv(summary_path, index=False)
    annual.to_csv(annual_path, index=False)

    latest = daily.iloc[-1]
    open_trade_note = ""
    if not trades.empty and trades.iloc[-1]["exit_to"] == "OPEN":
        last_trade = trades.iloc[-1]
        open_trade_note = (
            f"Current open trade: entered {last_trade['entry_date']} at {last_trade['entry_price']}; "
            f"marked through {last_trade['exit_date']} at {last_trade['exit_price']}."
        )

    lines = [
        f"# {STRATEGY_NAME}",
        "",
        "Rules:",
        "",
        "- Instrument: SOXL.",
        "- Signal source: S&P 500 VIX index close (`^VIX`).",
        "- Buy when VIX closes above 35; execute at the next SOXL open.",
        "- Sell when VIX closes below 10; execute at the next SOXL open.",
        "- Stay in cash otherwise. No leverage beyond SOXL, no DCA, no costs/slippage.",
        f"- Same split as the SOXL/TQQQ research: IS before {SPLIT_DATE.date()}, OOS from {SPLIT_DATE.date()} onward.",
        "",
        f"Data range: {daily.index[0].date()} to {daily.index[-1].date()} from yfinance adjusted OHLC.",
        f"Latest state: target `{latest['target']}`, latest VIX close `{latest['VIX_close']:.2f}`, pending next-open action `{latest['pending_next_open']}`.",
        open_trade_note,
        "",
        "## IS/OOS Summary",
        "",
        markdown_table(summary),
        "",
        "## Trades",
        "",
        markdown_table(trades) if not trades.empty else "No trades.",
        "",
        "## Outputs",
        "",
        f"- Daily curve: `{daily_path}`",
        f"- Trades: `{trades_path}`",
        f"- Summary: `{summary_path}`",
        f"- Annual table: `{annual_path}`",
    ]
    markdown_path.write_text("\n".join(line for line in lines if line is not None), encoding="utf-8")
    print(markdown_path)
    print(summary.to_string(index=False))


def main() -> None:
    frame = fetch_inputs()
    daily, trades = simulate_next_open(frame)
    is_mask = daily.index < SPLIT_DATE
    oos_mask = daily.index >= SPLIT_DATE
    full_mask = pd.Series(True, index=daily.index)
    summary = pd.DataFrame(
        [
            asdict(period_summary("IS", daily, trades, is_mask)),
            asdict(period_summary("OOS", daily, trades, oos_mask)),
            asdict(period_summary("Full", daily, trades, full_mask)),
        ]
    )
    annual = annual_rows(daily)
    write_report(daily, trades, summary, annual)


if __name__ == "__main__":
    main()
