from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf


START = "2010-03-11"
END_EXCLUSIVE = "2026-05-21"
END_LABEL = "2026-05-20"
SYMBOLS = ["SOXL", "TQQQ"]
OUT_DIR = Path("reports")


@dataclass(frozen=True)
class Result:
    rank: int | None
    family: str
    variant: str
    rebalance: str
    requested_range: str
    actual_range: str
    net_perf_pct: float
    cagr_pct: float
    max_drawdown_pct: float
    sharpe: float
    positions: int
    win_rate_pct: float | None
    avg_trade_pct: float | None
    median_trade_days: float | None
    soxl_return_pct: float
    soxl_max_drawdown_pct: float
    tqqq_return_pct: float
    tqqq_max_drawdown_pct: float
    soxl_only_net_pct: float
    soxl_only_max_drawdown_pct: float
    excess_vs_soxl_only_pct: float
    beats_soxl_only: bool
    notes: str


def flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df = df.copy()
        df.columns = ["_".join([str(part) for part in col if part]) for col in df.columns]
    return df


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
    if raw.empty:
        raise RuntimeError("No data returned by yfinance.")
    if isinstance(raw.columns, pd.MultiIndex):
        close = raw["Close"].copy()
    else:
        close = raw[["Close"]].copy()
        close.columns = SYMBOLS
    close = close[SYMBOLS].dropna()
    close.index = pd.to_datetime(close.index).tz_localize(None)
    return close


def max_drawdown(equity: pd.Series) -> float:
    drawdown = equity / equity.cummax() - 1
    return float(drawdown.min() * 100)


def perf_pct(equity: pd.Series) -> float:
    return (float(equity.iloc[-1]) - 1) * 100


def cagr_pct(equity: pd.Series) -> float:
    days = max((equity.index[-1] - equity.index[0]).days, 1)
    years = days / 365.25
    return (float(equity.iloc[-1]) ** (1 / years) - 1) * 100


def sharpe_ratio(strategy_returns: pd.Series) -> float:
    std = strategy_returns.std(ddof=0)
    if std == 0 or np.isnan(std):
        return 0.0
    return float(strategy_returns.mean() / std * np.sqrt(252))


def asset_equity(close: pd.DataFrame, symbol: str) -> pd.Series:
    return close[symbol] / close[symbol].iloc[0]


def build_rebalance_mask(index: pd.DatetimeIndex, freq: str) -> pd.Series:
    if freq == "daily":
        return pd.Series(True, index=index)
    periods = index.to_period("W-FRI" if freq == "weekly" else "M")
    return pd.Series(periods != periods.shift(1), index=index)


def trade_stats(close: pd.DataFrame, allocation: pd.Series) -> tuple[int, float | None, float | None, float | None]:
    if allocation.empty:
        return 0, None, None, None
    trades: list[float] = []
    holding_days: list[int] = []
    current = str(allocation.iloc[0])
    entry_date = allocation.index[0]
    entry_price = float(close.loc[entry_date, current])
    for ts, symbol in allocation.iloc[1:].items():
        symbol = str(symbol)
        if symbol == current:
            continue
        exit_price = float(close.loc[ts, current])
        trades.append(exit_price / entry_price - 1)
        holding_days.append(max((ts - entry_date).days, 0))
        current = symbol
        entry_date = ts
        entry_price = float(close.loc[ts, current])
    exit_price = float(close.loc[allocation.index[-1], current])
    trades.append(exit_price / entry_price - 1)
    holding_days.append(max((allocation.index[-1] - entry_date).days, 0))
    win_rate = len([trade for trade in trades if trade > 0]) / len(trades) * 100 if trades else None
    avg_trade = float(np.mean(trades) * 100) if trades else None
    median_days = float(np.median(holding_days)) if holding_days else None
    return len(trades), win_rate, avg_trade, median_days


def apply_hysteresis(raw_choice: pd.Series, score_diff: pd.Series, threshold: float) -> pd.Series:
    if threshold <= 0 or raw_choice.empty:
        return raw_choice
    out: list[str] = []
    current: str | None = None
    for ts, choice in raw_choice.items():
        choice = str(choice)
        if current is None:
            current = choice
        elif choice != current and abs(float(score_diff.loc[ts])) >= threshold:
            current = choice
        out.append(current)
    return pd.Series(out, index=raw_choice.index)


def apply_rebalance(raw_choice: pd.Series, freq: str) -> pd.Series:
    if freq == "daily":
        return raw_choice
    mask = build_rebalance_mask(raw_choice.index, freq)
    return raw_choice.where(mask).ffill()


def apply_stop_switch(close: pd.DataFrame, allocation: pd.Series, stop_pct: float | None) -> pd.Series:
    if stop_pct is None or allocation.empty:
        return allocation
    out: list[str] = []
    current = str(allocation.iloc[0])
    entry_price = float(close.loc[allocation.index[0], current])
    for ts, desired in allocation.items():
        desired = str(desired)
        if desired != current:
            current = desired
            entry_price = float(close.loc[ts, current])
        elif float(close.loc[ts, current]) <= entry_price * (1 - stop_pct):
            current = "TQQQ" if current == "SOXL" else "SOXL"
            entry_price = float(close.loc[ts, current])
        out.append(current)
    return pd.Series(out, index=allocation.index)


def backtest_allocation(close: pd.DataFrame, raw_choice: pd.Series, *, rebalance: str, stop_pct: float | None) -> tuple[pd.Series, pd.Series, pd.Series]:
    choice = raw_choice.reindex(close.index).ffill().dropna()
    choice = apply_rebalance(choice, rebalance).ffill().dropna()
    choice = apply_stop_switch(close.loc[choice.index], choice, stop_pct)
    allocation = choice.shift(1).dropna()
    tested_close = close.loc[allocation.index]
    returns = tested_close.pct_change().fillna(0)
    strategy_returns = pd.Series(
        [returns.loc[ts, str(allocation.loc[ts])] for ts in tested_close.index],
        index=tested_close.index,
    )
    equity = (1 + strategy_returns).cumprod()
    return equity, strategy_returns, allocation


