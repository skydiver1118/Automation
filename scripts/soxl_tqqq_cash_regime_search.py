from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from soxl_tqqq_dca_overlay_search import cagr_pct, load_best_rotation_inputs, max_drawdown, sharpe_pct  # noqa: E402


SYMBOLS = ["SOXL", "TQQQ"]
START = "2010-03-11"
END_EXCLUSIVE = "2026-05-21"


def fetch_context() -> pd.DataFrame:
    raw = yf.download(
        ["SOXL", "TQQQ", "QQQ"],
        start=START,
        end=END_EXCLUSIVE,
        interval="1d",
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    close = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]]
    close = close[["SOXL", "TQQQ", "QQQ"]].dropna()
    close.index = pd.to_datetime(close.index).tz_localize(None)
    return close


def pass_trend(price: float, sma: float, buffer: float) -> bool:
    return bool(np.isfinite(sma) and price >= sma * (1 + buffer))


def fail_trend(price: float, sma: float, buffer: float) -> bool:
    return bool(np.isfinite(sma) and price < sma * (1 - buffer))


def choose_signal(
    *,
    mode: str,
    selected: int,
    prices: np.ndarray,
    sma_assets: np.ndarray,
    qqq_price: float,
    qqq_sma: float,
    exit_buffer: float,
    reentry_buffer: float,
    risk_on: bool,
) -> tuple[int, bool]:
    other = 1 - selected

    def asset_pass(symbol: int, buffer: float) -> bool:
        return pass_trend(float(prices[symbol]), float(sma_assets[symbol]), buffer)

    def asset_fail(symbol: int, buffer: float) -> bool:
        return fail_trend(float(prices[symbol]), float(sma_assets[symbol]), buffer)

    if mode == "selected_sma_cash":
        if risk_on and asset_fail(selected, exit_buffer):
            return -1, False
        if not risk_on and not asset_pass(selected, reentry_buffer):
            return -1, False
        return selected, True

    if mode == "selected_sma_else_other":
        selected_ok = asset_pass(selected, reentry_buffer if not risk_on else -exit_buffer)
        other_ok = asset_pass(other, reentry_buffer if not risk_on else -exit_buffer)
        if selected_ok:
            return selected, True
        if other_ok:
            return other, True
        return -1, False

    if mode == "qqq_sma_cash":
        if risk_on and fail_trend(qqq_price, qqq_sma, exit_buffer):
            return -1, False
        if not risk_on and not pass_trend(qqq_price, qqq_sma, reentry_buffer):
            return -1, False
        return selected, True

    if mode == "selected_and_qqq_cash":
        selected_exit = asset_fail(selected, exit_buffer)
        qqq_exit = fail_trend(qqq_price, qqq_sma, exit_buffer)
        selected_reentry = asset_pass(selected, reentry_buffer)
        qqq_reentry = pass_trend(qqq_price, qqq_sma, reentry_buffer)
        if risk_on and (selected_exit or qqq_exit):
            return -1, False
        if not risk_on and not (selected_reentry and qqq_reentry):
            return -1, False
        return selected, True

    if mode == "selected_or_qqq_cash":
        selected_exit = asset_fail(selected, exit_buffer)
        qqq_exit = fail_trend(qqq_price, qqq_sma, exit_buffer)
        selected_reentry = asset_pass(selected, reentry_buffer)
        qqq_reentry = pass_trend(qqq_price, qqq_sma, reentry_buffer)
        if risk_on and (selected_exit and qqq_exit):
            return -1, False
        if not risk_on and not (selected_reentry or qqq_reentry):
            return -1, False
        return selected, True

    raise ValueError(f"Unknown mode: {mode}")


