from __future__ import annotations

from pathlib import Path
import math

import numpy as np
import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
SYMBOLS = ["SMH", "QQQ"]
CONTEXT_SYMBOLS = ["SMH", "QQQ"]
START = "2010-03-11"
END_EXCLUSIVE = "2026-05-24"
SPLIT_DATE = pd.Timestamp("2020-01-01")


def fetch_adjusted_close() -> pd.DataFrame:
    raw = yf.download(
        CONTEXT_SYMBOLS,
        start=START,
        end=END_EXCLUSIVE,
        interval="1d",
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    if raw.empty:
        raise RuntimeError("No yfinance close data returned.")
    close = raw["Close"].copy() if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]].copy()
    close = close[CONTEXT_SYMBOLS].dropna()
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


def metrics(equity: np.ndarray, dates: pd.DatetimeIndex, mask: np.ndarray, cash: np.ndarray | None = None) -> dict[str, object]:
    sub = equity[mask]
    sub_dates = dates[mask]
    norm = sub / sub[0]
    out = {
        "range": f"{sub_dates[0].date()} to {sub_dates[-1].date()}",
        "return_pct": round((float(norm[-1]) - 1) * 100, 2),
        "max_drawdown_pct": round(max_drawdown(norm), 2),
        "sharpe": round(sharpe_ratio(norm), 3),
    }
    if cash is not None:
        out["cash_days_pct"] = round(float(np.mean(cash[mask]) * 100), 2)
    return out


def cash_risk_on(
    *,
    mode: str,
    selected: int,
    close_row: np.ndarray,
    asset_sma_row: np.ndarray,
    qqq_sma: float,
    prior_risk_on: bool,
    exit_buffer: float,
    reentry_buffer: float,
) -> bool:
    if mode == "none":
        return True
    selected_exit = np.isfinite(asset_sma_row[selected]) and close_row[selected] < asset_sma_row[selected] * (1 - exit_buffer)
    selected_reentry = np.isfinite(asset_sma_row[selected]) and close_row[selected] >= asset_sma_row[selected] * (1 + reentry_buffer)
    qqq_exit = np.isfinite(qqq_sma) and close_row[1] < qqq_sma * (1 - exit_buffer)
    qqq_reentry = np.isfinite(qqq_sma) and close_row[1] >= qqq_sma * (1 + reentry_buffer)
    if mode == "selected":
        return (not selected_exit) if prior_risk_on else bool(selected_reentry)
    if mode == "qqq":
        return (not qqq_exit) if prior_risk_on else bool(qqq_reentry)
    if mode == "selected_or_qqq":
        return (not (selected_exit and qqq_exit)) if prior_risk_on else bool(selected_reentry or qqq_reentry)
    if mode == "selected_and_qqq":
        return (not (selected_exit or qqq_exit)) if prior_risk_on else bool(selected_reentry and qqq_reentry)
    raise ValueError(f"Unknown cash mode: {mode}")


def variant_name(params: dict[str, object]) -> str:
    vol = "none" if params["vol_target"] is None else f"{params['vol_target']:.0%}/{params['vol_window']}d"
    return (
        f"cash={params['cash_mode']} SMA{params['cash_sma']} exit={params['cash_exit_buffer']:.0%} "
        f"reentry={params['cash_reentry_buffer']:.0%}; unit={params['unit_exposure']:.2f}, "
        f"cap={params['max_exposure']:.2f}, add={params['add1_drop']:.0%}/{params['add2_drop']:.0%}, "
        f"sell={params['sell_mode']} {params['sell_param']:.0%}, max_days={params['max_extra_days']}, "
        f"trend_sma={params['trend_guard_sma'] if params['trend_guard_sma'] is not None else 'none'}, "
        f"trend_exp={params['trend_guard_exposure'] if params['trend_guard_exposure'] is not None else 'none'}, "
        f"vol_target={vol}"
    )


