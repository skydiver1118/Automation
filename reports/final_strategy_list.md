# Final Strategy List

This list adds the requested strategies from `Compare momentum strategies` and `Rank stock trading strategies`.
Performance is kept in one table, and strategy rule details are stored in the `strategies/` folder.

| Source | Universe | Strategy | Period | Return Metric | Return | Max Drawdown | Sharpe | IS Max DD | Detail File |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Compare momentum strategies | SOXL/TQQQ ETFs | SOXL/TQQQ Rotation with cash daily scanner | 2020-01-02 to 2026-05-22 | Cumulative Return | 9,826.01% | -53.40% | 1.402 | N/A | `strategies/soxl_tqqq_rotation_with_cash_daily_scanner.yaml` |
| Rank stock trading strategies | S&P 500 | SP500 Top5 L63 S0 none DCA1 | 2020-01-01 through latest available data as of 2026-05-24 | OOS Return | 810.89% | -18.21% | 1.25 | -32.36% | `strategies/sp500_top5_l63_s0_none_dca1.yaml` |
| Rank stock trading strategies | Nasdaq-100 | NASDAQ100 Top3 L126 S21 none DCA3 | 2020-01-01 through latest available data as of 2026-05-24 | OOS Return | 2,123.73% | -37.50% | 1.40 | -31.89% | `strategies/nasdaq100_top3_l126_s21_none_dca3.yaml` |
| Compare momentum strategies | SMH historical component stocks | SMH_HIST_PIT Top2 L252 S0 smh_sma100 DCA1 | 2020-01-01 through latest available data as of 2026-05-24 | OOS Return | 993.60% | -26.89% | 1.23 | -22.84% | `strategies/smh_hist_pit_top2_l252_s0_smh_sma100_dca1.yaml` |

## Source Files

- SOXL/TQQQ comparison: `SOXL_TQQQ_Three_Strategy_2020_To_Date.csv`
- SMH historical component momentum search: `reports/smh_historical_components_momentum_is2010_2019_oos2020_2026ytd.md`
- Momentum IS/OOS ranking: `reports/momentum_is2010_2019_oos2020_2026ytd_separate_sp500_nasdaq_cash_dca_with_oos_benchmarks.md`
- Machine-readable performance table: `reports/final_strategy_performance.csv`
