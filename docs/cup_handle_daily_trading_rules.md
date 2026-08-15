# Cup & Handle Daily Trading Rules

This is technical strategy research and automation plumbing, not investment advice.

## Pattern Scan

- Universe: current S&P 500 symbols.
- Data: daily OHLCV.
- Pattern: daily cup-and-handle geometry from the local detector.
- Candidate pool: top 10 scores after `TargetReturnPct > 30%`.
- Pattern volume gate: handle average volume must be `<= 1.05x` cup average volume.

## Entry

- Scanner runs after the close.
- Entry trigger: daily close at or above the cup/handle breakout level.
- Entry volume gate: breakout-day volume must be `>= 1.40x` the prior 50 trading-day average volume.
- Stock trend filter: close above SMA50 and stock 63-day return greater than S&P 500 63-day return.
- Market filter: S&P 500 close above SMA100.
- Portfolio size: maximum 3 concurrent strategy positions.
- Position sizing: target account equity allocation is split equally across 3 slots.
- Execution account: Alpaca paper account by default.

## Exit

- Initial stop: entry price minus `3.5 x ATR14`.
- Target: none.
- Time stop: 60 trading days.
- Daily scanner sells a strategy-managed paper position if the latest close is at or below its stop or its 60-trading-day holding window has expired.

## Operational Notes

- The live scanner uses close-confirmed breakouts because it runs at 5 PM after the market close.
- Orders are submitted only when `--execute` is supplied.
- The scheduled automation uses `.env.alpaca` for `ALPACA_API_KEY` and `ALPACA_SECRET_KEY`.
