from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pandas as pd

from src.strategy_lab.compare_universe_topn_monthly import is_month_end_signal
from src.strategy_lab.sp500_top5 import load_or_fetch_prices, momentum_scores


@dataclass(frozen=True)
class MembershipResult:
    top_n: int
    buy_events: int
    unique_tickers: int
    passed: int
    violations: int
    unknown: int


def pct(value: float) -> str:
    return f"{value:.2%}"


def load_membership_table(path: Path) -> pd.DataFrame:
    members = pd.read_csv(path)
    members["Date added parsed"] = pd.to_datetime(members["Date added"], errors="coerce").dt.date
    return members[
        [
            "Yahoo Symbol",
            "Symbol",
            "Security",
            "GICS Sector",
            "Date added",
            "Date added parsed",
        ]
    ].rename(
        columns={
            "Yahoo Symbol": "ticker",
            "Symbol": "sp500_symbol",
            "Security": "security",
            "GICS Sector": "sector",
            "Date added": "sp500_date_added",
            "Date added parsed": "sp500_date_added_parsed",
        }
    )


def run_buy_log(prices: pd.DataFrame, start: date, end: date, top_n: int) -> list[dict[str, object]]:
    close = prices["Close"].dropna(axis=1, thresh=128).sort_index()
    open_prices = prices["Open"].reindex(columns=close.columns).sort_index()
    close = close.loc[(close.index.date >= start) | (close.index < pd.Timestamp(start))]
    close = close.loc[close.index.date <= end]
    open_prices = open_prices.reindex(index=close.index)

    holdings = pd.Series(dtype=float)
    equity = 1.0
    rows: list[dict[str, object]] = []

    for signal_index in range(126, len(close) - 2):
        entry_index = signal_index + 1
        exit_index = signal_index + 2
        signal_date = close.index[signal_index].date()
        trade_date = close.index[entry_index].date()
        if trade_date < start or trade_date > end:
            continue

        if is_month_end_signal(signal_index, close.index, holdings):
            scores = momentum_scores(close, signal_index, 126, score_mode="skip", skip_days=21)
            selected = scores.head(top_n)
            next_holdings = pd.Series(1.0 / top_n, index=selected.index, dtype=float)
            old = set(holdings.index)

            for rank, ticker in enumerate(selected.index, start=1):
                if ticker in old:
                    continue
                rows.append(
                    {
                        "top_n": top_n,
                        "signal_date": signal_date.isoformat(),
                        "purchase_date": trade_date.isoformat(),
                        "ticker": ticker,
                        "rank": rank,
                        "score": float(selected[ticker]),
                        "purchase_open": float(open_prices.iloc[entry_index][ticker]),
                        "new_weight": float(next_holdings[ticker]),
                        "equity_before_trade": equity,
                    }
                )

            holdings = next_holdings

        one_day_returns = open_prices.iloc[exit_index] / open_prices.iloc[entry_index] - 1.0
        daily_return = 0.0
        for ticker, weight in holdings.items():
            value = one_day_returns.get(ticker)
            if pd.notna(value):
                daily_return += float(weight) * float(value)
        equity *= 1.0 + daily_return

    return rows


def add_membership_validation(buys: pd.DataFrame, membership: pd.DataFrame) -> pd.DataFrame:
    validated = buys.merge(membership, how="left", on="ticker")
    purchase_dates = pd.to_datetime(validated["purchase_date"]).dt.date

    statuses: list[str] = []
    days_before_added: list[object] = []
    for purchase_date, date_added in zip(purchase_dates, validated["sp500_date_added_parsed"]):
        if pd.isna(date_added):
            statuses.append("UNKNOWN_DATE_ADDED")
            days_before_added.append("")
            continue
        if purchase_date >= date_added:
            statuses.append("PASS")
            days_before_added.append(0)
            continue
        statuses.append("VIOLATION_BUY_BEFORE_SP500_ADDED")
        days_before_added.append((date_added - purchase_date).days)

    validated["membership_status"] = statuses
    validated["days_before_sp500_added"] = days_before_added
    columns = [
        "top_n",
        "signal_date",
        "purchase_date",
        "ticker",
        "security",
        "sector",
        "sp500_date_added",
        "membership_status",
        "days_before_sp500_added",
        "rank",
        "score",
        "purchase_open",
        "new_weight",
        "equity_before_trade",
    ]
    return validated[columns].sort_values(["top_n", "purchase_date", "rank", "ticker"])


