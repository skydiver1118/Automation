from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
START = "2010-03-11"
END_EXCLUSIVE = "2026-05-21"
SYMBOLS = ["SOXL", "TQQQ"]


def fetch_close() -> pd.DataFrame:
    raw = yf.download(
        SYMBOLS,
        start=START,
        end=END_EXCLUSIVE,
        interval="1d",
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    if isinstance(raw.columns, pd.MultiIndex):
        close = raw["Close"].copy()
    else:
        close = raw[["Close"]].copy()
        close.columns = SYMBOLS
    close = close[SYMBOLS].dropna()
    close.index = pd.to_datetime(close.index).tz_localize(None)
    return close


def max_drawdown(values: np.ndarray) -> float:
    return float(np.min(values / np.maximum.accumulate(values) - 1) * 100)


def cagr_pct(values: np.ndarray, dates: pd.DatetimeIndex) -> float:
    years = max((dates[-1] - dates[0]).days, 1) / 365.25
    return float((values[-1] ** (1 / years) - 1) * 100)


def sharpe_pct(returns: np.ndarray) -> float:
    std = float(np.std(returns))
    if std == 0 or np.isnan(std):
        return 0.0
    return float(np.mean(returns) / std * np.sqrt(252))


def load_best_rotation_inputs() -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    close = fetch_close()
    alloc = pd.read_csv(REPORTS / "soxl_tqqq_rotation_best_allocation.csv", parse_dates=["date"])
    alloc = alloc.set_index("date")["allocation"].sort_index()
    curve = pd.read_csv(REPORTS / "soxl_tqqq_rotation_best_equity.csv", parse_dates=["date"]).set_index("date")
    common = close.index.intersection(alloc.index).intersection(curve.index)
    return close.loc[common], alloc.loc[common], curve.loc[common]


def apply_dca_overlay(
    close: pd.DataFrame,
    allocation: pd.Series,
    *,
    account_mode: str,
    anchor_mode: str,
    add1_drop: float,
    add2_drop: float,
    sell_mode: str,
    sell_param: float,
    max_extra_days: int | None,
) -> tuple[pd.Series, pd.Series, list[dict[str, object]]]:
    symbols = allocation.map({"SOXL": 0, "TQQQ": 1}).to_numpy(dtype=int)
    prices = close[SYMBOLS].to_numpy(dtype=float)
    asset_returns = np.vstack([np.zeros(2), prices[1:] / prices[:-1] - 1])

    equity = np.ones(len(close), dtype=float)
    unit_history = np.ones(len(close), dtype=float)
    trades: list[dict[str, object]] = []

    symbol = int(symbols[0])
    units = 1
    entry_price = float(prices[0, symbol])
    anchor = entry_price
    high = entry_price
    low_since_extra = entry_price
    extra_avg_cost = np.nan
    extra_entry_i: int | None = None

    def exposure_from_units(unit_count: int) -> float:
        if account_mode == "reserve_cash":
            return unit_count / 3
        return float(unit_count)

    for i in range(1, len(close)):
        today_symbol = int(symbols[i])
        if today_symbol != symbol:
            trades.append(
                {
                    "date": close.index[i].date().isoformat(),
                    "action": "RESET_ON_ROTATION",
                    "from_symbol": SYMBOLS[symbol],
                    "to_symbol": SYMBOLS[today_symbol],
                    "units_before": units,
                    "price": round(float(prices[i, today_symbol]), 4),
                }
            )
            symbol = today_symbol
            units = 1
            entry_price = float(prices[i, symbol])
            anchor = entry_price
            high = entry_price
            low_since_extra = entry_price
            extra_avg_cost = np.nan
            extra_entry_i = None

        exposure = exposure_from_units(units)
        equity[i] = equity[i - 1] * (1 + exposure * float(asset_returns[i, symbol]))
        price = float(prices[i, symbol])
        high = max(high, price)
        if anchor_mode == "rolling_high":
            anchor = high

        if units > 1:
            low_since_extra = min(low_since_extra, price)
            sell_extra = False
            reason = ""
            if sell_mode == "recover_to_anchor":
                sell_extra = price >= anchor * (1 - sell_param)
                reason = f"price >= anchor minus {sell_param:.0%}"
            elif sell_mode == "rebound_from_low":
                sell_extra = price >= low_since_extra * (1 + sell_param)
                reason = f"price rebounded {sell_param:.0%} from DCA low"
            elif sell_mode == "extra_profit":
                sell_extra = bool(np.isfinite(extra_avg_cost)) and price >= extra_avg_cost * (1 + sell_param)
                reason = f"extra shares profit >= {sell_param:.0%}"
            if max_extra_days is not None and extra_entry_i is not None and (i - extra_entry_i) >= max_extra_days:
                sell_extra = True
                reason = f"extra shares max holding days {max_extra_days}"
            if sell_extra:
                trades.append(
                    {
                        "date": close.index[i].date().isoformat(),
                        "action": "SELL_EXTRAS",
                        "symbol": SYMBOLS[symbol],
                        "units_before": units,
                        "units_after": 1,
                        "price": round(price, 4),
                        "reason": reason,
                    }
                )
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
            trades.append(
                {
                    "date": close.index[i].date().isoformat(),
                    "action": "BUY_EXTRA_1",
                    "symbol": SYMBOLS[symbol],
                    "units_after": units,
                    "price": round(price, 4),
                    "drop_from_anchor_pct": round(drop_from_anchor * 100, 2),
                }
            )
        elif units == 2 and drop_from_anchor <= -add2_drop:
            units = 3
            extra_avg_cost = float(np.mean([extra_avg_cost, price])) if np.isfinite(extra_avg_cost) else price
            trades.append(
                {
                    "date": close.index[i].date().isoformat(),
                    "action": "BUY_EXTRA_2",
                    "symbol": SYMBOLS[symbol],
                    "units_after": units,
                    "price": round(price, 4),
                    "drop_from_anchor_pct": round(drop_from_anchor * 100, 2),
                }
            )
        unit_history[i] = units

    return pd.Series(equity, index=close.index), pd.Series(unit_history, index=close.index), trades


def yearly_returns(equity: pd.Series) -> dict[int, float]:
    out: dict[int, float] = {}
    for year, group in equity.groupby(equity.index.year):
        out[int(year)] = round((float(group.iloc[-1]) / float(group.iloc[0]) - 1) * 100, 2)
    return out


def run() -> None:
    close, allocation, curve = load_best_rotation_inputs()
    base_rotation = curve["best_rotation_equity"]
    soxl_only = curve["soxl_only_equity"]
    soxl_bh = curve["soxl_buy_hold_equity"]
    tqqq_bh = curve["tqqq_buy_hold_equity"]

    rows: list[dict[str, object]] = []
    best_curves: dict[str, pd.Series] = {}
    best_units: dict[str, pd.Series] = {}
    best_trade_logs: dict[str, list[dict[str, object]]] = {}

    variants = []
    for account_mode in ["reserve_cash", "margin_3x"]:
        for anchor_mode in ["entry", "rolling_high"]:
            for add1 in [0.05, 0.10, 0.15, 0.20, 0.25]:
                for add2 in [0.10, 0.15, 0.20, 0.30, 0.40]:
                    if add2 <= add1:
                        continue
                    for sell_mode, sell_params in {
                        "recover_to_anchor": [0.00, 0.03, 0.05, 0.10],
                        "rebound_from_low": [0.05, 0.10, 0.15, 0.20, 0.30],
                        "extra_profit": [0.03, 0.05, 0.10, 0.15, 0.20],
                    }.items():
                        for sell_param in sell_params:
                            for max_days in [None, 5, 10, 20, 40, 63]:
                                variants.append((account_mode, anchor_mode, add1, add2, sell_mode, sell_param, max_days))

    for account_mode, anchor_mode, add1, add2, sell_mode, sell_param, max_days in variants:
        equity, units, trades = apply_dca_overlay(
            close,
            allocation,
            account_mode=account_mode,
            anchor_mode=anchor_mode,
            add1_drop=add1,
            add2_drop=add2,
            sell_mode=sell_mode,
            sell_param=sell_param,
            max_extra_days=max_days,
        )
        returns = equity.pct_change().fillna(0).to_numpy()
        variant = (
            f"{account_mode}; anchor={anchor_mode}; add at {add1:.0%}/{add2:.0%}; "
            f"sell={sell_mode} {sell_param:.0%}; max_extra_days={max_days if max_days is not None else 'none'}"
        )
        max_units = int(units.max())
        extra_days_pct = round(float((units > 1).mean() * 100), 2)
        row = {
            "variant": variant,
            "account_mode": account_mode,
            "anchor_mode": anchor_mode,
            "add1_drop_pct": round(add1 * 100, 2),
            "add2_drop_pct": round(add2 * 100, 2),
            "sell_mode": sell_mode,
            "sell_param_pct": round(sell_param * 100, 2),
            "max_extra_days": max_days if max_days is not None else "none",
            "net_return_pct": round((float(equity.iloc[-1]) - 1) * 100, 2),
            "cagr_pct": round(cagr_pct(equity.to_numpy(), equity.index), 2),
            "max_drawdown_pct": round(max_drawdown(equity.to_numpy()), 2),
            "sharpe": round(sharpe_pct(returns), 2),
            "dca_trade_events": len([t for t in trades if str(t["action"]).startswith(("BUY_EXTRA", "SELL_EXTRAS"))]),
            "rotation_resets": len([t for t in trades if t["action"] == "RESET_ON_ROTATION"]),
            "max_units": max_units,
            "extra_exposure_days_pct": extra_days_pct,
            "base_rotation_return_pct": round((float(base_rotation.iloc[-1]) / float(base_rotation.iloc[0]) - 1) * 100, 2),
            "base_rotation_max_drawdown_pct": round(max_drawdown((base_rotation / base_rotation.iloc[0]).to_numpy()), 2),
            "soxl_only_return_pct": round((float(soxl_only.iloc[-1]) / float(soxl_only.iloc[0]) - 1) * 100, 2),
            "soxl_only_max_drawdown_pct": round(max_drawdown((soxl_only / soxl_only.iloc[0]).to_numpy()), 2),
            "beats_base_return": bool(float(equity.iloc[-1]) > float(base_rotation.iloc[-1] / base_rotation.iloc[0])),
            "reduces_base_drawdown": bool(max_drawdown(equity.to_numpy()) > max_drawdown((base_rotation / base_rotation.iloc[0]).to_numpy())),
            "reduces_soxl_only_drawdown": bool(max_drawdown(equity.to_numpy()) > max_drawdown((soxl_only / soxl_only.iloc[0]).to_numpy())),
        }
        rows.append(row)
        key = "best_return" if account_mode == "margin_3x" else "best_drawdown"
        existing = best_curves.get(key)
        if key == "best_return":
            if existing is None or equity.iloc[-1] > existing.iloc[-1]:
                best_curves[key] = equity
                best_units[key] = units
                best_trade_logs[key] = trades
        else:
            if existing is None or max_drawdown(equity.to_numpy()) > max_drawdown(existing.to_numpy()):
                best_curves[key] = equity
                best_units[key] = units
                best_trade_logs[key] = trades

    result = pd.DataFrame(rows)
    result = result.sort_values(
        ["reduces_base_drawdown", "max_drawdown_pct", "net_return_pct"],
        ascending=[False, False, False],
    ).reset_index(drop=True)
    result.insert(0, "rank_drawdown_first", np.arange(1, len(result) + 1))
    by_return = result.sort_values("net_return_pct", ascending=False).reset_index(drop=True)
    by_return.insert(0, "rank_return_first", np.arange(1, len(by_return) + 1))

    all_path = REPORTS / "soxl_tqqq_dca_overlay_search_all.csv"
    dd_path = REPORTS / "soxl_tqqq_dca_overlay_best_drawdown.csv"
    ret_path = REPORTS / "soxl_tqqq_dca_overlay_best_return.csv"
    report_path = REPORTS / "soxl_tqqq_dca_overlay_report.md"
    curve_path = REPORTS / "soxl_tqqq_dca_overlay_curves.csv"
    units_path = REPORTS / "soxl_tqqq_dca_overlay_units.csv"
    result.to_csv(all_path, index=False)
    result.head(50).to_csv(dd_path, index=False)
    by_return.head(50).to_csv(ret_path, index=False)

    curves = pd.DataFrame(
        {
            "date": close.index,
            "base_rotation": base_rotation / base_rotation.iloc[0],
            "soxl_only": soxl_only / soxl_only.iloc[0],
            "soxl_buy_hold": soxl_bh / soxl_bh.iloc[0],
            "tqqq_buy_hold": tqqq_bh / tqqq_bh.iloc[0],
        }
    )
    units_df = pd.DataFrame({"date": close.index})
    for key, equity in best_curves.items():
        curves[key] = equity.values
        units_df[key + "_units"] = best_units[key].values
        pd.DataFrame(best_trade_logs[key]).to_csv(REPORTS / f"soxl_tqqq_dca_overlay_{key}_trades.csv", index=False)
    curves.to_csv(curve_path, index=False)
    units_df.to_csv(units_path, index=False)

    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(13, 7))
        for col, label in [
            ("base_rotation", "Base SOXL/TQQQ rotation"),
            ("soxl_only", "SOXL-only baseline"),
            ("best_drawdown", "Best DCA drawdown reducer"),
            ("best_return", "Best DCA return/margin"),
        ]:
            if col in curves:
                ax.plot(pd.to_datetime(curves["date"]), curves[col], label=label, linewidth=2 if col.startswith("best") else 1.5)
        ax.set_yscale("log")
        ax.set_title("SOXL/TQQQ Rotation With DCA Overlay")
        ax.set_ylabel("Growth of $1, log scale")
        ax.grid(True, which="both", alpha=0.25)
        ax.legend()
        fig.tight_layout()
        fig.savefig(REPORTS / "soxl_tqqq_dca_overlay_curves.png", dpi=180)
        plt.close(fig)
    except Exception:
        pass

    best_dd = result.iloc[0]
    best_ret = by_return.iloc[0]
    safer = result[result["reduces_soxl_only_drawdown"]]

    def markdown_table(frame: pd.DataFrame) -> str:
        headers = [str(column) for column in frame.columns]
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
        ]
        for _, row in frame.iterrows():
            lines.append("| " + " | ".join(str(value).replace("|", "\\|") for value in row.tolist()) + " |")
        return "\n".join(lines)

    lines = [
        "# SOXL/TQQQ DCA Overlay Search",
        "",
        f"Tested {len(result):,} DCA overlay variants on the existing best SOXL/TQQQ rotation from {close.index[0].date()} to {close.index[-1].date()}. The core position remains 1 unit. DCA variants can add up to 2 extra units and sell extras on rebounds while keeping the 1-unit core.",
        "",
        "Two account modes were tested: `reserve_cash` treats 3 units as full deployable account capital, so the core position is one-third invested; `margin_3x` keeps the original 1x core and allows exposure to rise as high as 3x.",
        "",
        "## Best Drawdown Reducer",
        "",
        markdown_table(best_dd.to_frame().T),
        "",
        "## Best Return Variant",
        "",
        markdown_table(best_ret.to_frame().T),
        "",
        "## Key Finding",
        "",
        f"- Variants that reduced drawdown versus the base rotation: {int(result['reduces_base_drawdown'].sum()):,} of {len(result):,}.",
        f"- Variants that reduced drawdown versus SOXL-only: {len(safer):,} of {len(result):,}.",
        "- Margin-style DCA generally increases drawdown because it adds exposure into falling leveraged ETFs.",
        "- Reserve-cash DCA reduces account drawdown, but total return is much lower because the normal core is only one-third invested.",
        "",
        "## Files",
        "",
        f"- Full grid: `{all_path}`",
        f"- Best drawdown rows: `{dd_path}`",
        f"- Best return rows: `{ret_path}`",
        f"- Curves: `{curve_path}`",
        f"- Unit exposure history: `{units_path}`",
        f"- Chart: `{REPORTS / 'soxl_tqqq_dca_overlay_curves.png'}`",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Tested {len(result):,} variants")
    print("Best drawdown reducer:")
    print(best_dd[["variant", "net_return_pct", "max_drawdown_pct", "base_rotation_max_drawdown_pct", "soxl_only_max_drawdown_pct"]].to_string())
    print()
    print("Best return:")
    print(best_ret[["variant", "net_return_pct", "max_drawdown_pct", "base_rotation_max_drawdown_pct", "soxl_only_max_drawdown_pct"]].to_string())
    print(report_path)


if __name__ == "__main__":
    run()
