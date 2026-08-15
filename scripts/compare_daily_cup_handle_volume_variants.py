from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.cup_handle_rotation_backtest import benchmark_equity, markdown_table, summary_metrics  # noqa: E402


INITIAL_CAPITAL = 100000.0
IS_START = "2010-01-01"
IS_END = "2020-01-01"
OOS_START = "2020-01-01"
OOS_END = "2026-05-30"
OOS_END_EXCLUSIVE = "2026-05-31"


def metric_from_equity(path: Path, start: str, end: str, trades_path: Path) -> dict[str, object]:
    equity = pd.read_csv(path)
    equity_series = equity.set_index(pd.to_datetime(equity["Date"]))["Equity"].astype(float)
    mask = (equity_series.index >= pd.Timestamp(start)) & (equity_series.index < pd.Timestamp(end))
    trades = pd.read_csv(trades_path) if trades_path.exists() else pd.DataFrame()
    if not trades.empty:
        entry_dates = pd.to_datetime(trades["EntryDate"])
        trades = trades[(entry_dates >= pd.Timestamp(start)) & (entry_dates < pd.Timestamp(end))]
    return summary_metrics(equity_series[mask], trades)


def add_sp500_deltas(frame: pd.DataFrame, bench_is: dict[str, object], bench_oos: dict[str, object]) -> pd.DataFrame:
    frame = frame.copy()
    frame["IS_Return_vs_SP500_PctPts"] = (frame["IS_TotalReturnPct"] - bench_is["total_return_pct"]).round(2)
    frame["IS_Sharpe_vs_SP500"] = (frame["IS_Sharpe"] - bench_is["sharpe"]).round(3)
    frame["OOS_Return_vs_SP500_PctPts"] = (frame["OOS_TotalReturnPct"] - bench_oos["total_return_pct"]).round(2)
    frame["OOS_Sharpe_vs_SP500"] = (frame["OOS_Sharpe"] - bench_oos["sharpe"]).round(3)
    return frame


def row_from_metrics(family: str, selection: str, variant: str, is_metrics: dict[str, object], oos_metrics: dict[str, object]) -> dict[str, object]:
    return {
        "Family": family,
        "Selection": selection,
        "Variant": variant,
        "IS_TotalReturnPct": is_metrics.get("total_return_pct"),
        "IS_Sharpe": is_metrics.get("sharpe"),
        "IS_Trades": is_metrics.get("trade_count"),
        "OOS_TotalReturnPct": oos_metrics.get("total_return_pct"),
        "OOS_Sharpe": oos_metrics.get("sharpe"),
        "OOS_Trades": oos_metrics.get("trade_count"),
    }


def selected_rows_from_rankings(path: Path, family: str) -> list[dict[str, object]]:
    rankings = pd.read_csv(path)
    best_is = rankings.sort_values(["TotalReturnPct_IS", "Sharpe_IS"], ascending=[False, False]).iloc[0]
    best_oos = rankings.sort_values(["TotalReturnPct_OOS", "Sharpe_OOS"], ascending=[False, False]).iloc[0]

    def make(selection: str, row: pd.Series) -> dict[str, object]:
        return {
            "Family": family,
            "Selection": selection,
            "Variant": row["Variant"],
            "IS_TotalReturnPct": row["TotalReturnPct_IS"],
            "IS_Sharpe": row["Sharpe_IS"],
            "IS_Trades": row["Trades_IS"],
            "OOS_TotalReturnPct": row["TotalReturnPct_OOS"],
            "OOS_Sharpe": row["Sharpe_OOS"],
            "OOS_Trades": row["Trades_OOS"],
        }

    return [make("Best by IS return", best_is), make("Best by OOS return", best_oos)]


def all_variant_rows(path: Path, family: str) -> pd.DataFrame:
    rankings = pd.read_csv(path)
    return pd.DataFrame(
        {
            "Family": family,
            "Variant": rankings["Variant"],
            "IS_TotalReturnPct": rankings["TotalReturnPct_IS"],
            "IS_Sharpe": rankings["Sharpe_IS"],
            "IS_Trades": rankings["Trades_IS"],
            "OOS_TotalReturnPct": rankings["TotalReturnPct_OOS"],
            "OOS_Sharpe": rankings["Sharpe_OOS"],
            "OOS_Trades": rankings["Trades_OOS"],
        }
    )


