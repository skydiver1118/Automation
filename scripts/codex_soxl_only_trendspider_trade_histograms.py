from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf


START = "2010-03-11"
END_EXCLUSIVE = "2026-05-21"
OUT_DIR = Path("reports")

TRENDSPIDER_VISIBLE = {
    "positions": 78,
    "net_perf_pct": 49269.5,
    "asset_perf_pct": 24358.6,
    "max_drawdown_pct": -65.5,
    "win_rate_pct": 45.0,
    "mean_trade_return_pct": 16.37,
}


def fetch_soxl_close() -> pd.Series:
    data = yf.download(
        "SOXL",
        start=START,
        end=END_EXCLUSIVE,
        interval="1d",
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [column[0] for column in data.columns]
    close = data["Close"].dropna()
    close.index = pd.to_datetime(close.index).tz_localize(None)
    return close


def trendspider_signal_trades(close: pd.Series) -> pd.DataFrame:
    fast_sma = close.rolling(50).mean()
    slow_sma = close.rolling(63).mean()

    in_position = False
    entry_price = np.nan
    entry_date: pd.Timestamp | None = None
    entry_index = 0
    rows: list[dict[str, object]] = []

    for candle_index, (ts, price) in enumerate(close.items()):
        trend_on = np.isfinite(fast_sma.iloc[candle_index]) and np.isfinite(slow_sma.iloc[candle_index]) and (
            fast_sma.iloc[candle_index] > slow_sma.iloc[candle_index]
        )

        if not in_position and trend_on:
            in_position = True
            entry_price = float(price)
            entry_date = ts
            entry_index = candle_index

        stop_hit = in_position and float(price) <= entry_price * 0.9
        trend_exit = in_position and not trend_on

        if stop_hit or trend_exit:
            assert entry_date is not None
            rows.append(
                {
                    "entry_date": entry_date.date().isoformat(),
                    "exit_date": ts.date().isoformat(),
                    "trading_days": candle_index - entry_index + 1,
                    "calendar_days": (ts - entry_date).days + 1,
                    "return_pct": (float(price) / entry_price - 1) * 100,
                    "exit_reason": "10% stop" if stop_hit else "SMA state exit",
                }
            )
            in_position = False
            entry_price = np.nan
            entry_date = None

    if in_position and entry_date is not None:
        ts = close.index[-1]
        price = float(close.iloc[-1])
        rows.append(
            {
                "entry_date": entry_date.date().isoformat(),
                "exit_date": ts.date().isoformat(),
                "trading_days": len(close) - entry_index,
                "calendar_days": (ts - entry_date).days + 1,
                "return_pct": (price / entry_price - 1) * 100,
                "exit_reason": "open at test end",
            }
        )

    return pd.DataFrame(rows)


def save_histograms(trades: pd.DataFrame, output_path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.4), dpi=180)

    hold = trades["calendar_days"]
    hold_bins = [0, 5, 10, 20, 30, 45, 60, 90, 120, 180, 270, 420]
    axes[0].hist(hold, bins=hold_bins, color="#2563eb", edgecolor="white", linewidth=1.0)
    axes[0].axvline(hold.median(), color="#f59e0b", linewidth=2, label=f"Median: {hold.median():.0f}d")
    axes[0].axvline(hold.mean(), color="#16a34a", linewidth=2, linestyle="--", label=f"Mean: {hold.mean():.1f}d")
    axes[0].set_title("Holding Period")
    axes[0].set_xlabel("Calendar days in trade")
    axes[0].set_ylabel("Number of trades")
    axes[0].grid(axis="y", alpha=0.25)
    axes[0].legend(frameon=False)

    returns = trades["return_pct"]
    return_bins = [-30, -20, -15, -10, -5, 0, 10, 25, 50, 100, 200, 320]
    axes[1].hist(returns, bins=return_bins, color="#7c3aed", edgecolor="white", linewidth=1.0)
    axes[1].axvline(0, color="#374151", linewidth=1.5)
    axes[1].axvline(returns.median(), color="#f59e0b", linewidth=2, label=f"Median: {returns.median():.1f}%")
    axes[1].axvline(returns.mean(), color="#16a34a", linewidth=2, linestyle="--", label=f"Mean: {returns.mean():.1f}%")
    axes[1].set_title("Return Per Trade")
    axes[1].set_xlabel("Trade return (%)")
    axes[1].set_ylabel("Number of trades")
    axes[1].grid(axis="y", alpha=0.25)
    axes[1].legend(frameon=False)

    fig.suptitle("Codex SOXL Only: TrendSpider-Rule Trade Histograms", x=0.03, y=1.02, ha="left", fontsize=16)
    fig.text(
        0.03,
        0.965,
        "SMA50/SMA63 state with 10% stop; reconstructed from saved TrendSpider indicator logic",
        fontsize=9,
        color="#4b5563",
    )
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def bucket_table(series: pd.Series, bins: list[float], labels: list[str]) -> pd.Series:
    bucketed = pd.cut(series, bins=bins, labels=labels, include_lowest=True)
    return bucketed.value_counts().sort_index()