def build_ticker_summary(validated: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    grouped = validated.groupby("ticker", sort=True)
    for ticker, frame in grouped:
        first_purchase = frame["purchase_date"].min()
        worst_status = (
            "VIOLATION_BUY_BEFORE_SP500_ADDED"
            if (frame["membership_status"] == "VIOLATION_BUY_BEFORE_SP500_ADDED").any()
            else ("UNKNOWN_DATE_ADDED" if (frame["membership_status"] == "UNKNOWN_DATE_ADDED").any() else "PASS")
        )
        rows.append(
            {
                "ticker": ticker,
                "security": frame["security"].dropna().iloc[0] if frame["security"].notna().any() else "",
                "sector": frame["sector"].dropna().iloc[0] if frame["sector"].notna().any() else "",
                "sp500_date_added": frame["sp500_date_added"].dropna().iloc[0]
                if frame["sp500_date_added"].notna().any()
                else "",
                "first_purchase_date": first_purchase,
                "last_purchase_date": frame["purchase_date"].max(),
                "buy_events": len(frame),
                "top_n_variants": ", ".join(str(value) for value in sorted(frame["top_n"].unique())),
                "membership_status": worst_status,
                "max_days_before_sp500_added": frame.loc[
                    frame["days_before_sp500_added"] != "", "days_before_sp500_added"
                ].max()
                if (frame["days_before_sp500_added"] != "").any()
                else "",
            }
        )
    return pd.DataFrame(rows).sort_values(["membership_status", "ticker"])


def build_result_rows(validated: pd.DataFrame) -> list[MembershipResult]:
    rows: list[MembershipResult] = []
    for top_n, frame in validated.groupby("top_n", sort=True):
        rows.append(
            MembershipResult(
                top_n=int(top_n),
                buy_events=len(frame),
                unique_tickers=frame["ticker"].nunique(),
                passed=int((frame["membership_status"] == "PASS").sum()),
                violations=int((frame["membership_status"] == "VIOLATION_BUY_BEFORE_SP500_ADDED").sum()),
                unknown=int((frame["membership_status"] == "UNKNOWN_DATE_ADDED").sum()),
            )
        )
    return rows


def main() -> None:
    start = date(2020, 1, 1)
    end = date(2026, 5, 17)
    data_start = date(2018, 12, 19)
    data_dir = Path("data/sp500_top5")
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    membership = load_membership_table(data_dir / "sp500_constituents.csv")
    tickers = membership["ticker"].dropna().astype(str).tolist()
    prices = load_or_fetch_prices(
        data_dir / f"adjusted_open_close_{data_start.isoformat()}_{end.isoformat()}.csv",
        tickers,
        data_start,
        end,
        False,
    )

    buy_rows: list[dict[str, object]] = []
    for top_n in [1, 2, 3]:
        buy_rows.extend(run_buy_log(prices, start, end, top_n))

    buys = pd.DataFrame(buy_rows)
    validated = add_membership_validation(buys, membership)
    ticker_summary = build_ticker_summary(validated)
    violations = validated[validated["membership_status"] == "VIOLATION_BUY_BEFORE_SP500_ADDED"]
    result_rows = build_result_rows(validated)

    base = "sp500_membership_validation_top1_top2_top3_monthly_o2o_2020_2026ytd"
    csv_path = report_dir / f"{base}.csv"
    summary_csv_path = report_dir / f"{base}_ticker_summary.csv"
    violations_csv_path = report_dir / f"{base}_violations.csv"
    xlsx_path = report_dir / f"{base}.xlsx"
    md_path = report_dir / f"{base}.md"

    validated.to_csv(csv_path, index=False)
    ticker_summary.to_csv(summary_csv_path, index=False)
    violations.to_csv(violations_csv_path, index=False)
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        validated.to_excel(writer, sheet_name="Buy validation", index=False)
        ticker_summary.to_excel(writer, sheet_name="Ticker summary", index=False)
        violations.to_excel(writer, sheet_name="Violations", index=False)

    lines = [
        "# S&P 500 Membership Validation for Strategy Buys",
        "",
        f"Strategy checked: S&P 500 Top1/Top2/Top3 monthly skip-momentum, 126 trading-day lookback, skip latest 21 trading days, open-to-open execution.",
        f"Period checked: {start.isoformat()} through {end.isoformat()}.",
        "Membership source: local cached current S&P 500 constituents table, using the `Date added` column.",
        "",
        "| Top N | Buy events | Unique tickers | Pass | Violations | Unknown date |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in result_rows:
        lines.append(
            f"| {row.top_n} | {row.buy_events} | {row.unique_tickers} | {row.passed} | {row.violations} | {row.unknown} |"
        )
    lines.extend(
        [
            "",
            "A violation means the simulated purchase date is earlier than the stock's S&P 500 `Date added` value.",
            "This confirms index-membership lookahead bias whenever violations are present.",
            "",
            "## Violation Ticker Summary",
            "",
            "| Ticker | Security | S&P 500 Date Added | First Purchase | Buy Events | Top N Variants | Max Days Early |",
            "| --- | --- | --- | --- | ---: | --- | ---: |",
        ]
    )
    violation_summary = ticker_summary[
        ticker_summary["membership_status"] == "VIOLATION_BUY_BEFORE_SP500_ADDED"
    ].sort_values(["first_purchase_date", "ticker"])
    for _, row in violation_summary.iterrows():
        lines.append(
            "| "
            f"{row['ticker']} | {row['security']} | {row['sp500_date_added']} | "
            f"{row['first_purchase_date']} | {row['buy_events']} | {row['top_n_variants']} | "
            f"{row['max_days_before_sp500_added']} |"
        )
    lines.extend(
        [
            "",
            "## Output Files",
            "",
            f"- Buy-level validation CSV: `{csv_path}`",
            f"- Ticker summary CSV: `{summary_csv_path}`",
            f"- Violations-only CSV: `{violations_csv_path}`",
            f"- Excel workbook: `{xlsx_path}`",
            "",
            "Important limitation: this check uses the current constituent table's `Date added` field. A full institutional-quality test still needs a point-in-time S&P 500 membership history, including removals and re-additions.",
            "",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")

    print(md_path)
    for row in result_rows:
        print(
            f"top{row.top_n}: buys={row.buy_events}, unique={row.unique_tickers}, "
            f"pass={row.passed}, violations={row.violations}, unknown={row.unknown}"
        )
    print(f"violation_tickers={violation_summary['ticker'].nunique()}")


if __name__ == "__main__":
    main()