def simulate(
    close: pd.DataFrame,
    allocation: pd.Series,
    *,
    mode: str,
    sma_window: int,
    exit_buffer: float,
    reentry_buffer: float,
    unit_exposure: float,
    max_exposure: float,
    dca: bool,
    add1_drop: float,
    add2_drop: float,
    sell_profit: float,
    max_extra_days: int,
) -> tuple[pd.Series, pd.DataFrame, list[dict[str, object]]]:
    dates = close.index
    prices = close[SYMBOLS].to_numpy(dtype=float)
    qqq = close["QQQ"].to_numpy(dtype=float)
    returns = np.vstack([np.zeros(2), prices[1:] / prices[:-1] - 1])
    selected_codes = allocation.map({"SOXL": 0, "TQQQ": 1}).to_numpy(dtype=int)
    sma_assets = close[SYMBOLS].rolling(sma_window).mean().to_numpy(dtype=float)
    qqq_sma = close["QQQ"].rolling(sma_window).mean().to_numpy(dtype=float)

    equity = np.ones(len(close), dtype=float)
    exposure_values = np.zeros(len(close), dtype=float)
    units_values = np.zeros(len(close), dtype=float)
    held_codes = np.full(len(close), -1, dtype=int)
    risk_on = True
    held = int(selected_codes[0])
    units = 1
    anchor = float(prices[0, held])
    high = anchor
    low_since_extra = anchor
    extra_avg_cost = np.nan
    extra_entry_i: int | None = None
    trades: list[dict[str, object]] = []

    for i in range(1, len(close)):
        signal_i = i - 1
        desired, risk_on = choose_signal(
            mode=mode,
            selected=int(selected_codes[i]),
            prices=prices[signal_i],
            sma_assets=sma_assets[signal_i],
            qqq_price=float(qqq[signal_i]),
            qqq_sma=float(qqq_sma[signal_i]),
            exit_buffer=exit_buffer,
            reentry_buffer=reentry_buffer,
            risk_on=risk_on,
        )

        if desired == -1:
            if held != -1:
                trades.append(
                    {
                        "date": dates[i].date().isoformat(),
                        "action": "EXIT_TO_CASH",
                        "from_symbol": SYMBOLS[held],
                        "units_before": units,
                        "price": round(float(prices[i, held]), 4),
                    }
                )
            held = -1
            units = 0
            equity[i] = equity[i - 1]
            exposure_values[i] = 0
            units_values[i] = 0
            held_codes[i] = -1
            continue

        if held == -1 or desired != held:
            action = "ENTER_FROM_CASH" if held == -1 else "ROTATE"
            trades.append(
                {
                    "date": dates[i].date().isoformat(),
                    "action": action,
                    "from_symbol": "CASH" if held == -1 else SYMBOLS[held],
                    "to_symbol": SYMBOLS[desired],
                    "units_before": units,
                    "price": round(float(prices[i, desired]), 4),
                }
            )
            held = desired
            units = 1
            anchor = float(prices[i, held])
            high = anchor
            low_since_extra = anchor
            extra_avg_cost = np.nan
            extra_entry_i = None

        exposure = min(units * unit_exposure, max_exposure)
        equity[i] = equity[i - 1] * (1 + exposure * float(returns[i, held]))
        price = float(prices[i, held])
        high = max(high, price)
        anchor = high

        if dca and units > 1:
            low_since_extra = min(low_since_extra, price)
            sell_extra = price >= extra_avg_cost * (1 + sell_profit) if np.isfinite(extra_avg_cost) else False
            timed_exit = extra_entry_i is not None and (i - extra_entry_i) >= max_extra_days
            if sell_extra or timed_exit:
                trades.append(
                    {
                        "date": dates[i].date().isoformat(),
                        "action": "SELL_EXTRAS",
                        "symbol": SYMBOLS[held],
                        "units_before": units,
                        "units_after": 1,
                        "price": round(price, 4),
                        "reason": "profit" if sell_extra else "max_extra_days",
                    }
                )
                units = 1
                low_since_extra = price
                extra_avg_cost = np.nan
                extra_entry_i = None

        drop_from_anchor = price / anchor - 1
        if dca and units == 1 and drop_from_anchor <= -add1_drop:
            units = 2
            extra_avg_cost = price
            extra_entry_i = i
            low_since_extra = price
            trades.append(
                {
                    "date": dates[i].date().isoformat(),
                    "action": "BUY_EXTRA_1",
                    "symbol": SYMBOLS[held],
                    "units_after": units,
                    "price": round(price, 4),
                    "drop_from_anchor_pct": round(drop_from_anchor * 100, 2),
                }
            )
        elif dca and units == 2 and drop_from_anchor <= -add2_drop:
            units = 3
            extra_avg_cost = float(np.mean([extra_avg_cost, price])) if np.isfinite(extra_avg_cost) else price
            trades.append(
                {
                    "date": dates[i].date().isoformat(),
                    "action": "BUY_EXTRA_2",
                    "symbol": SYMBOLS[held],
                    "units_after": units,
                    "price": round(price, 4),
                    "drop_from_anchor_pct": round(drop_from_anchor * 100, 2),
                }
            )

        exposure_values[i] = min(units * unit_exposure, max_exposure)
        units_values[i] = units
        held_codes[i] = held

    detail = pd.DataFrame(
        {
            "date": dates,
            "equity": equity,
            "exposure": exposure_values,
            "units": units_values,
            "held": np.where(held_codes == 0, "SOXL", np.where(held_codes == 1, "TQQQ", "CASH")),
            "base_allocation": allocation.values,
        }
    )
    return pd.Series(equity, index=dates), detail, trades