def simulate(
    close_px: np.ndarray,
    dates: pd.DatetimeIndex,
    selected_codes: np.ndarray,
    trend_sma_cache: dict[int, np.ndarray],
    cash_sma_cache: dict[int, tuple[np.ndarray, np.ndarray]],
    realized_vol_cache: dict[int, np.ndarray],
    *,
    cash_mode: str,
    cash_sma: int,
    cash_exit_buffer: float,
    cash_reentry_buffer: float,
    unit_exposure: float,
    max_exposure: float,
    add1_drop: float,
    add2_drop: float,
    sell_mode: str,
    sell_param: float,
    max_extra_days: int,
    trend_guard_sma: int | None,
    trend_guard_exposure: float | None,
    vol_target: float | None,
    vol_window: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, int]:
    n = len(dates)
    trend_sma = trend_sma_cache[trend_guard_sma] if trend_guard_sma is not None else None
    cash_asset_sma, qqq_sma = cash_sma_cache[cash_sma]
    realized_vol = realized_vol_cache[vol_window]

    equity = np.ones(n, dtype=float)
    exposure_history = np.zeros(n, dtype=float)
    cash_history = np.zeros(n, dtype=bool)
    trade_events = 0

    held_code = int(selected_codes[0])
    in_cash = False
    risk_on = True
    units = 1
    price0 = float(close_px[0, held_code])
    anchor = price0
    high = price0
    low_since_extra = price0
    extra_avg_cost = np.nan
    extra_entry_i: int | None = None
    current_exposure = min(units * unit_exposure, max_exposure)

    def set_next_exposure(signal_i: int) -> float:
        if in_cash:
            return 0.0
        exposure = min(units * unit_exposure, max_exposure)
        if trend_sma is not None and np.isfinite(trend_sma[signal_i, held_code]) and close_px[signal_i, held_code] < trend_sma[signal_i, held_code]:
            exposure = min(exposure, trend_guard_exposure if trend_guard_exposure is not None else exposure)
        if vol_target is not None and np.isfinite(realized_vol[signal_i, held_code]) and realized_vol[signal_i, held_code] > 0:
            exposure = min(exposure, vol_target / realized_vol[signal_i, held_code])
        return max(0.0, exposure)

    for i in range(1, n):
        if in_cash:
            equity[i] = equity[i - 1]
        else:
            equity[i] = equity[i - 1] * (1 + current_exposure * (float(close_px[i, held_code]) / float(close_px[i - 1, held_code]) - 1))
        exposure_history[i] = current_exposure if not in_cash else 0.0
        cash_history[i] = in_cash

        selected = int(selected_codes[i])
        risk_on = cash_risk_on(
            mode=cash_mode,
            selected=selected,
            close_row=close_px[i],
            asset_sma_row=cash_asset_sma[i],
            qqq_sma=float(qqq_sma[i]),
            prior_risk_on=risk_on,
            exit_buffer=cash_exit_buffer,
            reentry_buffer=cash_reentry_buffer,
        )
        if not risk_on:
            if not in_cash:
                trade_events += 1
                in_cash = True
                units = 0
                extra_avg_cost = np.nan
                extra_entry_i = None
            current_exposure = 0.0
            continue

        if in_cash:
            held_code = selected
            price = float(close_px[i, held_code])
            trade_events += 1
            in_cash = False
            units = 1
            anchor = price
            high = price
            low_since_extra = price
            extra_avg_cost = np.nan
            extra_entry_i = None
            current_exposure = set_next_exposure(i)
            continue

        if selected != held_code:
            held_code = selected
            price = float(close_px[i, held_code])
            trade_events += 1
            units = 1
            anchor = price
            high = price
            low_since_extra = price
            extra_avg_cost = np.nan
            extra_entry_i = None
            current_exposure = set_next_exposure(i)
            continue

        price = float(close_px[i, held_code])
        high = max(high, price)
        anchor = high

        if units > 1:
            low_since_extra = min(low_since_extra, price)
            sell_extra = False
            if sell_mode == "extra_profit":
                sell_extra = bool(np.isfinite(extra_avg_cost)) and price >= extra_avg_cost * (1 + sell_param)
            elif sell_mode == "rebound_from_low":
                sell_extra = price >= low_since_extra * (1 + sell_param)
            if max_extra_days is not None and extra_entry_i is not None and (i - extra_entry_i) >= max_extra_days:
                sell_extra = True
            if sell_extra:
                trade_events += 1
                units = 1
                low_since_extra = price
                extra_avg_cost = np.nan
                extra_entry_i = None

        drop_from_anchor = price / anchor - 1
        if units == 1 and drop_from_anchor <= -add1_drop:
            units = 2
            extra_avg_cost = price
            extra_entry_i = i
            low_since_extra = price
            trade_events += 1
        elif units == 2 and drop_from_anchor <= -add2_drop:
            units = 3
            extra_avg_cost = float(np.mean([extra_avg_cost, price])) if np.isfinite(extra_avg_cost) else price
            trade_events += 1
        current_exposure = set_next_exposure(i)

    return equity, exposure_history, cash_history, trade_events


