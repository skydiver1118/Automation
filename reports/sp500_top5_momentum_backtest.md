# S&P 500 Top-5 Momentum Backtest

## Rules

- Universe: current S&P 500 constituents from Wikipedia.
- Data: Yahoo Finance adjusted daily close via yfinance.
- Signal: rank by trailing adjusted-close momentum.
- Execution model: rank after the close, then execute exits and entries at the next trading day's open.
- Portfolio model: five 20% slots; cash is idle when fewer than five names are held.

## Summary

- Start: 2024-01-02
- End: 2024-12-31
- Trading days: 252
- Ticker count with usable data: 501
- Total return: 3.98%
- CAGR: 3.99%
- Max drawdown: -37.34%
- Sharpe: 0.29
- Buy trades: 116
- Sell trades: 111
- Final holdings: APP, PLTR, AXON, TSLA, UAL

## Notes

This first pass uses the current S&P 500 membership. That is acceptable for a recent one-month smoke test, but a multi-year research-grade test should use point-in-time constituents to avoid survivorship bias.