def metrics(equity: pd.Series, base: pd.Series, soxl_only: pd.Series, detail: pd.DataFrame, trades: list[dict[str, object]]) -> dict[str, object]:
    values = equity.to_numpy(dtype=float)
    returns = equity.pct_change().fillna(0).to_numpy(dtype=float)
    year_2022 = equity[equity.index.year == 2022]
    ret_2022 = (float(year_2022.iloc[-1]) / float(year_2022.iloc[0]) - 1) * 100
    dd_2022 = max_drawdown((year_2022 / year_2022.iloc[0]).to_numpy(dtype=float))
    dd = max_drawdown(values)
    cagr = cagr_pct(values, equity.index)
    return {
        "net_return_pct": round((float(values[-1]) - 1) * 100, 2),
        "cagr_pct": round(cagr, 2),
        "max_drawdown_pct": round(dd, 2),
        "calmar": round(cagr / abs(dd), 3) if dd else np.nan,
        "sharpe": round(sharpe_pct(returns), 2),
        "return_2022_pct": round(ret_2022, 2),
        "drawdown_2022_pct": round(dd_2022, 2),
        "cash_days_pct": round(float((detail["held"] == "CASH").mean() * 100), 2),
        "avg_exposure": round(float(detail["exposure"].mean()), 3),
        "days_above_1x_pct": round(float((detail["exposure"] > 1).mean() * 100), 2),
        "trade_events": len(trades),
        "dca_events": len([trade for trade in trades if str(trade["action"]).startswith(("BUY_EXTRA", "SELL_EXTRAS"))]),
        "base_rotation_return_pct": round((float(base.iloc[-1]) / float(base.iloc[0]) - 1) * 100, 2),
        "base_rotation_max_drawdown_pct": round(max_drawdown((base / base.iloc[0]).to_numpy(dtype=float)), 2),
        "soxl_only_return_pct": round((float(soxl_only.iloc[-1]) / float(soxl_only.iloc[0]) - 1) * 100, 2),
        "soxl_only_max_drawdown_pct": round(max_drawdown((soxl_only / soxl_only.iloc[0]).to_numpy(dtype=float)), 2),
    }


