# Strategy Performance Metrics

Reusable local performance report agent.

Default SOXL/TQQQ cash-rotation report:

```powershell
python scripts/strategy_performance_metrics.py --strategy soxl_tqqq_rotation_cash --start 2020-01-02
```

Outputs include:

- Summary metrics
- Annual return and drawdown
- Trade list with holding period
- Holding-period summary by win/loss
- Equity curve CSV
- Drawdown curve CSV
- Equity/drawdown plot
