# NASDAQ100 Top3 L126 S21 none DCA3

Signal agent for the monthly Nasdaq-100 top-3 skip-momentum strategy.

- Universe: reconstructed Nasdaq-100 membership from current constituents plus changes table
- Timeframe: monthly
- Score: `Close[t - 21 trading days] / Close[t - 126 trading days] - 1`
- Entry: hold the top 3 ranked eligible Nasdaq-100 stocks
- Exit/rebalance: monthly rebalance at the first trading day open of each month
- Cash filter: none
- DCA: DCA3 exposure ramp, one third per monthly rebalance until full exposure

Default signal command:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_nasdaq100_top3_l126_s21_dca3_task.ps1 --alpaca --env-file .env.alpaca --email-to skydiver1118@gmail.com
```

Submit Alpaca paper extended-hours DAY limit orders using the latest close as the limit price:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_nasdaq100_top3_l126_s21_dca3_task.ps1 --alpaca --execute --env-file .env.alpaca --email-to skydiver1118@gmail.com
```

Execution guardrails:

- The Alpaca-backed run now skips unless the `as_of` date is the first Alpaca trading day of the month.
- It also skips if state already records a rebalance for that month.
- Use `--force` only for manual reruns or testing outside the scheduled rebalance window.

Outputs:

- `reports/nasdaq100_top3_l126_s21_dca3_signal.csv`
- `reports/nasdaq100_top3_l126_s21_dca3_signal.json`
- `reports/nasdaq100_top3_l126_s21_dca3_execution.json`

If Gmail SMTP environment variables are set, the scan also emails the signal and execution summary to `skydiver1118@gmail.com`.

The task wrapper prefers the pinned Python 3.14 install, but it only accepts interpreters that can import `pandas`, `numpy`, and `alpaca` with the local dependency folders loaded. That avoids falling through to a broken `python` shim during automation runs.