def write_report(trades: pd.DataFrame, output_path: Path) -> None:
    hold_counts = bucket_table(
        trades["calendar_days"],
        [0, 5, 10, 20, 30, 45, 60, 90, 120, 180, 270, 420],
        ["0-5", "6-10", "11-20", "21-30", "31-45", "46-60", "61-90", "91-120", "121-180", "181-270", "271-420"],
    )
    return_counts = bucket_table(
        trades["return_pct"],
        [-30, -20, -15, -10, -5, 0, 10, 25, 50, 100, 200, 320],
        ["-30 to -20", "-20 to -15", "-15 to -10", "-10 to -5", "-5 to 0", "0 to 10", "10 to 25", "25 to 50", "50 to 100", "100 to 200", "200 to 320"],
    )

    hold_rows = "\n".join(f"| {bucket} | {int(count)} |" for bucket, count in hold_counts.items())
    return_rows = "\n".join(f"| {bucket} | {int(count)} |" for bucket, count in return_counts.items())

    wins = int((trades["return_pct"] > 0).sum())
    losses = int((trades["return_pct"] <= 0).sum())

    markdown = f"""# Codex SOXL Only: TrendSpider-Rule Trade Histograms

![Holding period and return histograms](codex_soxl_only_trendspider_holding_return_histograms.png)

This is a reconstruction from the saved TrendSpider indicator logic for `Codex SOXL Only Signals (50, 63, 10)`: SMA50/SMA63 state entry, exit on SMA state off or a 10% close-based stop. TrendSpider's visible Strategy Tester panel reported {TRENDSPIDER_VISIBLE["positions"]} positions; this reconstruction finds {len(trades)} trades from yfinance-adjusted SOXL data over the same displayed period, so treat the histograms as TrendSpider-rule-aligned rather than a raw TrendSpider trade export.

## Summary

| Metric | Reconstructed trades | TrendSpider visible aggregate |
| --- | ---: | ---: |
| Positions | {len(trades)} | {TRENDSPIDER_VISIBLE["positions"]} |
| Winners | {wins} | not individually exported |
| Losses | {losses} | not individually exported |
| Win rate | {(wins / len(trades) * 100):.2f}% | {TRENDSPIDER_VISIBLE["win_rate_pct"]:.2f}% |
| Mean return/trade | {trades["return_pct"].mean():.2f}% | {TRENDSPIDER_VISIBLE["mean_trade_return_pct"]:.2f}% |
| Median return/trade | {trades["return_pct"].median():.2f}% | not visible |
| Median holding period | {trades["calendar_days"].median():.0f} calendar days | not visible |
| Mean holding period | {trades["calendar_days"].mean():.1f} calendar days | not visible |
| Max holding period | {int(trades["calendar_days"].max())} calendar days | not visible |

## Holding Period Buckets

| Calendar days | Trades |
| --- | ---: |
{hold_rows}

## Return Buckets

| Return % | Trades |
| --- | ---: |
{return_rows}
"""

    output_path.write_text(markdown, encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    close = fetch_soxl_close()
    trades = trendspider_signal_trades(close)
    trades.to_csv(OUT_DIR / "codex_soxl_only_trendspider_trade_reconstruction.csv", index=False)
    save_histograms(trades, OUT_DIR / "codex_soxl_only_trendspider_holding_return_histograms.png")
    write_report(trades, OUT_DIR / "codex_soxl_only_trendspider_trade_histograms.md")

    print(f"trades={len(trades)}")
    print(f"wins={(trades['return_pct'] > 0).sum()}")
    print(f"losses={(trades['return_pct'] <= 0).sum()}")
    print(f"mean_return={trades['return_pct'].mean():.2f}")
    print(f"median_hold={trades['calendar_days'].median():.0f}")
    print(f"wrote={OUT_DIR / 'codex_soxl_only_trendspider_holding_return_histograms.png'}")


if __name__ == "__main__":
    main()