def annual_tables(curves: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    returns: list[dict[str, object]] = []
    drawdowns: list[dict[str, object]] = []
    curves = curves.copy()
    curves["year"] = curves["date"].dt.year
    value_cols = [column for column in curves.columns if column not in {"date", "year"}]
    for year, group in curves.groupby("year"):
        ret_row: dict[str, object] = {"Year": int(year), "Period": f"{group['date'].iloc[0].date()} to {group['date'].iloc[-1].date()}"}
        dd_row = ret_row.copy()
        for column in value_cols:
            series = group[column].astype(float)
            ret_row[column] = round((series.iloc[-1] / series.iloc[0] - 1) * 100, 2)
            dd_row[column] = round((series / series.cummax() - 1).min() * 100, 2)
        returns.append(ret_row)
        drawdowns.append(dd_row)
    return pd.DataFrame(returns), pd.DataFrame(drawdowns)


def html_table(frame: pd.DataFrame) -> str:
    headers = "".join(f"<th>{column}</th>" for column in frame.columns)
    rows = []
    for _, row in frame.iterrows():
        rows.append("<tr>" + "".join(f"<td>{value}</td>" for value in row.tolist()) + "</tr>")
    return "<table><thead><tr>" + headers + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"


def write_xlsx(path: Path, sheets: dict[str, pd.DataFrame]) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for name, frame in sheets.items():
            frame.to_excel(writer, sheet_name=name[:31], index=False)
        for worksheet in writer.book.worksheets:
            worksheet.freeze_panes = "A2"
            for column_cells in worksheet.columns:
                width = max(len(str(cell.value)) if cell.value is not None else 0 for cell in column_cells)
                worksheet.column_dimensions[column_cells[0].column_letter].width = min(max(width + 2, 10), 56)


def run() -> None:
    close_context = fetch_context()
    close_base, allocation_base, source_curve = load_best_rotation_inputs()
    common = close_context.index.intersection(close_base.index).intersection(allocation_base.index).intersection(source_curve.index)
    close = close_context.loc[common]
    allocation = allocation_base.loc[common]
    source_curve = source_curve.loc[common]
    base_rotation = source_curve["best_rotation_equity"] / source_curve["best_rotation_equity"].iloc[0]
    soxl_only = source_curve["soxl_only_equity"] / source_curve["soxl_only_equity"].iloc[0]

    rows: list[dict[str, object]] = []
    curve_store: dict[str, pd.Series] = {}
    detail_store: dict[str, pd.DataFrame] = {}
    trade_store: dict[str, list[dict[str, object]]] = {}

    modes = ["selected_sma_cash", "selected_sma_else_other", "qqq_sma_cash", "selected_and_qqq_cash", "selected_or_qqq_cash"]
    sma_windows = [100, 120, 150, 180, 200, 220, 250, 300]
    exit_buffers = [0.00, 0.01, 0.02, 0.03, 0.05, 0.07, 0.10]
    reentry_buffers = [0.00, 0.01, 0.02, 0.03, 0.05, 0.07]
    configs = [
        {"unit_exposure": 1.00, "max_exposure": 1.00, "dca": False, "add1_drop": 0.10, "add2_drop": 0.20, "sell_profit": 0.20, "max_extra_days": 20},
        {"unit_exposure": 0.75, "max_exposure": 1.00, "dca": False, "add1_drop": 0.10, "add2_drop": 0.20, "sell_profit": 0.20, "max_extra_days": 20},
        {"unit_exposure": 0.50, "max_exposure": 1.00, "dca": False, "add1_drop": 0.10, "add2_drop": 0.20, "sell_profit": 0.20, "max_extra_days": 20},
        {"unit_exposure": 0.67, "max_exposure": 2.00, "dca": True, "add1_drop": 0.10, "add2_drop": 0.20, "sell_profit": 0.20, "max_extra_days": 20},
        {"unit_exposure": 0.50, "max_exposure": 1.50, "dca": True, "add1_drop": 0.10, "add2_drop": 0.20, "sell_profit": 0.20, "max_extra_days": 20},
    ]

    for mode in modes:
        for sma_window in sma_windows:
            for exit_buffer in exit_buffers:
                for reentry_buffer in reentry_buffers:
                    if reentry_buffer < exit_buffer and exit_buffer >= 0.05:
                        continue
                    for config in configs:
                        equity, detail, trades = simulate(
                            close,
                            allocation,
                            mode=mode,
                            sma_window=sma_window,
                            exit_buffer=exit_buffer,
                            reentry_buffer=reentry_buffer,
                            **config,
                        )
                        variant = (
                            f"{mode}; SMA{sma_window}; exit below SMA-{exit_buffer:.0%}; "
                            f"reenter above SMA+{reentry_buffer:.0%}; unit={config['unit_exposure']:.2f}; "
                            f"cap={config['max_exposure']:.2f}; dca={config['dca']}"
                        )
                        row = {
                            "variant": variant,
                            "mode": mode,
                            "sma_window": sma_window,
                            "exit_buffer_pct": round(exit_buffer * 100, 2),
                            "reentry_buffer_pct": round(reentry_buffer * 100, 2),
                            **config,
                            **metrics(equity, base_rotation, soxl_only, detail, trades),
                        }
                        rows.append(row)
                        candidates = [
                            ("best_return_dd50", row["max_drawdown_pct"] >= -50, row["net_return_pct"]),
                            ("best_return_dd40", row["max_drawdown_pct"] >= -40, row["net_return_pct"]),
                            ("best_2022_loss_control", row["return_2022_pct"] >= -25, row["net_return_pct"]),
                            ("best_calmar", True, row["calmar"]),
                            ("best_balanced", row["max_drawdown_pct"] >= -55 and row["return_2022_pct"] >= -35, row["net_return_pct"]),
                        ]
                        for key, predicate, score in candidates:
                            if not predicate:
                                continue
                            current = curve_store.get(key)
                            current_score = current.attrs.get("score", -np.inf) if current is not None else -np.inf
                            if float(score) > current_score:
                                equity.attrs["score"] = float(score)
                                curve_store[key] = equity
                                detail_store[key] = detail
                                trade_store[key] = trades

    result = pd.DataFrame(rows)
    result = result.sort_values(["max_drawdown_pct", "net_return_pct"], ascending=[False, False]).reset_index(drop=True)
    result.insert(0, "rank_drawdown", np.arange(1, len(result) + 1))

    summary_cases = [
        ("Best return with max DD <= 50%", result[result["max_drawdown_pct"] >= -50].sort_values("net_return_pct", ascending=False)),
        ("Best return with max DD <= 40%", result[result["max_drawdown_pct"] >= -40].sort_values("net_return_pct", ascending=False)),
        ("Best return with 2022 loss <= 25%", result[result["return_2022_pct"] >= -25].sort_values("net_return_pct", ascending=False)),
        ("Best balanced: DD <= 55%, 2022 loss <= 35%", result[(result["max_drawdown_pct"] >= -55) & (result["return_2022_pct"] >= -35)].sort_values("net_return_pct", ascending=False)),
        ("Best Calmar", result.sort_values("calmar", ascending=False)),
        ("Best raw return", result.sort_values("net_return_pct", ascending=False)),
    ]
    summary_rows = []
    for case, frame in summary_cases:
        if not frame.empty:
            row = frame.iloc[0].to_dict()
            row["case"] = case
            summary_rows.append(row)
    summary = pd.DataFrame(summary_rows)
    summary_cols = [
        "case",
        "variant",
        "net_return_pct",
        "cagr_pct",
        "max_drawdown_pct",
        "return_2022_pct",
        "drawdown_2022_pct",
        "calmar",
        "sharpe",
        "cash_days_pct",
        "avg_exposure",
        "days_above_1x_pct",
        "trade_events",
        "dca_events",
        "base_rotation_return_pct",
        "base_rotation_max_drawdown_pct",
        "soxl_only_return_pct",
        "soxl_only_max_drawdown_pct",
    ]

    all_path = REPORTS / "soxl_tqqq_cash_regime_search_all.csv"
    top_path = REPORTS / "soxl_tqqq_cash_regime_top.csv"
    result.to_csv(all_path, index=False)
    result.head(200).to_csv(top_path, index=False)

    curves = pd.DataFrame({"date": close.index, "base_rotation": base_rotation.values, "soxl_only": soxl_only.values})
    for key, equity in curve_store.items():
        curves[key] = equity.values
        detail_store[key].to_csv(REPORTS / f"soxl_tqqq_cash_regime_{key}_daily.csv", index=False)
        pd.DataFrame(trade_store[key]).to_csv(REPORTS / f"soxl_tqqq_cash_regime_{key}_trades.csv", index=False)
    annual_returns, annual_drawdowns = annual_tables(curves)

    xlsx_path = ROOT / "SOXL_TQQQ_Cash_Regime_Search.xlsx"
    html_path = ROOT / "SOXL_TQQQ_Cash_Regime_Search.html"
    csv_path = ROOT / "SOXL_TQQQ_Cash_Regime_Summary.csv"
    summary[summary_cols].to_csv(csv_path, index=False)
    write_xlsx(
        xlsx_path,
        {
            "Summary": summary[summary_cols],
            "Annual Return %": annual_returns,
            "Annual Drawdown %": annual_drawdowns,
            "Top 200": result.head(200),
            "All Results": result,
            "Curves": curves,
        },
    )
    html_path.write_text(
        "<!doctype html><html><head><meta charset='utf-8'><title>SOXL/TQQQ Cash Regime Search</title>"
        "<style>body{font-family:Arial,sans-serif;margin:28px;color:#111827}table{border-collapse:collapse;font-size:13px}"
        "th,td{border:1px solid #d1d5db;padding:7px 10px;text-align:right;vertical-align:top}th{background:#f3f4f6}"
        "th:nth-child(1),td:nth-child(1),th:nth-child(2),td:nth-child(2){text-align:left}td:nth-child(2){max-width:650px}</style></head><body>"
        "<h1>SOXL/TQQQ Cash Regime Search</h1>"
        "<p>Cash filters tested against the existing SOXL/TQQQ rotation with optional DCA overlay.</p>"
        "<h2>Summary</h2>"
        + html_table(summary[summary_cols])
        + "<h2>Annual Return %</h2>"
        + html_table(annual_returns)
        + "<h2>Annual Max Drawdown %</h2>"
        + html_table(annual_drawdowns)
        + "</body></html>",
        encoding="utf-8",
    )

    try:
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(13, 7))
        for col in ["base_rotation", "soxl_only", "best_return_dd50", "best_return_dd40", "best_balanced"]:
            if col in curves:
                ax.plot(pd.to_datetime(curves["date"]), curves[col], label=col, linewidth=2 if col.startswith("best") else 1.4)
        ax.set_yscale("log")
        ax.set_title("SOXL/TQQQ Cash Regime Variants")
        ax.set_ylabel("Growth of $1, log scale")
        ax.grid(True, which="both", alpha=0.25)
        ax.legend()
        fig.tight_layout()
        fig.savefig(ROOT / "SOXL_TQQQ_Cash_Regime_Curves.png", dpi=180)
        plt.close(fig)
    except Exception:
        pass

    print(f"Tested {len(result):,} variants")
    print(summary[summary_cols].to_string(index=False))
    print(xlsx_path)
    print(html_path)
    print(csv_path)


if __name__ == "__main__":
    run()
