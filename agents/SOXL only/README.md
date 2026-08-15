# SOXL only

Daily scanner agent for the standalone SOXL strategy:

- Symbol: SOXL
- Timeframe: daily
- Entry state: SMA50 > SMA63
- Exit state: SMA50 <= SMA63
- Risk exit: close <= 10% below active entry price

Default paper execution command (entry + exit):

```powershell
python scripts/soxl_only_signal_scanner.py --agent "SOXL only" --alpaca --execute --qty 1
```

Read Alpaca paper position and generate the signal:

```powershell
python scripts/soxl_only_signal_scanner.py --agent "SOXL only" --alpaca
```

Submit Alpaca paper order when signal is BUY or SELL (same as default mode):

```powershell
python scripts/soxl_only_signal_scanner.py --agent "SOXL only" --alpaca --execute --qty 1
```

Submit an Alpaca paper order eligible for extended hours:

```powershell
python scripts/soxl_only_signal_scanner.py --agent "SOXL only" --alpaca --execute --extended-hours --limit-offset-pct 0 --qty 1
```

Extended-hours orders are submitted as DAY limit orders with `extended_hours=True`. Alpaca does not treat after-hours market orders the same way; use `--limit-offset-pct` if you want the buy limit above the latest close or the sell limit below the latest close.

Outputs:

- `reports/soxl_only_signal.csv`
- `reports/soxl_only_signal.json`

Required environment variables for Alpaca:

- `ALPACA_API_KEY`
- `ALPACA_SECRET_KEY`