def main() -> None:
    output_dir = Path("reports/cup_handle_daily_volume_3stock_comparison")
    output_dir.mkdir(parents=True, exist_ok=True)

    bench_is = summary_metrics(benchmark_equity(IS_START, IS_END, INITIAL_CAPITAL), pd.DataFrame())
    bench_oos = summary_metrics(benchmark_equity(OOS_START, OOS_END_EXCLUSIVE, INITIAL_CAPITAL), pd.DataFrame())

    base_dir = Path("reports/cup_handle_daily_rotation_backtest_volume_top10")
    base_is = metric_from_equity(base_dir / "cup_handle_rotation_equity.csv", IS_START, IS_END, base_dir / "cup_handle_rotation_trades.csv")
    base_oos = metric_from_equity(base_dir / "cup_handle_rotation_equity.csv", OOS_START, OOS_END_EXCLUSIVE, base_dir / "cup_handle_rotation_trades.csv")

    rows = [
        row_from_metrics("Base 3-stock rotation", "Single rule", "daily pattern + volume gates", base_is, base_oos)
    ]
    trend_path = Path("reports/cup_handle_daily_trend_filter_variants_volume_top10/cup_handle_trend_filter_variant_rankings.csv")
    atr_path = Path("reports/cup_handle_daily_atr_exit_variants_volume_top10_rs_sma100/cup_handle_atr_exit_variant_rankings.csv")
    rows.extend(selected_rows_from_rankings(trend_path, "Trend filters"))
    rows.extend(selected_rows_from_rankings(atr_path, "ATR exits"))

    entry = pd.read_csv("reports/cup_handle_daily_entry_window_test_volume_top10/entry_window_results.csv")
    entry_is = entry.sort_values(["IS_TotalReturnPct", "IS_Sharpe"], ascending=[False, False]).iloc[0]
    entry_oos = entry.sort_values(["OOS_TotalReturnPct", "OOS_Sharpe"], ascending=[False, False]).iloc[0]
    for selection, item in [("Best by IS return", entry_is), ("Best by OOS return", entry_oos)]:
        rows.append(
            {
                "Family": "Entry window 3-10 days",
                "Selection": selection,
                "Variant": f"{int(item['EntryWindowTradingDays'])} trading days",
                "IS_TotalReturnPct": item["IS_TotalReturnPct"],
                "IS_Sharpe": item["IS_Sharpe"],
                "IS_Trades": item["IS_Trades"],
                "OOS_TotalReturnPct": item["OOS_TotalReturnPct"],
                "OOS_Sharpe": item["OOS_Sharpe"],
                "OOS_Trades": item["OOS_Trades"],
            }
        )

    summary = add_sp500_deltas(pd.DataFrame(rows), bench_is, bench_oos)
    summary.to_csv(output_dir / "daily_volume_3stock_summary.csv", index=False)

    all_variants = pd.concat(
        [
            all_variant_rows(trend_path, "Trend filters"),
            all_variant_rows(atr_path, "ATR exits"),
            pd.DataFrame(
                {
                    "Family": "Entry window 3-10 days",
                    "Variant": entry["EntryWindowTradingDays"].map(lambda value: f"{int(value)} trading days"),
                    "IS_TotalReturnPct": entry["IS_TotalReturnPct"],
                    "IS_Sharpe": entry["IS_Sharpe"],
                    "IS_Trades": entry["IS_Trades"],
                    "OOS_TotalReturnPct": entry["OOS_TotalReturnPct"],
                    "OOS_Sharpe": entry["OOS_Sharpe"],
                    "OOS_Trades": entry["OOS_Trades"],
                }
            ),
        ],
        ignore_index=True,
    )
    all_variants = add_sp500_deltas(all_variants, bench_is, bench_oos)
    all_variants.to_csv(output_dir / "daily_volume_all_variant_results.csv", index=False)

    signal_count = len(pd.read_csv(base_dir / "cup_handle_daily_rotation_signals.csv"))
    lines = [
        "# Daily Cup-And-Handle Volume 3-Stock Rerun",
        "",
        "This is technical strategy research, not investment advice.",
        "",
        "## Setup",
        "",
        "- Pattern timeframe: daily candles, scanned every 5 trading days for historical runtime control.",
        "- Daily pattern volume gate: handle average volume <= `1.05x` cup average volume for formed patterns.",
        "- Entry volume gate: breakout-day daily volume >= `1.40x` prior 50-trading-day average volume.",
        "- Candidate pool: top 10 daily-pattern scores per scan date after `TargetReturnPct > 30%`.",
        "- Portfolio: maximum 3 concurrent stocks.",
        f"- Signals generated: `{signal_count}`.",
        f"- IS: `{IS_START}` to `{IS_END}`; OOS: `{OOS_START}` to `{OOS_END}`.",
        "",
        "## S&P 500 Benchmark",
        "",
        "| Segment | Total Return % | Sharpe |",
        "| --- | ---: | ---: |",
        f"| IS | {bench_is['total_return_pct']} | {bench_is['sharpe']} |",
        f"| OOS | {bench_oos['total_return_pct']} | {bench_oos['sharpe']} |",
        "",
        "## Comparison Summary",
        "",
        markdown_table(summary),
        "",
        "## Files",
        "",
        "- `daily_volume_3stock_summary.csv`",
        "- `daily_volume_all_variant_results.csv`",
    ]
    (output_dir / "daily_volume_3stock_comparison.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"summary={output_dir / 'daily_volume_3stock_summary.csv'}")
    print(f"all_variants={output_dir / 'daily_volume_all_variant_results.csv'}")
    print(f"report={output_dir / 'daily_volume_3stock_comparison.md'}")


if __name__ == "__main__":
    main()