def soxl_only_baseline(close: pd.DataFrame, fast: int = 50, slow: int = 63, stop_pct: float = 0.10) -> tuple[pd.Series, list[float]]:
    soxl = close["SOXL"]
    fast_ma = soxl.rolling(fast).mean()
    slow_ma = soxl.rolling(slow).mean()
    trend_on = (fast_ma > slow_ma).fillna(False)
    capital = 1.0
    in_position = False
    entry_price = np.nan
    equity_values: list[float] = []
    trades: list[float] = []
    for ts, price in soxl.items():
        price = float(price)
        if not in_position and bool(trend_on.loc[ts]):
            in_position = True
            entry_price = price
        mark = capital if not in_position else capital * (price / entry_price)
        stop_hit = in_position and price <= entry_price * (1 - stop_pct)
        trend_exit = in_position and not bool(trend_on.loc[ts])
        if stop_hit or trend_exit:
            trade = price / entry_price - 1
            trades.append(trade)
            capital *= 1 + trade
            in_position = False
            entry_price = np.nan
            mark = capital
        equity_values.append(mark)
    if in_position:
        trade = float(soxl.iloc[-1]) / entry_price - 1
        trades.append(trade)
        equity_values[-1] = capital * (1 + trade)
    return pd.Series(equity_values, index=close.index), trades


def summarize(
    *,
    close: pd.DataFrame,
    family: str,
    variant: str,
    rebalance: str,
    equity: pd.Series,
    strategy_returns: pd.Series,
    allocation: pd.Series,
    baseline_equity: pd.Series,
    notes: str,
) -> Result:
    tested_close = close.loc[equity.index]
    soxl_eq = asset_equity(tested_close, "SOXL")
    tqqq_eq = asset_equity(tested_close, "TQQQ")
    baseline = baseline_equity.reindex(equity.index).ffill()
    baseline = baseline / baseline.iloc[0]
    positions, win_rate, avg_trade, median_days = trade_stats(tested_close, allocation.reindex(equity.index).dropna())
    net = perf_pct(equity)
    baseline_net = perf_pct(baseline)
    return Result(
        rank=None,
        family=family,
        variant=variant,
        rebalance=rebalance,
        requested_range=f"{START} to {END_LABEL}",
        actual_range=f"{equity.index[0].date().isoformat()} to {equity.index[-1].date().isoformat()}",
        net_perf_pct=round(net, 2),
        cagr_pct=round(cagr_pct(equity), 2),
        max_drawdown_pct=round(max_drawdown(equity), 2),
        sharpe=round(sharpe_ratio(strategy_returns), 2),
        positions=positions,
        win_rate_pct=round(win_rate, 2) if win_rate is not None else None,
        avg_trade_pct=round(avg_trade, 2) if avg_trade is not None else None,
        median_trade_days=round(median_days, 2) if median_days is not None else None,
        soxl_return_pct=round(perf_pct(soxl_eq), 2),
        soxl_max_drawdown_pct=round(max_drawdown(soxl_eq), 2),
        tqqq_return_pct=round(perf_pct(tqqq_eq), 2),
        tqqq_max_drawdown_pct=round(max_drawdown(tqqq_eq), 2),
        soxl_only_net_pct=round(baseline_net, 2),
        soxl_only_max_drawdown_pct=round(max_drawdown(baseline), 2),
        excess_vs_soxl_only_pct=round(net - baseline_net, 2),
        beats_soxl_only=bool(net > baseline_net),
        notes=notes,
    )


def total_return_score(close: pd.DataFrame, lookback: int, skip: int) -> pd.DataFrame:
    current = close.shift(skip)
    previous = close.shift(lookback + skip)
    return current / previous - 1


def volatility_score(close: pd.DataFrame, lookback: int, skip: int) -> pd.DataFrame:
    returns = close.pct_change().shift(skip)
    return returns.rolling(lookback).std() * np.sqrt(252)