def buy_hold_equity(close: pd.Series) -> np.ndarray:
    return (close / close.iloc[0]).to_numpy(dtype=float)


def build_rows(name: str, equity: np.ndarray, dates: pd.DatetimeIndex, cash: np.ndarray | None = None) -> list[dict[str, object]]:
    rows = []
    for period_name, mask in {
        "IS 2010-2019": dates < SPLIT_DATE,
        "OOS 2020-date": dates >= SPLIT_DATE,
        "Full": np.ones(len(dates), dtype=bool),
    }.items():
        row = {"name": name, "period": period_name, **metrics(equity, dates, mask, cash)}
        rows.append(row)
    return rows


def main() -> None:
    REPORTS.mkdir(exist_ok=True)
    close_df = fetch_adjusted_close()
    dates = close_df.index
    lookback = 63
    momentum = close_df[SYMBOLS] / close_df[SYMBOLS].shift(lookback) - 1
    allocation = momentum.fillna(-np.inf).idxmax(axis=1)
    allocation = allocation.where(np.isfinite(momentum).any(axis=1), "QQQ")
    close_px = close_df[SYMBOLS].to_numpy(dtype=float)
    selected_codes = allocation.map({"SMH": 0, "QQQ": 1}).to_numpy(dtype=int)

    trend_sma_cache = {window: close_df[SYMBOLS].rolling(window).mean().to_numpy(dtype=float) for window in [150, 200]}
    cash_sma_cache = {
        window: (
            close_df[SYMBOLS].rolling(window).mean().to_numpy(dtype=float),
            close_df["QQQ"].rolling(window).mean().to_numpy(dtype=float),
        )
        for window in [150, 200, 250]
    }
    returns = close_df[SYMBOLS].pct_change().to_numpy(dtype=float)
    realized_vol_cache = {
        20: pd.DataFrame(returns, index=dates, columns=SYMBOLS).rolling(20).std().to_numpy(dtype=float) * np.sqrt(252),
    }

    variants = {
        "Rank 1 from SOXL/TQQQ top five": {
            "cash_mode": "selected_or_qqq",
            "cash_sma": 150,
            "cash_exit_buffer": 0.00,
            "cash_reentry_buffer": 0.00,
            "unit_exposure": 1.00,
            "max_exposure": 1.00,
            "add1_drop": 0.10,
            "add2_drop": 0.20,
            "sell_mode": "rebound_from_low",
            "sell_param": 0.05,
            "max_extra_days": 5,
            "trend_guard_sma": 200,
            "trend_guard_exposure": 0.50,
            "vol_target": None,
            "vol_window": 20,
        },
        "Rank 2 from SOXL/TQQQ top five": {
            "cash_mode": "selected",
            "cash_sma": 200,
            "cash_exit_buffer": 0.03,
            "cash_reentry_buffer": 0.04,
            "unit_exposure": 1.00,
            "max_exposure": 1.00,
            "add1_drop": 0.05,
            "add2_drop": 0.15,
            "sell_mode": "extra_profit",
            "sell_param": 0.15,
            "max_extra_days": 10,
            "trend_guard_sma": 200,
            "trend_guard_exposure": 0.50,
            "vol_target": None,
            "vol_window": 20,
        },
        "Rank 3 from SOXL/TQQQ top five": {
            "cash_mode": "selected_and_qqq",
            "cash_sma": 200,
            "cash_exit_buffer": 0.00,
            "cash_reentry_buffer": 0.02,
            "unit_exposure": 1.00,
            "max_exposure": 2.00,
            "add1_drop": 0.05,
            "add2_drop": 0.15,
            "sell_mode": "extra_profit",
            "sell_param": 0.15,
            "max_extra_days": 10,
            "trend_guard_sma": None,
            "trend_guard_exposure": None,
            "vol_target": 0.50,
            "vol_window": 20,
        },
        "Rank 4 from SOXL/TQQQ top five": {
            "cash_mode": "selected",
            "cash_sma": 200,
            "cash_exit_buffer": 0.05,
            "cash_reentry_buffer": 0.05,
            "unit_exposure": 1.00,
            "max_exposure": 1.00,
            "add1_drop": 0.08,
            "add2_drop": 0.20,
            "sell_mode": "extra_profit",
            "sell_param": 0.10,
            "max_extra_days": 20,
            "trend_guard_sma": 200,
            "trend_guard_exposure": 0.50,
            "vol_target": None,
            "vol_window": 20,
        },
        "Rank 5 from SOXL/TQQQ top five": {
            "cash_mode": "selected",
            "cash_sma": 200,
            "cash_exit_buffer": 0.05,
            "cash_reentry_buffer": 0.05,
            "unit_exposure": 1.00,
            "max_exposure": 1.00,
            "add1_drop": 0.15,
            "add2_drop": 0.30,
            "sell_mode": "rebound_from_low",
            "sell_param": 0.05,
            "max_extra_days": 5,
            "trend_guard_sma": 200,
            "trend_guard_exposure": 0.50,
            "vol_target": None,
            "vol_window": 20,
        },
    }

    rows: list[dict[str, object]] = []
    daily = pd.DataFrame({"date": dates, "allocation_signal": allocation.values, "SMH_close": close_df["SMH"].values, "QQQ_close": close_df["QQQ"].values})
    for label, params in variants.items():
        equity, exposure, cash, trade_events = simulate(close_px, dates, selected_codes, trend_sma_cache, cash_sma_cache, realized_vol_cache, **params)
        for row in build_rows(label, equity, dates, cash):
            row["variant"] = variant_name(params)
            row["trade_events"] = trade_events
            row["avg_exposure"] = round(float(np.mean(exposure)), 3)
            rows.append(row)
        daily[label + "_equity"] = equity
        daily[label + "_exposure"] = exposure
        daily[label + "_cash"] = cash

    for symbol in SYMBOLS:
        rows.extend(build_rows(f"Buy and hold {symbol}", buy_hold_equity(close_df[symbol]), dates, None))

    summary = pd.DataFrame(rows)
    csv_path = ROOT / "SMH_QQQ_Same_Strategy_Return_Drawdown.csv"
    xlsx_path = ROOT / "SMH_QQQ_Same_Strategy_Return_Drawdown.xlsx"
    daily_path = REPORTS / "smh_qqq_same_strategy_daily.csv"
    summary.to_csv(csv_path, index=False)
    daily.to_csv(daily_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        summary.to_excel(writer, sheet_name="Summary", index=False)
        daily.to_excel(writer, sheet_name="Daily", index=False)
    print(summary.to_string(index=False))
    print(csv_path)
    print(xlsx_path)
    print(daily_path)


if __name__ == "__main__":
    main()
