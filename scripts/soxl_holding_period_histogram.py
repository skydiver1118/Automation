from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf


START = "2018-01-09"
END_EXCLUSIVE = "2026-05-20"
LOOKBACK_BARS = 63
OUT_DIR = Path("reports")


def fetch_close() -> pd.DataFrame:
    data = yf.download(
        ["SOXL", "SMH"],
        start=START,
        end=END_EXCLUSIVE,
        interval="1d",
        auto_adjust=True,
        prepost=False,
        progress=False,
        threads=False,
    )
    close = data["Close"].dropna()
    close.index = pd.to_datetime(close.index).tz_localize(None)
    return close


def codex_soxl_state(close: pd.DataFrame) -> pd.Series:
    selected = 0
    last_month_key = ""
    states: list[int] = []

    for candle_index, ts in enumerate(close.index):
        month_key = ts.strftime("%Y-%m")
        previous_index = candle_index - 1

        if month_key != last_month_key and previous_index >= LOOKBACK_BARS:
            soxl_score = (
                close["SOXL"].iloc[previous_index]
                / close["SOXL"].iloc[previous_index - LOOKBACK_BARS]
                - 1
            )
            smh_score = (
                close["SMH"].iloc[previous_index]
                / close["SMH"].iloc[previous_index - LOOKBACK_BARS]
                - 1
            )
            selected = int(soxl_score > 0 and soxl_score > smh_score)

        last_month_key = month_key
        states.append(selected)

    return pd.Series(states, index=close.index, name="soxl_selected")


def continuous_trades(close: pd.DataFrame, state: pd.Series) -> pd.DataFrame:
    entries = state.eq(1) & state.shift(1, fill_value=0).ne(1)
    exits = state.ne(1) & state.shift(1, fill_value=0).eq(1)

    trades: list[dict[str, object]] = []
    in_trade = False
    entry_date: pd.Timestamp | None = None
    entry_index = 0
    entry_price = 0.0

    for candle_index, ts in enumerate(close.index):
        if not in_trade and bool(entries.loc[ts]):
            in_trade = True
            entry_date = ts
            entry_index = candle_index
            entry_price = float(close.loc[ts, "SOXL"])
            continue

        if in_trade and bool(exits.loc[ts]):
            exit_price = float(close.loc[ts, "SOXL"])
            assert entry_date is not None
            trades.append(
                {
                    "entry_date": entry_date.date().isoformat(),
                    "exit_date": ts.date().isoformat(),
                    "trading_days": candle_index - entry_index + 1,
                    "calendar_days": (ts - entry_date).days + 1,
                    "return_pct": (exit_price / entry_price - 1) * 100,
                }
            )
            in_trade = False

    if in_trade and entry_date is not None:
        ts = close.index[-1]
        exit_price = float(close.loc[ts, "SOXL"])
        trades.append(
            {
                "entry_date": entry_date.date().isoformat(),
                "exit_date": ts.date().isoformat(),
                "trading_days": len(close) - entry_index,
                "calendar_days": (ts - entry_date).days + 1,
                "return_pct": (exit_price / entry_price - 1) * 100,
            }
        )

    return pd.DataFrame(trades)


def monthly_selected_slots(close: pd.DataFrame, state: pd.Series) -> pd.DataFrame:
    first_trading_days = close.groupby(close.index.to_period("M")).head(1).index
    rows: list[dict[str, object]] = []

    for slot_index, ts in enumerate(first_trading_days):
        if int(state.loc[ts]) != 1:
            continue
        exit_date = (
            first_trading_days[slot_index + 1]
            if slot_index + 1 < len(first_trading_days)
            else close.index[-1]
        )
        entry_pos = close.index.get_loc(ts)
        exit_pos = close.index.get_loc(exit_date)
        rows.append(
            {
                "entry_date": ts.date().isoformat(),
                "exit_date": exit_date.date().isoformat(),
                "trading_days": int(exit_pos - entry_pos + 1),
                "calendar_days": int((exit_date - ts).days + 1),
            }
        )

    return pd.DataFrame(rows)


