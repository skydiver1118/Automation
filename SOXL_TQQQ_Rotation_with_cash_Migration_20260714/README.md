# SOXL/TQQQ Rotation with Cash Migration Bundle

Created: 2026-07-14

This bundle preserves the creator chat, strategy documentation, scanner implementation, automation scripts, backtest source, and generated backtest results for migration to another Windows PC.

## Contents

- `chat/`: complete raw Codex session plus a readable user/assistant transcript and thread metadata.
- `scanner/`: portable scanner project, Alpaca environment template, installer, runner, and weekday task installer.
- `backtest/`: strategy-search source code and generated cash-rotation results.
- `documentation/`: Word, Excel, HTML, CSV, text, and chart summaries created during strategy development.
- `MANIFEST-SHA256.txt`: SHA-256 checksums for transfer verification.

## Strategy Rules

- Rotate monthly between SOXL and TQQQ using 63-day relative momentum minus 0.5 times annualized volatility, skipping the most recent 10 trading days.
- Prefer the selected ETF when it is above SMA50; otherwise use the alternate ETF if that ETF is above SMA50.
- Require a 5% score difference before switching the base rotation.
- Exit to cash when both the selected ETF and QQQ are below SMA150.
- Re-enter when either the selected ETF or QQQ is at least 1% above SMA150.
- Hold one target state: SOXL, TQQQ, or CASH.

## Set Up the Scanner on Another PC

1. Copy the entire bundle to the new PC.
2. Install Python 3.14 from python.org and enable the Python launcher, or ensure `python` is available in PowerShell.
3. Open PowerShell in the `scanner` folder.
4. Run `powershell -ExecutionPolicy Bypass -File .\install_scanner.ps1`.
5. Edit `.env.alpaca` and add the new PC's Alpaca paper API key and secret. Never reuse or transfer plaintext credentials through this bundle.
6. Test without orders: `powershell -ExecutionPolicy Bypass -File .\run_scanner.ps1`.
7. Test Alpaca position access without orders:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_scanner.ps1 --agent "SOXL/TQQQ Rotation with cash" --env-file .env.alpaca --alpaca
```

8. Only after validating the signal and paper account, run the execution command:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_scanner.ps1 --agent "SOXL/TQQQ Rotation with cash" --env-file .env.alpaca --alpaca --execute --extended-hours --limit-offset-pct 0 --qty 1
```

9. Install the weekday 4:10 PM local-time task with `powershell -ExecutionPolicy Bypass -File .\install_daily_task.ps1`. Confirm the new PC is set to the `America/New_York` time zone before relying on the schedule.

The scanner defaults to Alpaca paper trading. Do not add `--live` until paper execution has been independently verified.

## Restore the Codex Chat

The guaranteed portable record is `chat/Rank_stock_trading_strategies_transcript.md`; it is readable without Codex. The raw session is also included for best-effort restoration.

1. Close Codex Desktop on the destination PC.
2. Back up `%USERPROFILE%\.codex` before changing its contents.
3. Run `powershell -ExecutionPolicy Bypass -File .\chat\import_chat_best_effort.ps1`.
4. Restart Codex Desktop and search for `Rank stock trading strategies`.

Codex Desktop's storage format can change between versions. The import script copies the session and adds its legacy index entry without overwriting existing history, but appearance in the app is not guaranteed. The raw JSONL and Markdown transcript remain complete migration records.

## Reproduce Backtests

From the bundle root, create a Python environment with the packages in `scanner/requirements.txt`, then run:

```powershell
.\scanner\.venv\Scripts\python.exe .\backtest\scripts\soxl_tqqq_rotation_search.py
.\scanner\.venv\Scripts\python.exe .\backtest\scripts\soxl_tqqq_cash_regime_search.py
```

The cash-regime search depends on `soxl_tqqq_dca_overlay_search.py` and on the base allocation/equity CSV files already included in `backtest/reports`. Backtests download adjusted market history from Yahoo Finance, so reproduced numbers can differ if the data vendor revises historical prices.

## Security

- No `.env.alpaca` file or known plaintext Alpaca key assignment is included.
- `.env.alpaca.example` contains placeholders only.
- Review the full chat archive before sharing this bundle with anyone else because it contains the complete historical conversation and tool output.
