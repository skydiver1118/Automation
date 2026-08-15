# SOXL/TQQQ Rotation with cash

Daily scanner agent for the SOXL/TQQQ rotation with cash-regime protection.
Default automation runner now uses dependency-free scanner script `scripts/soxl_tqqq_cash_signal_scanner_stdlib.py` to avoid pandas/yfinance/alpaca package ACL issues.

- Symbols: SOXL and TQQQ
- Context trend symbol: QQQ
- Timeframe: daily
- Base rotation: monthly relative momentum using 63-day return minus 0.5 x annualized volatility, skipping the most recent 10 trading days
- Rotation filter: prefer the chosen ETF when it is above SMA50; otherwise use the alternate ETF if it is above SMA50
- Hysteresis: 5% score difference required to switch the base rotation
- Cash exit: go to cash when both the selected ETF and QQQ are below SMA150
- Re-entry: return to the selected ETF when either the selected ETF or QQQ is above SMA150 + 1%
- Positioning: target SOXL, TQQQ, or CASH; no DCA in the balanced cash version

Interpreter to use for automation:

```text
C:\Users\skydiver1118\AppData\Local\Programs\Python\Python314\python.exe
```

Default dry-run command:

```powershell
C:\Users\skydiver1118\AppData\Local\Programs\Python\Python314\python.exe scripts/soxl_tqqq_cash_signal_scanner.py --agent "SOXL/TQQQ Rotation with cash"
```

Read Alpaca paper positions and generate the signal:

```powershell
C:\Users\skydiver1118\AppData\Local\Programs\Python\Python314\python.exe scripts/soxl_tqqq_cash_signal_scanner.py --agent "SOXL/TQQQ Rotation with cash" --env-file .env.alpaca --alpaca
```

Submit Alpaca paper orders when the account is not aligned with the target:

```powershell
C:\Users\skydiver1118\AppData\Local\Programs\Python\Python314\python.exe scripts/soxl_tqqq_cash_signal_scanner.py --agent "SOXL/TQQQ Rotation with cash" --env-file .env.alpaca --alpaca --execute --qty 1
```

Submit Alpaca paper orders eligible for extended hours:

```powershell
C:\Users\skydiver1118\AppData\Local\Programs\Python\Python314\python.exe scripts/soxl_tqqq_cash_signal_scanner.py --agent "SOXL/TQQQ Rotation with cash" --env-file .env.alpaca --alpaca --execute --extended-hours --limit-offset-pct 0 --qty 1
```

Extended-hours orders are submitted as DAY limit orders with `extended_hours=True`.

Outputs:

- `reports/soxl_tqqq_cash_signal.csv`
- `reports/soxl_tqqq_cash_signal.json`
- `reports/soxl_tqqq_cash_run_status.json`

Required environment variables for Alpaca:

- `ALPACA_API_KEY`
- `ALPACA_SECRET_KEY`

The scanner loads `.env.alpaca` by default, and `--env-file .env.alpaca` is included in the agent commands used by automation.

Task Scheduler action template (hardened):

- Program/script: `powershell.exe`
- Add arguments: `-ExecutionPolicy Bypass -File scripts/run_soxl_tqqq_cash_daily_scanner_task.ps1 --agent "SOXL/TQQQ Rotation with cash" --env-file .env.alpaca --alpaca --execute --extended-hours --limit-offset-pct 0 --qty 1 --email-to skydiver1118@gmail.com`
- Start in: `C:\Users\skydiver1118\Documents\New project`
- Run log: `reports/logs/soxl_tqqq_cash_scanner_YYYYMMDD_HHMMSS.log`

Permanent permission repair (run once in the Windows account that owns the task):

```powershell
powershell -ExecutionPolicy Bypass -File scripts/fix_soxl_tqqq_scanner_acl.ps1
powershell -ExecutionPolicy Bypass -File scripts/fix_soxl_tqqq_cash_scheduler.ps1
powershell -ExecutionPolicy Bypass -File scripts/run_soxl_tqqq_cash_daily_scanner_task.ps1 --agent "SOXL/TQQQ Rotation with cash" --env-file .env.alpaca --alpaca --execute --extended-hours --limit-offset-pct 0 --qty 1 --email-to skydiver1118@gmail.com
```

Expected verification:

- wrapper run exits successfully;
- `reports/soxl_tqqq_cash_signal.csv` and `.json` update;
- new log file appears in `reports/logs/`.

Network outage behavior:

- The wrapper enables `--allow-stale-fallback` on the dependency-free scanner.
- If Yahoo/Alpaca endpoints are blocked/unreachable, scanner still exits successfully, writes CSV/JSON with `data_source=stale_fallback`, sets `position_source=stale_fallback`, and skips order execution safely.
- `reports/soxl_tqqq_cash_run_status.json` explicitly records `mode`, `can_trade_live`, `execute_requested`, `executed_trade`, and `stale_reason`.
- This prevents silent task failure while preserving an explicit incident trail in the run log and output files.
