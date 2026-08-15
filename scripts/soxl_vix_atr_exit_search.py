from __future__ import annotations

from dataclasses import dataclass
from itertools import product
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
OUTPUT_STEM = "soxl_vix_atr_exit_search"


@dataclass(frozen=True)
class Config:
    name: str
    exit_vix_below: float
    atr_window: int | None
    atr_mult: float | None
    cooldown_days: int


def fetch_ohlc() -> pd.DataFrame:
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
    if raw.empty or not isinstance(raw.columns, pd.MultiIndex):
        raise RuntimeError("No multi-symbol yfinance data returned for SOXL and ^VIX.")
    frame = pd.DataFrame(
        {
            "SOXL_open": raw["Open"]["SOXL"],
            "SOXL_high": raw["High"]["SOXL"],
            "SOXL_low": raw["Low"]["SOXL"],
            "SOXL_close": raw["Close"]["SOXL"],
            "VIX_close": raw["Close"]["^VIX"],
        }
    ).dropna()
    frame.index = pd.to_datetime(frame.index).tz_localize(None)
    return frame


def add_atr(frame: pd.DataFrame, window: int) -> pd.Series:
    previous_close = frame["SOXL_close"].shift(1)
    true_range = pd.concat(
        [
            frame["SOXL_high"] - frame["SOXL_low"],
            (frame["SOXL_high"] - previous_close).abs(),
            (frame["SOXL_low"] - previous_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    return true_range.rolling(window).mean()


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


def simulate(frame: pd.DataFrame, config: Config) -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = frame.copy()
    atr = add_atr(frame, config.atr_window).to_numpy(dtype=float) if config.atr_window is not None else None
    dates = frame.index
    opens = frame["SOXL_open"].to_numpy(dtype=float)
    closes = frame["SOXL_close"].to_numpy(dtype=float)
    vix = frame["VIX_close"].to_numpy(dtype=float)

    capital = 1.0
    in_position = False
    pending: str | None = None
    pending_reason = ""
    entry_date: pd.Timestamp | None = None
    entry_price: float | None = None
    high_close: float | None = None
    cooldown_remaining = 0
    rows: list[dict[str, object]] = []
    trades: list[dict[str, object]] = []

    for i, date in enumerate(dates):
        action = "HOLD"
        action_reason = ""
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
                high_close = float(closes[i])
                execution_price = float(opens[i])
                action = "BUY"
                action_reason = pending_reason
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
                        "exit_reason": pending_reason,
                        "holding_calendar_days": int((date - entry_date).days),
                        "holding_trading_days": int(len(dates[(dates >= entry_date) & (dates <= date)]) - 1),
                    }
                )
                capital = open_equity
                in_position = False
                entry_date = None
                entry_price = None
                high_close = None
                cooldown_remaining = config.cooldown_days
                execution_price = exit_price
                action = "SELL"
                action_reason = pending_reason
                equity = capital
            else:
                equity = capital * (closes[i] / previous_close) if in_position else capital

        capital = float(equity)
        if in_position:
            high_close = max(float(high_close), float(closes[i])) if high_close is not None else float(closes[i])

        pending = None
        pending_reason = ""
        signal = "NONE"
        if in_position:
            exit_reasons: list[str] = []
            if vix[i] < config.exit_vix_below:
                exit_reasons.append(f"vix_below_{config.exit_vix_below:g}")
            if atr is not None and np.isfinite(atr[i]) and high_close is not None:
                atr_stop = high_close - float(config.atr_mult) * float(atr[i])
                if closes[i] <= atr_stop:
                    exit_reasons.append(f"atr{config.atr_window}_{config.atr_mult:g}x")
            if exit_reasons:
                pending = "SELL"
                pending_reason = "+".join(exit_reasons)
                signal = "SELL_NEXT_OPEN"
        elif cooldown_remaining > 0:
            cooldown_remaining -= 1
        elif vix[i] > 35:
            pending = "BUY"
            pending_reason = "vix_above_35"
            signal = "BUY_NEXT_OPEN"

        rows.append(
            {
                "date": date.date().isoformat(),
                "equity": capital,
                "target": "SOXL" if in_position else "CASH",
                "action": action,
                "action_reason": action_reason,
                "execution_price": execution_price,
                "signal": signal,
                "pending_next_open": pending or "",
                "pending_reason": pending_reason,
                "SOXL_open": opens[i],
                "SOXL_close": closes[i],
                "VIX_close": vix[i],
                "benchmark_soxl_buy_hold": closes[i] / closes[0],
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
                "exit_reason": "open",
                "holding_calendar_days": int((final_date - entry_date).days),
                "holding_trading_days": int(len(dates[dates >= entry_date]) - 1),
            }
        )

    daily = pd.DataFrame(rows)
    daily["date"] = pd.to_datetime(daily["date"])
    return daily.set_index("date"), pd.DataFrame(trades)


def summarize(equity: pd.Series) -> dict[str, float]:
    normalized = equity / equity.iloc[0]
    returns = normalized.pct_change().dropna()
    return {
        "return_pct": round((normalized.iloc[-1] - 1.0) * 100, 2),
        "cagr_pct": round(cagr_pct(equity), 2),
        "max_drawdown_pct": round(max_drawdown(equity), 2),
        "sharpe": round(sharpe_ratio(equity), 3),
        "volatility_pct": round(returns.std(ddof=0) * math.sqrt(252) * 100, 2),
    }


def result_row(config: Config, daily: pd.DataFrame, trades: pd.DataFrame) -> dict[str, object]:
    is_daily = daily[daily.index < SPLIT_DATE]
    oos_daily = daily[daily.index >= SPLIT_DATE]
    is_metrics = summarize(is_daily["equity"])
    oos_metrics = summarize(oos_daily["equity"])
    full_metrics = summarize(daily["equity"])
    return {
        "variant": config.name,
        "exit_vix_below": config.exit_vix_below,
        "atr_window": config.atr_window,
        "atr_mult": config.atr_mult,
        "cooldown_days": config.cooldown_days,
        "is_return_pct": is_metrics["return_pct"],
        "is_max_drawdown_pct": is_metrics["max_drawdown_pct"],
        "is_sharpe": is_metrics["sharpe"],
        "oos_return_pct": oos_metrics["return_pct"],
        "oos_max_drawdown_pct": oos_metrics["max_drawdown_pct"],
        "oos_sharpe": oos_metrics["sharpe"],
        "full_return_pct": full_metrics["return_pct"],
        "full_max_drawdown_pct": full_metrics["max_drawdown_pct"],
        "full_sharpe": full_metrics["sharpe"],
        "oos_exposure_days_pct": round(oos_daily["target"].eq("SOXL").mean() * 100, 2),
        "trades": len(trades),
    }


def configs() -> list[Config]:
    output: list[Config] = []
    for exit_vix in [10, 15, 20]:
        output.append(Config(f"exit VIX<{exit_vix:g}", exit_vix, None, None, 0))
    for exit_vix, window, mult, cooldown in product([10, 15, 20], [10, 14, 21], [2.0, 3.0, 4.0, 5.0, 6.0], [0, 21]):
        suffix = f"; cooldown {cooldown}d" if cooldown else ""
        output.append(Config(f"exit VIX<{exit_vix:g}; ATR{window} trail {mult:g}x{suffix}", exit_vix, window, mult, cooldown))
    return output


def markdown_table(frame: pd.DataFrame) -> str:
    text = frame.fillna("").astype(str)
    lines = [
        "| " + " | ".join(text.columns) + " |",
        "| " + " | ".join(["---"] * len(text.columns)) + " |",
    ]
    for _, row in text.iterrows():
        lines.append("| " + " | ".join(str(row[column]).replace("|", "\\|") for column in text.columns) + " |")
    return "\n".join(lines)


def write_outputs(results: pd.DataFrame, best_daily: pd.DataFrame, best_trades: pd.DataFrame) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    all_path = REPORTS / f"{OUTPUT_STEM}_all.csv"
    selected_path = REPORTS / f"{OUTPUT_STEM}_selected.csv"
    daily_path = REPORTS / f"{OUTPUT_STEM}_best_daily.csv"
    trades_path = REPORTS / f"{OUTPUT_STEM}_best_trades.csv"
    md_path = REPORTS / f"{OUTPUT_STEM}.md"

    selected = results[
        (results["is_return_pct"] > 0)
        & (results["oos_return_pct"] > 0)
        & (results["oos_exposure_days_pct"] >= 10)
    ].sort_values(["is_max_drawdown_pct", "is_sharpe", "oos_return_pct"], ascending=[False, False, False]).head(20)
    selected.insert(0, "selection_rank", np.arange(1, len(selected) + 1))

    results.to_csv(all_path, index=False)
    selected.to_csv(selected_path, index=False)
    best_daily.to_csv(daily_path)
    best_trades.to_csv(trades_path, index=False)

    show_cols = [
        "selection_rank",
        "variant",
        "is_return_pct",
        "is_max_drawdown_pct",
        "is_sharpe",
        "oos_return_pct",
        "oos_max_drawdown_pct",
        "oos_sharpe",
        "oos_exposure_days_pct",
        "trades",
    ]
    lines = [
        "# SOXL VIX ATR Exit Search",
        "",
        "Rules: buy SOXL next open after VIX closes above 35. Sell next open after VIX closes below the configured threshold or after an ATR trailing-stop signal.",
        f"ATR stop: SOXL close <= highest close since entry - multiplier * ATR(window). Split: IS before {SPLIT_DATE.date()}, OOS from {SPLIT_DATE.date()}.",
        "",
        "## Selected Variants",
        "",
        markdown_table(selected[show_cols]),
        "",
        "## Outputs",
        "",
        f"- All variants: `{all_path}`",
        f"- Selected variants: `{selected_path}`",
        f"- Best selected daily curve: `{daily_path}`",
        f"- Best selected trades: `{trades_path}`",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(md_path)
    print(selected[show_cols].to_string(index=False))


def main() -> None:
    frame = fetch_ohlc()
    rows: list[dict[str, object]] = []
    daily_by_name: dict[str, pd.DataFrame] = {}
    trades_by_name: dict[str, pd.DataFrame] = {}
    for config in configs():
        daily, trades = simulate(frame, config)
        rows.append(result_row(config, daily, trades))
        daily_by_name[config.name] = daily
        trades_by_name[config.name] = trades
    results = pd.DataFrame(rows)
    selected = results[
        (results["is_return_pct"] > 0)
        & (results["oos_return_pct"] > 0)
        & (results["oos_exposure_days_pct"] >= 10)
    ].sort_values(["is_max_drawdown_pct", "is_sharpe", "oos_return_pct"], ascending=[False, False, False])
    best_name = str(selected.iloc[0]["variant"])
    write_outputs(results, daily_by_name[best_name], trades_by_name[best_name])


if __name__ == "__main__":
    main()
