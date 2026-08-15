from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd
import yfinance as yf


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
sys.path.insert(0, str(ROOT / "scripts"))

from soxl_tqqq_cash_signal_scanner import StrategyConfig, build_base_rotation  # noqa: E402
from soxl_tqqq_dca_overlay_search import cagr_pct, max_drawdown, sharpe_pct  # noqa: E402


SYMBOLS = ["SOXL", "TQQQ"]
CONTEXT_SYMBOLS = ["SOXL", "TQQQ", "QQQ"]
START = "2010-03-11"


def fetch_close() -> pd.DataFrame:
    raw = yf.download(
        CONTEXT_SYMBOLS,
        start=START,
        interval="1d",
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    if raw.empty:
        raise RuntimeError("No yfinance data returned.")
    close = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw[["Close"]]
    close = close[CONTEXT_SYMBOLS].dropna().copy()
    close.index = pd.to_datetime(close.index).tz_localize(None)
    return close


def trend_pass(price: float, sma: float, buffer: float) -> bool:
    return bool(np.isfinite(sma) and price >= sma * (1 + buffer))


def trend_fail(price: float, sma: float, buffer: float) -> bool:
    return bool(np.isfinite(sma) and price < sma * (1 - buffer))


def normal_risk_on(
    *,
    mode: str,
    selected: str,
    close_row: pd.Series,
    asset_sma: pd.Series,
    qqq_sma: float,
    exit_buffer: float,
    reentry_buffer: float,
    prior_risk_on: bool,
) -> bool:
    selected_exit = trend_fail(float(close_row[selected]), float(asset_sma[selected]), exit_buffer)
    qqq_exit = trend_fail(float(close_row["QQQ"]), qqq_sma, exit_buffer)
    selected_reentry = trend_pass(float(close_row[selected]), float(asset_sma[selected]), reentry_buffer)
    qqq_reentry = trend_pass(float(close_row["QQQ"]), qqq_sma, reentry_buffer)
    if mode == "selected_or_qqq":
        if prior_risk_on:
            return not (selected_exit and qqq_exit)
        return selected_reentry or qqq_reentry
    if mode == "selected_and_qqq":
        if prior_risk_on:
            return not (selected_exit or qqq_exit)
        return selected_reentry and qqq_reentry
    if mode == "qqq_only":
        if prior_risk_on:
            return not qqq_exit
        return qqq_reentry
    raise ValueError(f"Unknown cash mode: {mode}")


def deep_dca_allowed(
    *,
    filter_name: str,
    selected: str,
    signal_i: int,
    close: pd.DataFrame,
    qqq_sma200: pd.Series,
    asset_sma20: pd.DataFrame,
) -> bool:
    if filter_name == "none":
        return True
    if filter_name == "qqq_above_sma200_minus5":
        return float(close["QQQ"].iloc[signal_i]) >= float(qqq_sma200.iloc[signal_i]) * 0.95
    if filter_name == "qqq_above_sma200":
        return float(close["QQQ"].iloc[signal_i]) >= float(qqq_sma200.iloc[signal_i])
    if filter_name == "selected_above_sma20":
        return float(close[selected].iloc[signal_i]) >= float(asset_sma20[selected].iloc[signal_i])
    if filter_name == "selected_5d_positive":
        return float(close[selected].iloc[signal_i]) > float(close[selected].iloc[max(signal_i - 5, 0)])
    raise ValueError(f"Unknown DCA filter: {filter_name}")


def staged_exposure(discount: float, *, start: float, max_discount: float, entry_exposure: float, max_exposure: float) -> float:
    if discount > -start:
        return 0.0
    if discount <= -max_discount:
        return max_exposure
    midpoint = (start + max_discount) / 2
    if discount <= -midpoint:
        return min(max_exposure, (entry_exposure + max_exposure) / 2)
    return min(max_exposure, entry_exposure)


def simulate(
    close: pd.DataFrame,
    base_target: pd.Series,
    *,
    cash_mode: str,
    cash_sma: int,
    exit_buffer: float,
    reentry_buffer: float,
    dca_sma: int,
    dca_start: float,
    dca_max_discount: float,
    dca_entry_exposure: float,
    dca_max_exposure: float,
    dca_filter: str,
    recover_buffer: float,
    max_dca_days: int | None,
    normal_exposure: float,
) -> tuple[pd.Series, pd.DataFrame, list[dict[str, object]]]:
    asset_returns = close[SYMBOLS].pct_change().fillna(0)
    cash_sma_assets = close[SYMBOLS].rolling(cash_sma).mean()
    cash_sma_qqq = close["QQQ"].rolling(cash_sma).mean()
    dca_sma_assets = close[SYMBOLS].rolling(dca_sma).mean()
    qqq_sma200 = close["QQQ"].rolling(200).mean()
    asset_sma20 = close[SYMBOLS].rolling(20).mean()

    equity = np.ones(len(close), dtype=float)
    held_values: list[str] = ["CASH"] * len(close)
    exposure_values = np.zeros(len(close), dtype=float)
    regime_values: list[str] = ["WARMUP"] * len(close)
    trades: list[dict[str, object]] = []
    prior_risk_on = True
    prior_held = "CASH"
    dca_entry_i: int | None = None

    for i in range(1, len(close)):
        signal_i = i - 1
        selected = str(base_target.iloc[i])
        date = close.index[i]
        if selected not in SYMBOLS or not np.isfinite(cash_sma_assets[selected].iloc[signal_i]):
            equity[i] = equity[i - 1]
            continue

        risk_on = normal_risk_on(
            mode=cash_mode,
            selected=selected,
            close_row=close.iloc[signal_i],
            asset_sma=cash_sma_assets.iloc[signal_i],
            qqq_sma=float(cash_sma_qqq.iloc[signal_i]),
            exit_buffer=exit_buffer,
            reentry_buffer=reentry_buffer,
            prior_risk_on=prior_risk_on,
        )
        prior_risk_on = risk_on

        discount = float(close[selected].iloc[signal_i] / dca_sma_assets[selected].iloc[signal_i] - 1)
        is_recovered = float(close[selected].iloc[signal_i]) >= float(dca_sma_assets[selected].iloc[signal_i]) * (1 - recover_buffer)
        timed_out = max_dca_days is not None and dca_entry_i is not None and (i - dca_entry_i) >= max_dca_days
        allow_dca = (
            not risk_on
            and not is_recovered
            and not timed_out
            and discount <= -dca_start
            and deep_dca_allowed(
                filter_name=dca_filter,
                selected=selected,
                signal_i=signal_i,
                close=close,
                qqq_sma200=qqq_sma200,
                asset_sma20=asset_sma20,
            )
        )

        if risk_on:
            held = selected
            exposure = normal_exposure
            regime = "RISK_ON"
            dca_entry_i = None
        elif allow_dca:
            held = selected
            exposure = staged_exposure(
                discount,
                start=dca_start,
                max_discount=dca_max_discount,
                entry_exposure=dca_entry_exposure,
                max_exposure=dca_max_exposure,
            )
            regime = "DEEP_DCA"
            if dca_entry_i is None:
                dca_entry_i = i
        else:
            held = "CASH"
            exposure = 0.0
            regime = "CASH"
            dca_entry_i = None

        if held != prior_held:
            trades.append(
                {
                    "date": date.date().isoformat(),
                    "action": "ENTER_" + held if prior_held == "CASH" else "EXIT_TO_CASH" if held == "CASH" else "ROTATE",
                    "from_symbol": prior_held,
                    "to_symbol": held,
                    "exposure": round(exposure, 3),
                    "regime": regime,
                    "discount_to_sma_pct": round(discount * 100, 2),
                }
            )
            prior_held = held

        if held == "CASH":
            equity[i] = equity[i - 1]
        else:
            equity[i] = equity[i - 1] * (1 + exposure * float(asset_returns[held].iloc[i]))
        held_values[i] = held
        exposure_values[i] = exposure
        regime_values[i] = regime

    detail = pd.DataFrame(
        {
            "date": close.index,
            "equity": equity,
            "held": held_values,
            "exposure": exposure_values,
            "regime": regime_values,
            "base_target": base_target.values,
        }
    )
    return pd.Series(equity, index=close.index), detail, trades


def metric_for_period(equity: pd.Series, detail: pd.DataFrame, *, start: str) -> dict[str, object]:
    period = equity[equity.index >= pd.Timestamp(start)].copy()
    period = period / period.iloc[0]
    detail_period = detail[detail["date"] >= pd.Timestamp(start)]
    values = period.to_numpy(dtype=float)
    returns = period.pct_change().fillna(0).to_numpy(dtype=float)
    year_2022 = period[period.index.year == 2022]
    if year_2022.empty:
        ret_2022 = np.nan
        dd_2022 = np.nan
    else:
        ret_2022 = (float(year_2022.iloc[-1]) / float(year_2022.iloc[0]) - 1) * 100
        dd_2022 = max_drawdown((year_2022 / year_2022.iloc[0]).to_numpy(dtype=float))
    dd = max_drawdown(values)
    cagr = cagr_pct(values, period.index)
    return {
        f"{start}_return_pct": round((float(values[-1]) - 1) * 100, 2),
        f"{start}_cagr_pct": round(cagr, 2),
        f"{start}_max_drawdown_pct": round(dd, 2),
        f"{start}_calmar": round(cagr / abs(dd), 3) if dd else np.nan,
        f"{start}_sharpe": round(sharpe_pct(returns), 2),
        f"{start}_2022_return_pct": round(ret_2022, 2) if np.isfinite(ret_2022) else np.nan,
        f"{start}_2022_drawdown_pct": round(dd_2022, 2) if np.isfinite(dd_2022) else np.nan,
        f"{start}_cash_days_pct": round(float((detail_period["held"] == "CASH").mean() * 100), 2),
        f"{start}_deep_dca_days_pct": round(float((detail_period["regime"] == "DEEP_DCA").mean() * 100), 2),
        f"{start}_avg_exposure": round(float(detail_period["exposure"].mean()), 3),
    }


def annual_tables(curves: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    curves = curves.copy()
    curves["year"] = curves["date"].dt.year
    value_cols = [col for col in curves.columns if col not in {"date", "year"}]
    returns = []
    drawdowns = []
    for year, group in curves.groupby("year"):
        ret_row: dict[str, object] = {"Year": int(year), "Period": f"{group['date'].iloc[0].date()} to {group['date'].iloc[-1].date()}"}
        dd_row = ret_row.copy()
        for col in value_cols:
            series = group[col].astype(float)
            ret_row[col] = round((series.iloc[-1] / series.iloc[0] - 1) * 100, 2)
            dd_row[col] = round((series / series.cummax() - 1).min() * 100, 2)
        returns.append(ret_row)
        drawdowns.append(dd_row)
    return pd.DataFrame(returns), pd.DataFrame(drawdowns)


def html_table(frame: pd.DataFrame) -> str:
    headers = "".join(f"<th>{col}</th>" for col in frame.columns)
    rows = []
    for _, row in frame.iterrows():
        rows.append("<tr>" + "".join(f"<td>{value}</td>" for value in row.tolist()) + "</tr>")
    return "<table><thead><tr>" + headers + "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>"


def write_xlsx(path: Path, sheets: dict[str, pd.DataFrame]) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for name, frame in sheets.items():
            frame.to_excel(writer, sheet_name=name[:31], index=False)
        for ws in writer.book.worksheets:
            ws.freeze_panes = "A2"
            for col_cells in ws.columns:
                width = max(len(str(cell.value)) if cell.value is not None else 0 for cell in col_cells)
                ws.column_dimensions[col_cells[0].column_letter].width = min(max(width + 2, 10), 54)


def run() -> None:
    close = fetch_close()
    base_target = build_base_rotation(close, StrategyConfig()).reindex(close.index).ffill()
    close = close.loc[base_target.dropna().index]
    base_target = base_target.loc[close.index]

    rows: list[dict[str, object]] = []
    curve_store: dict[str, pd.Series] = {}
    detail_store: dict[str, pd.DataFrame] = {}
    trade_store: dict[str, list[dict[str, object]]] = {}

    cash_modes = ["selected_or_qqq", "selected_and_qqq"]
    cash_smas = [150, 200]
    exit_buffers = [0.00]
    reentry_buffers = [0.01]
    dca_starts = [0.20, 0.25]
    dca_maxes = [0.50]
    entry_exposures = [0.50, 0.67, 1.00]
    max_exposures = [1.00, 1.50, 2.00]
    dca_filters = ["none", "selected_above_sma20"]
    recover_buffers = [0.05]
    max_days_values: list[int | None] = [20, 63]
    normal_exposures = [1.00]

    tested = 0
    for cash_mode in cash_modes:
        for cash_sma in cash_smas:
            for exit_buffer in exit_buffers:
                for reentry_buffer in reentry_buffers:
                    for dca_start in dca_starts:
                        for dca_max in dca_maxes:
                            if dca_max <= dca_start:
                                continue
                            for entry_exp in entry_exposures:
                                for max_exp in max_exposures:
                                    if max_exp < entry_exp:
                                        continue
                                    for dca_filter in dca_filters:
                                        for recover_buffer in recover_buffers:
                                            for max_days in max_days_values:
                                                for normal_exp in normal_exposures:
                                                    tested += 1
                                                    if tested % 25 == 0:
                                                        print(f"Tested {tested} variants...", flush=True)
                                                    equity, detail, trades = simulate(
                                                        close,
                                                        base_target,
                                                        cash_mode=cash_mode,
                                                        cash_sma=cash_sma,
                                                        exit_buffer=exit_buffer,
                                                        reentry_buffer=reentry_buffer,
                                                        dca_sma=200,
                                                        dca_start=dca_start,
                                                        dca_max_discount=dca_max,
                                                        dca_entry_exposure=entry_exp,
                                                        dca_max_exposure=max_exp,
                                                        dca_filter=dca_filter,
                                                        recover_buffer=recover_buffer,
                                                        max_dca_days=max_days,
                                                        normal_exposure=normal_exp,
                                                    )
                                                    variant = (
                                                        f"{cash_mode}; cashSMA{cash_sma}; exit {exit_buffer:.0%}; reentry {reentry_buffer:.0%}; "
                                                        f"DCA below SMA200 {dca_start:.0%}->{dca_max:.0%}; exp {entry_exp:.2f}->{max_exp:.2f}; "
                                                        f"filter={dca_filter}; recover={recover_buffer:.0%}; maxDays={max_days}; normal={normal_exp:.2f}"
                                                    )
                                                    row = {
                                                        "variant": variant,
                                                        "cash_mode": cash_mode,
                                                        "cash_sma": cash_sma,
                                                        "exit_buffer_pct": round(exit_buffer * 100, 2),
                                                        "reentry_buffer_pct": round(reentry_buffer * 100, 2),
                                                        "dca_start_below_sma_pct": round(dca_start * 100, 2),
                                                        "dca_max_below_sma_pct": round(dca_max * 100, 2),
                                                        "dca_entry_exposure": entry_exp,
                                                        "dca_max_exposure": max_exp,
                                                        "dca_filter": dca_filter,
                                                        "recover_buffer_pct": round(recover_buffer * 100, 2),
                                                        "max_dca_days": max_days if max_days is not None else "none",
                                                        "normal_exposure": normal_exp,
                                                        "trade_events": len(trades),
                                                        **metric_for_period(equity, detail, start="2010"),
                                                        **metric_for_period(equity, detail, start="2020"),
                                                    }
                                                    rows.append(row)
                                                    candidates = [
                                                        ("best_2010_balanced", row["2010_max_drawdown_pct"] >= -50, row["2010_return_pct"]),
                                                        ("best_2020_balanced", row["2020_max_drawdown_pct"] >= -50, row["2020_return_pct"]),
                                                        ("best_2020_2022_control", row["2020_2022_return_pct"] >= -20, row["2020_return_pct"]),
                                                        ("best_low_dd", row["2010_max_drawdown_pct"] >= -40 and row["2020_max_drawdown_pct"] >= -40, row["2010_return_pct"]),
                                                        ("best_calmar_2010", True, row["2010_calmar"]),
                                                        ("best_calmar_2020", True, row["2020_calmar"]),
                                                        ("best_raw_2010", True, row["2010_return_pct"]),
                                                        ("best_raw_2020", True, row["2020_return_pct"]),
                                                    ]
                                                    for key, ok, score in candidates:
                                                        if not ok:
                                                            continue
                                                        current = curve_store.get(key)
                                                        current_score = current.attrs.get("score", -np.inf) if current is not None else -np.inf
                                                        if float(score) > current_score:
                                                            equity.attrs["score"] = float(score)
                                                            curve_store[key] = equity
                                                            detail_store[key] = detail
                                                            trade_store[key] = trades

    result = pd.DataFrame(rows)
    result = result.sort_values(["2010_max_drawdown_pct", "2010_return_pct"], ascending=[False, False]).reset_index(drop=True)
    result.insert(0, "rank_drawdown_first", np.arange(1, len(result) + 1))
    all_path = REPORTS / "soxl_tqqq_cash_dca_deep_search_all.csv"
    top_path = REPORTS / "soxl_tqqq_cash_dca_deep_top.csv"
    result.to_csv(all_path, index=False)
    result.head(300).to_csv(top_path, index=False)

    summary_cases = [
        ("Best full-period return with DD <= 50%", result[result["2010_max_drawdown_pct"] >= -50].sort_values("2010_return_pct", ascending=False)),
        ("Best 2020-to-date return with DD <= 50%", result[result["2020_max_drawdown_pct"] >= -50].sort_values("2020_return_pct", ascending=False)),
        ("Best 2020 strategy with 2022 loss <= 20%", result[result["2020_2022_return_pct"] >= -20].sort_values("2020_return_pct", ascending=False)),
        ("Best low drawdown under 40%", result[(result["2010_max_drawdown_pct"] >= -40) & (result["2020_max_drawdown_pct"] >= -40)].sort_values("2010_return_pct", ascending=False)),
        ("Best full-period Calmar", result.sort_values("2010_calmar", ascending=False)),
        ("Best 2020 Calmar", result.sort_values("2020_calmar", ascending=False)),
        ("Best raw full-period return", result.sort_values("2010_return_pct", ascending=False)),
        ("Best raw 2020 return", result.sort_values("2020_return_pct", ascending=False)),
    ]
    summary_rows = []
    for case, frame in summary_cases:
        if frame.empty:
            continue
        row = frame.iloc[0].to_dict()
        row["case"] = case
        summary_rows.append(row)
    summary = pd.DataFrame(summary_rows)
    summary_cols = [
        "case",
        "variant",
        "2010_return_pct",
        "2010_cagr_pct",
        "2010_max_drawdown_pct",
        "2010_calmar",
        "2010_cash_days_pct",
        "2010_deep_dca_days_pct",
        "2020_return_pct",
        "2020_cagr_pct",
        "2020_max_drawdown_pct",
        "2020_2022_return_pct",
        "2020_2022_drawdown_pct",
        "2020_calmar",
        "2020_cash_days_pct",
        "2020_deep_dca_days_pct",
        "trade_events",
    ]
    summary = summary[summary_cols]

    curves = pd.DataFrame({"date": close.index})
    for key, equity in curve_store.items():
        curves[key] = equity.values
        detail_store[key].to_csv(REPORTS / f"soxl_tqqq_cash_dca_deep_{key}_daily.csv", index=False)
        pd.DataFrame(trade_store[key]).to_csv(REPORTS / f"soxl_tqqq_cash_dca_deep_{key}_trades.csv", index=False)
    annual_returns, annual_drawdowns = annual_tables(curves)

    xlsx_path = ROOT / "SOXL_TQQQ_Cash_DCA_Deep_Search.xlsx"
    html_path = ROOT / "SOXL_TQQQ_Cash_DCA_Deep_Search.html"
    csv_path = ROOT / "SOXL_TQQQ_Cash_DCA_Deep_Summary.csv"
    summary.to_csv(csv_path, index=False)
    write_xlsx(
        xlsx_path,
        {
            "Summary": summary,
            "Annual Return %": annual_returns,
            "Annual Drawdown %": annual_drawdowns,
            "Top 300": result.head(300),
            "All Results": result,
            "Curves": curves,
        },
    )
    html_path.write_text(
        "<!doctype html><html><head><meta charset='utf-8'><title>SOXL/TQQQ Cash + Deep DCA Search</title>"
        "<style>body{font-family:Arial,sans-serif;margin:28px;color:#111827}table{border-collapse:collapse;font-size:13px}"
        "th,td{border:1px solid #d1d5db;padding:7px 10px;text-align:right;vertical-align:top}th{background:#f3f4f6}"
        "th:nth-child(1),td:nth-child(1),th:nth-child(2),td:nth-child(2){text-align:left}td:nth-child(2){max-width:680px}</style></head><body>"
        "<h1>SOXL/TQQQ Cash + Deep DCA Search</h1>"
        "<p>DCA is only allowed while normal trend rules are risk-off and the selected ETF is deeply below SMA200.</p>"
        "<h2>Summary</h2>"
        + html_table(summary)
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
        for col in ["best_2010_balanced", "best_2020_balanced", "best_2020_2022_control", "best_low_dd", "best_calmar_2010"]:
            if col in curves:
                ax.plot(pd.to_datetime(curves["date"]), curves[col] / curves[col].iloc[0], label=col, linewidth=1.8)
        ax.set_yscale("log")
        ax.set_title("SOXL/TQQQ Cash + Deep DCA Candidates")
        ax.set_ylabel("Growth of $1, log scale")
        ax.grid(True, which="both", alpha=0.25)
        ax.legend()
        fig.tight_layout()
        fig.savefig(ROOT / "SOXL_TQQQ_Cash_DCA_Deep_Curves.png", dpi=180)
        plt.close(fig)
    except Exception:
        pass

    print(f"Tested {len(result):,} variants")
    print(summary.to_string(index=False))
    print(xlsx_path)
    print(html_path)
    print(csv_path)


if __name__ == "__main__":
    run()
