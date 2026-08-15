# SOXL/TQQQ Advanced DCA Search

Tested 3,168 variants with partial reserve sizing, exposure caps, trend guards, and equity drawdown guards.

## Summary Cases

| case | variant | net_return_pct | cagr_pct | max_drawdown_pct | calmar | sharpe | max_exposure_used | avg_exposure | days_above_1x_pct | dca_trade_events | base_rotation_return_pct | base_rotation_max_drawdown_pct | soxl_only_return_pct | soxl_only_max_drawdown_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Best return with DD better than SOXL-only | unit=0.67, cap=2.00, anchor=rolling_high, add=10%/20%, sell=extra_profit 20%, max_days=20, trend_sma=200, dd_guard=45.0 | 2823010.49 | 90.5 | -65.54 | 1.381 | 1.26 | 2.0 | 0.929 | 29.7 | 304 | 775116.8 | -79.24 | 41069.8 | -66.18 |
| Best return with DD <= 60% | unit=0.50, cap=1.50, anchor=rolling_high, add=10%/20%, sell=extra_profit 20%, max_days=20, trend_sma=200, dd_guard=45.0 | 356512.48 | 67.26 | -59.85 | 1.124 | 1.18 | 1.5 | 0.73 | 8.77 | 304 | 775116.8 | -79.24 | 41069.8 | -66.18 |
| Best return with DD <= 50% | unit=0.50, cap=1.00, anchor=entry, add=10%/20%, sell=extra_profit 20%, max_days=10, trend_sma=none, dd_guard=none | 43682.98 | 46.59 | -47.87 | 0.973 | 1.2 | 1.0 | 0.511 | 0.0 | 51 | 775116.8 | -79.24 | 41069.8 | -66.18 |
| Best Calmar | unit=1.00, cap=2.00, anchor=rolling_high, add=5%/20%, sell=extra_profit 15%, max_days=20, trend_sma=100, dd_guard=none | 24991345075.06 | 237.38 | -82.46 | 2.879 | 1.71 | 2.0 | 1.448 | 44.88 | 447 | 775116.8 | -79.24 | 41069.8 | -66.18 |
| Best raw return | unit=1.00, cap=2.00, anchor=rolling_high, add=5%/20%, sell=extra_profit 15%, max_days=20, trend_sma=100, dd_guard=none | 24991345075.06 | 237.38 | -82.46 | 2.879 | 1.71 | 2.0 | 1.448 | 44.88 | 447 | 775116.8 | -79.24 | 41069.8 | -66.18 |

## Files

- Full grid: `C:\Users\skydiver1118\Documents\New project\reports\soxl_tqqq_dca_advanced_search_all.csv`
- Top balanced rows: `C:\Users\skydiver1118\Documents\New project\reports\soxl_tqqq_dca_advanced_balanced.csv`
- Curves: `C:\Users\skydiver1118\Documents\New project\reports\soxl_tqqq_dca_advanced_curves.csv`
- Exposure history: `C:\Users\skydiver1118\Documents\New project\reports\soxl_tqqq_dca_advanced_exposure.csv`
- Easy-open summary: `C:\Users\skydiver1118\Documents\New project\SOXL_TQQQ_DCA_Advanced_Summary.html`