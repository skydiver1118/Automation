# SOXL/TQQQ Rotation with cash

Daily scanner agent for the SOXL/TQQQ rotation with cash-regime protection.

- Symbols: SOXL and TQQQ
- Context trend symbol: QQQ
- Timeframe: daily
- Base rotation: monthly relative momentum using 63-day return minus 0.5 x annualized volatility, skipping the most recent 10 trading days
- Rotation filter: prefer the chosen ETF when it is above SMA50; otherwise use the alternate ETF if it is above SMA50
- Hysteresis: 5% score difference required to switch the base rotation
- Cash exit: go to cash when both the selected ETF and QQQ are below SMA150
- Re-entry: return to the selected ETF when either the selected ETF or QQQ is above SMA150 + 1%
- Positioning: target SOXL, TQQQ, or CASH; no DCA in the balanced cash version

Default dry-run command:

```powershell
python scripts/soxl_tqqq_cash_signal_scanner.py --agent "SOXL/TQQQ Rotation with cash"
```

Read Alpaca paper positions and generate the signal:

```powershell
python scripts/soxl_tqqq_cash_signal_scanner.py --agent "SOXL/TQQQ Rotation with cash" --env-file .env.alpaca --alpaca
```

Submit Alpaca paper orders when the account is not aligned with the target:

```powershell
python scripts/soxl_tqqq_cash_signal_scanner.py --agent "SOXL/TQQQ Rotation with cash" --env-file .env.alpaca --alpaca --execute --qty 1
```

Submit Alpaca paper orders eligible for extended hours:

```powershell
python scripts/soxl_tqqq_cash_signal_scanner.py --agent "SOXL/TQQQ Rotation with cash" --env-file .env.alpaca --alpaca --execute --extended-hours --limit-offset-pct 0 --qty 1
```

Extended-hours orders are submitted as DAY limit orders with `extended_hours=True`.

Outputs:

- `reports/soxl_tqqq_cash_signal.csv`
- `reports/soxl_tqqq_cash_signal.json`

Required environment variables for Alpaca:

- `ALPACA_API_KEY`
- `ALPACA_SECRET_KEY`

The scanner loads `.env.alpaca` by default, and `--env-file .env.alpaca` is included in the agent commands used by automation.