def choose_from_scores(score: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    diff = score["SOXL"] - score["TQQQ"]
    choice = pd.Series(np.where(diff >= 0, "SOXL", "TQQQ"), index=score.index)
    return choice, diff


def generate_momentum_variants(close: pd.DataFrame, baseline_equity: pd.Series) -> list[Result]:
    results: list[Result] = []
    lookbacks = [10, 21, 42, 63, 84, 126, 168, 252]
    skips = [0, 5, 21]
    rebalances = ["daily", "weekly", "monthly"]
    hysteresis_levels = [0.0, 0.02]
    stop_levels: list[float | None] = [None, 0.10, 0.20]
    trend_windows = [0, 100, 200]
    score_modes = ["return", "return_over_vol", "return_minus_vol"]
    for lookback in lookbacks:
        ret_score = total_return_score(close, lookback, 0)
        for skip in skips:
            score_return = total_return_score(close, lookback, skip)
            vol = volatility_score(close, max(lookback, 10), skip)
            scores = {
                "return": score_return,
                "return_over_vol": score_return / vol.replace(0, np.nan),
                "return_minus_half_vol": score_return - 0.5 * vol,
                "return_minus_vol": score_return - vol,
            }
            for score_mode, score in scores.items():
                base_raw, diff = choose_from_scores(score)
                for trend_window in trend_windows:
                    raw = base_raw.copy()
                    if trend_window > 0:
                        trend_ok = close > close.rolling(trend_window).mean()
                        other = pd.Series(np.where(raw == "SOXL", "TQQQ", "SOXL"), index=raw.index)
                        raw = pd.Series(
                            [
                                pick
                                if bool(trend_ok.loc[ts, pick])
                                else alt
                                if bool(trend_ok.loc[ts, alt])
                                else pick
                                for ts, pick, alt in zip(raw.index, raw, other)
                            ],
                            index=raw.index,
                        )
                        trend_label = f", chosen/alternate above SMA{trend_window}"
                    else:
                        trend_label = ""
                    for hysteresis in hysteresis_levels:
                        selected = apply_hysteresis(raw.dropna(), diff.reindex(raw.index).fillna(0), hysteresis)
                        for rebalance in rebalances:
                            for stop_pct in stop_levels:
                                equity, strategy_returns, allocation = backtest_allocation(
                                    close,
                                    selected,
                                    rebalance=rebalance,
                                    stop_pct=stop_pct,
                                )
                                if len(equity) < 252:
                                    continue
                                skip_label = "" if skip == 0 else f", skip {skip}d"
                                hyst_label = "" if hysteresis == 0 else f", {hysteresis:.0%} hysteresis"
                                stop_label = "" if stop_pct is None else f", switch on {stop_pct:.0%} stop"
                                results.append(
                                    summarize(
                                        close=close,
                                        family="Relative momentum rotation",
                                        variant=f"{lookback}d {score_mode}{skip_label}{trend_label}{hyst_label}{stop_label}",
                                        rebalance=rebalance,
                                        equity=equity,
                                        strategy_returns=strategy_returns,
                                        allocation=allocation,
                                        baseline_equity=baseline_equity,
                                        notes="Always invested in SOXL or TQQQ; signal uses prior-close data; no costs/slippage.",
                                    )
                                )
        # Simple non-skipped score retained so short lookbacks can also act as a control.
        if lookback in [21, 63, 126, 252]:
            raw, diff = choose_from_scores(ret_score)
            selected = apply_hysteresis(raw.dropna(), diff.reindex(raw.index).fillna(0), 0.0)
            equity, strategy_returns, allocation = backtest_allocation(close, selected, rebalance="monthly", stop_pct=None)
            results.append(
                summarize(
                    close=close,
                    family="Relative momentum rotation",
                    variant=f"{lookback}d return control, monthly",
                    rebalance="monthly",
                    equity=equity,
                    strategy_returns=strategy_returns,
                    allocation=allocation,
                    baseline_equity=baseline_equity,
                    notes="Control variant.",
                )
            )
    return results


def generate_pullback_variants(close: pd.DataFrame, baseline_equity: pd.Series) -> list[Result]:
    results: list[Result] = []
    long_lookbacks = [42, 63, 84, 126, 168, 252]
    short_lookbacks = [3, 5, 10, 21]
    rebalances = ["daily", "weekly"]
    stop_levels: list[float | None] = [None, 0.10, 0.20]
    for long_lb in long_lookbacks:
        long_score = total_return_score(close, long_lb, 0)
        long_choice, long_diff = choose_from_scores(long_score)
        trend = close > close.rolling(100).mean()
        for short_lb in short_lookbacks:
            short_score = total_return_score(close, short_lb, 0)
            pullback_choice = pd.Series(
                np.where(short_score["SOXL"] <= short_score["TQQQ"], "SOXL", "TQQQ"),
                index=close.index,
            )
            for require_long_leader_trend in [False, True]:
                if require_long_leader_trend:
                    raw = pd.Series(
                        [
                            pull
                            if bool(trend.loc[ts, pull]) and bool(long_score.loc[ts, pull] > 0)
                            else lead
                            for ts, pull, lead in zip(close.index, pullback_choice, long_choice)
                        ],
                        index=close.index,
                    )
                    trend_label = ", pullback asset must be above SMA100 and positive long momentum"
                else:
                    raw = pd.Series(
                        [
                            pull if bool(long_score.loc[ts, pull] > 0) else lead
                            for ts, pull, lead in zip(close.index, pullback_choice, long_choice)
                        ],
                        index=close.index,
                    )
                    trend_label = ", pullback asset must have positive long momentum"
                for rebalance in rebalances:
                    for stop_pct in stop_levels:
                        equity, strategy_returns, allocation = backtest_allocation(
                            close,
                            raw.dropna(),
                            rebalance=rebalance,
                            stop_pct=stop_pct,
                        )
                        if len(equity) < 252:
                            continue
                        stop_label = "" if stop_pct is None else f", switch on {stop_pct:.0%} stop"
                        results.append(
                            summarize(
                                close=close,
                                family="Momentum pullback rotation",
                                variant=f"{long_lb}d leader fallback, buy weaker {short_lb}d pullback{trend_label}{stop_label}",
                                rebalance=rebalance,
                                equity=equity,
                                strategy_returns=strategy_returns,
                                allocation=allocation,
                                baseline_equity=baseline_equity,
                                notes="Mean-reversion entry inside a longer momentum framework; prior-close signal; no costs/slippage.",
                            )
                        )
    return results


def generate_ensemble_variants(close: pd.DataFrame, baseline_equity: pd.Series) -> list[Result]:
    results: list[Result] = []
    lookback_sets = [(21, 63, 126), (42, 84, 168), (63, 126, 252), (10, 21, 63, 126)]
    rebalances = ["daily", "weekly", "monthly"]
    stop_levels: list[float | None] = [None, 0.10, 0.20]
    for lookbacks in lookback_sets:
        votes = []
        for lookback in lookbacks:
            score = total_return_score(close, lookback, 0)
            votes.append((score["SOXL"] >= score["TQQQ"]).astype(int))
        vote_sum = sum(votes)
        base_raw = pd.Series(np.where(vote_sum >= (len(lookbacks) / 2), "SOXL", "TQQQ"), index=close.index)
        for trend_window in [0, 100, 200]:
            selected = base_raw.copy()
            if trend_window > 0:
                trend_ok = close > close.rolling(trend_window).mean()
                other = pd.Series(np.where(selected == "SOXL", "TQQQ", "SOXL"), index=selected.index)
                selected = pd.Series(
                    [
                        pick
                        if bool(trend_ok.loc[ts, pick])
                        else alt
                        if bool(trend_ok.loc[ts, alt])
                        else pick
                        for ts, pick, alt in zip(selected.index, selected, other)
                    ],
                    index=selected.index,
                )
                trend_label = f", chosen/alternate above SMA{trend_window}"
            else:
                trend_label = ""
            for rebalance in rebalances:
                for stop_pct in stop_levels:
                    equity, strategy_returns, allocation = backtest_allocation(
                        close,
                        selected.dropna(),
                        rebalance=rebalance,
                        stop_pct=stop_pct,
                    )
                    if len(equity) < 252:
                        continue
                    stop_label = "" if stop_pct is None else f", switch on {stop_pct:.0%} stop"
                    results.append(
                        summarize(
                            close=close,
                            family="Multi-lookback vote rotation",
                            variant=f"Vote {lookbacks}{trend_label}{stop_label}",
                            rebalance=rebalance,
                            equity=equity,
                            strategy_returns=strategy_returns,
                            allocation=allocation,
                            baseline_equity=baseline_equity,
                            notes="SOXL/TQQQ chosen by majority of relative momentum windows; no costs/slippage.",
                        )
                    )
    return results


def write_plot(best_equity: pd.Series, close: pd.DataFrame, baseline_equity: pd.Series) -> Path | None:
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return None
    path = OUT_DIR / "soxl_tqqq_rotation_best_equity.png"
    tested_close = close.loc[best_equity.index]
    soxl = asset_equity(tested_close, "SOXL")
    tqqq = asset_equity(tested_close, "TQQQ")
    baseline = baseline_equity.reindex(best_equity.index).ffill()
    baseline = baseline / baseline.iloc[0]
    plt.figure(figsize=(11, 6))
    plt.plot(best_equity.index, best_equity, label="Best SOXL/TQQQ rotation", linewidth=1.6)
    plt.plot(baseline.index, baseline, label="SOXL-only SMA50/SMA63 10% stop", linewidth=1.2)
    plt.plot(soxl.index, soxl, label="SOXL buy/hold", linewidth=1.0, alpha=0.8)
    plt.plot(tqqq.index, tqqq, label="TQQQ buy/hold", linewidth=1.0, alpha=0.8)
    plt.yscale("log")
    plt.title("Best Local SOXL/TQQQ Rotation Search Result")
    plt.ylabel("Growth of $1, log scale")
    plt.grid(True, alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
    return path


def write_outputs(results: list[Result], best_equity: pd.Series, best_allocation: pd.Series, close: pd.DataFrame, baseline_equity: pd.Series) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    all_df = pd.DataFrame([asdict(result) for result in results])
    all_df = all_df.sort_values(
        ["beats_soxl_only", "excess_vs_soxl_only_pct", "net_perf_pct", "max_drawdown_pct"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)
    all_df["rank"] = all_df.index + 1
    all_path = OUT_DIR / "soxl_tqqq_rotation_search_all.csv"
    best_path = OUT_DIR / "soxl_tqqq_rotation_search_best.csv"
    json_path = OUT_DIR / "soxl_tqqq_rotation_search_all.json"
    curve_path = OUT_DIR / "soxl_tqqq_rotation_best_equity.csv"
    allocation_path = OUT_DIR / "soxl_tqqq_rotation_best_allocation.csv"
    report_path = OUT_DIR / "soxl_tqqq_rotation_search.md"
    all_df.to_csv(all_path, index=False)
    all_df.head(50).to_csv(best_path, index=False)
    json_path.write_text(json.dumps(all_df.to_dict(orient="records"), indent=2), encoding="utf-8")
    equity_df = pd.DataFrame(
        {
            "date": best_equity.index,
            "best_rotation_equity": best_equity.values,
            "soxl_only_equity": (baseline_equity.reindex(best_equity.index).ffill() / baseline_equity.reindex(best_equity.index).ffill().iloc[0]).values,
            "soxl_buy_hold_equity": asset_equity(close.loc[best_equity.index], "SOXL").values,
            "tqqq_buy_hold_equity": asset_equity(close.loc[best_equity.index], "TQQQ").values,
        }
    )
    equity_df.to_csv(curve_path, index=False)
    pd.DataFrame({"date": best_allocation.index, "allocation": best_allocation.values}).to_csv(allocation_path, index=False)
    plot_path = write_plot(best_equity, close, baseline_equity)

    top = all_df.head(10).copy()
    families = (
        all_df.sort_values(["family", "beats_soxl_only", "excess_vs_soxl_only_pct"], ascending=[True, False, False])
        .groupby("family", as_index=False)
        .head(1)
        .sort_values("excess_vs_soxl_only_pct", ascending=False)
    )
    baseline_net = float(top["soxl_only_net_pct"].iloc[0])
    baseline_dd = float(top["soxl_only_max_drawdown_pct"].iloc[0])
    beat_count = int(all_df["beats_soxl_only"].sum())
    def markdown_table(frame: pd.DataFrame) -> str:
        try:
            return frame.to_markdown(index=False)
        except Exception:
            return frame.to_csv(index=False)

    lines = [
        "# SOXL/TQQQ Local Rotation Strategy Search",
        "",
        f"Tested {len(all_df):,} always-invested SOXL/TQQQ variants from {START} to {END_LABEL}. Signals use prior-close data and daily adjusted yfinance prices. Results exclude commissions, slippage, taxes, borrow/friction, and are in-sample optimized.",
        "",
        f"Baseline hurdle: automated SOXL-only SMA50/SMA63 state with 10% stop returned {baseline_net:,.2f}% with {baseline_dd:,.2f}% max drawdown over the comparable local period.",
        "",
        f"Variants beating the SOXL-only hurdle by total return: {beat_count:,} of {len(all_df):,}.",
        "",
        "## Top 10 By Excess Vs SOXL-Only",
        "",
        markdown_table(top[
            [
                "rank",
                "family",
                "variant",
                "rebalance",
                "actual_range",
                "net_perf_pct",
                "excess_vs_soxl_only_pct",
                "max_drawdown_pct",
                "positions",
                "win_rate_pct",
                "median_trade_days",
                "soxl_return_pct",
                "tqqq_return_pct",
            ]
        ]),
        "",
        "## Best Variant Per Family",
        "",
        markdown_table(families[
            [
                "rank",
                "family",
                "variant",
                "rebalance",
                "net_perf_pct",
                "excess_vs_soxl_only_pct",
                "max_drawdown_pct",
                "positions",
                "sharpe",
            ]
        ]),
        "",
        "## Files",
        "",
        f"- Full grid: `{all_path}`",
        f"- Top 50: `{best_path}`",
        f"- Best equity curve: `{curve_path}`",
        f"- Best allocation history: `{allocation_path}`",
    ]
    if plot_path is not None:
        lines.append(f"- Equity plot: `{plot_path}`")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "The best in-sample variants usually rotate by short-to-intermediate relative momentum, often with a stop-switch overlay. That fits the character of these ETFs: SOXL can dominate semiconductor-led bursts, while TQQQ can reduce some single-sector damage when chips weaken but large-cap growth remains bid.",
            "",
            "Treat the winner as a candidate, not a finished trading system. The search intentionally tried many knobs, so the top row is exposed to overfitting. A better production path is to choose a simple family from the top group, then validate it on walk-forward slices before wiring it into the daily scanner.",
        ]
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Total variants: {len(all_df):,}")
    print(f"Beating SOXL-only: {beat_count:,}")
    print()
    print(top[["rank", "family", "variant", "rebalance", "net_perf_pct", "excess_vs_soxl_only_pct", "max_drawdown_pct", "positions"]].to_string(index=False))
    print()
    print(f"Wrote {report_path}")


def run() -> None:
    close = fetch_close()
    baseline_equity, _ = soxl_only_baseline(close)
    results: list[Result] = []
    results.extend(generate_momentum_variants(close, baseline_equity))
    results.extend(generate_pullback_variants(close, baseline_equity))
    results.extend(generate_ensemble_variants(close, baseline_equity))
    if not results:
        raise RuntimeError("No variants were generated.")

    best_equity = pd.Series(dtype=float)
    best_allocation = pd.Series(dtype=object)
    best_excess = -np.inf
    for result in results:
        if result.excess_vs_soxl_only_pct > best_excess:
            best_excess = result.excess_vs_soxl_only_pct
            # Recompute the best after output sorting to keep memory use lower during the large grid.
    result_rows = pd.DataFrame([asdict(result) for result in results])
    best_row = result_rows.sort_values(["beats_soxl_only", "excess_vs_soxl_only_pct", "net_perf_pct"], ascending=[False, False, False]).iloc[0]
    best_equity, _, best_allocation = recompute_variant(close, str(best_row["family"]), str(best_row["variant"]), str(best_row["rebalance"]))
    write_outputs(results, best_equity, best_allocation, close, baseline_equity)


def _choice_with_hysteresis(raw: np.ndarray, diff: np.ndarray, threshold: float) -> np.ndarray:
    out = raw.copy()
    current = -1
    for i, choice in enumerate(raw):
        if choice < 0:
            out[i] = current
            continue
        if current < 0:
            current = int(choice)
        elif choice != current and abs(float(diff[i])) >= threshold:
            current = int(choice)
        out[i] = current
    return out


def _apply_rebalance_codes(raw: np.ndarray, dates: pd.DatetimeIndex, freq: str) -> np.ndarray:
    out = np.full(len(raw), -1, dtype=np.int8)
    current = -1
    if freq == "weekly":
        periods = dates.to_period("W-FRI")
        rebalance = np.r_[True, periods[1:] != periods[:-1]]
    elif freq == "monthly":
        periods = dates.to_period("M")
        rebalance = np.r_[True, periods[1:] != periods[:-1]]
    else:
        rebalance = np.ones(len(raw), dtype=bool)
    for i, choice in enumerate(raw):
        if choice >= 0 and (rebalance[i] or current < 0):
            current = int(choice)
        out[i] = current
    return out


def _apply_stop_codes(prices: np.ndarray, raw: np.ndarray, stop_pct: float | None) -> np.ndarray:
    if stop_pct is None:
        return raw
    out = np.full(len(raw), -1, dtype=np.int8)
    current = -1
    entry = np.nan
    for i, desired in enumerate(raw):
        if desired < 0:
            out[i] = current
            continue
        if current < 0 or desired != current:
            current = int(desired)
            entry = float(prices[i, current])
        elif float(prices[i, current]) <= entry * (1 - stop_pct):
            current = 1 - current
            entry = float(prices[i, current])
        out[i] = current
    return out


def _fast_eval(
    *,
    close: pd.DataFrame,
    prices: np.ndarray,
    returns: np.ndarray,
    raw_choice: np.ndarray,
    diff: np.ndarray,
    family: str,
    variant: str,
    rebalance: str,
    stop_pct: float | None,
    baseline_equity: pd.Series,
    baseline_values: np.ndarray,
    notes: str,
    best_excess: float,
) -> tuple[dict[str, object] | None, float, pd.Series | None, pd.Series | None]:
    raw_choice = _choice_with_hysteresis(raw_choice, diff, _extract_hysteresis(variant))
    selected = _apply_rebalance_codes(raw_choice, close.index, rebalance)
    selected = _apply_stop_codes(prices, selected, stop_pct)
    allocation = np.roll(selected, 1)
    allocation[0] = -1
    valid = allocation >= 0
    if valid.sum() < 252:
        return None, best_excess, None, None
    start = int(np.argmax(valid))
    idx = np.arange(start, len(close))
    alloc = allocation[idx].astype(int)
    strat_returns = returns[idx, alloc]
    strat_returns[0] = 0
    equity_values = np.cumprod(1 + strat_returns)
    eq_index = close.index[idx]
    net = (float(equity_values[-1]) - 1) * 100
    years = max((eq_index[-1] - eq_index[0]).days, 1) / 365.25
    cagr = (float(equity_values[-1]) ** (1 / years) - 1) * 100
    equity_dd = float(np.min(equity_values / np.maximum.accumulate(equity_values) - 1) * 100)
    std = float(np.std(strat_returns))
    sharpe = 0.0 if std == 0 or np.isnan(std) else float(np.mean(strat_returns) / std * np.sqrt(252))
    soxl_slice = prices[idx, 0] / prices[idx[0], 0]
    tqqq_slice = prices[idx, 1] / prices[idx[0], 1]
    soxl_ret = (float(soxl_slice[-1]) - 1) * 100
    tqqq_ret = (float(tqqq_slice[-1]) - 1) * 100
    soxl_dd = float(np.min(soxl_slice / np.maximum.accumulate(soxl_slice) - 1) * 100)
    tqqq_dd = float(np.min(tqqq_slice / np.maximum.accumulate(tqqq_slice) - 1) * 100)
    baseline_slice = baseline_values[idx] / baseline_values[idx[0]]
    baseline_net = (float(baseline_slice[-1]) - 1) * 100
    baseline_dd = float(np.min(baseline_slice / np.maximum.accumulate(baseline_slice) - 1) * 100)

    trades: list[float] = []
    holding_days: list[int] = []
    current = int(alloc[0])
    entry_i = int(idx[0])
    entry_price = float(prices[entry_i, current])
    for real_i, symbol_code in zip(idx[1:], alloc[1:]):
        symbol_code = int(symbol_code)
        if symbol_code == current:
            continue
        trades.append(float(prices[real_i, current] / entry_price - 1))
        holding_days.append(max((close.index[real_i] - close.index[entry_i]).days, 0))
        current = symbol_code
        entry_i = int(real_i)
        entry_price = float(prices[entry_i, current])
    trades.append(float(prices[idx[-1], current] / entry_price - 1))
    holding_days.append(max((close.index[idx[-1]] - close.index[entry_i]).days, 0))
    positions = len(trades)
    win_rate = len([trade for trade in trades if trade > 0]) / positions * 100 if positions else None
    avg_trade = float(np.mean(trades) * 100) if trades else None
    median_days = float(np.median(holding_days)) if holding_days else None
    excess = net - baseline_net
    row = {
        "rank": None,
        "family": family,
        "variant": variant,
        "rebalance": rebalance,
        "requested_range": f"{START} to {END_LABEL}",
        "actual_range": f"{eq_index[0].date().isoformat()} to {eq_index[-1].date().isoformat()}",
        "net_perf_pct": round(net, 2),
        "cagr_pct": round(cagr, 2),
        "max_drawdown_pct": round(equity_dd, 2),
        "sharpe": round(sharpe, 2),
        "positions": positions,
        "win_rate_pct": round(win_rate, 2) if win_rate is not None else None,
        "avg_trade_pct": round(avg_trade, 2) if avg_trade is not None else None,
        "median_trade_days": round(median_days, 2) if median_days is not None else None,
        "soxl_return_pct": round(soxl_ret, 2),
        "soxl_max_drawdown_pct": round(soxl_dd, 2),
        "tqqq_return_pct": round(tqqq_ret, 2),
        "tqqq_max_drawdown_pct": round(tqqq_dd, 2),
        "soxl_only_net_pct": round(baseline_net, 2),
        "soxl_only_max_drawdown_pct": round(baseline_dd, 2),
        "excess_vs_soxl_only_pct": round(excess, 2),
        "beats_soxl_only": bool(excess > 0),
        "notes": notes,
    }
    if excess > best_excess:
        equity = pd.Series(equity_values, index=eq_index)
        allocation_series = pd.Series(np.where(alloc == 0, "SOXL", "TQQQ"), index=eq_index)
        return row, excess, equity, allocation_series
    return row, best_excess, None, None


def _extract_hysteresis(variant: str) -> float:
    for pct in [1, 2, 5, 10]:
        if f"{pct}% hysteresis" in variant:
            return pct / 100
    return 0.0


def _score_arrays(prices: np.ndarray, lookback: int, skip: int) -> tuple[np.ndarray, np.ndarray]:
    score = np.full_like(prices, np.nan, dtype=float)
    score[lookback + skip :] = prices[lookback : len(prices) - skip] / prices[: len(prices) - lookback - skip] - 1
    daily = np.vstack([np.zeros(2), prices[1:] / prices[:-1] - 1])
    vol_df = pd.DataFrame(daily).shift(skip).rolling(max(lookback, 10)).std() * np.sqrt(252)
    return score, vol_df.to_numpy()


def _raw_from_score(score: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    diff = score[:, 0] - score[:, 1]
    raw = np.where(diff >= 0, 0, 1).astype(np.int8)
    raw[~np.isfinite(diff)] = -1
    safe_diff = np.where(np.isfinite(diff), diff, 0)
    return raw, safe_diff


def _apply_trend_to_raw(prices: np.ndarray, raw: np.ndarray, trend_window: int) -> np.ndarray:
    if trend_window <= 0:
        return raw.copy()
    sma = pd.DataFrame(prices).rolling(trend_window).mean().to_numpy()
    trend_ok = prices > sma
    out = raw.copy()
    for i, pick in enumerate(raw):
        if pick < 0:
            continue
        alt = 1 - int(pick)
        if not bool(trend_ok[i, pick]) and bool(trend_ok[i, alt]):
            out[i] = alt
    return out


def _fast_write_outputs(rows: list[dict[str, object]], best_equity: pd.Series, best_allocation: pd.Series, close: pd.DataFrame, baseline_equity: pd.Series) -> None:
    OUT_DIR.mkdir(exist_ok=True)
    all_df = pd.DataFrame(rows).sort_values(
        ["beats_soxl_only", "excess_vs_soxl_only_pct", "net_perf_pct", "max_drawdown_pct"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)
    all_df["rank"] = all_df.index + 1
    all_path = OUT_DIR / "soxl_tqqq_rotation_search_all.csv"
    best_path = OUT_DIR / "soxl_tqqq_rotation_search_best.csv"
    curve_path = OUT_DIR / "soxl_tqqq_rotation_best_equity.csv"
    allocation_path = OUT_DIR / "soxl_tqqq_rotation_best_allocation.csv"
    report_path = OUT_DIR / "soxl_tqqq_rotation_search.md"
    all_df.to_csv(all_path, index=False)
    all_df.head(50).to_csv(best_path, index=False)
    (OUT_DIR / "soxl_tqqq_rotation_search_all.json").write_text(json.dumps(all_df.to_dict(orient="records"), indent=2), encoding="utf-8")
    comparable_baseline = baseline_equity.reindex(best_equity.index).ffill()
    comparable_baseline = comparable_baseline / comparable_baseline.iloc[0]
    equity_df = pd.DataFrame(
        {
            "date": best_equity.index,
            "best_rotation_equity": best_equity.values,
            "soxl_only_equity": comparable_baseline.values,
            "soxl_buy_hold_equity": asset_equity(close.loc[best_equity.index], "SOXL").values,
            "tqqq_buy_hold_equity": asset_equity(close.loc[best_equity.index], "TQQQ").values,
        }
    )
    equity_df.to_csv(curve_path, index=False)
    pd.DataFrame({"date": best_allocation.index, "allocation": best_allocation.values}).to_csv(allocation_path, index=False)
    plot_path = write_plot(best_equity, close, baseline_equity)
    top = all_df.head(10)
    families = (
        all_df.sort_values(["family", "beats_soxl_only", "excess_vs_soxl_only_pct"], ascending=[True, False, False])
        .groupby("family", as_index=False)
        .head(1)
        .sort_values("excess_vs_soxl_only_pct", ascending=False)
    )

    def md(frame: pd.DataFrame) -> str:
        display = frame.copy()
        headers = [str(column) for column in display.columns]
        rows = []
        for _, row in display.iterrows():
            rows.append([str(value).replace("|", "\\|") for value in row.tolist()])
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
        ]
        lines.extend("| " + " | ".join(row) + " |" for row in rows)
        return "\n".join(lines)

    beat_count = int(all_df["beats_soxl_only"].sum())
    baseline_net = float(top["soxl_only_net_pct"].iloc[0])
    baseline_dd = float(top["soxl_only_max_drawdown_pct"].iloc[0])
    report = [
        "# SOXL/TQQQ Local Rotation Strategy Search",
        "",
        f"Tested {len(all_df):,} always-invested SOXL/TQQQ variants from {START} to {END_LABEL}. Signals use prior-close data and daily adjusted yfinance prices. Results exclude commissions, slippage, taxes, borrow/friction, and are in-sample optimized.",
        "",
        f"Baseline hurdle: automated SOXL-only SMA50/SMA63 state with 10% stop returned {baseline_net:,.2f}% with {baseline_dd:,.2f}% max drawdown over each variant's comparable period.",
        "",
        f"Variants beating the SOXL-only hurdle by total return: {beat_count:,} of {len(all_df):,}.",
        "",
        "## Top 10 By Excess Vs SOXL-Only",
        "",
        md(top[["rank", "family", "variant", "rebalance", "actual_range", "net_perf_pct", "excess_vs_soxl_only_pct", "max_drawdown_pct", "positions", "win_rate_pct", "median_trade_days", "soxl_return_pct", "tqqq_return_pct"]]),
        "",
        "## Best Variant Per Family",
        "",
        md(families[["rank", "family", "variant", "rebalance", "net_perf_pct", "excess_vs_soxl_only_pct", "max_drawdown_pct", "positions", "sharpe"]]),
        "",
        "## Files",
        "",
        f"- Full grid: `{all_path}`",
        f"- Top 50: `{best_path}`",
        f"- Best equity curve: `{curve_path}`",
        f"- Best allocation history: `{allocation_path}`",
    ]
    if plot_path is not None:
        report.append(f"- Equity plot: `{plot_path}`")
    report.extend(
        [
            "",
            "## Interpretation",
            "",
            "The strongest in-sample candidates favor short-to-intermediate relative strength between SOXL and TQQQ, usually with a switch-on-stop overlay. That lets the strategy ride SOXL during semiconductor surges and move into TQQQ when the broader leveraged Nasdaq trend is stronger.",
            "",
            "The top row is not automatically production-ready because this search deliberately tried many combinations. The practical next step is to pick a simple high-ranking variant and run walk-forward or year-by-year validation before using it in the daily signal automation.",
        ]
    )
    report_path.write_text("\n".join(report), encoding="utf-8")
    print(f"Total variants: {len(all_df):,}")
    print(f"Beating SOXL-only: {beat_count:,}")
    print(top[["rank", "family", "variant", "rebalance", "net_perf_pct", "excess_vs_soxl_only_pct", "max_drawdown_pct", "positions"]].to_string(index=False))
    print(f"Wrote {report_path}")


def fast_run() -> None:
    close = fetch_close()
    prices = close[SYMBOLS].to_numpy(dtype=float)
    returns = np.vstack([np.zeros(2), prices[1:] / prices[:-1] - 1])
    baseline_equity, _ = soxl_only_baseline(close)
    baseline_values = baseline_equity.to_numpy(dtype=float)
    rows: list[dict[str, object]] = []
    best_excess = -np.inf
    best_equity: pd.Series | None = None
    best_allocation: pd.Series | None = None

    def add_candidate(family: str, variant: str, rebalance: str, raw: np.ndarray, diff: np.ndarray, stop_pct: float | None, notes: str) -> None:
        nonlocal best_excess, best_equity, best_allocation
        row, best_excess_candidate, equity, allocation = _fast_eval(
            close=close,
            prices=prices,
            returns=returns,
            raw_choice=raw,
            diff=diff,
            family=family,
            variant=variant,
            rebalance=rebalance,
            stop_pct=stop_pct,
            baseline_equity=baseline_equity,
            baseline_values=baseline_values,
            notes=notes,
            best_excess=best_excess,
        )
        if row is None:
            return
        rows.append(row)
        if best_excess_candidate > best_excess:
            best_excess = best_excess_candidate
            best_equity = equity
            best_allocation = allocation

    lookbacks = [5, 10, 21, 42, 63, 84, 105, 126, 168, 189, 252]
    skips = [0, 5, 10, 21]
    score_modes = ["return", "return_over_vol", "return_minus_half_vol", "return_minus_vol"]
    trend_windows = [0, 50, 100, 200]
    hysteresis_levels = [0.0, 0.02, 0.05]
    rebalances = ["daily", "weekly", "monthly"]
    stop_levels: list[float | None] = [None, 0.10, 0.20, 0.30]
    for lookback in lookbacks:
        for skip in skips:
            ret_score, vol = _score_arrays(prices, lookback, skip)
            score_map = {
                "return": ret_score,
                "return_over_vol": ret_score / np.where(vol == 0, np.nan, vol),
                "return_minus_half_vol": ret_score - 0.5 * vol,
                "return_minus_vol": ret_score - vol,
            }
            for score_mode in score_modes:
                base_raw, diff = _raw_from_score(score_map[score_mode])
                for trend_window in trend_windows:
                    raw = _apply_trend_to_raw(prices, base_raw, trend_window)
                    trend_label = "" if trend_window == 0 else f", chosen/alternate above SMA{trend_window}"
                    for hysteresis in hysteresis_levels:
                        hyst_label = "" if hysteresis == 0 else f", {hysteresis:.0%} hysteresis"
                        for rebalance in rebalances:
                            for stop_pct in stop_levels:
                                skip_label = "" if skip == 0 else f", skip {skip}d"
                                stop_label = "" if stop_pct is None else f", switch on {stop_pct:.0%} stop"
                                add_candidate(
                                    "Relative momentum rotation",
                                    f"{lookback}d {score_mode}{skip_label}{trend_label}{hyst_label}{stop_label}",
                                    rebalance,
                                    raw,
                                    diff,
                                    stop_pct,
                                    "Always invested in SOXL or TQQQ; signal uses prior-close data; no costs/slippage.",
                                )

    # Pullback variants: use long momentum as a regime, but buy the shorter-term laggard.
    for long_lb in [42, 63, 84, 126, 168, 252]:
        long_score, _ = _score_arrays(prices, long_lb, 0)
        leader, leader_diff = _raw_from_score(long_score)
        for short_lb in [3, 5, 10, 21]:
            short_score, _ = _score_arrays(prices, short_lb, 0)
            short_diff = short_score[:, 0] - short_score[:, 1]
            pullback = np.where(short_diff <= 0, 0, 1).astype(np.int8)
            pullback[~np.isfinite(short_diff)] = -1
            for require_sma100 in [False, True]:
                raw = leader.copy()
                sma100 = pd.DataFrame(prices).rolling(100).mean().to_numpy()
                trend_ok = prices > sma100
                for i in range(len(raw)):
                    pick = int(pullback[i])
                    if pick < 0:
                        continue
                    if require_sma100:
                        if trend_ok[i, pick] and long_score[i, pick] > 0:
                            raw[i] = pick
                    elif long_score[i, pick] > 0:
                        raw[i] = pick
                trend_label = ", pullback asset above SMA100 and positive long momentum" if require_sma100 else ", pullback asset positive long momentum"
                for rebalance in ["daily", "weekly"]:
                    for stop_pct in [None, 0.10, 0.20]:
                        stop_label = "" if stop_pct is None else f", switch on {stop_pct:.0%} stop"
                        add_candidate(
                            "Momentum pullback rotation",
                            f"{long_lb}d leader fallback, buy weaker {short_lb}d pullback{trend_label}{stop_label}",
                            rebalance,
                            raw,
                            leader_diff,
                            stop_pct,
                            "Mean-reversion entry inside a longer momentum framework; prior-close signal; no costs/slippage.",
                        )

    for lookback_set in [(21, 63, 126), (42, 84, 168), (63, 126, 252), (10, 21, 63, 126)]:
        votes = np.zeros(len(close), dtype=float)
        diff_sum = np.zeros(len(close), dtype=float)
        for lookback in lookback_set:
            score, _ = _score_arrays(prices, lookback, 0)
            diff = score[:, 0] - score[:, 1]
            votes += np.where(diff >= 0, 1, 0)
            diff_sum += np.where(np.isfinite(diff), diff, 0)
        raw = np.where(votes >= (len(lookback_set) / 2), 0, 1).astype(np.int8)
        raw[: max(lookback_set)] = -1
        for trend_window in [0, 100, 200]:
            selected = _apply_trend_to_raw(prices, raw, trend_window)
            trend_label = "" if trend_window == 0 else f", chosen/alternate above SMA{trend_window}"
            for rebalance in rebalances:
                for stop_pct in stop_levels:
                    stop_label = "" if stop_pct is None else f", switch on {stop_pct:.0%} stop"
                    add_candidate(
                        "Multi-lookback vote rotation",
                        f"Vote {lookback_set}{trend_label}{stop_label}",
                        rebalance,
                        selected,
                        diff_sum,
                        stop_pct,
                        "SOXL/TQQQ chosen by majority of relative momentum windows; no costs/slippage.",
                    )

    if best_equity is None or best_allocation is None:
        raise RuntimeError("No valid variants were evaluated.")
    _fast_write_outputs(rows, best_equity, best_allocation, close, baseline_equity)


def parse_stop(variant: str) -> float | None:
    for pct in [10, 15, 20, 30]:
        if f"switch on {pct}% stop" in variant:
            return pct / 100
    return None


def recompute_variant(close: pd.DataFrame, family: str, variant: str, rebalance: str) -> tuple[pd.Series, pd.Series, pd.Series]:
    stop_pct = parse_stop(variant)
    if family == "Relative momentum rotation":
        lookback = int(variant.split("d ", 1)[0])
        skip = 0
        if "skip " in variant:
            skip = int(variant.split("skip ", 1)[1].split("d", 1)[0])
        score_mode = variant.split("d ", 1)[1].split(",", 1)[0]
        score_return = total_return_score(close, lookback, skip)
        vol = volatility_score(close, max(lookback, 10), skip)
        if score_mode == "return":
            score = score_return
        elif score_mode == "return_over_vol":
            score = score_return / vol.replace(0, np.nan)
        elif score_mode == "return_minus_half_vol":
            score = score_return - 0.5 * vol
        elif score_mode == "return_minus_vol":
            score = score_return - vol
        elif score_mode == "return control":
            score = score_return
        else:
            raise ValueError(f"Cannot recompute score mode: {score_mode}")
        raw, diff = choose_from_scores(score)
        for tw in [50, 100, 150, 200]:
            if f"SMA{tw}" in variant:
                trend_ok = close > close.rolling(tw).mean()
                other = pd.Series(np.where(raw == "SOXL", "TQQQ", "SOXL"), index=raw.index)
                raw = pd.Series(
                    [pick if bool(trend_ok.loc[ts, pick]) else alt if bool(trend_ok.loc[ts, alt]) else pick for ts, pick, alt in zip(raw.index, raw, other)],
                    index=raw.index,
                )
                break
        hysteresis = 0.0
        for pct in [1, 2, 5, 10]:
            if f"{pct}% hysteresis" in variant:
                hysteresis = pct / 100
                break
        selected = apply_hysteresis(raw.dropna(), diff.reindex(raw.index).fillna(0), hysteresis)
        return backtest_allocation(close, selected, rebalance=rebalance, stop_pct=stop_pct)

    if family == "Multi-lookback vote rotation":
        lookbacks = tuple(int(part.strip()) for part in variant.split("(", 1)[1].split(")", 1)[0].split(","))
        votes = [(total_return_score(close, lookback, 0)["SOXL"] >= total_return_score(close, lookback, 0)["TQQQ"]).astype(int) for lookback in lookbacks]
        raw = pd.Series(np.where(sum(votes) >= (len(lookbacks) / 2), "SOXL", "TQQQ"), index=close.index)
        for tw in [100, 200]:
            if f"SMA{tw}" in variant:
                trend_ok = close > close.rolling(tw).mean()
                other = pd.Series(np.where(raw == "SOXL", "TQQQ", "SOXL"), index=raw.index)
                raw = pd.Series(
                    [pick if bool(trend_ok.loc[ts, pick]) else alt if bool(trend_ok.loc[ts, alt]) else pick for ts, pick, alt in zip(raw.index, raw, other)],
                    index=raw.index,
                )
        return backtest_allocation(close, raw.dropna(), rebalance=rebalance, stop_pct=stop_pct)

    if family == "Momentum pullback rotation":
        long_lb = int(variant.split("d leader", 1)[0])
        short_lb = int(variant.split("weaker ", 1)[1].split("d", 1)[0])
        long_score = total_return_score(close, long_lb, 0)
        long_choice, _ = choose_from_scores(long_score)
        short_score = total_return_score(close, short_lb, 0)
        pullback_choice = pd.Series(np.where(short_score["SOXL"] <= short_score["TQQQ"], "SOXL", "TQQQ"), index=close.index)
        if "SMA100" in variant:
            trend = close > close.rolling(100).mean()
            raw = pd.Series(
                [pull if bool(trend.loc[ts, pull]) and bool(long_score.loc[ts, pull] > 0) else lead for ts, pull, lead in zip(close.index, pullback_choice, long_choice)],
                index=close.index,
            )
        else:
            raw = pd.Series(
                [pull if bool(long_score.loc[ts, pull] > 0) else lead for ts, pull, lead in zip(close.index, pullback_choice, long_choice)],
                index=close.index,
            )
        return backtest_allocation(close, raw.dropna(), rebalance=rebalance, stop_pct=stop_pct)

    raise ValueError(f"Cannot recompute family: {family}")


if __name__ == "__main__":
    fast_run()
