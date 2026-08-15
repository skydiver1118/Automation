from __future__ import annotations

from pathlib import Path
import math
import sys

import numpy as np
import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
sys.path.insert(0, str(ROOT / "scripts"))

from soxl_tqqq_cash_signal_scanner import (  # noqa: E402
    StrategyConfig as CashScannerConfig,
    build_base_rotation,
    cash_filtered_targets,
)


START = pd.Timestamp("2020-01-01")
SYMBOLS = ["SOXL", "TQQQ"]


def fetch_adjusted_close() -> pd.DataFrame:
    raw = yf.download(
        ["SOXL", "TQQQ", "QQQ"],
        start="2010-03-11",
        end="2026-05-24",
        interval="1d",
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    if raw.empty:
        raise RuntimeError("No price data returned by yfinance.")
    close = raw["Close"].copy() if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]].copy()
    close = close[["SOXL", "TQQQ", "QQQ"]].dropna()
    close.index = pd.to_datetime(close.index).tz_localize(None)
    return close


def max_drawdown(values: np.ndarray) -> float:
    return float(np.min(values / np.maximum.accumulate(values) - 1) * 100)


def sharpe_ratio(values: np.ndarray) -> float:
    if len(values) < 2:
        return np.nan
    returns = np.empty(len(values), dtype=float)
    returns[0] = 0.0
    returns[1:] = values[1:] / values[:-1] - 1
    std = float(np.std(returns))
    if std == 0 or not np.isfinite(std):
        return np.nan
    return float(np.mean(returns) / std * math.sqrt(252))


def summary_row(name: str, equity: pd.Series) -> dict[str, object]:
    values = equity.to_numpy(dtype=float)
    return {
        "strategy": name,
        "period": f"{equity.index[0].date()} to {equity.index[-1].date()}",
        "cumulative_return_pct": round((float(values[-1]) / float(values[0]) - 1) * 100, 2),
        "max_drawdown_pct": round(max_drawdown(values / values[0]), 2),
        "sharpe": round(sharpe_ratio(values / values[0]), 3),
    }


def run_soxl_only(close: pd.DataFrame) -> pd.Series:
    soxl = close["SOXL"]
    fast = soxl.rolling(50).mean()
    slow = soxl.rolling(63).mean()
    trend_on = fast > slow
    equity = np.ones(len(close), dtype=float)
    in_position = False
    entry_price: float | None = None

    for i in range(1, len(close)):
        if in_position:
            equity[i] = equity[i - 1] * (float(soxl.iloc[i]) / float(soxl.iloc[i - 1]))
        else:
            equity[i] = equity[i - 1]

        if not np.isfinite(fast.iloc[i]) or not np.isfinite(slow.iloc[i]):
            continue

        close_i = float(soxl.iloc[i])
        if not in_position and bool(trend_on.iloc[i]):
            in_position = True
            entry_price = close_i
        elif in_position and entry_price is not None:
            stop_hit = close_i <= entry_price * 0.90
            trend_exit = not bool(trend_on.iloc[i])
            if stop_hit or trend_exit:
                in_position = False
                entry_price = None

    return pd.Series(equity, index=close.index, name="SOXL only daily scanner")


def run_cash_rotation_scanner(close: pd.DataFrame) -> pd.Series:
    config = CashScannerConfig()
    base = build_base_rotation(close, config)
    targets = cash_filtered_targets(close, base, config).reindex(close.index).ffill().fillna("CASH")
    equity = np.ones(len(close), dtype=float)
    held = str(targets.iloc[0])

    for i in range(1, len(close)):
        if held in SYMBOLS:
            equity[i] = equity[i - 1] * (float(close[held].iloc[i]) / float(close[held].iloc[i - 1]))
        else:
            equity[i] = equity[i - 1]
        held = str(targets.iloc[i])

    return pd.Series(equity, index=close.index, name="SOXL/TQQQ Rotation with cash daily scanner")


def cash_risk_on(
    *,
    selected: int,
    close_row: np.ndarray,
    asset_sma_row: np.ndarray,
    qqq_sma: float,
    prior_risk_on: bool,
) -> bool:
    selected_exit = np.isfinite(asset_sma_row[selected]) and close_row[selected] < asset_sma_row[selected]
    selected_reentry = np.isfinite(asset_sma_row[selected]) and close_row[selected] >= asset_sma_row[selected]
    qqq_exit = np.isfinite(qqq_sma) and close_row[2] < qqq_sma
    qqq_reentry = np.isfinite(qqq_sma) and close_row[2] >= qqq_sma
    if prior_risk_on:
        return not (selected_exit and qqq_exit)
    return bool(selected_reentry or qqq_reentry)


