from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(frozen=True)
class RoundTrip:
    ticker: str
    entry_date: pd.Timestamp
    entry_price: float
    exit_date: pd.Timestamp
    exit_price: float
    return_pct: float


@dataclass(frozen=True)
class OpenTrade:
    ticker: str
    entry_date: pd.Timestamp
    entry_price: float
    mark_date: pd.Timestamp
    mark_price: float
    return_pct: float


def calculate_trade_stats(trades_path: Path, prices_path: Path) -> tuple[list[RoundTrip], list[OpenTrade]]:
    trades = pd.read_csv(trades_path, parse_dates=["date"])
    prices = pd.read_csv(prices_path, header=[0, 1], index_col=0, parse_dates=True)
    opens = prices["Open"]
    closes = prices["Close"]
    final_date = closes.index.max()
    final_close = closes.loc[final_date]

    lots: dict[str, dict[str, float | pd.Timestamp]] = {}
    closed: list[RoundTrip] = []

    for _, trade in trades.iterrows():
        ticker = str(trade["ticker"])
        trade_date = trade["date"]
        if trade["action"] == "BUY":
            lots[ticker] = {
                "entry_date": trade_date,
                "entry_price": float(opens.loc[trade_date, ticker]),
            }
        elif trade["action"] == "SELL" and ticker in lots:
            lot = lots.pop(ticker)
            exit_price = float(opens.loc[trade_date, ticker])
            entry_price = float(lot["entry_price"])
            closed.append(
                RoundTrip(
                    ticker=ticker,
                    entry_date=pd.Timestamp(lot["entry_date"]),
                    entry_price=entry_price,
                    exit_date=trade_date,
                    exit_price=exit_price,
                    return_pct=(exit_price / entry_price) - 1.0,
                )
            )

    open_trades: list[OpenTrade] = []
    for ticker, lot in lots.items():
        if ticker not in final_close or pd.isna(final_close[ticker]):
            continue
        entry_price = float(lot["entry_price"])
        mark_price = float(final_close[ticker])
        open_trades.append(
            OpenTrade(
                ticker=ticker,
                entry_date=pd.Timestamp(lot["entry_date"]),
                entry_price=entry_price,
                mark_date=final_date,
                mark_price=mark_price,
                return_pct=(mark_price / entry_price) - 1.0,
            )
        )

    return closed, open_trades


def main() -> None:
    parser = argparse.ArgumentParser(description="Calculate closed win/loss trade stats from generated logs.")
    parser.add_argument("--trades", type=Path, default=Path("reports/sp500_top5_trades.csv"))
    parser.add_argument(
        "--prices",
        type=Path,
        default=Path("data/sp500_top5/adjusted_closes_2024-12-19_2026-05-12.csv"),
    )
    args = parser.parse_args()

    closed, open_trades = calculate_trade_stats(args.trades, args.prices)
    wins = [trade for trade in closed if trade.return_pct > 0]
    losses = [trade for trade in closed if trade.return_pct < 0]
    flats = [trade for trade in closed if abs(trade.return_pct) < 1e-12]
    open_wins = [trade for trade in open_trades if trade.return_pct > 0]
    open_losses = [trade for trade in open_trades if trade.return_pct < 0]

    print(f"closed_trades: {len(closed)}")
    print(f"wins: {len(wins)}")
    print(f"losses: {len(losses)}")
    print(f"flats: {len(flats)}")
    print(f"win_rate: {len(wins) / len(closed):.2%}" if closed else "win_rate: n/a")
    print(f"avg_win: {sum(trade.return_pct for trade in wins) / len(wins):.2%}" if wins else "avg_win: n/a")
    print(
        f"avg_loss: {sum(trade.return_pct for trade in losses) / len(losses):.2%}"
        if losses
        else "avg_loss: n/a"
    )
    print(f"open_positions: {len(open_trades)}")
    print(f"open_unrealized_wins: {len(open_wins)}")
    print(f"open_unrealized_losses: {len(open_losses)}")
    print("closed_detail:")
    for trade in closed:
        print(f"{trade.ticker},{trade.entry_date.date()},{trade.exit_date.date()},{trade.return_pct:.2%}")
    print("open_detail:")
    for trade in open_trades:
        print(f"{trade.ticker},{trade.entry_date.date()},{trade.mark_date.date()},{trade.return_pct:.2%}")


if __name__ == "__main__":
    main()