def save_histogram(
    data: pd.DataFrame,
    output_path: Path,
    title: str,
    subtitle: str,
    bins: list[int],
) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.6), dpi=180)
    values = data["calendar_days"]
    ax.hist(values, bins=bins, color="#2563eb", edgecolor="white", linewidth=1.2)
    ax.axvline(values.median(), color="#f59e0b", linewidth=2, label=f"Median: {values.median():.0f} days")
    ax.axvline(values.mean(), color="#16a34a", linewidth=2, linestyle="--", label=f"Mean: {values.mean():.1f} days")
    ax.set_title(title, loc="left", fontsize=15, pad=12)
    ax.text(0, 1.01, subtitle, transform=ax.transAxes, fontsize=9, color="#4b5563")
    ax.set_xlabel("Calendar days in trade")
    ax.set_ylabel("Number of trades")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output_path, bbox_inches="tight")
    plt.close(fig)


def markdown_summary(trades: pd.DataFrame, monthly_slots: pd.DataFrame) -> str:
    bins = [0, 30, 60, 90, 120, 150, 180, 240, 300, 360]
    labels = ["0-30", "31-60", "61-90", "91-120", "121-150", "151-180", "181-240", "241-300", "301-360"]
    bucketed = pd.cut(trades["calendar_days"], bins=bins, labels=labels, include_lowest=True)
    bucket_counts = bucketed.value_counts().sort_index()
    bucket_rows = "\n".join(f"| {bucket} | {int(count)} |" for bucket, count in bucket_counts.items())

    return f"""# Codex SOXL Holding Period Histogram

Source-aligned reconstruction of the saved TrendSpider strategy `Codex SOXL`.

- Symbol: SOXL
- Comparator: SMH
- Signal: 63-trading-day relative strength, evaluated on the first trading day of each month using the prior daily close
- Test window: {START} to 2026-05-19
- Continuous entry-to-exit trades: {len(trades)}
- Monthly SOXL-selected rebalance slots: {len(monthly_slots)}

![Continuous SOXL trade holding-period histogram](codex_soxl_holding_period_histogram.png)

## Continuous Trade Buckets

| Calendar days in trade | Trades |
| --- | ---: |
{bucket_rows}

## Continuous Trade Summary

| Metric | Value |
| --- | ---: |
| Trades | {len(trades)} |
| Min calendar days | {int(trades["calendar_days"].min())} |
| Median calendar days | {trades["calendar_days"].median():.0f} |
| Mean calendar days | {trades["calendar_days"].mean():.1f} |
| Max calendar days | {int(trades["calendar_days"].max())} |
| Median trading days | {trades["trading_days"].median():.0f} |

## Monthly Rebalance-Slot Check

This secondary view counts each SOXL-selected monthly rebalance slot separately. It is useful because TrendSpider's visible tester count appears closer to per-signal/monthly accounting than to continuous entry-to-exit rotations.

![Monthly SOXL-selected slot holding-period histogram](codex_soxl_monthly_slot_holding_period_histogram.png)
"""


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    close = fetch_close()
    state = codex_soxl_state(close)
    trades = continuous_trades(close, state)
    monthly_slots = monthly_selected_slots(close, state)

    trades.to_csv(OUT_DIR / "codex_soxl_holding_period_trades.csv", index=False)
    monthly_slots.to_csv(OUT_DIR / "codex_soxl_monthly_selected_slots.csv", index=False)

    save_histogram(
        trades,
        OUT_DIR / "codex_soxl_holding_period_histogram.png",
        "Codex SOXL: Continuous Trade Holding Periods",
        f"{len(trades)} entry-to-exit SOXL trades, {START} to 2026-05-19",
        bins=[0, 30, 60, 90, 120, 150, 180, 240, 300, 360],
    )
    save_histogram(
        monthly_slots,
        OUT_DIR / "codex_soxl_monthly_slot_holding_period_histogram.png",
        "Codex SOXL: Monthly SOXL-Selected Slots",
        f"{len(monthly_slots)} selected monthly rebalance slots, {START} to 2026-05-19",
        bins=[15, 20, 25, 30, 35, 40],
    )
    (OUT_DIR / "codex_soxl_holding_period_histogram.md").write_text(
        markdown_summary(trades, monthly_slots),
        encoding="utf-8",
    )

    print(f"continuous_trades={len(trades)}")
    print(f"monthly_selected_slots={len(monthly_slots)}")
    print(f"median_calendar_days={trades['calendar_days'].median():.0f}")
    print(f"mean_calendar_days={trades['calendar_days'].mean():.1f}")
    print(f"max_calendar_days={int(trades['calendar_days'].max())}")
    print(f"wrote={OUT_DIR / 'codex_soxl_holding_period_histogram.png'}")


if __name__ == "__main__":
    main()