def run_rank1_dca(close: pd.DataFrame) -> pd.Series:
    close_px = close[["SOXL", "TQQQ", "QQQ"]].to_numpy(dtype=float)
    dates = close.index
    allocation = pd.read_csv(REPORTS / "soxl_tqqq_rotation_best_allocation.csv", parse_dates=["date"])
    allocation = allocation.set_index("date")["allocation"].sort_index().reindex(dates).ffill()
    selected_codes = allocation.map({"SOXL": 0, "TQQQ": 1}).fillna(1).to_numpy(dtype=int)
    asset_sma = close[SYMBOLS].rolling(150).mean().to_numpy(dtype=float)
    qqq_sma = close["QQQ"].rolling(150).mean().to_numpy(dtype=float)
    trend_sma = close[SYMBOLS].rolling(200).mean().to_numpy(dtype=float)

    equity = np.ones(len(close), dtype=float)
    held_code = int(selected_codes[0])
    in_cash = False
    risk_on = True
    units = 1
    price0 = float(close_px[0, held_code])
    anchor = price0
    low_since_extra = price0
    extra_entry_i: int | None = None
    current_exposure = 1.0

    def next_exposure(i: int) -> float:
        if in_cash:
            return 0.0
        exposure = 1.0
        if np.isfinite(trend_sma[i, held_code]) and close_px[i, held_code] < trend_sma[i, held_code]:
            exposure = min(exposure, 0.5)
        return exposure

    for i in range(1, len(dates)):
        if in_cash:
            equity[i] = equity[i - 1]
        else:
            equity[i] = equity[i - 1] * (1 + current_exposure * (float(close_px[i, held_code]) / float(close_px[i - 1, held_code]) - 1))

        selected = int(selected_codes[i])
        risk_on = cash_risk_on(
            selected=selected,
            close_row=close_px[i],
            asset_sma_row=asset_sma[i],
            qqq_sma=float(qqq_sma[i]),
            prior_risk_on=risk_on,
        )
        if not risk_on:
            in_cash = True
            units = 0
            extra_entry_i = None
            current_exposure = 0.0
            continue

        if in_cash:
            in_cash = False
            held_code = selected
            units = 1
            anchor = float(close_px[i, held_code])
            low_since_extra = anchor
            extra_entry_i = None
            current_exposure = next_exposure(i)
            continue

        if selected != held_code:
            held_code = selected
            units = 1
            anchor = float(close_px[i, held_code])
            low_since_extra = anchor
            extra_entry_i = None
            current_exposure = next_exposure(i)
            continue

        price = float(close_px[i, held_code])
        anchor = max(anchor, price)
        if units > 1:
            low_since_extra = min(low_since_extra, price)
            if price >= low_since_extra * 1.05 or (extra_entry_i is not None and i - extra_entry_i >= 5):
                units = 1
                extra_entry_i = None
                low_since_extra = price

        drop = price / anchor - 1
        if units == 1 and drop <= -0.10:
            units = 2
            extra_entry_i = i
            low_since_extra = price
        elif units == 2 and drop <= -0.20:
            units = 3
        current_exposure = next_exposure(i)

    return pd.Series(equity, index=close.index, name="selected_or_qqq SMA150 DCA/trend guard")


def main() -> None:
    REPORTS.mkdir(exist_ok=True)
    close = fetch_adjusted_close()[["SOXL", "TQQQ", "QQQ"]].dropna()

    curves = pd.DataFrame(index=close.index)
    strategies = [
        run_cash_rotation_scanner(close),
        run_soxl_only(close),
        run_rank1_dca(close),
    ]
    rows = []
    for curve in strategies:
        curves[curve.name] = curve
        rows.append(summary_row(curve.name, curve.loc[curve.index >= START]))

    summary = pd.DataFrame(rows)
    csv_path = ROOT / "SOXL_TQQQ_Three_Strategy_2020_To_Date.csv"
    xlsx_path = ROOT / "SOXL_TQQQ_Three_Strategy_2020_To_Date.xlsx"
    curves_path = REPORTS / "soxl_tqqq_three_strategy_2020_to_date_curves.csv"
    summary.to_csv(csv_path, index=False)
    curves_2020 = curves.loc[curves.index >= START]
    curves_2020.reset_index(names="date").to_csv(curves_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Summary", index=False)
        curves_2020.reset_index(names="date").to_excel(writer, sheet_name="Daily Curves", index=False)
    print(summary.to_string(index=False))
    print(csv_path)
    print(xlsx_path)
    print(curves_path)


if __name__ == "__main__":
    main()
